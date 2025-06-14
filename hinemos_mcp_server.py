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
        
    async def get_facility_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_facility_list, **kwargs)

    async def get_facility_tree(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_facility_tree, **kwargs)

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

    # --- ジョブ管理API ---
    async def get_job_tree_simple(self, ownerRoleId=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_job_tree_simple, ownerRoleId)

    async def get_job_tree_full(self, ownerRoleId=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_job_tree_full, ownerRoleId)

    async def get_job_info(self, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_job_info, jobunitId, jobId)

    async def get_job_info_bulk(self, jobList):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_job_info_bulk, jobList)

    async def add_jobunit(self, jobunit, isClient=False):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_jobunit, jobunit, isClient)

    async def modify_jobunit(self, jobunitId, jobunit, isClient=False):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_jobunit, jobunitId, jobunit, isClient)

    async def delete_jobunit(self, jobunitId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_jobunit, jobunitId)

    async def get_edit_lock(self, jobunitId, updateTime, forceFlag):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_edit_lock, jobunitId, updateTime, forceFlag)

    async def check_edit_lock(self, jobunitId, editSession):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.check_edit_lock, jobunitId, editSession)

    async def release_edit_lock(self, jobunitId, editSession):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.release_edit_lock, jobunitId, editSession)

    async def add_jobnet(self, jobunitId, jobnet):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_jobnet, jobunitId, jobnet)

    async def add_command_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_command_job, jobunitId, job)

    async def add_file_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_file_job, jobunitId, job)

    async def add_refer_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_refer_job, jobunitId, job)

    async def add_monitor_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_monitor_job, jobunitId, job)

    async def add_approval_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_approval_job, jobunitId, job)

    async def add_joblinksend_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_joblinksend_job, jobunitId, job)

    async def add_joblinkrcv_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_joblinkrcv_job, jobunitId, job)

    async def add_filecheck_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_filecheck_job, jobunitId, job)

    async def add_rpa_job(self, jobunitId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_rpa_job, jobunitId, job)

    async def delete_job(self, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_job, jobunitId, jobId)

    async def run_job(self, jobunitId, jobId, runJobRequest):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.run_job, jobunitId, jobId, runJobRequest)

    async def run_job_kick(self, jobKickId, runJobKickRequest):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.run_job_kick, jobKickId, runJobKickRequest)

    async def session_job_operation(self, sessionId, jobunitId, jobId, operation):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.session_job_operation, sessionId, jobunitId, jobId, operation)

    async def session_node_operation(self, sessionId, jobunitId, jobId, facilityId, operation):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.session_node_operation, sessionId, jobunitId, jobId, facilityId, operation)

    async def get_session_job_detail(self, sessionId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_session_job_detail, sessionId)

    async def get_session_node_detail(self, sessionId, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_session_node_detail, sessionId, jobunitId, jobId)

    async def get_session_file_detail(self, sessionId, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_session_file_detail, sessionId, jobunitId, jobId)

    async def get_session_job_jobInfo(self, sessionId, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_session_job_jobInfo, sessionId, jobunitId, jobId)

    async def get_session_job_allDetail(self, sessionId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_session_job_allDetail, sessionId)

    async def history_search(self, size, filter):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.history_search, size, filter)

    async def add_schedule(self, schedule):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_schedule, schedule)

    async def add_filecheck(self, filecheck):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_filecheck, filecheck)

    async def add_manual(self, manual):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_manual, manual)

    async def add_joblinkrcv(self, joblinkrcv):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_joblinkrcv, joblinkrcv)

    async def get_kick_list(self):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_kick_list)

    async def kick_search(self, condition):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.kick_search, condition)

    async def set_kick_valid(self, setStatus):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.set_kick_valid, setStatus)

    async def delete_kick(self, jobkickIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_kick, jobkickIds)

    async def session_approval_search(self, request):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.session_approval_search, request)

    async def modify_approval_info(self, sessionId, jobunitId, jobId, info):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_approval_info, sessionId, jobunitId, jobId, info)

    async def get_queue_list(self, roleId=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_queue_list, roleId)

    async def get_queue_detail(self, queueId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_queue_detail, queueId)

    async def add_queue(self, queue):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_queue, queue)

    async def modify_queue(self, queueId, queue):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_queue, queueId, queue)

    async def delete_queue(self, queueIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_queue, queueIds)

    async def queue_activity_search(self, request):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.queue_activity_search, request)

    async def queue_activity_detail(self, queueId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.queue_activity_detail, queueId)

    async def get_joblinksend_setting_list(self, ownerRoleId=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_joblinksend_setting_list, ownerRoleId)

    async def get_joblinksend_setting_detail(self, joblinkSendSettingId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_joblinksend_setting_detail, joblinkSendSettingId)

    async def add_joblinksend_setting(self, setting):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_joblinksend_setting, setting)

    async def modify_joblinksend_setting(self, joblinkSendSettingId, setting):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_joblinksend_setting, joblinkSendSettingId, setting)

    async def delete_joblinksend_setting(self, joblinkSendSettingIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_joblinksend_setting, joblinkSendSettingIds)

    async def regist_joblink_message(self, message):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.regist_joblink_message, message)

    async def send_joblink_message_manual(self, message):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.send_joblink_message_manual, message)

    async def joblink_message_search(self, request):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.joblink_message_search, request)

    async def available_start_operation(self, sessionId, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.available_start_operation, sessionId, jobunitId, jobId)

    async def available_start_operation_node(self, sessionId, jobunitId, jobId, facilityId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.available_start_operation_node, sessionId, jobunitId, jobId, facilityId)

    async def available_stop_operation(self, sessionId, jobunitId, jobId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.available_stop_operation, sessionId, jobunitId, jobId)

    async def available_stop_operation_node(self, sessionId, jobunitId, jobId, facilityId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.available_stop_operation_node, sessionId, jobunitId, jobId, facilityId)

    async def get_rpa_login_resolution(self):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_rpa_login_resolution)

    async def get_rpa_screenshot(self, sessionId, jobunitId, jobId, facilityId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_rpa_screenshot, sessionId, jobunitId, jobId, facilityId)

    async def get_rpa_screenshot_file(self, sessionId, jobunitId, jobId, facilityId, regDate):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_rpa_screenshot_file, sessionId, jobunitId, jobId, facilityId, regDate)

    async def get_jobmap_icon_image_iconId(self, ownerRoleId=None):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_jobmap_icon_image_iconId, ownerRoleId)

    async def delete_premakejobsession(self, jobkickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_premakejobsession, jobkickId)

    async def get_schedule_plan(self, plan):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_schedule_plan, plan)

    async def get_job_referrer_queue(self, queueId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_job_referrer_queue, queueId)

    async def queue_search(self, search):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.queue_search, search)

    async def modify_jobnet(self, jobunitId, jobId, jobnet):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_jobnet, jobunitId, jobId, jobnet)

    async def modify_command_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_command_job, jobunitId, jobId, job)

    async def modify_file_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_file_job, jobunitId, jobId, job)

    async def modify_refer_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_refer_job, jobunitId, jobId, job)

    async def modify_monitor_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_monitor_job, jobunitId, jobId, job)

    async def modify_approval_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_approval_job, jobunitId, jobId, job)

    async def modify_joblinksend_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_joblinksend_job, jobunitId, jobId, job)

    async def modify_joblinkrcv_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_joblinkrcv_job, jobunitId, jobId, job)

    async def modify_filecheck_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_filecheck_job, jobunitId, jobId, job)

    async def modify_rpa_job(self, jobunitId, jobId, job):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_rpa_job, jobunitId, jobId, job)

    async def get_schedule_detail(self, jobKickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_schedule_detail, jobKickId)

    async def get_filecheck_detail(self, jobKickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_filecheck_detail, jobKickId)

    async def get_manual_detail(self, jobKickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_manual_detail, jobKickId)

    async def get_joblinkrcv_detail(self, jobKickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_joblinkrcv_detail, jobKickId)

    async def get_kick_detail(self, jobKickId):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_kick_detail, jobKickId)

    async def modify_schedule(self, jobKickId, schedule):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_schedule, jobKickId, schedule)

    async def modify_filecheck(self, jobKickId, filecheck):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_filecheck, jobKickId, filecheck)

    async def modify_manual(self, jobKickId, manual):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_manual, jobKickId, manual)

    async def modify_joblinkrcv(self, jobKickId, joblinkrcv):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_joblinkrcv, jobKickId, joblinkrcv)

    async def delete_schedule(self, jobkickIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_schedule, jobkickIds)

    async def delete_filecheck(self, jobkickIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_filecheck, jobkickIds)

    async def delete_manual(self, jobkickIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_manual, jobkickIds)

    async def delete_joblinkrcv(self, jobkickIds):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_joblinkrcv, jobkickIds)

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