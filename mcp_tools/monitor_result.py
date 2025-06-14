from mcp.types import Tool

def get_tools():
    return [
        Tool(
            name="event_search",
            description="Hinemos 7.1イベント一覧検索（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "object",
                        "description": "検索条件（facilityId, priority, generationDateFrom, generationDateTo, outputDateFrom, outputDateTo, monitorId, application, confirmType, ownerRoleId等）"
                    },
                    "size": {
                        "type": "integer",
                        "description": "取得件数上限（例: 1000）"
                    }
                },
                "required": ["filter"]
            }
        ),
        Tool(
            name="scope_list",
            description="Hinemos 7.1スコープ一覧取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {"type": "string", "description": "親ファシリティID"},
                    "status_flag": {"type": "boolean", "description": "ステータス情報取得フラグ"},
                    "event_flag": {"type": "boolean", "description": "イベント情報取得フラグ"},
                    "order_flg": {"type": "boolean", "description": "ソート順フラグ"},
                }
            }
        ),
        Tool(
            name="status_search",
            description="Hinemos 7.1ステータス一覧検索（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "object",
                        "description": "検索条件（facilityId, priority, monitorId, application, ownerRoleId等）"
                    },
                    "size": {
                        "type": "integer",
                        "description": "取得件数上限（例: 500）"
                    }
                },
                "required": ["filter"]
            }
        ),
        Tool(
            name="status_delete",
            description="Hinemos 7.1ステータス削除（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_data_info_request_list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "facilityId": {"type": "string"},
                                "monitorId": {"type": "string"},
                                "monitorDetailId": {"type": "string"},
                                "pluginId": {"type": "string"},
                                "outputDate": {"type": "string"}
                            },
                            "required": ["facilityId", "monitorId", "pluginId", "outputDate"]
                        },
                        "description": "削除対象リスト"
                    }
                },
                "required": ["status_data_info_request_list"]
            }
        ),
        Tool(
            name="event_download",
            description="Hinemos 7.1イベントファイルダウンロード（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "object",
                        "description": "検索条件（facilityId, priority, generationDateFrom, generationDateTo等）"
                    },
                    "selected_events": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "monitorId": {"type": "string"},
                                "monitorDetailId": {"type": "string"},
                                "pluginId": {"type": "string"},
                                "facilityId": {"type": "string"},
                                "outputDate": {"type": "string"}
                            }
                        },
                        "description": "ダウンロード対象イベントリスト"
                    },
                    "filename": {"type": "string", "description": "出力ファイル名"}
                },
                "required": ["filter", "filename"]
            }
        ),
        Tool(
            name="event_detail_search",
            description="Hinemos 7.1イベント詳細検索（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitorId": {"type": "string"},
                    "monitorDetailId": {"type": "string"},
                    "pluginId": {"type": "string"},
                    "facilityId": {"type": "string"},
                    "outputDate": {"type": "string"}
                },
                "required": ["monitorId", "pluginId", "facilityId", "outputDate"]
            }
        ),
        Tool(
            name="event_comment",
            description="Hinemos 7.1イベントコメント更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitorId": {"type": "string"},
                    "monitorDetailId": {"type": "string"},
                    "pluginId": {"type": "string"},
                    "facilityId": {"type": "string"},
                    "outputDate": {"type": "string"},
                    "comment": {"type": "string"},
                    "commentDate": {"type": "string"},
                    "commentUser": {"type": "string"}
                },
                "required": ["monitorId", "pluginId", "facilityId", "outputDate", "comment", "commentDate", "commentUser"]
            }
        ),
        Tool(
            name="event_confirm",
            description="Hinemos 7.1イベント確認状態更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "monitorId": {"type": "string"},
                                "monitorDetailId": {"type": "string"},
                                "pluginId": {"type": "string"},
                                "facilityId": {"type": "string"},
                                "outputDate": {"type": "string"}
                            },
                            "required": ["monitorId", "pluginId", "facilityId", "outputDate"]
                        }
                    },
                    "confirmType": {"type": "integer", "description": "確認タイプ（0:未確認, 1:確認中, 2:確認済）"}
                },
                "required": ["list", "confirmType"]
            }
        ),
        Tool(
            name="event_multiConfirm",
            description="Hinemos 7.1イベント一括確認更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirmType": {"type": "integer", "description": "確認タイプ"},
                    "filter": {
                        "type": "object",
                        "description": "検索条件（facilityId, priority, generationDateFrom, generationDateTo, confirmType等）"
                    }
                },
                "required": ["confirmType", "filter"]
            }
        ),
        Tool(
            name="event_collectGraphFlg",
            description="Hinemos 7.1性能グラフフラグ更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "monitorId": {"type": "string"},
                                "monitorDetailId": {"type": "string"},
                                "pluginId": {"type": "string"},
                                "facilityId": {"type": "string"},
                                "outputDate": {"type": "string"}
                            },
                            "required": ["monitorId", "pluginId", "facilityId", "outputDate"]
                        }
                    },
                    "collectGraphFlg": {"type": "boolean", "description": "性能グラフ用フラグ"}
                },
                "required": ["list", "collectGraphFlg"]
            }
        ),
        Tool(
            name="event_update",
            description="Hinemos 7.1イベント情報更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "info": {
                        "type": "object",
                        "description": "イベント情報（monitorId, monitorDetailId, pluginId, facilityId, outputDate, priority, message, comment等）"
                    }
                },
                "required": ["info"]
            }
        ),
        Tool(
            name="eventCustomCommand_exec",
            description="Hinemos 7.1イベントカスタムコマンド実行（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "commandNo": {"type": "integer", "description": "コマンド番号"},
                    "eventList": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "monitorId": {"type": "string"},
                                "monitorDetailId": {"type": "string"},
                                "pluginId": {"type": "string"},
                                "facilityId": {"type": "string"},
                                "outputDate": {"type": "string"}
                            },
                            "required": ["monitorId", "pluginId", "facilityId", "outputDate"]
                        }
                    }
                },
                "required": ["commandNo", "eventList"]
            }
        ),
        Tool(
            name="eventCustomCommand_result",
            description="Hinemos 7.1イベントカスタムコマンド結果取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "コマンド結果ID"}
                },
                "required": ["uuid"]
            }
        ),
        Tool(
            name="event_collectValid_mapKeyFacility",
            description="Hinemos 7.1イベントデータマップ取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facilityIdList": {"type": "string", "description": "カンマ区切りのファシリティIDリスト"}
                }
            }
        ),
    ]

async def dispatch(name, manager, arguments):
    if name == "event_search":
        return await manager.event_search(
            filter=arguments.get("filter"),
            size=arguments.get("size"),
        )
    elif name == "scope_list":
        return await manager.scope_list(
            facility_id=arguments.get("facility_id"),
            status_flag=arguments.get("status_flag"),
            event_flag=arguments.get("event_flag"),
            order_flg=arguments.get("order_flg"),
        )
    elif name == "status_search":
        return await manager.status_search(
            filter=arguments.get("filter"),
            size=arguments.get("size"),
        )
    elif name == "status_delete":
        return await manager.status_delete(
            status_data_info_request_list=arguments.get("status_data_info_request_list"),
        )
    elif name == "event_download":
        return await manager.event_download(
            filter=arguments.get("filter"),
            selected_events=arguments.get("selected_events"),
            filename=arguments.get("filename"),
        )
    elif name == "event_detail_search":
        return await manager.event_detail_search(
            monitorId=arguments.get("monitorId"),
            monitorDetailId=arguments.get("monitorDetailId"),
            pluginId=arguments.get("pluginId"),
            facilityId=arguments.get("facilityId"),
            outputDate=arguments.get("outputDate"),
        )
    elif name == "event_comment":
        return await manager.event_comment(
            monitorId=arguments.get("monitorId"),
            monitorDetailId=arguments.get("monitorDetailId"),
            pluginId=arguments.get("pluginId"),
            facilityId=arguments.get("facilityId"),
            outputDate=arguments.get("outputDate"),
            comment=arguments.get("comment"),
            commentDate=arguments.get("commentDate"),
            commentUser=arguments.get("commentUser"),
        )
    elif name == "event_confirm":
        return await manager.event_confirm(
            list=arguments.get("list"),
            confirmType=arguments.get("confirmType"),
        )
    elif name == "event_multiConfirm":
        return await manager.event_multiConfirm(
            confirmType=arguments.get("confirmType"),
            filter=arguments.get("filter"),
        )
    elif name == "event_collectGraphFlg":
        return await manager.event_collectGraphFlg(
            list=arguments.get("list"),
            collectGraphFlg=arguments.get("collectGraphFlg"),
        )
    elif name == "event_update":
        return await manager.event_update(
            info=arguments.get("info"),
        )
    elif name == "eventCustomCommand_exec":
        return await manager.eventCustomCommand_exec(
            commandNo=arguments.get("commandNo"),
            eventList=arguments.get("eventList"),
        )
    elif name == "eventCustomCommand_result":
        return await manager.eventCustomCommand_result(
            uuid=arguments.get("uuid"),
        )
    elif name == "event_collectValid_mapKeyFacility":
        return await manager.event_collectValid_mapKeyFacility(
            facilityIdList=arguments.get("facilityIdList"),
        )
    return None