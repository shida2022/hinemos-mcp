#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinemos MCP Server - REST API Version for Hinemos 7.1
A Model Context Protocol (MCP) server for Hinemos 7.1 using REST API
"""

import asyncio
import logging
import os
import sys
import aiohttp
import base64
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from hinemos_client import HinemosClient

# Fix encoding for Windows Japanese environment
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import TextContent, Tool, ListToolsResult

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('hinemos_mcp_debug.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("hinemos-mcp")

class HinemosRESTManager:
    """Hinemos 7.1 Manager client using REST API"""
    
    def __init__(self, endpoint: str, username: str, password: str):
        # REST API形式のエンドポイントに変換
        self.endpoint = endpoint.rstrip('/')
        # Hinemos 7.1のREST APIエンドポイントパス
        if not self.endpoint.endswith('/HinemosWS/rest'):
            self.endpoint = self.endpoint + '/HinemosWS/rest'
        
        self.username = username
        self.password = password
        self.session = None
        self.connected = False
        
        # Create basic auth header
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        self.auth_header = f"Basic {encoded_credentials}"
        
        logger.info(f"Hinemos 7.1 REST Manager initialized for endpoint: {self.endpoint}")
    
    async def _ensure_session(self):
        """Ensure aiohttp session is available"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': self.auth_header,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=aiohttp.ClientTimeout(total=30)
            )
    
    async def _make_request(self, method: str, path: str, data: dict = None, params: dict = None) -> Dict[str, Any]:
        """Make HTTP request to Hinemos REST API"""
        await self._ensure_session()
        
        url = f"{self.endpoint}{path}"
        logger.info(f"Making {method} request to: {url}")
        if data:
            logger.debug(f"Request data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        if params:
            logger.debug(f"Request params: {params}")
        
        try:
            kwargs = {}
            if params:
                kwargs['params'] = params
            if data:
                kwargs['json'] = data
            
            async with self.session.request(method, url, **kwargs) as response:
                response_text = await response.text()
                logger.debug(f"Response status: {response.status}, text: {response_text[:1000]}")
                
                if response.status in [200, 201, 204]:
                    if response_text:
                        try:
                            return json.loads(response_text)
                        except json.JSONDecodeError:
                            return {"status": "success", "message": "レスポンスを受信しました"}
                    else:
                        return {"status": "success"}
                else:
                    # エラーレスポンスを詳細に解析
                    error_detail = response_text
                    try:
                        error_json = json.loads(response_text)
                        if isinstance(error_json, dict) and 'message' in error_json:
                            error_detail = error_json['message']
                    except:
                        pass
                    
                    raise Exception(f"HTTP {response.status}: {error_detail}")
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            raise Exception(f"ネットワークエラー: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise Exception(f"レスポンスの解析エラー: {str(e)}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to Hinemos Manager"""
        logger.info("Testing connection to Hinemos 7.1 Manager")
        try:
            # Simple API call to test connectivity
            result = await self._make_request('GET', '/repository/node')
            self.connected = True
            return {
                "status": "connected",
                "manager_type": "rest",
                "endpoint": self.endpoint,
                "username": self.username,
                "message": "Hinemos 7.1マネージャーとの接続が正常に確立されました（REST API）"
            }
        except Exception as e:
            self.connected = False
            logger.error(f"Connection test failed: {e}")
            return {
                "status": "connection_failed",
                "manager_type": "rest",
                "endpoint": self.endpoint,
                "error": str(e),
                "message": f"Hinemos 7.1マネージャーとの接続に失敗しました: {str(e)}"
            }
    
    async def get_node_list(self, owner_role_id: str = None) -> Dict[str, Any]:
        """Get node list from Hinemos repository"""
        logger.info(f"Getting node list with owner_role_id: {owner_role_id}")
        
        try:
            params = {}
            if owner_role_id:
                params['ownerRoleId'] = owner_role_id
            
            result = await self._make_request('GET', '/repository/node', params=params)
            
            # Process the result to extract node information
            nodes = []
            if isinstance(result, list):
                for node in result:
                    nodes.append({
                        "facility_id": node.get('facilityId'),
                        "facility_name": node.get('facilityName'),
                        "ip_address": node.get('ipAddressVersion4', node.get('ipAddressVersion6')),
                        "platform_family": node.get('platformFamily'),
                        "description": node.get('description'),
                        "owner_role_id": node.get('ownerRoleId'),
                        "valid": node.get('valid', True)
                    })
            elif isinstance(result, dict) and 'list' in result:
                # Handle wrapped response format
                for node in result['list']:
                    nodes.append({
                        "facility_id": node.get('facilityId'),
                        "facility_name": node.get('facilityName'),
                        "ip_address": node.get('ipAddressVersion4', node.get('ipAddressVersion6')),
                        "platform_family": node.get('platformFamily'),
                        "description": node.get('description'),
                        "owner_role_id": node.get('ownerRoleId'),
                        "valid": node.get('valid', True)
                    })
            
            return {
                "nodes": nodes,
                "count": len(nodes),
                "status": "success",
                "message": f"{len(nodes)}個のノードを取得しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error getting node list: {e}")
            return {
                "nodes": [],
                "count": 0,
                "status": "error",
                "error": str(e),
                "message": f"ノードリストの取得に失敗しました: {str(e)}"
            }
    
    async def add_node(self, facility_id: str, facility_name: str, ip_address: str, 
                      platform_family: str = "LINUX", description: str = "", 
                      owner_role_id: str = "ADMINISTRATORS") -> Dict[str, Any]:
        """Add a new node to Hinemos repository"""
        logger.info(f"Adding node: {facility_id} - {facility_name} ({ip_address})")
        
        try:
            node_data = {
                "facilityId": facility_id,
                "facilityName": facility_name,
                "description": description,
                "facilityType": "NODE",
                "ipAddressVersion4": ip_address,
                "platformFamily": platform_family,
                "ownerRoleId": owner_role_id,
                "valid": True,
                "autoDeviceSearch": False,
                "createUserId": self.username,
                "createDatetime": int(datetime.now().timestamp() * 1000),
                "modifyUserId": self.username,
                "modifyDatetime": int(datetime.now().timestamp() * 1000)
            }
            
            result = await self._make_request('POST', '/repository/node', node_data)
            
            return {
                "facility_id": facility_id,
                "facility_name": facility_name,
                "ip_address": ip_address,
                "platform_family": platform_family,
                "owner_role_id": owner_role_id,
                "status": "created",
                "result": result,
                "message": f"ノード '{facility_name}' ({facility_id}) を正常に追加しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error adding node: {e}")
            return {
                "facility_id": facility_id,
                "status": "error",
                "error": str(e),
                "message": f"ノードの追加に失敗しました: {str(e)}"
            }
    
    async def delete_node(self, facility_ids: List[str]) -> Dict[str, Any]:
        """Delete nodes from Hinemos repository"""
        logger.info(f"Deleting nodes: {facility_ids}")
        
        deleted_nodes = []
        failed_nodes = []
        
        for facility_id in facility_ids:
            try:
                await self._make_request('DELETE', f'/repository/node/{facility_id}')
                deleted_nodes.append(facility_id)
                logger.info(f"Successfully deleted node: {facility_id}")
            except Exception as e:
                failed_nodes.append({"facility_id": facility_id, "error": str(e)})
                logger.error(f"Failed to delete node {facility_id}: {e}")
        
        return {
            "deleted_nodes": deleted_nodes,
            "failed_nodes": failed_nodes,
            "deleted_count": len(deleted_nodes),
            "failed_count": len(failed_nodes),
            "status": "completed",
            "message": f"{len(deleted_nodes)}個のノードを削除しました（失敗: {len(failed_nodes)}個）（REST API）"
        }
    
    async def add_http_monitor(self, monitor_id: str, monitor_name: str, facility_id: str, 
                             url: str, interval: int = 300, timeout: int = 10000,
                             owner_role_id: str = "ADMINISTRATORS") -> Dict[str, Any]:
        """Add HTTP monitoring setting"""
        logger.info(f"Adding HTTP monitor: {monitor_id} for {facility_id}")
        
        try:
            monitor_data = {
                "monitorId": monitor_id,
                "description": monitor_name,
                "monitorTypeId": "MON_HTTP_N",
                "facilityId": facility_id,
                "runInterval": interval,
                "ownerRoleId": owner_role_id,
                "monitorFlg": True,
                "collectorFlg": False,
                "url": url,
                "timeout": timeout,
                "userAgent": "Hinemos HTTP Monitor",
                "httpInfo": {
                    "requestUrl": url,
                    "timeout": timeout,
                    "userAgent": "Hinemos HTTP Monitor"
                },
                "createUserId": self.username,
                "createDatetime": int(datetime.now().timestamp() * 1000),
                "modifyUserId": self.username,
                "modifyDatetime": int(datetime.now().timestamp() * 1000)
            }
            
            result = await self._make_request('POST', '/monitor/http', monitor_data)
            
            return {
                "monitor_id": monitor_id,
                "monitor_name": monitor_name,
                "facility_id": facility_id,
                "url": url,
                "interval": interval,
                "timeout": timeout,
                "status": "created",
                "result": result,
                "message": f"HTTP監視 '{monitor_name}' ({monitor_id}) を正常に追加しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error adding HTTP monitor: {e}")
            return {
                "monitor_id": monitor_id,
                "status": "error",
                "error": str(e),
                "message": f"HTTP監視の追加に失敗しました: {str(e)}"
            }
    
    async def add_ping_monitor(self, monitor_id: str, monitor_name: str, facility_id: str,
                              interval: int = 300, run_count: int = 3, timeout: int = 5000,
                              owner_role_id: str = "ADMINISTRATORS") -> Dict[str, Any]:
        """Add Ping monitoring setting"""
        logger.info(f"Adding Ping monitor: {monitor_id} for {facility_id}")
        
        try:
            monitor_data = {
                "monitorId": monitor_id,
                "description": monitor_name,
                "monitorTypeId": "MON_PING_N",
                "facilityId": facility_id,
                "runInterval": interval,
                "ownerRoleId": owner_role_id,
                "monitorFlg": True,
                "collectorFlg": False,
                "runCount": run_count,
                "timeout": timeout,
                "pingInfo": {
                    "runCount": run_count,
                    "timeout": timeout
                },
                "createUserId": self.username,
                "createDatetime": int(datetime.now().timestamp() * 1000),
                "modifyUserId": self.username,
                "modifyDatetime": int(datetime.now().timestamp() * 1000)
            }
            
            result = await self._make_request('POST', '/monitor/ping', monitor_data)
            
            return {
                "monitor_id": monitor_id,
                "monitor_name": monitor_name,
                "facility_id": facility_id,
                "interval": interval,
                "run_count": run_count,
                "timeout": timeout,
                "status": "created",
                "result": result,
                "message": f"Ping監視 '{monitor_name}' ({monitor_id}) を正常に追加しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error adding Ping monitor: {e}")
            return {
                "monitor_id": monitor_id,
                "status": "error",
                "error": str(e),
                "message": f"Ping監視の追加に失敗しました: {str(e)}"
            }
    
    async def get_monitor_list(self, owner_role_id: str = None) -> Dict[str, Any]:
        """Get monitor list"""
        logger.info(f"Getting monitor list with owner_role_id: {owner_role_id}")
        
        try:
            params = {}
            if owner_role_id:
                params['ownerRoleId'] = owner_role_id
            
            result = await self._make_request('GET', '/monitor', params=params)
            
            monitors = []
            monitor_list = result
            if isinstance(result, dict) and 'list' in result:
                monitor_list = result['list']
            
            if isinstance(monitor_list, list):
                for monitor in monitor_list:
                    monitors.append({
                        "monitor_id": monitor.get('monitorId'),
                        "monitor_name": monitor.get('description'),
                        "monitor_type": monitor.get('monitorTypeId'),
                        "facility_id": monitor.get('facilityId'),
                        "monitor_flg": monitor.get('monitorFlg'),
                        "collector_flg": monitor.get('collectorFlg'),
                        "owner_role_id": monitor.get('ownerRoleId'),
                        "run_interval": monitor.get('runInterval')
                    })
            
            return {
                "monitors": monitors,
                "count": len(monitors),
                "status": "success",
                "message": f"{len(monitors)}個の監視設定を取得しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error getting monitor list: {e}")
            return {
                "monitors": [],
                "count": 0,
                "status": "error",
                "error": str(e),
                "message": f"監視設定リストの取得に失敗しました: {str(e)}"
            }
    
    async def delete_monitor(self, monitor_ids: List[str]) -> Dict[str, Any]:
        """Delete monitoring settings"""
        logger.info(f"Deleting monitors: {monitor_ids}")
        
        deleted_monitors = []
        failed_monitors = []
        
        for monitor_id in monitor_ids:
            try:
                await self._make_request('DELETE', f'/monitor/{monitor_id}')
                deleted_monitors.append(monitor_id)
                logger.info(f"Successfully deleted monitor: {monitor_id}")
            except Exception as e:
                failed_monitors.append({"monitor_id": monitor_id, "error": str(e)})
                logger.error(f"Failed to delete monitor {monitor_id}: {e}")
        
        return {
            "deleted_monitors": deleted_monitors,
            "failed_monitors": failed_monitors,
            "deleted_count": len(deleted_monitors),
            "failed_count": len(failed_monitors),
            "status": "completed",
            "message": f"{len(deleted_monitors)}個の監視設定を削除しました（失敗: {len(failed_monitors)}個）（REST API）"
        }
    
    async def get_event_list(self, facility_id: str = None, priority: int = None,
                           start_date: str = None, end_date: str = None,
                           owner_role_id: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get event list from Hinemos"""
        logger.info(f"Getting event list with filters: facility_id={facility_id}, priority={priority}")
        
        try:
            params = {}
            if facility_id:
                params['facilityId'] = facility_id
            if priority is not None:
                params['priority'] = priority
            if start_date:
                params['outputFromDate'] = start_date
            if end_date:
                params['outputToDate'] = end_date
            if owner_role_id:
                params['ownerRoleId'] = owner_role_id
            if limit:
                params['limit'] = limit
            
            result = await self._make_request('GET', '/monitor/event', params=params)
            
            events = []
            event_list = result
            if isinstance(result, dict) and 'list' in result:
                event_list = result['list']
            
            if isinstance(event_list, list):
                for event in event_list:
                    events.append({
                        "output_date": event.get('outputDate'),
                        "facility_id": event.get('facilityId'),
                        "message": event.get('message'),
                        "priority": event.get('priority'),
                        "monitor_id": event.get('monitorId'),
                        "monitor_detail_id": event.get('monitorDetailId'),
                        "application": event.get('application'),
                        "scope_text": event.get('scopeText'),
                        "generation_date": event.get('generationDate'),
                        "confirm_flg": event.get('confirmFlg')
                    })
            
            return {
                "events": events,
                "count": len(events),
                "status": "success",
                "message": f"{len(events)}個のイベントを取得しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error getting event list: {e}")
            return {
                "events": [],
                "count": 0,
                "status": "error",
                "error": str(e),
                "message": f"イベントリストの取得に失敗しました: {str(e)}"
            }
    
    async def get_scope_list(self, owner_role_id: str = None) -> Dict[str, Any]:
        """Get scope list from Hinemos repository"""
        logger.info(f"Getting scope list with owner_role_id: {owner_role_id}")
        
        try:
            params = {}
            if owner_role_id:
                params['ownerRoleId'] = owner_role_id
            
            result = await self._make_request('GET', '/repository/scope', params=params)
            
            scopes = []
            scope_list = result
            if isinstance(result, dict) and 'list' in result:
                scope_list = result['list']
            
            if isinstance(scope_list, list):
                for scope in scope_list:
                    scopes.append({
                        "facility_id": scope.get('facilityId'),
                        "facility_name": scope.get('facilityName'),
                        "description": scope.get('description'),
                        "facility_type": scope.get('facilityType'),
                        "owner_role_id": scope.get('ownerRoleId'),
                        "valid": scope.get('valid', True)
                    })
            
            return {
                "scopes": scopes,
                "count": len(scopes),
                "status": "success",
                "message": f"{len(scopes)}個のスコープを取得しました（REST API）"
            }
            
        except Exception as e:
            logger.error(f"Error getting scope list: {e}")
            return {
                "scopes": [],
                "count": 0,
                "status": "error",
                "error": str(e),
                "message": f"スコープリストの取得に失敗しました: {str(e)}"
            }
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            logger.info("HTTP session closed")

# Mock Hinemos Manager for testing when real Hinemos is not available
class MockHinemosManager:
    """Mock Hinemos Manager for testing when real Hinemos is not available"""
    
    def __init__(self):
        self.connected = True
        logger.info("Mock Hinemos Manager initialized")
    
    async def test_connection(self) -> Dict[str, Any]:
        return {
            "status": "connected",
            "manager_type": "mock",
            "message": "モック接続テストが正常に完了しました（Hinemos 7.1 REST API対応版）"
        }
    
    async def get_node_list(self, **kwargs) -> Dict[str, Any]:
        return {
            "nodes": [
                {"facility_id": "TEST_001", "facility_name": "Test Server 1", "ip_address": "192.168.1.100"},
                {"facility_id": "TEST_002", "facility_name": "Test Server 2", "ip_address": "192.168.1.101"}
            ],
            "count": 2,
            "status": "success",
            "message": "モックノードリストを正常に取得しました（REST API）"
        }
    
    async def add_node(self, facility_id: str, facility_name: str, ip_address: str, **kwargs) -> Dict[str, Any]:
        return {
            "facility_id": facility_id,
            "facility_name": facility_name,
            "ip_address": ip_address,
            "status": "created",
            "message": f"モックノード '{facility_name}' を正常に追加しました（REST API）"
        }
    
    async def delete_node(self, facility_ids: List[str]) -> Dict[str, Any]:
        return {
            "deleted_nodes": facility_ids,
            "failed_nodes": [],
            "deleted_count": len(facility_ids),
            "failed_count": 0,
            "status": "completed",
            "message": f"モック: {len(facility_ids)}個のノードを削除しました（REST API）"
        }
    
    async def add_http_monitor(self, monitor_id: str, monitor_name: str, facility_id: str, url: str, **kwargs) -> Dict[str, Any]:
        return {
            "monitor_id": monitor_id,
            "monitor_name": monitor_name,
            "facility_id": facility_id,
            "url": url,
            "status": "created",
            "message": f"モックHTTP監視 '{monitor_name}' を正常に追加しました（REST API）"
        }
    
    async def add_ping_monitor(self, monitor_id: str, monitor_name: str, facility_id: str, **kwargs) -> Dict[str, Any]:
        return {
            "monitor_id": monitor_id,
            "monitor_name": monitor_name,
            "facility_id": facility_id,
            "status": "created",
            "message": f"モックPing監視 '{monitor_name}' を正常に追加しました（REST API）"
        }
    
    async def get_monitor_list(self, **kwargs) -> Dict[str, Any]:
        return {
            "monitors": [
                {"monitor_id": "HTTP_001", "monitor_name": "Web Server Check", "monitor_type": "MON_HTTP_N"},
                {"monitor_id": "PING_001", "monitor_name": "Ping Check", "monitor_type": "MON_PING_N"}
            ],
            "count": 2,
            "status": "success",
            "message": "モック監視設定リストを正常に取得しました（REST API）"
        }
    
    async def delete_monitor(self, monitor_ids: List[str]) -> Dict[str, Any]:
        return {
            "deleted_monitors": monitor_ids,
            "failed_monitors": [],
            "deleted_count": len(monitor_ids),
            "failed_count": 0,
            "status": "completed",
            "message": f"モック: {len(monitor_ids)}個の監視設定を削除しました（REST API）"
        }
    
    async def get_event_list(self, **kwargs) -> Dict[str, Any]:
        return {
            "events": [
                {
                    "output_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "facility_id": "TEST_001",
                    "message": "モック: HTTP監視でエラーが発生しました（REST API）",
                    "priority": "CRITICAL"
                }
            ],
            "count": 1,
            "status": "success",
            "message": "モックイベントリストを正常に取得しました（REST API）"
        }
    
    async def get_scope_list(self, **kwargs) -> Dict[str, Any]:
        return {
            "scopes": [
                {"facility_id": "SCOPE_001", "facility_name": "本社", "facility_type": "SCOPE"},
                {"facility_id": "SCOPE_002", "facility_name": "支社", "facility_type": "SCOPE"}
            ],
            "count": 2,
            "status": "success",
            "message": "モックスコープリストを正常に取得しました（REST API）"
        }
    
    async def close(self):
        pass

class HinemosSyncManager:
    """同期版 Hinemos REST APIクライアントラッパー（hinemos_client.py利用）"""
    def __init__(self):
        self.client = HinemosClient()
        self.logged_in = False

    async def test_connection(self) -> Dict[str, Any]:
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.client.login)
            self.logged_in = True
            return {
                "status": "connected",
                "manager_type": "sync",
                "message": "Hinemos REST API接続に成功しました"
            }
        except Exception as e:
            return {
                "status": "connection_failed",
                "manager_type": "sync",
                "error": str(e),
                "message": f"Hinemos REST API接続に失敗しました: {str(e)}"
            }

    async def get_node_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_node_list)

    async def add_node(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_node, kwargs)

    async def delete_node(self, facility_ids: list) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_node, facility_ids)

    async def add_http_monitor(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_http_monitor, **kwargs)

    async def add_ping_monitor(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_ping_monitor, **kwargs)

    async def get_monitor_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_monitor_list)

    async def delete_monitor(self, monitor_ids: list) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_monitor, monitor_ids)

    async def get_event_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_event_list)

    async def get_scope_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        # スコープ一覧取得APIはget_facility_listで代用
        return await loop.run_in_executor(None, self.client.get_facility_list)

    async def close(self):
        self.client.logout()

# Global manager instance
hinemos_manager: Optional[HinemosRESTManager] = None

# Create the MCP server
server = Server("hinemos-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available Hinemos tools"""
    logger.info("LIST_TOOLS called - returning available tools")
    
    try:
        # First, let's try to understand what ListToolsResult expects
        logger.info("Inspecting ListToolsResult...")
        logger.info(f"ListToolsResult annotations: {getattr(ListToolsResult, '__annotations__', 'none')}")
        
        # Create tools for Hinemos 7.1 REST API
        tools = [
            Tool(
                name="test_connection",
                description="Hinemos 7.1サーバーへの接続をテスト（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_node_list",
                description="Hinemos 7.1リポジトリからノードリストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールIDフィルター（オプション）"
                        }
                    }
                }
            ),
            Tool(
                name="delete_node",
                description="Hinemos 7.1リポジトリからノードを削除（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "facility_ids": {
                            "type": "array", 
                            "items": {"type": "string"}, 
                            "description": "削除するファシリティIDのリスト"
                        }
                    },
                    "required": ["facility_ids"]
                }
            ),
            Tool(
                name="add_http_monitor",
                description="Hinemos 7.1にHTTP監視設定を追加（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "monitor_id": {
                            "type": "string", 
                            "description": "ユニークな監視ID"
                        },
                        "monitor_name": {
                            "type": "string", 
                            "description": "監視設定の表示名"
                        },
                        "facility_id": {
                            "type": "string", 
                            "description": "対象ファシリティID"
                        },
                        "url": {
                            "type": "string", 
                            "description": "監視対象URL"
                        },
                        "interval": {
                            "type": "integer", 
                            "description": "チェック間隔（秒）", 
                            "default": 300
                        },
                        "timeout": {
                            "type": "integer", 
                            "description": "タイムアウト（ミリ秒）", 
                            "default": 10000
                        },
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールID",
                            "default": "ADMINISTRATORS"
                        }
                    },
                    "required": ["monitor_id", "monitor_name", "facility_id", "url"]
                }
            ),
            Tool(
                name="add_ping_monitor",
                description="Hinemos 7.1にPing監視設定を追加（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "monitor_id": {
                            "type": "string", 
                            "description": "ユニークな監視ID"
                        },
                        "monitor_name": {
                            "type": "string", 
                            "description": "監視設定の表示名"
                        },
                        "facility_id": {
                            "type": "string", 
                            "description": "対象ファシリティID"
                        },
                        "interval": {
                            "type": "integer", 
                            "description": "チェック間隔（秒）", 
                            "default": 300
                        },
                        "run_count": {
                            "type": "integer", 
                            "description": "ping試行回数", 
                            "default": 3
                        },
                        "timeout": {
                            "type": "integer", 
                            "description": "タイムアウト（ミリ秒）", 
                            "default": 5000
                        },
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールID",
                            "default": "ADMINISTRATORS"
                        }
                    },
                    "required": ["monitor_id", "monitor_name", "facility_id"]
                }
            ),
            Tool(
                name="get_monitor_list",
                description="Hinemos 7.1から監視設定リストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールIDフィルター（オプション）"
                        }
                    }
                }
            ),
            Tool(
                name="delete_monitor",
                description="Hinemos 7.1から監視設定を削除（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "monitor_ids": {
                            "type": "array", 
                            "items": {"type": "string"}, 
                            "description": "削除する監視IDのリスト"
                        }
                    },
                    "required": ["monitor_ids"]
                }
            ),
            Tool(
                name="get_event_list",
                description="Hinemos 7.1からイベントリストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "facility_id": {
                            "type": "string", 
                            "description": "ファシリティIDフィルター（オプション）"
                        },
                        "priority": {
                            "type": "integer", 
                            "description": "優先度フィルター（オプション）"
                        },
                        "start_date": {
                            "type": "string", 
                            "description": "開始日フィルター（YYYY-MM-DD形式、オプション）"
                        },
                        "end_date": {
                            "type": "string", 
                            "description": "終了日フィルター（YYYY-MM-DD形式、オプション）"
                        },
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールIDフィルター（オプション）"
                        },
                        "limit": {
                            "type": "integer", 
                            "description": "取得件数の上限（デフォルト: 100）",
                            "default": 100
                        }
                    }
                }
            ),
            Tool(
                name="get_scope_list",
                description="Hinemos 7.1からスコープリストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "owner_role_id": {
                            "type": "string", 
                            "description": "オーナーロールIDフィルター（オプション）"
                        }
                    }
                }
            )
        ]
        
        logger.info(f"Created {len(tools)} tools")
        
        # Try different ways to construct ListToolsResult
        try:
            # # Method 1: Basic construction
            # result = ListToolsResult(tools=tools)
            # logger.info("Method 1: Basic ListToolsResult construction succeeded")
            return tools
        except Exception as e1:
            logger.warning(f"Method 1 failed: {e1}")
            
            try:
                # Method 2: With explicit parameters inspection
                import inspect
                sig = inspect.signature(ListToolsResult.__init__)
                logger.info(f"ListToolsResult signature: {sig}")
                
                # Try with all possible parameters
                result = ListToolsResult(tools=tools, nextCursor=None)
                logger.info("Method 2: ListToolsResult with nextCursor succeeded")
                return result
            except Exception as e2:
                logger.warning(f"Method 2 failed: {e2}")
                
                try:
                    # Method 3: Positional arguments
                    result = ListToolsResult(tools)
                    logger.info("Method 3: Positional arguments succeeded")
                    return result
                except Exception as e3:
                    logger.warning(f"Method 3 failed: {e3}")
                    
                    # Method 4: Create using class attributes
                    result = ListToolsResult.__new__(ListToolsResult)
                    result.tools = tools
                    logger.info("Method 4: Manual attribute setting")
                    return result
                    
    except Exception as e:
        logger.error(f"All methods failed in handle_list_tools: {e}", exc_info=True)
        
        # Last resort: try creating the simplest possible result
        try:
            minimal_tool = Tool(
                name="test_connection",
                description="Test",
                inputSchema={"type": "object", "properties": {}}
            )
            return ListToolsResult(tools=[minimal_tool])
        except Exception as final_e:
            logger.error(f"Even minimal approach failed: {final_e}")
            raise

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls"""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    global hinemos_manager
    
    # Initialize manager if not available
    if hinemos_manager is None:
        logger.warning("Hinemos manager not initialized, using mock manager")
        hinemos_manager = MockHinemosManager()
    
    try:
        result = None
        
        if name == "test_connection":
            logger.info("Testing connection")
            result = await hinemos_manager.test_connection()
            
        elif name == "get_node_list":
            logger.info("Executing get_node_list")
            result = await hinemos_manager.get_node_list(**arguments)
            
        elif name == "add_node":
            logger.info("Executing add_node")
            result = await hinemos_manager.add_node(**arguments)
            
        elif name == "delete_node":
            logger.info("Executing delete_node")
            result = await hinemos_manager.delete_node(**arguments)
            
        elif name == "add_http_monitor":
            logger.info("Executing add_http_monitor")
            result = await hinemos_manager.add_http_monitor(**arguments)
            
        elif name == "add_ping_monitor":
            logger.info("Executing add_ping_monitor")
            result = await hinemos_manager.add_ping_monitor(**arguments)
            
        elif name == "get_monitor_list":
            logger.info("Executing get_monitor_list")
            result = await hinemos_manager.get_monitor_list(**arguments)
            
        elif name == "delete_monitor":
            logger.info("Executing delete_monitor")
            result = await hinemos_manager.delete_monitor(**arguments)
            
        elif name == "get_event_list":
            logger.info("Executing get_event_list")
            result = await hinemos_manager.get_event_list(**arguments)
            
        elif name == "get_scope_list":
            logger.info("Executing get_scope_list")
            result = await hinemos_manager.get_scope_list(**arguments)
            
        else:
            logger.error(f"Unknown tool: {name}")
            available_tools = ["test_connection", "get_node_list", "add_node", "delete_node", 
                             "add_http_monitor", "add_ping_monitor", "get_monitor_list", 
                             "delete_monitor", "get_event_list", "get_scope_list"]
            return [TextContent(
                type="text", 
                text=f"未知のツール: {name}\n\n利用可能なツール: {', '.join(available_tools)}"
            )]
        
        # Format result
        import json
        result_text = json.dumps(result, indent=2, ensure_ascii=False)
        logger.info(f"Tool {name} completed successfully")
        
        return [TextContent(
            type="text", 
            text=f"**{name}** が正常に完了しました:\n\n```json\n{result_text}\n```"
        )]
        
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
        return [TextContent(
            type="text", 
            text=f"**{name}** でエラーが発生しました: {str(e)}"
        )]

async def main():
    """Main entry point"""
    logger.info("Starting Hinemos MCP Server (REST API Version for Hinemos 7.1)")
    
    # Debug: Check MCP library details
    try:
        import mcp
        logger.info(f"MCP version: {getattr(mcp, '__version__', 'unknown')}")
        
        from mcp.types import ListToolsResult, Tool
        logger.info(f"ListToolsResult: {ListToolsResult}")
        logger.info(f"Tool: {Tool}")
        
        # Try to create a test instance to understand the structure
        test_tool = Tool(name="test", description="test", inputSchema={"type": "object", "properties": {}})
        logger.info(f"Test tool created: {test_tool}")
        
        # Try to create a test ListToolsResult
        try:
            test_result = ListToolsResult(tools=[test_tool])
            logger.info(f"Test ListToolsResult created successfully: {test_result}")
        except Exception as te:
            logger.error(f"Test ListToolsResult creation failed: {te}")
            
    except Exception as e:
        logger.error(f"MCP library inspection failed: {e}")
    
    # Check environment variables
    endpoint = os.getenv("HINEMOS_ENDPOINT")
    username = os.getenv("HINEMOS_USERNAME") 
    password = os.getenv("HINEMOS_PASSWORD")
    
    logger.info("Configuration:")
    logger.info(f"   HINEMOS_ENDPOINT: {endpoint or 'not set'}")
    logger.info(f"   HINEMOS_USERNAME: {username or 'not set'}")
    logger.info(f"   HINEMOS_PASSWORD: {'set' if password else 'not set'}")
    
    global hinemos_manager
    
    if not all([endpoint, username, password]):
        logger.warning("Hinemos credentials not fully configured, using mock manager")
        hinemos_manager = MockHinemosManager()
    else:
        logger.info("Hinemos credentials configured, initializing REST client")
        try:
            hinemos_manager = HinemosSyncManager()
            logger.info("REST client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize REST client: {e}")
            logger.warning("Falling back to mock manager")
            hinemos_manager = MockHinemosManager()
    
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting MCP server...")
    
    try:
        async with stdio_server() as streams:
            await server.run(
                streams[0], 
                streams[1], 
                InitializationOptions(
                    server_name="hinemos-mcp",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        raise
    finally:
        # Cleanup
        if hinemos_manager and hasattr(hinemos_manager, 'close'):
            await hinemos_manager.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)