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
        return await loop.run_in_executor(None, self.client.get_calendar, **kwargs)

    async def add_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_calendar, **kwargs)

    async def modify_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_calendar, **kwargs)

    async def delete_calendar(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_calendar, **kwargs)

    async def get_calendar_month(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_month, **kwargs)

    async def get_calendar_week(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_week, **kwargs)

    async def get_calendar_pattern_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_pattern_list, **kwargs)

    async def get_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_calendar_pattern, **kwargs)

    async def add_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_calendar_pattern, **kwargs)

    async def modify_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_calendar_pattern, **kwargs)

    async def delete_calendar_pattern(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_calendar_pattern, **kwargs)
    
    async def get_collect_id(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_collect_id, **kwargs)

    async def get_collect_data(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_collect_data, **kwargs)

    async def get_item_code_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_item_code_list, **kwargs)

    async def get_collect_item_code_master_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_collect_item_code_master_list, **kwargs)

    async def get_collect_key_map_for_analytics(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_collect_key_map_for_analytics, **kwargs)

    async def get_available_collector_item_list(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_available_collector_item_list, **kwargs)

    async def get_collect_master_info(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.get_collect_master_info, **kwargs)

    async def add_collect_setting(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.add_collect_setting, **kwargs)

    async def modify_collect_setting(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.modify_collect_setting, **kwargs)

    async def delete_collect_setting(self, **kwargs) -> Dict[str, Any]:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.client.delete_collect_setting, **kwargs)
        
    async def close(self):
        self.client.logout()

# Global manager instance
hinemos_manager = None

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
            ),
            Tool(
                name="get_calendar_list",
                description="Hinemos 7.1からカレンダー一覧を取得（REST API）",
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
                name="get_calendar",
                description="Hinemos 7.1からカレンダー情報を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "カレンダーID"
                        }
                    },
                    "required": ["calendar_id"]
                }
            ),
            Tool(
                name="add_calendar",
                description="Hinemos 7.1にカレンダーを追加（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_info": {
                            "type": "object",
                            "description": "追加するカレンダー情報"
                        }
                    },
                    "required": ["calendar_info"]
                }
            ),
            Tool(
                name="modify_calendar",
                description="Hinemos 7.1のカレンダーを更新（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "カレンダーID"
                        },
                        "calendar_info": {
                            "type": "object",
                            "description": "更新するカレンダー情報"
                        }
                    },
                    "required": ["calendar_id", "calendar_info"]
                }
            ),
            Tool(
                name="delete_calendar",
                description="Hinemos 7.1からカレンダーを削除（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "削除するカレンダーIDリスト"
                        }
                    },
                    "required": ["calendar_ids"]
                }
            ),
            Tool(
                name="get_calendar_month",
                description="Hinemos 7.1からカレンダー月別稼働状態を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "カレンダーID"
                        },
                        "year": {
                            "type": "integer",
                            "description": "年"
                        },
                        "month": {
                            "type": "integer",
                            "description": "月"
                        }
                    },
                    "required": ["calendar_id", "year", "month"]
                }
            ),
            Tool(
                name="get_calendar_week",
                description="Hinemos 7.1からカレンダー週情報を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "カレンダーID"
                        },
                        "year": {
                            "type": "integer",
                            "description": "年"
                        },
                        "month": {
                            "type": "integer",
                            "description": "月"
                        },
                        "day": {
                            "type": "integer",
                            "description": "日"
                        }
                    },
                    "required": ["calendar_id", "year", "month", "day"]
                }
            ),
            Tool(
                name="get_calendar_pattern_list",
                description="Hinemos 7.1からカレンダパターン一覧を取得（REST API）",
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
                name="get_calendar_pattern",
                description="Hinemos 7.1からカレンダパターン情報を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_pattern_id": {
                            "type": "string",
                            "description": "カレンダパターンID"
                        }
                    },
                    "required": ["calendar_pattern_id"]
                }
            ),
            Tool(
                name="add_calendar_pattern",
                description="Hinemos 7.1にカレンダパターンを追加（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "pattern_info": {
                            "type": "object",
                            "description": "追加するカレンダパターン情報"
                        }
                    },
                    "required": ["pattern_info"]
                }
            ),
            Tool(
                name="modify_calendar_pattern",
                description="Hinemos 7.1のカレンダパターンを更新（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_pattern_id": {
                            "type": "string",
                            "description": "カレンダパターンID"
                        },
                        "pattern_info": {
                            "type": "object",
                            "description": "更新するカレンダパターン情報"
                        }
                    },
                    "required": ["calendar_pattern_id", "pattern_info"]
                }
            ),
            Tool(
                name="delete_calendar_pattern",
                description="Hinemos 7.1からカレンダパターンを削除（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "calendar_pattern_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "削除するカレンダパターンIDリスト"
                        }
                    },
                    "required": ["calendar_pattern_ids"]
                }
            ),
            Tool(
                name="get_collect_id",
                description="Hinemos 7.1から収集IDリストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "monitor_id": {"type": "string", "description": "監視設定ID"},
                        "item_name": {"type": "string", "description": "収集項目コード"},
                        "display_name": {"type": "string", "description": "表示名"},
                        "facility_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "ファシリティIDリスト"
                        },
                        "size": {"type": "integer", "description": "取得件数（オプション）"}
                    },
                    "required": ["monitor_id", "item_name", "display_name", "facility_ids"]
                }
            ),
            Tool(
                name="get_collect_data",
                description="Hinemos 7.1から収集データを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id_list": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "収集IDリスト"
                        },
                        "summary_type": {"type": "string", "description": "サマリタイプ"},
                        "from_time": {"type": "string", "description": "取得開始日時 (yyyy-MM-dd HH:mm:ss)"},
                        "to_time": {"type": "string", "description": "取得終了日時 (yyyy-MM-dd HH:mm:ss)"},
                        "size": {"type": "integer", "description": "取得件数（オプション）"}
                    },
                    "required": ["id_list", "summary_type", "from_time", "to_time"]
                }
            ),
            Tool(
                name="get_item_code_list",
                description="Hinemos 7.1から収集項目コードリストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "facility_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "ファシリティIDリスト"
                        },
                        "size": {"type": "integer", "description": "取得件数（オプション）"}
                    },
                    "required": ["facility_ids"]
                }
            ),
            Tool(
                name="get_collect_item_code_master_list",
                description="Hinemos 7.1から収集項目コードマスタ一覧を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_collect_key_map_for_analytics",
                description="Hinemos 7.1から収集値キーの一覧を取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "facility_id": {"type": "string", "description": "ファシリティID"},
                        "owner_role_id": {"type": "string", "description": "オーナーロールID"}
                    },
                    "required": ["facility_id", "owner_role_id"]
                }
            ),
            Tool(
                name="get_available_collector_item_list",
                description="Hinemos 7.1から収集可能な項目リストを取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "facility_id": {"type": "string", "description": "ファシリティID"}
                    },
                    "required": ["facility_id"]
                }
            ),
            Tool(
                name="get_collect_master_info",
                description="Hinemos 7.1から収集マスタ情報を一括取得（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="add_collect_setting",
                description="Hinemos 7.1に収集設定を追加（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "collect_info": {
                            "type": "object",
                            "description": "追加する収集設定情報"
                        }
                    },
                    "required": ["collect_info"]
                }
            ),
            Tool(
                name="modify_collect_setting",
                description="Hinemos 7.1の収集設定を更新（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "collect_id": {"type": "string", "description": "収集設定ID"},
                        "collect_info": {
                            "type": "object",
                            "description": "更新する収集設定情報"
                        }
                    },
                    "required": ["collect_id", "collect_info"]
                }
            ),
            Tool(
                name="delete_collect_setting",
                description="Hinemos 7.1から収集設定を削除（REST API）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "collect_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "削除する収集設定IDリスト"
                        }
                    },
                    "required": ["collect_ids"]
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
            
        elif name == "get_calendar_list":
            logger.info("Executing get_calendar_list")
            result = await hinemos_manager.get_calendar_list(**arguments)

        elif name == "get_calendar":
            logger.info("Executing get_calendar")
            result = await hinemos_manager.get_calendar(**arguments)

        elif name == "add_calendar":
            logger.info("Executing add_calendar")
            result = await hinemos_manager.add_calendar(**arguments)

        elif name == "modify_calendar":
            logger.info("Executing modify_calendar")
            result = await hinemos_manager.modify_calendar(**arguments)

        elif name == "delete_calendar":
            logger.info("Executing delete_calendar")
            result = await hinemos_manager.delete_calendar(**arguments)

        elif name == "get_calendar_month":
            logger.info("Executing get_calendar_month")
            result = await hinemos_manager.get_calendar_month(**arguments)

        elif name == "get_calendar_week":
            logger.info("Executing get_calendar_week")
            result = await hinemos_manager.get_calendar_week(**arguments)

        elif name == "get_calendar_pattern_list":
            logger.info("Executing get_calendar_pattern_list")
            result = await hinemos_manager.get_calendar_pattern_list(**arguments)

        elif name == "get_calendar_pattern":
            logger.info("Executing get_calendar_pattern")
            result = await hinemos_manager.get_calendar_pattern(**arguments)

        elif name == "add_calendar_pattern":
            logger.info("Executing add_calendar_pattern")
            result = await hinemos_manager.add_calendar_pattern(**arguments)

        elif name == "modify_calendar_pattern":
            logger.info("Executing modify_calendar_pattern")
            result = await hinemos_manager.modify_calendar_pattern(**arguments)

        elif name == "delete_calendar_pattern":
            logger.info("Executing delete_calendar_pattern")
            result = await hinemos_manager.delete_calendar_pattern(**arguments)

        elif name == "get_collect_id":
            logger.info("Executing get_collect_id")
            result = await hinemos_manager.get_collect_id(**arguments)

        elif name == "get_collect_data":
            logger.info("Executing get_collect_data")
            result = await hinemos_manager.get_collect_data(**arguments)

        elif name == "get_item_code_list":
            logger.info("Executing get_item_code_list")
            result = await hinemos_manager.get_item_code_list(**arguments)

        elif name == "get_collect_item_code_master_list":
            logger.info("Executing get_collect_item_code_master_list")
            result = await hinemos_manager.get_collect_item_code_master_list(**arguments)

        elif name == "get_collect_key_map_for_analytics":
            logger.info("Executing get_collect_key_map_for_analytics")
            result = await hinemos_manager.get_collect_key_map_for_analytics(**arguments)

        elif name == "get_available_collector_item_list":
            logger.info("Executing get_available_collector_item_list")
            result = await hinemos_manager.get_available_collector_item_list(**arguments)

        elif name == "get_collect_master_info":
            logger.info("Executing get_collect_master_info")
            result = await hinemos_manager.get_collect_master_info(**arguments)

        elif name == "add_collect_setting":
            logger.info("Executing add_collect_setting")
            result = await hinemos_manager.add_collect_setting(**arguments)

        elif name == "modify_collect_setting":
            logger.info("Executing modify_collect_setting")
            result = await hinemos_manager.modify_collect_setting(**arguments)

        elif name == "delete_collect_setting":
            logger.info("Executing delete_collect_setting")
            result = await hinemos_manager.delete_collect_setting(**arguments)

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