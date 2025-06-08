#!/usr/bin/env python3
"""
Hinemos MCP Server
運用監視ツールHinemosとAIアシスタントを接続するMCPサーバ
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import xml.etree.ElementTree as ET
import aiohttp
import base64
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, Tool, TextContent, ImageContent
from pydantic import BaseModel

# Hinemosクライアント設定
@dataclass
class HinemosConfig:
    base_url: str  # http://hinemos-server:8080/HinemosWS/
    username: str
    password: str
    timeout: int = 30

# アプリケーションコンテキスト
@dataclass 
class AppContext:
    hinemos_config: HinemosConfig
    session: aiohttp.ClientSession

class HinemosClient:
    """Hinemos SOAP API クライアント"""
    
    def __init__(self, config: HinemosConfig, session: aiohttp.ClientSession):
        self.config = config
        self.session = session
        self.auth_header = self._create_auth_header()
    
    def _create_auth_header(self) -> str:
        """Basic認証ヘッダーを生成"""
        credentials = f"{self.config.username}:{self.config.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    async def _soap_request(self, endpoint: str, action: str, body: str) -> Dict[str, Any]:
        """SOAP リクエストを送信"""
        soap_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Header/>
            <soap:Body>
                {body}
            </soap:Body>
        </soap:Envelope>"""
        
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': action,
            'Authorization': self.auth_header
        }
        
        url = f"{self.config.base_url}{endpoint}"
        
        async with self.session.post(
            url, 
            data=soap_envelope, 
            headers=headers,
            timeout=self.config.timeout
        ) as response:
            response.raise_for_status()
            content = await response.text()
            return self._parse_soap_response(content)
    
    def _parse_soap_response(self, xml_content: str) -> Dict[str, Any]:
        """SOAP レスポンスをパースしてJSONに変換"""
        try:
            root = ET.fromstring(xml_content)
            # 名前空間を考慮したパース
            namespaces = {
                'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                'hinemos': 'http://hinemos.ntt-data.co.jp'  # 実際の名前空間に応じて調整
            }
            
            body = root.find('.//soap:Body', namespaces)
            if body is not None:
                # レスポンスデータを辞書に変換
                return self._xml_to_dict(body)
            return {}
        except ET.ParseError as e:
            logging.error(f"XML parsing error: {e}")
            return {"error": f"XML parsing failed: {e}"}
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """XML要素を辞書に変換"""
        result = {}
        
        # テキストコンテンツ
        if element.text and element.text.strip():
            result['_text'] = element.text.strip()
        
        # 属性
        if element.attrib:
            result['_attributes'] = element.attrib
        
        # 子要素
        for child in element:
            child_data = self._xml_to_dict(child)
            tag = child.tag.split('}')[-1]  # 名前空間プレフィックスを除去
            
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_data)
            else:
                result[tag] = child_data
        
        return result
    
    async def get_monitor_status(self, facility_id: Optional[str] = None) -> Dict[str, Any]:
        """監視ステータスを取得"""
        body = f"""
        <hinemos:getMonitorStatus xmlns:hinemos="http://hinemos.ntt-data.co.jp">
            {f'<facilityId>{facility_id}</facilityId>' if facility_id else ''}
        </hinemos:getMonitorStatus>
        """
        return await self._soap_request("MonitorEndpoint", "getMonitorStatus", body)
    
    async def get_event_list(self, 
                           facility_id: Optional[str] = None,
                           priority: Optional[int] = None,
                           limit: int = 100) -> Dict[str, Any]:
        """イベント一覧を取得"""
        body = f"""
        <hinemos:getEventList xmlns:hinemos="http://hinemos.ntt-data.co.jp">
            {f'<facilityId>{facility_id}</facilityId>' if facility_id else ''}
            {f'<priority>{priority}</priority>' if priority else ''}
            <limit>{limit}</limit>
        </hinemos:getEventList>
        """
        return await self._soap_request("MonitorEndpoint", "getEventList", body)
    
    async def get_job_status(self, job_unit_id: Optional[str] = None) -> Dict[str, Any]:
        """ジョブステータスを取得"""
        body = f"""
        <hinemos:getJobStatus xmlns:hinemos="http://hinemos.ntt-data.co.jp">
            {f'<jobUnitId>{job_unit_id}</jobUnitId>' if job_unit_id else ''}
        </hinemos:getJobStatus>
        """
        return await self._soap_request("JobEndpoint", "getJobStatus", body)
    
    async def get_node_list(self) -> Dict[str, Any]:
        """ノード一覧を取得"""
        body = """
        <hinemos:getNodeList xmlns:hinemos="http://hinemos.ntt-data.co.jp">
        </hinemos:getNodeList>
        """
        return await self._soap_request("RepositoryEndpoint", "getNodeList", body)
    
    async def execute_job(self, job_id: str, facility_id: str) -> Dict[str, Any]:
        """ジョブを実行"""
        body = f"""
        <hinemos:executeJob xmlns:hinemos="http://hinemos.ntt-data.co.jp">
            <jobId>{job_id}</jobId>
            <facilityId>{facility_id}</facilityId>
        </hinemos:executeJob>
        """
        return await self._soap_request("JobEndpoint", "executeJob", body)

# サーバー設定
mcp = FastMCP("Hinemos Integration Server")

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """アプリケーションライフサイクル管理"""
    # 環境変数から設定を読み込み（実際の実装では環境変数を使用）
    hinemos_config = HinemosConfig(
        base_url="http://localhost:8080/HinemosWS/",
        username="hinemos",
        password="hinemos123"
    )
    
    # HTTPセッション作成
    session = aiohttp.ClientSession()
    
    try:
        yield AppContext(
            hinemos_config=hinemos_config,
            session=session
        )
    finally:
        await session.close()

mcp = FastMCP("Hinemos Integration Server", lifespan=app_lifespan)

# リソース定義
@mcp.resource("hinemos://monitor/status")
async def get_monitor_status_resource() -> Resource:
    """監視ステータスリソース"""
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    status_data = await client.get_monitor_status()
    
    return Resource(
        uri="hinemos://monitor/status",
        name="Hinemos Monitor Status",
        description="Current monitoring status from Hinemos",
        mimeType="application/json",
        text=str(status_data)
    )

@mcp.resource("hinemos://events/recent")
async def get_recent_events_resource() -> Resource:
    """最近のイベントリソース"""
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    events_data = await client.get_event_list(limit=50)
    
    return Resource(
        uri="hinemos://events/recent",
        name="Recent Hinemos Events",
        description="Recent events and alerts from Hinemos monitoring",
        mimeType="application/json",
        text=str(events_data)
    )

# ツール定義
@mcp.tool()
async def check_node_status(node_id: str) -> List[TextContent]:
    """指定されたノードの監視ステータスを確認する
    
    Args:
        node_id: 確認するノードのID
        
    Returns:
        ノードの現在のステータス情報
    """
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    try:
        status = await client.get_monitor_status(facility_id=node_id)
        return [TextContent(
            type="text",
            text=f"Node {node_id} status: {status}"
        )]
    except Exception as e:
        return [TextContent(
            type="text", 
            text=f"Error checking node {node_id}: {str(e)}"
        )]

@mcp.tool()
async def get_critical_events(hours: int = 24) -> List[TextContent]:
    """過去指定時間内の重要なイベントを取得する
    
    Args:
        hours: 過去何時間のイベントを取得するか（デフォルト: 24時間）
        
    Returns:
        重要度の高いイベント一覧
    """
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    try:
        # 重要度 1 = Critical, 2 = Warning 
        events = await client.get_event_list(priority=1, limit=100)
        return [TextContent(
            type="text",
            text=f"Critical events in last {hours} hours: {events}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error retrieving critical events: {str(e)}"
        )]

@mcp.tool()
async def execute_hinemos_job(job_id: str, target_node: str) -> List[TextContent]:
    """Hinemosジョブを実行する
    
    Args:
        job_id: 実行するジョブのID
        target_node: ジョブを実行する対象ノード
        
    Returns:
        ジョブ実行結果
    """
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    try:
        result = await client.execute_job(job_id, target_node)
        return [TextContent(
            type="text",
            text=f"Job {job_id} executed on {target_node}: {result}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing job {job_id}: {str(e)}"
        )]

@mcp.tool()
async def list_managed_nodes() -> List[TextContent]:
    """管理対象ノード一覧を取得する
    
    Returns:
        Hinemosで管理されているノードの一覧
    """
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    try:
        nodes = await client.get_node_list()
        return [TextContent(
            type="text",
            text=f"Managed nodes: {nodes}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error retrieving node list: {str(e)}"
        )]

# プロンプト定義
@mcp.prompt()
async def system_health_report() -> str:
    """システム全体の健全性レポートを生成する"""
    return """
    Please analyze the current Hinemos monitoring data and provide a comprehensive system health report including:
    
    1. Overall system status summary
    2. Critical alerts and their impact
    3. Node availability status
    4. Recent significant events
    5. Recommended actions for any issues found
    
    Use the available Hinemos tools to gather this information and format it in a clear, actionable report.
    """

@mcp.prompt()
async def incident_investigation(event_id: str) -> str:
    """特定のインシデントについて詳細調査を行う"""
    return f"""
    Please investigate the incident with event ID: {event_id}
    
    Gather the following information:
    1. Event details and timeline
    2. Affected systems and services
    3. Related events that occurred around the same time
    4. Historical patterns for similar events
    5. Suggested remediation steps
    
    Provide a structured incident analysis report.
    """

if __name__ == "__main__":
    import asyncio
    
    async def main():
        from mcp.server import stdio_server
        
        async with stdio_server(mcp) as streams:
            await mcp.run(*streams)
    
    asyncio.run(main())
