from mcp.types import Tool
from typing import List

def get_tools():
    return [
        Tool(
            name="get_calendar_list",
            description="Hinemos 7.1カレンダー一覧を取得（REST API）",
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
            description="Hinemos 7.1カレンダー情報を取得（REST API）",
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
            description="Hinemos 7.1カレンダーを追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_info": {
                        "type": "object",
                        "description": (
                            "カレンダー情報(dict)。例:\n"
                            "{\n"
                            "  \"calendarId\": \"CALENDAR_001\",                # 必須, 1-64文字, 英数字/アンダースコア/ハイフン\n"
                            "  \"calendarName\": \"営業日カレンダー\",           # 必須, 最大256文字\n"
                            "  \"description\": \"営業日の定義\",                # 任意, 最大256文字\n"
                            "  \"ownerRoleId\": \"ADMINISTRATORS\",              # 必須, 最大64文字\n"
                            "  \"validTimeFrom\": \"2024-01-01T00:00:00.000Z\",  # 必須, ISO8601形式（自動でHinemos形式に変換）\n"
                            "  \"validTimeTo\": \"2024-12-31T23:59:59.999Z\",    # 必須, ISO8601形式（自動でHinemos形式に変換）\n"
                            "  \"calendarDetailList\": [                         # 任意, 詳細リスト\n"
                            "    {\n"
                            "      \"orderNo\": 1,\n"
                            "      \"year\": 2024,\n"
                            "      \"month\": 1,\n"
                            "      \"day\": 1,\n"
                            "      \"dayType\": \"SPECIFIC_DAY\",                # 例: \"SPECIFIC_DAY\", \"DAY\"\n"
                            "      \"startTime\": \"09:00:00\",                  # \"HH:mm:ss\"形式\n"
                            "      \"endTime\": \"18:00:00\",                    # \"HH:mm:ss\"形式\n"
                            "      \"executeFlg\": true,                        # true: 稼働日, false: 非稼働日\n"
                            "      \"description\": \"元日\"\n"
                            "    },\n"
                            "    # 曜日指定の場合（週間パターン）\n"
                            "    {\n"
                            "      \"orderNo\": 2,\n"
                            "      \"yearNo\": 0,                               # 0: 全年\n"
                            "      \"monthNo\": 0,                              # 0: 全月\n"
                            "      \"dayNo\": 1,                                # 1=日曜, 2=月曜, 3=火曜, 4=水曜, 5=木曜, 6=金曜, 7=土曜\n"
                            "      \"dayType\": \"DAY\",\n"
                            "      \"startTime\": \"00:00:00\",\n"
                            "      \"endTime\": \"24:00:00\",\n"
                            "      \"executeFlg\": false,                       # 非稼働日\n"
                            "      \"description\": \"日曜日は非稼働\",\n"
                            "      \"weekNo\": null,\n"
                            "      \"weekXth\": null,\n"
                            "      \"calPatternId\": null,\n"
                            "      \"afterDay\": 0,\n"
                            "      \"substituteFlg\": false,\n"
                            "      \"substituteTime\": 24,\n"
                            "      \"substituteLimit\": 10,\n"
                            "      \"calPatternInfo\": null\n"
                            "    }\n"
                            "  ]\n"
                            "}\n"
                            "注意: \n"
                            "- validTimeFrom/validTimeToはISO8601形式で指定可能（内部で自動変換）\n"
                            "- dayNo（曜日）は1=日曜日から7=土曜日まで（0は無効）\n"
                            "- executeFlg: true=稼働日, false=非稼働日\n"
                            "- 時刻はHH:mm:ss形式で指定（HH:mmも可）"
                        )
                    }
                },
                "required": ["calendar_info"]
            }
        ),
        Tool(
            name="modify_calendar",
            description="Hinemos 7.1カレンダーを更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "カレンダーID"
                    },
                    "calendar_info": {
                        "type": "object",
                        "description": (
                            "カレンダー情報(dict)。add_calendarと同じだがcalendarIdは除く"
                        )
                    }
                },
                "required": ["calendar_id", "calendar_info"]
            }
        ),
        Tool(
            name="delete_calendar",
            description="Hinemos 7.1カレンダーを削除（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "削除するカレンダーIDリスト 例: [\"CALENDAR_001\", \"CALENDAR_002\"]"
                    }
                },
                "required": ["calendar_ids"]
            }
        ),
        Tool(
            name="get_calendar_month",
            description="Hinemos 7.1カレンダー月別稼働状態を取得（REST API）",
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
            description="Hinemos 7.1カレンダー週情報（詳細）を取得（REST API）",
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
            description="Hinemos 7.1カレンダーパターン一覧を取得（REST API）",
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
            description="Hinemos 7.1カレンダーパターン情報を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_pattern_id": {
                        "type": "string",
                        "description": "カレンダーパターンID"
                    }
                },
                "required": ["calendar_pattern_id"]
            }
        ),
        Tool(
            name="add_calendar_pattern",
            description="Hinemos 7.1カレンダーパターンを追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern_info": {
                        "type": "object",
                        "description": (
                            "カレンダーパターン情報(dict)。例:\n"
                            "{\n"
                            "  \"calendarPatternId\": \"PATTERN_001\",           # 必須, 1-64文字, 英数字/アンダースコア/ハイフン\n"
                            "  \"calendarPatternName\": \"週末パターン\",        # 必須, 最大256文字\n"
                            "  \"ownerRoleId\": \"ADMINISTRATORS\",              # 必須, 最大64文字\n"
                            "  \"description\": \"土日を非稼働とするパターン\",   # 任意, 最大256文字\n"
                            "  \"calPatternDetailInfoEntities\": [               # 任意, 詳細日付リスト\n"
                            "    {\n"
                            "      \"yearNo\": 2025,                            # 年\n"
                            "      \"monthNo\": 12,                             # 月\n"
                            "      \"dayNo\": 25                                # 日\n"
                            "    }\n"
                            "  ]\n"
                            "}\n"
                            "注意: \n"
                            "- calendarPatternId（calPatternIdではない）が正しいキー名\n"
                            "- calendarPatternName（calPatternNameではない）が正しいキー名\n"
                            "- calPatternDetailInfoEntitiesで特定日付を指定可能"
                        )
                    }
                },
                "required": ["pattern_info"]
            }
        ),
        Tool(
            name="modify_calendar_pattern",
            description="Hinemos 7.1カレンダーパターンを更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_pattern_id": {
                        "type": "string",
                        "description": "カレンダーパターンID"
                    },
                    "pattern_info": {
                        "type": "object",
                        "description": (
                            "カレンダーパターン情報(dict)。add_calendar_patternと同じだがcalPatternIdは除く"
                        )
                    }
                },
                "required": ["calendar_pattern_id", "pattern_info"]
            }
        ),
        Tool(
            name="delete_calendar_pattern",
            description="Hinemos 7.1カレンダーパターンを削除（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendar_pattern_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "削除するカレンダーパターンIDリスト 例: [\"PATTERN_001\", \"PATTERN_002\"]"
                    }
                },
                "required": ["calendar_pattern_ids"]
            }
        ),
    ]

async def dispatch(name, manager, arguments):
    if name == "get_calendar_list":
        return await manager.get_calendar_list(**arguments)
    elif name == "get_calendar":
        return await manager.get_calendar(**arguments)
    elif name == "add_calendar":
        return await manager.add_calendar(**arguments)
    elif name == "modify_calendar":
        return await manager.modify_calendar(**arguments)
    elif name == "delete_calendar":
        return await manager.delete_calendar(**arguments)
    elif name == "get_calendar_month":
        return await manager.get_calendar_month(**arguments)
    elif name == "get_calendar_week":
        return await manager.get_calendar_week(**arguments)
    elif name == "get_calendar_pattern_list":
        return await manager.get_calendar_pattern_list(**arguments)
    elif name == "get_calendar_pattern":
        return await manager.get_calendar_pattern(**arguments)
    elif name == "add_calendar_pattern":
        return await manager.add_calendar_pattern(**arguments)
    elif name == "modify_calendar_pattern":
        return await manager.modify_calendar_pattern(**arguments)
    elif name == "delete_calendar_pattern":
        return await manager.delete_calendar_pattern(**arguments)
    return None