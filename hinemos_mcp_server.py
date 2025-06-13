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
from client.hinemos_client import HinemosClient

# Fix encoding for Windows Japanese environment
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import TextContent, Tool, ListToolsResult

from mcp_tools import get_all_tools, dispatch_tool

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

    async def get_calendar_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_list, **kwargs)

    async def get_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar, kwargs["calendar_id"])

    async def add_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_calendar, kwargs['calendar_info'])

    async def modify_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_calendar, kwargs["calendar_id"], kwargs["calendar_info"])

    async def delete_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_calendar, kwargs["calendar_ids"])

    async def get_calendar_month(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_month, kwargs["calendar_id"], kwargs["year"], kwargs["month"])

    async def get_calendar_week(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_week, kwargs["calendar_id"], kwargs["year"], kwargs["month"], kwargs["day"])

    async def get_calendar_pattern_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_pattern_list, **kwargs)

    async def get_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_pattern, kwargs["calendar_pattern_id"])

    async def add_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_calendar_pattern, kwargs['pattern_info'])

    async def modify_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_calendar_pattern, kwargs["calendar_pattern_id"], kwargs["pattern_info"])

    async def delete_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_calendar_pattern, kwargs["calendar_pattern_ids"])

    # --- 監視設定一覧・検索 ---
    async def get_monitor_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_monitor_list)

    async def get_monitor_list_by_condition(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.search_monitor_list, kwargs.get("monitor_filter_info"))

    async def get_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_monitor, kwargs.get("monitor_id"))

    async def delete_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_monitor, kwargs.get("monitor_ids"))

    async def set_status_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.set_status_monitor, kwargs.get("monitor_ids"), kwargs.get("valid_flg"))

    async def set_status_collector(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.set_status_collector, kwargs.get("monitor_ids"), kwargs.get("valid_flg"))

    # --- HTTPシナリオ監視 ---
    async def add_http_scenario_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_http_scenario_monitor, kwargs.get("monitor_info"))

    async def modify_http_scenario_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_http_scenario_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_http_scenario_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_http_scenario_list, kwargs.get("monitor_id"))

    # --- HTTP監視（数値） ---
    async def add_http_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_http_numeric_monitor, kwargs.get("monitor_info"))

    async def modify_http_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_http_numeric_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_http_numeric_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_http_numeric_list, kwargs.get("monitor_id"))

    # --- HTTP監視（文字列） ---
    async def add_http_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_http_string_monitor, kwargs.get("monitor_info"))

    async def modify_http_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_http_string_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_http_string_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_http_string_list, kwargs.get("monitor_id"))

    # --- エージェント監視 ---
    async def add_agent_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_agent_monitor, kwargs.get("monitor_info"))

    async def modify_agent_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_agent_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_agent_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_agent_list, kwargs.get("monitor_id"))

    # --- JMX監視 ---
    async def add_jmx_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_jmx_monitor, kwargs.get("monitor_info"))

    async def modify_jmx_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_jmx_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_jmx_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_jmx_list, kwargs.get("monitor_id"))

    async def get_jmx_url_format_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_jmx_url_format_list)

    # --- PING監視 ---
    async def add_ping_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_ping_monitor, kwargs.get("monitor_info"))

    async def modify_ping_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_ping_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_ping_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_ping_list, kwargs.get("monitor_id"))

    # --- カスタム監視（数値） ---
    async def add_custom_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_custom_numeric_monitor, kwargs.get("monitor_info"))

    async def modify_custom_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_custom_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_custom_numeric_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_custom_list, kwargs.get("monitor_id"))

    # --- カスタム監視（文字列） ---
    async def add_custom_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_custom_string_monitor, kwargs.get("monitor_info"))

    async def modify_custom_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_custom_string_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_custom_string_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_custom_string_list, kwargs.get("monitor_id"))
    
    # --- リソース監視 ---
    async def add_performance_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_performance_monitor, kwargs.get("monitor_info"))

    async def modify_performance_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_performance_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_performance_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_performance_list, kwargs.get("monitor_id"))

    # --- JMXマスタ管理 ---
    async def get_jmx_master_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_jmx_master_list)

    async def add_jmx_master_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_jmx_master_list, kwargs.get("jmx_master_list"))

    async def delete_jmx_master(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_jmx_master, kwargs.get("jmx_master_ids"))

    async def delete_jmx_master_all(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_jmx_master_all)

    # --- 補助API ---
    async def get_jdbc_driver_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_jdbc_driver_list)

    async def get_binary_preset_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_binary_preset_list)

    async def get_monitor_string_tag_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_monitor_string_tag_list, kwargs.get("monitor_id"), kwargs.get("owner_role_id"))

    # --- SNMP監視（数値/文字列） ---
    async def add_snmp_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_snmp_numeric_monitor, kwargs.get("monitor_info"))

    async def modify_snmp_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_snmp_numeric_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_snmp_numeric_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_snmp_numeric_list, kwargs.get("monitor_id"))

    async def add_snmp_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_snmp_string_monitor, kwargs.get("monitor_info"))

    async def modify_snmp_string_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_snmp_string_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_snmp_string_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_snmp_string_list, kwargs.get("monitor_id"))

    # --- SQL監視 ---
    async def add_sql_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_sql_numeric_monitor, kwargs.get("monitor_info"))

    async def modify_sql_numeric_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_sql_numeric_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_sql_numeric_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_sql_numeric_list, kwargs.get("monitor_id"))

    # --- ログファイル監視 ---
    async def add_logfile_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_logfile_monitor, kwargs.get("monitor_info"))

    async def modify_logfile_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_logfile_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_logfile_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_logfile_list, kwargs.get("monitor_id"))

    # --- プロセス監視 ---
    async def add_process_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_process_monitor, kwargs.get("monitor_info"))

    async def modify_process_monitor(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_process_monitor, kwargs.get("monitor_id"), kwargs.get("monitor_info"))

    async def get_process_list(self, **kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_process_list, kwargs.get("monitor_id"))

    # --- 監視結果API ---
    async def event_search(self, filter, size=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_search,
            filter,
            size
        )

    async def scope_list(self, facility_id=None, status_flag=None, event_flag=None, order_flg=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.scope_list,
            facility_id,
            status_flag,
            event_flag,
            order_flg
        )

    async def status_search(self, filter, size=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.status_search,
            filter,
            size
        )

    async def status_delete(self, status_data_info_request_list):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.status_delete,
            status_data_info_request_list
        )

    async def event_download(self, filter, selected_events=None, filename=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_download,
            filter,
            selected_events,
            filename
        )

    async def event_detail_search(self, monitorId, monitorDetailId, pluginId, facilityId, outputDate):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_detail_search,
            monitorId,
            monitorDetailId,
            pluginId,
            facilityId,
            outputDate
        )

    async def event_comment(self, monitorId, monitorDetailId, pluginId, facilityId, outputDate, comment, commentDate, commentUser):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_comment,
            monitorId,
            monitorDetailId,
            pluginId,
            facilityId,
            outputDate,
            comment,
            commentDate,
            commentUser
        )

    async def event_confirm(self, list, confirmType):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_confirm,
            list,
            confirmType
        )

    async def event_multiConfirm(self, confirmType, filter):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_multiConfirm,
            confirmType,
            filter
        )

    async def event_collectGraphFlg(self, list, collectGraphFlg):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_collectGraphFlg,
            list,
            collectGraphFlg
        )

    async def event_update(self, info):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_update,
            info
        )

    async def eventCustomCommand_exec(self, commandNo, eventList):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.eventCustomCommand_exec,
            commandNo,
            eventList
        )

    async def eventCustomCommand_result(self, uuid):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.eventCustomCommand_result,
            uuid
        )

    async def event_collectValid_mapKeyFacility(self, facilityIdList=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.event_collectValid_mapKeyFacility,
            facilityIdList
        )

    async def close(self):
        self.client.logout()

# Global manager instance
hinemos_manager = None

# Create the MCP server
server = Server("hinemos-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:

    logger.info("LIST_TOOLS called - returning available tools")
    
    # First, let's try to understand what ListToolsResult expects
    logger.info("Inspecting ListToolsResult...")
    logger.info(f"ListToolsResult annotations: {getattr(ListToolsResult, '__annotations__', 'none')}")
    
    # Create tools for Hinemos 7.1 REST API
    tools = []
    extention_tools = get_all_tools()
    tools.extend(extention_tools)
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    global hinemos_manager
    if hinemos_manager is None:
        # ...モックやエラー処理...
        pass
    try:
        result = await dispatch_tool(name, hinemos_manager, arguments)
        if result is None:
            return [TextContent(type="text", text=f"未知のツール: {name}")]
        import json
        return [TextContent(type="text", text=f"**{name}**:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")]
    except Exception as e:
        return [TextContent(type="text", text=f"**{name}** でエラー: {str(e)}")]


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
        exit(1)
    else:
        logger.info("Hinemos credentials configured, initializing REST client")
        try:
            hinemos_manager = HinemosSyncManager()
            logger.info("REST client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize REST client: {e}")
            exit(1)

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