from mcp.types import Tool, TextContent
from typing import List

def get_tools():
    return [
        Tool(
            name="get_facility_tree",
            description="Hinemos 7.1リポジトリからファシリティツリーを取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner_role_id": {
                        "type": "string",
                        "description": "オーナーロールIDフィルター（オプション）"
                    },
                    "size": {
                        "type": "integer",
                        "description": "取得件数（オプション）"
                    }
                }
            }
        ),
        Tool(
            name="get_exec_target_facility_tree",
            description="Hinemos 7.1リポジトリから指定スコープ配下のファシリティツリーを取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_facility_id": {
                        "type": "string",
                        "description": "取得対象のfacilityId"
                    },
                    "owner_role_id": {
                        "type": "string",
                        "description": "オーナーロールIDフィルター（オプション）"
                    }
                },
                "required": ["target_facility_id"]
            }
        ),
        Tool(
            name="get_node_facility_tree",
            description="Hinemos 7.1リポジトリからノード情報を含むファシリティツリーを取得（REST API）",
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
            name="get_node_list",
            description="Hinemos 7.1リポジトリからノードリストを取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "parent_facility_id": {
                        "type": "string",
                        "description": "親facilityId（オプション）"
                    },
                    "size": {
                        "type": "integer",
                        "description": "取得件数（オプション）"
                    },
                    "level": {
                        "type": "string",
                        "description": "レベル（オプション, SCOPEやNODEなど）"
                    }
                }
            }
        ),
        Tool(
            name="get_node",
            description="Hinemos 7.1リポジトリからノード情報を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "ノードのfacilityId"
                    }
                },
                "required": ["facility_id"]
            }
        ),
        Tool(
            name="get_node_full",
            description="Hinemos 7.1リポジトリから構成情報を含むノード情報を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "ノードのfacilityId"
                    }
                },
                "required": ["facility_id"]
            }
        ),
        Tool(
            name="add_node",
            description="Hinemos 7.1リポジトリにノードを追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_info": {
                        "type": "object",
                        "description": (
                            "Hinemos仕様に準拠したノード情報(dict)。例:\n"
                            "{\n"
                            "  \"autoDeviceSearch\": true,\n"
                            "  \"administrator\": \"\",\n"
                            "  \"cloudService\": \"\",\n"
                            "  \"cloudScope\": \"\",\n"
                            "  \"cloudResourceType\": \"\",\n"
                            "  \"cloudResourceId\": \"\",\n"
                            "  \"cloudResourceName\": \"\",\n"
                            "  \"cloudLocation\": \"\",\n"
                            "  \"cloudLogPriority\": 16,\n"
                            "  \"contact\": \"\",\n"
                            "  \"hardwareType\": \"\",\n"
                            "  \"ipAddressV4\": \"172.31.24.200\",\n"
                            "  \"ipAddressV6\": \"\",\n"
                            "  \"ipAddressVersion\": \"IPV4\",  # \"IPV4\" または \"IPV6\"\n"
                            "  \"ipmiIpAddress\": \"\",\n"
                            "  \"ipmiLevel\": \"\",\n"
                            "  \"ipmiPort\": 0,\n"
                            "  \"ipmiProtocol\": \"RMCP+\",\n"
                            "  \"ipmiRetries\": 3,\n"
                            "  \"ipmiTimeout\": 5000,\n"
                            "  \"ipmiUser\": \"\",\n"
                            "  \"ipmiUserPassword\": \"\",\n"
                            "  \"jobPriority\": 16,\n"
                            "  \"jobMultiplicity\": 0,\n"
                            "  \"nodeName\": \"web2\",\n"
                            "  \"platformFamily\": \"LINUX\",\n"
                            "  \"snmpCommunity\": \"public\",\n"
                            "  \"snmpPort\": 161,\n"
                            "  \"snmpRetryCount\": 3,\n"
                            "  \"snmpTimeout\": 5000,\n"
                            "  \"snmpVersion\": \"TYPE_V2\",\n"
                            "  \"snmpSecurityLevel\": \"NOAUTH_NOPRIV\",\n"
                            "  \"snmpUser\": \"\",\n"
                            "  \"snmpAuthPassword\": \"\",\n"
                            "  \"snmpPrivPassword\": \"\",\n"
                            "  \"snmpAuthProtocol\": \"NONE\",\n"
                            "  \"snmpPrivProtocol\": \"NONE\",\n"
                            "  \"sshUser\": \"root\",\n"
                            "  \"sshUserPassword\": \"\",\n"
                            "  \"sshPrivateKeyFilepath\": \"\",\n"
                            "  \"sshPrivateKeyPassphrase\": \"\",\n"
                            "  \"sshPort\": 22,\n"
                            "  \"sshTimeout\": 50000,\n"
                            "  \"subPlatformFamily\": \"\",\n"
                            "  \"wbemPort\": 5988,\n"
                            "  \"wbemProtocol\": \"HTTP\",\n"
                            "  \"wbemRetryCount\": 3,\n"
                            "  \"wbemTimeout\": 5000,\n"
                            "  \"wbemUser\": \"root\",\n"
                            "  \"wbemUserPassword\": \"\",\n"
                            "  \"winrmPort\": 5985,\n"
                            "  \"winrmProtocol\": \"HTTP\",\n"
                            "  \"winrmRetries\": 3,\n"
                            "  \"winrmTimeout\": 5000,\n"
                            "  \"winrmUser\": \"\",\n"
                            "  \"winrmUserPassword\": \"\",\n"
                            "  \"winrmVersion\": \"\",\n"
                            "  \"agentAwakePort\": 24005,\n"
                            "  \"nodeOsInfo\": {\n"
                            "    \"osName\": \"\",\n"
                            "    \"osRelease\": \"\",\n"
                            "    \"osVersion\": \"\",\n"
                            "    \"characterSet\": \"\"\n"
                            "  },\n"
                            "  \"nodeCpuInfo\": [],\n"
                            "  \"nodeDeviceInfo\": [],\n"
                            "  \"nodeDiskInfo\": [],\n"
                            "  \"nodeFilesystemInfo\": [],\n"
                            "  \"nodeHostnameInfo\": [{\"hostname\": \"\"}],\n"
                            "  \"nodeMemoryInfo\": [],\n"
                            "  \"nodeNetworkInterfaceInfo\": [],\n"
                            "  \"nodeNoteInfo\": [{\"noteId\": 0, \"note\": \"\"}],\n"
                            "  \"nodeVariableInfo\": [],\n"
                            "  \"nodeNetstatInfo\": [],\n"
                            "  \"nodeProcessInfo\": [],\n"
                            "  \"nodePackageInfo\": [],\n"
                            "  \"nodeProductInfo\": [],\n"
                            "  \"nodeLicenseInfo\": [],\n"
                            "  \"ownerRoleId\": \"ALL_USERS\",\n"
                            "  \"facilityId\": \"WEB2\",\n"
                            "  \"facilityName\": \"静的Webサーバ2\",\n"
                            "  \"description\": \"\",\n"
                            "  \"iconImage\": \"\",\n"
                            "  \"valid\": true\n"
                            "}"
                        )
                    }
                },
                "required": ["node_info"]
            }
        ),
        Tool(
            name="modify_node",
            description="Hinemos 7.1リポジトリのノード情報を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "ノードのfacilityId"
                    },
                    "node_info": {
                        "type": "object",
                        "description": (
                            "ノード情報。例:\n"
                            "{\n"
                            "  \"facilityName\": \"サーバー001\",\n"
                            "  \"description\": \"Webサーバー\",\n"
                            "  \"ipAddressVersion\": 4,\n"
                            "  \"ipAddressV4\": \"192.168.1.100\",\n"
                            "  \"nodeName\": \"web-server-01\",\n"
                            "  \"platformFamily\": \"UNIX\",\n"
                            "  \"subPlatformFamily\": \"LINUX\",\n"
                            "  \"hardwareType\": \"X86_64\",\n"
                            "  \"ownerRoleId\": \"ADMINISTRATORS\",\n"
                            "  \"valid\": true\n"
                            "}"
                        )
                    }
                },
                "required": ["facility_id", "node_info"]
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
                        "description": "削除するfacilityIdリスト 例: [\"NODE001\", \"NODE002\"]"
                    }
                },
                "required": ["facility_ids"]
            }
        ),
        Tool(
            name="search_node",
            description="Hinemos 7.1リポジトリでノードを検索（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_params": {
                        "type": "object",
                        "description": (
                            "検索条件。例:\n"
                            "{\n"
                            "  \"facilityId\": \"NODE*\",\n"
                            "  \"facilityName\": \"*server*\",\n"
                            "  \"ipAddressV4\": \"192.168.1.*\",\n"
                            "  \"platformFamily\": \"UNIX\"\n"
                            "}"
                        )
                    }
                },
                "required": ["search_params"]
            }
        ),
        Tool(
            name="get_facility_list",
            description="Hinemos 7.1リポジトリからスコープ配下のスコープとノード一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "parent_facility_id": {
                        "type": "string",
                        "description": "親facilityId（オプション）"
                    }
                }
            }
        ),
        Tool(
            name="get_scope",
            description="Hinemos 7.1リポジトリからスコープ情報を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "スコープのfacilityId"
                    }
                },
                "required": ["facility_id"]
            }
        ),
        Tool(
            name="get_scope_default",
            description="Hinemos 7.1リポジトリからスコープ情報の初期値を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="add_scope",
            description="Hinemos 7.1リポジトリにスコープを追加（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "scope_info": {
                        "type": "object",
                        "description": (
                            "スコープ情報。例:\n"
                            "{\n"
                            "  \"parentFacilityId\": \"ROOT\",  # 親スコープID（必須）\n"
                            "  \"scopeInfo\": {\n"
                            "    \"facilityId\": \"SCOPE001\",         # スコープID（必須）\n"
                            "    \"facilityName\": \"開発環境\",        # スコープ名（必須）\n"
                            "    \"description\": \"開発チーム用スコープ\", # 説明（任意）\n"
                            "    \"ownerRoleId\": \"ADMINISTRATORS\"   # オーナーロールID（必須）\n"
                            "  }\n"
                            "}"
                        )
                    }
                },
                "required": ["scope_info"]
            }
        ),
        Tool(
            name="modify_scope",
            description="Hinemos 7.1リポジトリのスコープ情報を更新（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "スコープのfacilityId"
                    },
                    "scope_info": {
                        "type": "object",
                        "description": (
                            "スコープ情報。例:\n"
                            "{\n"
                            "  \"facilityName\": \"開発環境\",\n"
                            "  \"description\": \"開発チーム用スコープ\",\n"
                            "  \"ownerRoleId\": \"ADMINISTRATORS\"\n"
                            "}"
                        )
                    }
                },
                "required": ["facility_id", "scope_info"]
            }
        ),
        Tool(
            name="delete_scope",
            description="Hinemos 7.1リポジトリからスコープを削除（REST API）",
            inputSchema={
                "type": "object",
                "properties": {
                    "facility_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "削除するfacilityIdリスト 例: [\"SCOPE001\", \"SCOPE002\"]"
                    }
                },
                "required": ["facility_ids"]
            }
        ),
        Tool(
            name="get_platform_list",
            description="Hinemos 7.1リポジトリからノードへの設定可能なプラットフォーム一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_subplatform_list",
            description="Hinemos 7.1リポジトリからノードへの設定可能なサブプラットフォーム一覧を取得（REST API）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]

async def dispatch(name, manager, arguments):
    if name == "get_facility_tree":
        return await manager.get_facility_tree(**arguments)
    elif name == "get_exec_target_facility_tree":
        return await manager.get_exec_target_facility_tree(**arguments)
    elif name == "get_node_facility_tree":
        return await manager.get_node_facility_tree(**arguments)
    elif name == "get_node_list":
        return await manager.get_node_list(**arguments)
    elif name == "get_node":
        return await manager.get_node(**arguments)
    elif name == "get_node_full":
        return await manager.get_node_full(**arguments)
    elif name == "add_node":
        return await manager.add_node(**arguments)
    elif name == "modify_node":
        return await manager.modify_node(**arguments)
    elif name == "delete_node":
        return await manager.delete_node(**arguments)
    elif name == "search_node":
        return await manager.search_node(**arguments)
    elif name == "get_facility_list":
        return await manager.get_facility_list(**arguments)
    elif name == "get_scope":
        return await manager.get_scope(**arguments)
    elif name == "get_scope_default":
        return await manager.get_scope_default(**arguments)
    elif name == "add_scope":
        return await manager.add_scope(**arguments)
    elif name == "modify_scope":
        return await manager.modify_scope(**arguments)
    elif name == "delete_scope":
        return await manager.delete_scope(**arguments)
    elif name == "get_platform_list":
        return await manager.get_platform_list(**arguments)
    elif name == "get_subplatform_list":
        return await manager.get_subplatform_list(**arguments)
    return None