from mcp.types import Tool
from typing import List

def get_tools():
    return [
        # 監視設定一覧・検索
        Tool(
            name="get_monitor_list",
            description="Hinemos 7.1監視設定一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_monitor_list_by_condition",
            description="Hinemos 7.1条件指定監視設定一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_filter_info": {
                        "type": "object",
                        "description": "監視設定フィルター条件"
                    }
                },
                "required": ["monitor_filter_info"]
            }
        ),
        Tool(
            name="get_monitor",
            description="Hinemos 7.1監視設定を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    }
                },
                "required": ["monitor_id"]
            }
        ),
        Tool(
            name="delete_monitor",
            description="Hinemos 7.1監視設定を削除（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "削除する監視設定IDリスト"
                    }
                },
                "required": ["monitor_ids"]
            }
        ),
        Tool(
            name="set_status_monitor",
            description="Hinemos 7.1監視有効/無効を切り替え（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "対象監視設定IDリスト"
                    },
                    "valid_flg": {
                        "type": "boolean",
                        "description": "有効フラグ（true=有効, false=無効）"
                    }
                },
                "required": ["monitor_ids", "valid_flg"]
            }
        ),
        Tool(
            name="set_status_collector",
            description="Hinemos 7.1収集有効/無効を切り替え（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "対象監視設定IDリスト"
                    },
                    "valid_flg": {
                        "type": "boolean",
                        "description": "有効フラグ（true=有効, false=無効）"
                    }
                },
                "required": ["monitor_ids", "valid_flg"]
            }
        ),

        # HTTPシナリオ監視
        Tool(
            name="add_http_scenario_monitor",
            description="Hinemos 7.1 HTTPシナリオ監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "HTTPシナリオ監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"HTTP_SCENARIO_001\",\n"
                            "  \"monitorName\": \"Webサイト監視\",\n"
                            "  \"description\": \"ECサイトのシナリオ監視\",\n"
                            "  \"facilityId\": \"ROOT\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"httpScenarioCheckInfo\": {\n"
                            "    \"urlList\": [\n"
                            "      {\n"
                            "        \"id\": 1,\n"
                            "        \"url\": \"https://example.com/login\",\n"
                            "        \"description\": \"ログインページ\",\n"
                            "        \"statusCode\": \"200\",\n"
                            "        \"post\": \"username=test&password=test\",\n"
                            "        \"connectTimeout\": 10000,\n"
                            "        \"requestTimeout\": 60000\n"
                            "      }\n"
                            "    ],\n"
                            "    \"userAgent\": \"Hinemos HTTP Monitor\",\n"
                            "    \"connectTimeout\": 10000,\n"
                            "    \"requestTimeout\": 60000,\n"
                            "    \"authType\": \"NONE\"\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"thresholdUpperLimit\": 30000.0\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_http_scenario_monitor",
            description="Hinemos 7.1 HTTPシナリオ監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "HTTPシナリオ監視情報（add_http_scenario_monitorと同じ形式、monitorIdは除く）"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_http_scenario_list",
            description="Hinemos 7.1 HTTPシナリオ監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション、指定時は該当監視のみ取得）"
                    }
                }
            }
        ),

        # HTTP監視（数値）
        Tool(
            name="add_http_numeric_monitor",
            description="Hinemos 7.1 HTTP数値監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "HTTP数値監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"HTTP_NUMERIC_001\",\n"
                            "  \"monitorName\": \"レスポンス時間監視\",\n"
                            "  \"description\": \"HTTPレスポンス時間の数値監視\",\n"
                            "  \"facilityId\": \"ROOT\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"collectorFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"itemName\": \"レスポンス時間\",\n"
                            "  \"measure\": \"msec\",\n"
                            "  \"httpCheckInfo\": {\n"
                            "    \"url\": \"https://example.com/api/health\",\n"
                            "    \"connectTimeout\": 10000,\n"
                            "    \"requestTimeout\": 60000,\n"
                            "    \"userAgent\": \"Hinemos HTTP Monitor\",\n"
                            "    \"authType\": \"NONE\"\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdUpperLimit\": 5000.0\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_http_numeric_monitor",
            description="Hinemos 7.1 HTTP数値監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "HTTP数値監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_http_numeric_list",
            description="Hinemos 7.1 HTTP数値監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # HTTP監視（文字列）
        Tool(
            name="add_http_string_monitor",
            description="Hinemos 7.1 HTTP文字列監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "HTTP文字列監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"HTTP_STRING_001\",\n"
                            "  \"monitorName\": \"レスポンス内容監視\",\n"
                            "  \"facilityId\": \"ROOT\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"httpCheckInfo\": {\n"
                            "    \"url\": \"https://example.com/api/status\",\n"
                            "    \"connectTimeout\": 10000,\n"
                            "    \"requestTimeout\": 60000,\n"
                            "    \"authType\": \"BASIC\",\n"
                            "    \"authUser\": \"username\",\n"
                            "    \"authPassword\": \"password\"\n"
                            "  },\n"
                            "  \"stringValueInfo\": [\n"
                            "    {\n"
                            "      \"orderNo\": 1,\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"pattern\": \"ERROR\",\n"
                            "      \"processType\": \"CONTAINS\",\n"
                            "      \"caseSensitivityFlg\": false,\n"
                            "      \"validFlg\": true\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_http_string_monitor",
            description="Hinemos 7.1 HTTP文字列監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "HTTP文字列監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_http_string_list",
            description="Hinemos 7.1 HTTP文字列監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # エージェント監視
        Tool(
            name="add_agent_monitor",
            description="Hinemos 7.1 エージェント監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "エージェント監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"AGENT_001\",\n"
                            "  \"monitorName\": \"エージェント生存監視\",\n"
                            "  \"description\": \"Hinemosエージェントの監視\",\n"
                            "  \"facilityId\": \"REGISTERED\",\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"application\": \"agent_app\",\n"
                            "  \"monitorFlg\": true,\n"
                            "  \"runInterval\": \"MIN_05\",\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"priorityChangeJudgmentType\": \"NOT_PRIORITY_CHANGE\",\n"
                            "  \"truthValueInfo\": [\n"
                            "    {\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"truthValue\": \"FALSE_VALUE\",\n"
                            "      \"message\": \"エージェント停止\"\n"
                            "    }\n"
                            "  ]\n"
                            "}\n\n"
                            "重要な必須パラメータ:\n"
                            "- application: 必須（1-64文字）\n"
                            "- monitorFlg: 必須（通常true）\n"
                            "- collectorFlg: 必須（true/false明示）\n"
                            "- priorityChangeJudgmentType: 必須（\"NOT_PRIORITY_CHANGE\"）\n"
                            "- runInterval: MIN_01,MIN_05,MIN_10,MIN_30,MIN_60\n"
                            "- truthValueInfo.message: 必須（検出時のメッセージ）\n"
                            "- truthValueInfo.truthValue: \"TRUE_VALUE\"または\"FALSE_VALUE\"\n"
                            "- truthValueInfo.priority: INFO,WARNING,CRITICAL,UNKNOWN"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_agent_monitor",
            description="Hinemos 7.1エージェント監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "エージェント監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_agent_list",
            description="Hinemos 7.1エージェント監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # JMX監視
        Tool(
            name="add_jmx_monitor",
            description="Hinemos 7.1 JMX監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "JMX監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"JMX_001\",\n"
                            "  \"monitorName\": \"JVMガベージコレクション監視\",\n"
                            "  \"description\": \"GC実行回数の監視\",\n"
                            "  \"facilityId\": \"REGISTERED\",\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"application\": \"jmx_app\",\n"
                            "  \"monitorFlg\": true,\n"
                            "  \"runInterval\": \"MIN_05\",\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"itemName\": \"$[JMX_GARBAGE_COLLECTOR_CONCURRENTMARKSWEEP_COLLECTIONS]\",\n"
                            "  \"measure\": \"$[COUNTS]\",\n"
                            "  \"predictionFlg\": false,\n"
                            "  \"predictionMethod\": \"POLYNOMIAL_1\",\n"
                            "  \"predictionAnalysysRange\": 60,\n"
                            "  \"predictionTarget\": 60,\n"
                            "  \"changeFlg\": false,\n"
                            "  \"changeAnalysysRange\": 60,\n"
                            "  \"jmxCheckInfo\": {\n"
                            "    \"port\": 1234,\n"
                            "    \"convertFlg\": \"NONE\",\n"
                            "    \"masterId\": \"JMX_GARBAGE_COLLECTOR_CONCURRENT_MARK_SWEEP_COLLECTION_COUNT\",\n"
                            "    \"urlFormatName\": \"Default\"\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdLowerLimit\": 0.0,\n"
                            "      \"thresholdUpperLimit\": 100.0\n"
                            "    }\n"
                            "  ]\n"
                            "}\n\n"
                            "重要な必須パラメータ:\n"
                            "- application: 必須（1-64文字）\n"
                            "- monitorFlg: 必須（通常true）\n"
                            "- collectorFlg: 必須（通常false）\n"
                            "- itemName: 国際化キー（例: $[JMX_GARBAGE_COLLECTOR_CONCURRENTMARKSWEEP_COLLECTIONS]）\n"
                            "- measure: 国際化キー（例: $[COUNTS], $[BYTES]）\n"
                            "- jmxCheckInfo.masterId: 事前定義のマスタID\n"
                            "- jmxCheckInfo.convertFlg: \"NONE\", \"DELTA\", \"VALUE\"\n"
                            "- jmxCheckInfo.urlFormatName: \"Default\"等のフォーマット名\n"
                            "- predictionFlg,changeFlg: Boolean値\n"
                            "- numericValueInfo: 閾値設定（完全な8エントリ推奨）"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),

        Tool(
            name="modify_jmx_monitor",
            description="Hinemos 7.1 JMX監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "JMX監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_jmx_list",
            description="Hinemos 7.1 JMX監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),
        Tool(
            name="get_jmx_url_format_list",
            description="Hinemos 7.1 JMX URLフォーマット一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="add_ping_monitor",
            description="Hinemos 7.1 PING監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "PING監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"PING_001\",\n"
                            "  \"monitorName\": \"サーバー疎通監視\",\n"
                            "  \"description\": \"サーバーの疎通状況を監視\",\n"
                            "  \"facilityId\": \"REGISTERED\",\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"application\": \"ping_app\",\n"
                            "  \"monitorFlg\": true,\n"
                            "  \"runInterval\": \"MIN_05\",\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"itemName\": \"応答時間\",\n"
                            "  \"measure\": \"msec\",\n"
                            "  \"predictionFlg\": false,\n"
                            "  \"predictionMethod\": \"POLYNOMIAL_1\",\n"
                            "  \"predictionAnalysysRange\": 60,\n"
                            "  \"predictionTarget\": 60,\n"
                            "  \"changeFlg\": false,\n"
                            "  \"changeAnalysysRange\": 60,\n"
                            "  \"pingCheckInfo\": {\n"
                            "    \"runCount\": 1,\n"
                            "    \"runInterval\": 1000,\n"
                            "    \"timeout\": 5000\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"CHANGE\",\n"
                            "      \"priority\": \"INFO\",\n"
                            "      \"thresholdLowerLimit\": -1.0,\n"
                            "      \"thresholdUpperLimit\": 1.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"CHANGE\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdLowerLimit\": -2.0,\n"
                            "      \"thresholdUpperLimit\": 2.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"CHANGE\",\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"thresholdLowerLimit\": 0.0,\n"
                            "      \"thresholdUpperLimit\": 0.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"CHANGE\",\n"
                            "      \"priority\": \"UNKNOWN\",\n"
                            "      \"thresholdLowerLimit\": 0.0,\n"
                            "      \"thresholdUpperLimit\": 0.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"INFO\",\n"
                            "      \"thresholdLowerLimit\": 1000.0,\n"
                            "      \"thresholdUpperLimit\": 1.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdLowerLimit\": 3000.0,\n"
                            "      \"thresholdUpperLimit\": 51.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"thresholdLowerLimit\": 0.0,\n"
                            "      \"thresholdUpperLimit\": 0.0\n"
                            "    },\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"UNKNOWN\",\n"
                            "      \"thresholdLowerLimit\": 0.0,\n"
                            "      \"thresholdUpperLimit\": 0.0\n"
                            "    }\n"
                            "  ]\n"
                            "}\n\n"
                            "重要な注意事項:\n"
                            "- runInterval: SEC_30, MIN_01, MIN_05, MIN_10, MIN_30, MIN_60, NONEのみ有効\n"
                            "- application: 必須フィールド（1-64文字）\n"
                            "- monitorFlg: 必須（通常はtrue）\n"
                            "- collectorFlg: 必須（true/false明示的指定）\n"
                            "- numericValueInfo: 8要素必須（CHANGE×4 + BASIC×4の各優先度）\n"
                            "- facilityId: REGISTEREDまたは有効なノードID\n"
                            "- predictionFlg, changeFlg: falseを推奨\n"
                            "- predictionMethod: POLYNOMIAL_1固定\n"
                            "- predictionAnalysysRange, predictionTarget, changeAnalysysRange: 60推奨"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_ping_monitor",
            description="Hinemos 7.1 PING監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "PING監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_ping_list",
            description="Hinemos 7.1 PING監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # カスタム監視（数値）
        Tool(
            name="add_custom_numeric_monitor",
            description="Hinemos 7.1カスタム数値監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "カスタム数値監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"CUSTOM_NUMERIC_001\",\n"
                            "  \"monitorName\": \"カスタム数値監視\",\n"
                            "  \"description\": \"カスタム監視の説明\",\n"
                            "  \"facilityId\": \"REGISTERED\",\n"
                            "  \"runInterval\": \"MIN_05\",\n"
                            "  \"validFlg\": true,\n"
                            "  \"monitorFlg\": true,\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"application\": \"custom_app\",\n"
                            "  \"itemName\": \"カスタム値\",\n"
                            "  \"measure\": \"個\",\n"
                            "  \"predictionFlg\": false,\n"
                            "  \"changeFlg\": false,\n"
                            "  \"customCheckInfo\": {\n"
                            "    \"command\": \"/bin/echo 50\",\n"
                            "    \"commandExecTypeCode\": \"INDIVIDUAL\",\n"
                            "    \"specifyUser\": true,\n"
                            "    \"effectiveUser\": \"hinemos\",\n"
                            "    \"timeout\": 15000,\n"
                            "    \"convertFlg\": 0\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\"monitorNumericType\": \"BASIC\", \"priority\": \"INFO\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 30.0},\n"
                            "    {\"monitorNumericType\": \"BASIC\", \"priority\": \"WARNING\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 80.0},\n"
                            "    {\"monitorNumericType\": \"BASIC\", \"priority\": \"CRITICAL\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 0.0},\n"
                            "    {\"monitorNumericType\": \"BASIC\", \"priority\": \"UNKNOWN\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 0.0},\n"
                            "    {\"monitorNumericType\": \"CHANGE\", \"priority\": \"INFO\", \"message\": null, \"thresholdLowerLimit\": -1.0, \"thresholdUpperLimit\": 1.0},\n"
                            "    {\"monitorNumericType\": \"CHANGE\", \"priority\": \"WARNING\", \"message\": null, \"thresholdLowerLimit\": -2.0, \"thresholdUpperLimit\": 2.0},\n"
                            "    {\"monitorNumericType\": \"CHANGE\", \"priority\": \"CRITICAL\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 0.0},\n"
                            "    {\"monitorNumericType\": \"CHANGE\", \"priority\": \"UNKNOWN\", \"message\": null, \"thresholdLowerLimit\": 0.0, \"thresholdUpperLimit\": 0.0}\n"
                            "  ],\n"
                            "  \"priorityChangeFailureType\": \"NOT_PRIORITY_CHANGE\",\n"
                            "  \"priorityChangeJudgmentType\": \"NOT_PRIORITY_CHANGE\"\n"
                            "}\n\n"
                            "重要な必須パラメータ:\n"
                            "- application: 必須（1-64文字）\n"
                            "- monitorFlg: 必須（通常true）\n"
                            "- runInterval: 必須（MIN_01,MIN_05,MIN_10,MIN_30,MIN_60）\n"
                            "- customCheckInfo.specifyUser: 必須（true推奨）\n"
                            "- customCheckInfo.effectiveUser: specifyUser=trueの場合必須\n"
                            "- customCheckInfo.convertFlg: 0=変換なし, 1=差分値\n"
                            "- numericValueInfo: 8要素必須（BASIC×4 + CHANGE×4の各優先度）\n"
                            "- priorityChangeFailureType: \"PRIORITY_CHANGE\"または\"NOT_PRIORITY_CHANGE\"\n"
                            "- priorityChangeJudgmentType: \"NOT_PRIORITY_CHANGE\"推奨"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_custom_numeric_monitor",
            description="Hinemos 7.1カスタム数値監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "カスタム数値監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_custom_numeric_list",
            description="Hinemos 7.1カスタム数値監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # カスタム監視（文字列）
        Tool(
            name="add_custom_string_monitor",
            description="Hinemos 7.1カスタム文字列監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": "カスタム文字列監視情報"
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_custom_string_monitor",
            description="Hinemos 7.1カスタム文字列監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "カスタム文字列監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_custom_string_list",
            description="Hinemos 7.1カスタム文字列監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # リソース監視
        Tool(
            name="add_performance_monitor",
            description="Hinemos 7.1リソース監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "リソース監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"PERFORMANCE_001\",\n"
                            "  \"monitorName\": \"CPU使用率監視\",\n"
                            "  \"facilityId\": \"SERVER_001\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"collectorFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"itemName\": \"CPU使用率\",\n"
                            "  \"measure\": \"%\",\n"
                            "  \"perfCheckInfo\": {\n"
                            "    \"itemCode\": \"system.cpu.usage\",\n"
                            "    \"deviceDisplayName\": \"\",\n"
                            "    \"breakdownFlg\": false\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdUpperLimit\": 80.0\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_performance_monitor",
            description="Hinemos 7.1リソース監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "リソース監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_performance_list",
            description="Hinemos 7.1リソース監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # JMXマスタ管理
        Tool(
            name="get_jmx_master_list",
            description="Hinemos 7.1 JMXマスタ一覧を取得（REST API、システム管理者権限必要）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="add_jmx_master_list",
            description="Hinemos 7.1 JMXマスタを追加（REST API、システム管理者権限必要）",
            inputSchema={
                "type": "object",
                "properties": {
                    "jmx_master_list": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "JMXマスタ情報リスト"
                    }
                },
                "required": ["jmx_master_list"]
            }
        ),
        Tool(
            name="delete_jmx_master",
            description="Hinemos 7.1 JMXマスタを削除（REST API、システム管理者権限必要）",
            inputSchema={
                "type": "object",
                "properties": {
                    "jmx_master_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "削除するJMXマスタIDリスト"
                    }
                },
                "required": ["jmx_master_ids"]
            }
        ),
        Tool(
            name="delete_jmx_master_all",
            description="Hinemos 7.1 JMXマスタを全削除（REST API、システム管理者権限必要）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # 補助API
        Tool(
            name="get_jdbc_driver_list",
            description="Hinemos 7.1 JDBCドライバ一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_binary_preset_list",
            description="Hinemos 7.1バイナリプリセット一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_monitor_string_tag_list",
            description="Hinemos 7.1監視文字列タグ一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "owner_role_id": {
                        "type": "string",
                        "description": "オーナーロールID"
                    }
                },
                "required": ["monitor_id", "owner_role_id"]
            }
        ),

        # SNMP監視
        Tool(
            name="add_snmp_numeric_monitor",
            description="Hinemos 7.1 SNMP数値監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "SNMP数値監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"SNMP_NUMERIC_001\",\n"
                            "  \"monitorName\": \"SNMP数値監視\",\n"
                            "  \"facilityId\": \"SERVER_001\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"collectorFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"itemName\": \"CPU使用率\",\n"
                            "  \"measure\": \"%\",\n"
                            "  \"snmpCheckInfo\": {\n"
                            "    \"snmpOid\": \"1.3.6.1.4.1.2021.11.9.0\",\n"
                            "    \"snmpPort\": 161,\n"
                            "    \"snmpCommunity\": \"public\",\n"
                            "    \"snmpVersion\": \"TYPE_V2\",\n"
                            "    \"snmpTimeout\": 5000,\n"
                            "    \"snmpRetries\": 3\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdUpperLimit\": 80.0\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_snmp_numeric_monitor",
            description="Hinemos 7.1 SNMP数値監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "SNMP数値監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_snmp_numeric_list",
            description="Hinemos 7.1 SNMP数値監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # SNMP文字列監視
        Tool(
            name="add_snmp_string_monitor",
            description="Hinemos 7.1 SNMP文字列監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": "SNMP文字列監視情報"
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_snmp_string_monitor",
            description="Hinemos 7.1 SNMP文字列監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "SNMP文字列監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_snmp_string_list",
            description="Hinemos 7.1 SNMP文字列監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # SQL監視
        Tool(
            name="add_sql_numeric_monitor",
            description="Hinemos 7.1 SQL数値監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "SQL数値監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"SQL_NUMERIC_001\",\n"
                            "  \"monitorName\": \"SQL数値監視\",\n"
                            "  \"facilityId\": \"DB_SERVER_001\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"collectorFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"itemName\": \"レコード数\",\n"
                            "  \"measure\": \"件\",\n"
                            "  \"sqlCheckInfo\": {\n"
                            "    \"jdbcDriver\": \"org.postgresql.Driver\",\n"
                            "    \"url\": \"jdbc:postgresql://localhost:5432/hinemos\",\n"
                            "    \"user\": \"hinemos\",\n"
                            "    \"password\": \"hinemos\",\n"
                            "    \"query\": \"SELECT COUNT(*) FROM log_table WHERE created_at > NOW() - INTERVAL '1 hour'\"\n"
                            "  },\n"
                            "  \"numericValueInfo\": [\n"
                            "    {\n"
                            "      \"monitorNumericType\": \"BASIC\",\n"
                            "      \"priority\": \"WARNING\",\n"
                            "      \"thresholdUpperLimit\": 1000.0\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_sql_numeric_monitor",
            description="Hinemos 7.1 SQL数値監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "SQL数値監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_sql_numeric_list",
            description="Hinemos 7.1 SQL数値監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # ログファイル監視
        Tool(
            name="add_logfile_monitor",
            description="Hinemos 7.1 ログファイル監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "ログファイル監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"LOGFILE_001\",\n"
                            "  \"monitorName\": \"アプリケーションログ監視\",\n"
                            "  \"description\": \"エラーログの監視\",\n"
                            "  \"facilityId\": \"REGISTERED\",\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"application\": \"logfile_app\",\n"
                            "  \"monitorFlg\": true,\n"
                            "  \"runInterval\": \"MIN_01\",\n"
                            "  \"collectorFlg\": false,\n"
                            "  \"priorityChangeJudgmentType\": \"NOT_PRIORITY_CHANGE\",\n"
                            "  \"logfileCheckInfo\": {\n"
                            "    \"directory\": \"/var/log\",\n"
                            "    \"fileName\": \"application.log\",\n"
                            "    \"fileEncoding\": \"UTF-8\",\n"
                            "    \"fileReturnCode\": \"LF\"\n"
                            "  },\n"
                            "  \"stringValueInfo\": [\n"
                            "    {\n"
                            "      \"orderNo\": 1,\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"pattern\": \"ERROR\",\n"
                            "      \"processType\": true,\n"
                            "      \"caseSensitivityFlg\": false,\n"
                            "      \"validFlg\": true,\n"
                            "      \"message\": \"エラーログ検出\"\n"
                            "    }\n"
                            "  ]\n"
                            "}\n\n"
                            "重要な必須パラメータ:\n"
                            "- application: 必須（1-64文字）\n"
                            "- monitorFlg: 必須（通常true）\n"
                            "- collectorFlg: 必須（true/false明示）\n"
                            "- priorityChangeJudgmentType: 必須（\"NOT_PRIORITY_CHANGE\"）\n"
                            "- runInterval: SEC_30,MIN_01,MIN_05,MIN_10,MIN_30,MIN_60,NONE\n"
                            "- logfileCheckInfo.directory: 必須（ログファイルのディレクトリ）\n"
                            "- logfileCheckInfo.fileName: 必須（ログファイル名）\n"
                            "- stringValueInfo.message: 必須（検出時のメッセージ）\n"
                            "- stringValueInfo.processType: Boolean値（true推奨）\n"
                            "- fileReturnCode: \"LF\",\"CRLF\",\"CR\""
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_logfile_monitor",
            description="Hinemos 7.1ログファイル監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "ログファイル監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_logfile_list",
            description="Hinemos 7.1ログファイル監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        ),

        # プロセス監視
        Tool(
            name="add_process_monitor",
            description="Hinemos 7.1プロセス監視を追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_info": {
                        "type": "object",
                        "description": (
                            "プロセス監視情報。例:\n"
                            "{\n"
                            "  \"monitorId\": \"PROCESS_001\",\n"
                            "  \"monitorName\": \"Webサーバープロセス監視\",\n"
                            "  \"facilityId\": \"SERVER_001\",\n"
                            "  \"intervalSec\": 300,\n"
                            "  \"validFlg\": true,\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"processCheckInfo\": {\n"
                            "    \"command\": \"httpd\",\n"
                            "    \"param\": \"-D FOREGROUND\",\n"
                            "    \"caseSensitivityFlg\": false\n"
                            "  },\n"
                            "  \"truthValueInfo\": [\n"
                            "    {\n"
                            "      \"priority\": \"CRITICAL\",\n"
                            "      \"truthValue\": \"FALSE\",\n"
                            "      \"message\": \"Webサーバープロセス停止\"\n"
                            "    }\n"
                            "  ]\n"
                            "}"
                        )
                    }
                },
                "required": ["monitor_info"]
            }
        ),
        Tool(
            name="modify_process_monitor",
            description="Hinemos 7.1プロセス監視を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID"
                    },
                    "monitor_info": {
                        "type": "object",
                        "description": "プロセス監視情報"
                    }
                },
                "required": ["monitor_id", "monitor_info"]
            }
        ),
        Tool(
            name="get_process_list",
            description="Hinemos 7.1プロセス監視一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "monitor_id": {
                        "type": "string",
                        "description": "監視設定ID（オプション）"
                    }
                }
            }
        )
    ]

async def dispatch(name, manager, arguments):
    # 監視設定一覧・検索
    if name == "get_monitor_list":
        return await manager.get_monitor_list(**arguments)
    elif name == "get_monitor_list_by_condition":
        return await manager.get_monitor_list_by_condition(**arguments)
    elif name == "get_monitor":
        return await manager.get_monitor(**arguments)
    elif name == "delete_monitor":
        return await manager.delete_monitor(**arguments)
    elif name == "set_status_monitor":
        return await manager.set_status_monitor(**arguments)
    elif name == "set_status_collector":
        return await manager.set_status_collector(**arguments)

    # HTTPシナリオ監視
    elif name == "add_http_scenario_monitor":
        return await manager.add_http_scenario_monitor(**arguments)
    elif name == "modify_http_scenario_monitor":
        return await manager.modify_http_scenario_monitor(**arguments)
    elif name == "get_http_scenario_list":
        return await manager.get_http_scenario_list(**arguments)

    # HTTP監視（数値）
    elif name == "add_http_numeric_monitor":
        return await manager.add_http_numeric_monitor(**arguments)
    elif name == "modify_http_numeric_monitor":
        return await manager.modify_http_numeric_monitor(**arguments)
    elif name == "get_http_numeric_list":
        return await manager.get_http_numeric_list(**arguments)

    # HTTP監視（文字列）
    elif name == "add_http_string_monitor":
        return await manager.add_http_string_monitor(**arguments)
    elif name == "modify_http_string_monitor":
        return await manager.modify_http_string_monitor(**arguments)
    elif name == "get_http_string_list":
        return await manager.get_http_string_list(**arguments)

    # エージェント監視
    elif name == "add_agent_monitor":
        return await manager.add_agent_monitor(**arguments)
    elif name == "modify_agent_monitor":
        return await manager.modify_agent_monitor(**arguments)
    elif name == "get_agent_list":
        return await manager.get_agent_list(**arguments)

    # JMX監視
    elif name == "add_jmx_monitor":
        return await manager.add_jmx_monitor(**arguments)
    elif name == "modify_jmx_monitor":
        return await manager.modify_jmx_monitor(**arguments)
    elif name == "get_jmx_list":
        return await manager.get_jmx_list(**arguments)
    elif name == "get_jmx_url_format_list":
        return await manager.get_jmx_url_format_list(**arguments)

    # PING監視
    elif name == "add_ping_monitor":
        return await manager.add_ping_monitor(**arguments)
    elif name == "modify_ping_monitor":
        return await manager.modify_ping_monitor(**arguments)
    elif name == "get_ping_list":
        return await manager.get_ping_list(**arguments)

    # カスタム監視（数値）
    elif name == "add_custom_numeric_monitor":
        return await manager.add_custom_numeric_monitor(**arguments)
    elif name == "modify_custom_numeric_monitor":
        return await manager.modify_custom_numeric_monitor(**arguments)
    elif name == "get_custom_numeric_list":
        return await manager.get_custom_numeric_list(**arguments)

    # カスタム監視（文字列）
    elif name == "add_custom_string_monitor":
        return await manager.add_custom_string_monitor(**arguments)
    elif name == "modify_custom_string_monitor":
        return await manager.modify_custom_string_monitor(**arguments)
    elif name == "get_custom_string_list":
        return await manager.get_custom_string_list(**arguments)
    
    # リソース監視
    elif name == "add_performance_monitor":
        return await manager.add_performance_monitor(**arguments)
    elif name == "modify_performance_monitor":
        return await manager.modify_performance_monitor(**arguments)
    elif name == "get_performance_list":
        return await manager.get_performance_list(**arguments)

    # SNMP監視
    elif name == "add_snmp_numeric_monitor":
        return await manager.add_snmp_numeric_monitor(**arguments)
    elif name == "modify_snmp_numeric_monitor":
        return await manager.modify_snmp_numeric_monitor(**arguments)
    elif name == "get_snmp_numeric_list":
        return await manager.get_snmp_numeric_list(**arguments)
    elif name == "add_snmp_string_monitor":
        return await manager.add_snmp_string_monitor(**arguments)
    elif name == "modify_snmp_string_monitor":
        return await manager.modify_snmp_string_monitor(**arguments)
    elif name == "get_snmp_string_list":
        return await manager.get_snmp_string_list(**arguments)

    # SQL監視
    elif name == "add_sql_numeric_monitor":
        return await manager.add_sql_numeric_monitor(**arguments)
    elif name == "modify_sql_numeric_monitor":
        return await manager.modify_sql_numeric_monitor(**arguments)
    elif name == "get_sql_numeric_list":
        return await manager.get_sql_numeric_list(**arguments)

    # ログファイル監視
    elif name == "add_logfile_monitor":
        return await manager.add_logfile_monitor(**arguments)
    elif name == "modify_logfile_monitor":
        return await manager.modify_logfile_monitor(**arguments)
    elif name == "get_logfile_list":
        return await manager.get_logfile_list(**arguments)

    # プロセス監視
    elif name == "add_process_monitor":
        return await manager.add_process_monitor(**arguments)
    elif name == "modify_process_monitor":
        return await manager.modify_process_monitor(**arguments)
    elif name == "get_process_list":
        return await manager.get_process_list(**arguments)

    # JMXマスタ管理
    elif name == "get_jmx_master_list":
        return await manager.get_jmx_master_list(**arguments)
    elif name == "add_jmx_master_list":
        return await manager.add_jmx_master_list(**arguments)
    elif name == "delete_jmx_master":
        return await manager.delete_jmx_master(**arguments)
    elif name == "delete_jmx_master_all":
        return await manager.delete_jmx_master_all(**arguments)

    # 補助API
    elif name == "get_jdbc_driver_list":
        return await manager.get_jdbc_driver_list(**arguments)
    elif name == "get_binary_preset_list":
        return await manager.get_binary_preset_list(**arguments)
    elif name == "get_monitor_string_tag_list":
        return await manager.get_monitor_string_tag_list(**arguments)

    return None