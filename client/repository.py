import os
import logging
from typing import Optional, Dict, Any
from .base import BaseClient

class RepositoryClient(BaseClient):
    def get_facility_tree(self, owner_role_id: Optional[str] = None, size: Optional[int] = None) -> Dict[str, Any]:
        """
        ファシリティツリー取得API (/repository/facility_tree)
        Args:
            owner_role_id: オーナーロールID (任意)
            size: 取得件数 (任意)
        Returns:
            ファシリティツリー情報
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        if size:
            params["size"] = str(size)
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/facility_tree', params=params)

    def get_exec_target_facility_tree(self, target_facility_id: str, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        指定スコープ配下のファシリティツリー取得API (/repository/facility_tree/{targetFacilityId})
        Args:
            target_facility_id: 取得対象のfacilityId
            owner_role_id: オーナーロールID (任意)
        Returns:
            ファシリティツリー情報
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        endpoint = f"RepositoryRestEndpoints/repository/facility_tree/{target_facility_id}"
        return self._make_request('GET', endpoint, params=params)

    def get_node_facility_tree(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        ノード情報を含むファシリティツリー取得API (/repository/facility_nodeTree)
        Args:
            owner_role_id: オーナーロールID (任意)
        Returns:
            ファシリティツリー情報
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/facility_nodeTree', params=params)

    def get_node_list(self, parent_facility_id: Optional[str] = None, size: Optional[int] = None, level: Optional[str] = None) -> Dict[str, Any]:
        """
        ノード一覧取得API (/repository/node_withoutNodeConfigInfo)
        Args:
            parent_facility_id: 親facilityId (任意)
            size: 取得件数 (任意)
            level: レベル (任意, "SCOPE"や"NODE"など)
        Returns:
            ノード一覧
        """
        params = {}
        if parent_facility_id:
            params["parentFacilityId"] = parent_facility_id
        if size:
            params["size"] = str(size)
        if level:
            params["level"] = level
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/node_withoutNodeConfigInfo', params=params)

    def get_node(self, facility_id: str) -> Dict[str, Any]:
        """
        ノード情報取得API（構成情報含む）(/repository/node/{facilityId})
        Args:
            facility_id: ノードのfacilityId
        Returns:
            ノード情報
        """
        endpoint = f"RepositoryRestEndpoints/repository/node/{facility_id}"
        return self._make_request('GET', endpoint)

    def get_node_full(self, facility_id: str) -> Dict[str, Any]:
        """
        構成情報を含むノード情報取得API (/repository/node/{facilityId})
        Args:
            facility_id: ノードのfacilityId
        Returns:
            ノード情報
        """
        endpoint = f"RepositoryRestEndpoints/repository/node/{facility_id}"
        return self._make_request('GET', endpoint)

    def get_node_without_config(self, facility_id: str) -> Dict[str, Any]:
        """
        構成情報を除いたノード情報取得API (/repository/node_withoutNodeConfigInfo/{facilityId})
        Args:
            facility_id: ノードのfacilityId
        Returns:
            ノード情報
        """
        endpoint = f"RepositoryRestEndpoints/repository/node_withoutNodeConfigInfo/{facility_id}"
        return self._make_request('GET', endpoint)

    def add_node(self, node_info: dict) -> Dict[str, Any]:
        """
        ノード情報追加API (/repository/node)
        Args:
            node_info: Hinemos仕様に準拠したノード情報(dict)。
                例:
                {
                    "autoDeviceSearch": true,
                    "administrator": "",
                    "cloudService": "",
                    "cloudScope": "",
                    "cloudResourceType": "",
                    "cloudResourceId": "",
                    "cloudResourceName": "",
                    "cloudLocation": "",
                    "cloudLogPriority": 16,
                    "contact": "",
                    "hardwareType": "",
                    "ipAddressV4": "172.31.24.200",
                    "ipAddressV6": "",
                    "ipAddressVersion": "IPV4",  # "IPV4" または "IPV6"
                    "ipmiIpAddress": "",
                    "ipmiLevel": "",
                    "ipmiPort": 0,
                    "ipmiProtocol": "RMCP+",
                    "ipmiRetries": 3,
                    "ipmiTimeout": 5000,
                    "ipmiUser": "",
                    "ipmiUserPassword": "",
                    "jobPriority": 16,
                    "jobMultiplicity": 0,
                    "nodeName": "web2",
                    "platformFamily": "LINUX",
                    "snmpCommunity": "public",
                    "snmpPort": 161,
                    "snmpRetryCount": 3,
                    "snmpTimeout": 5000,
                    "snmpVersion": "TYPE_V2",
                    "snmpSecurityLevel": "NOAUTH_NOPRIV",
                    "snmpUser": "",
                    "snmpAuthPassword": "",
                    "snmpPrivPassword": "",
                    "snmpAuthProtocol": "NONE",
                    "snmpPrivProtocol": "NONE",
                    "sshUser": "root",
                    "sshUserPassword": "",
                    "sshPrivateKeyFilepath": "",
                    "sshPrivateKeyPassphrase": "",
                    "sshPort": 22,
                    "sshTimeout": 50000,
                    "subPlatformFamily": "",
                    "wbemPort": 5988,
                    "wbemProtocol": "HTTP",
                    "wbemRetryCount": 3,
                    "wbemTimeout": 5000,
                    "wbemUser": "root",
                    "wbemUserPassword": "",
                    "winrmPort": 5985,
                    "winrmProtocol": "HTTP",
                    "winrmRetries": 3,
                    "winrmTimeout": 5000,
                    "winrmUser": "",
                    "winrmUserPassword": "",
                    "winrmVersion": "",
                    "agentAwakePort": 24005,
                    "nodeOsInfo": {
                        "osName": "",
                        "osRelease": "",
                        "osVersion": "",
                        "characterSet": ""
                    },
                    "nodeCpuInfo": [],
                    "nodeDeviceInfo": [],
                    "nodeDiskInfo": [],
                    "nodeFilesystemInfo": [],
                    "nodeHostnameInfo": [{"hostname": ""}],
                    "nodeMemoryInfo": [],
                    "nodeNetworkInterfaceInfo": [],
                    "nodeNoteInfo": [{"noteId": 0, "note": ""}],
                    "nodeVariableInfo": [],
                    "nodeNetstatInfo": [],
                    "nodeProcessInfo": [],
                    "nodePackageInfo": [],
                    "nodeProductInfo": [],
                    "nodeLicenseInfo": [],
                    "ownerRoleId": "ALL_USERS",
                    "facilityId": "WEB2",
                    "facilityName": "静的Webサーバ2",
                    "description": "",
                    "iconImage": "",
                    "valid": True
                }
        Returns:
            追加結果
        """
        # Hinemos仕様に合わせて、IPバージョンは "IPV4"/"IPV6" で送ること
        # 必要に応じてデフォルト値を補完
        node_info = node_info.copy()
        if "ipAddressVersion" in node_info and isinstance(node_info["ipAddressVersion"], int):
            node_info["ipAddressVersion"] = "IPV4" if node_info["ipAddressVersion"] == 4 else "IPV6"
        return self._make_request('POST', 'RepositoryRestEndpoints/repository/node', json=node_info["node_info"])

    def modify_node(self, facility_id: str, node_info: dict) -> Dict[str, Any]:
        """
        ノード情報更新API (/repository/node/{facilityId})
        Args:
            facility_id: ノードのfacilityId
            node_info: ノード情報(dict)。例:
                {
                    "facilityName": "サーバー001",
                    "description": "Webサーバー",
                    "ipAddressVersion": 4,
                    "ipAddressV4": "192.168.1.100",
                    "nodeName": "web-server-01",
                    "platformFamily": "UNIX",
                    "subPlatformFamily": "LINUX",
                    "hardwareType": "X86_64",
                    "ownerRoleId": "ADMINISTRATORS",
                    "valid": True
                }
        Returns:
            更新結果
        """
        endpoint = f"RepositoryRestEndpoints/repository/node/{facility_id}"
        return self._make_request('PUT', endpoint, json=node_info)

    def delete_node(self, facility_ids: list) -> Dict[str, Any]:
        """
        ノード情報削除API (/repository/node)
        Args:
            facility_ids: 削除するfacilityIdリスト
                例: ["NODE001", "NODE002"]
        Returns:
            削除結果
        """
        # facilityIdsはカンマ区切りでクエリパラメータ
        params = {"facilityIds": ",".join(facility_ids)}
        return self._make_request('DELETE', 'RepositoryRestEndpoints/repository/node', params=params)

    def search_node(self, search_params: dict) -> Dict[str, Any]:
        """
        ノード検索API (/repository/node_withoutNodeConfigInfo_search)
        Args:
            search_params: 検索条件(dict)。例:
                {
                    "facilityId": "NODE*",
                    "facilityName": "*server*",
                    "ipAddressV4": "192.168.1.*",
                    "platformFamily": "UNIX"
                }
        Returns:
            検索結果
        """
        return self._make_request('POST', 'RepositoryRestEndpoints/repository/node_withoutNodeConfigInfo_search', json=search_params)

    def get_facility_list(self, parent_facility_id: Optional[str] = None) -> Dict[str, Any]:
        """
        スコープ配下のスコープとノード一覧取得API (/repository/facility)
        Args:
            parent_facility_id: 親facilityId (任意)
        Returns:
            施設一覧
        """
        params = {}
        if parent_facility_id:
            params["parentFacilityId"] = parent_facility_id
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/facility', params=params)

    def get_scope(self, facility_id: str) -> Dict[str, Any]:
        """
        スコープ情報取得API (/repository/scope/{facilityId})
        Args:
            facility_id: スコープのfacilityId
        Returns:
            スコープ情報
        """
        endpoint = f"RepositoryRestEndpoints/repository/scope/{facility_id}"
        return self._make_request('GET', endpoint)

    def get_scope_default(self) -> Dict[str, Any]:
        """
        スコープ情報の初期値取得API (/repository/scope_default)
        Returns:
            スコープ情報
        """
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/scope_default')

    def add_scope(self, scope_info: dict) -> Dict[str, Any]:
        """
        スコープ情報追加API (/repository/scope)
        Args:
            scope_info: スコープ情報(dict)。例:
                {
                    "parentFacilityId": "ROOT",  # 親スコープID（必須）
                    "scopeInfo": {
                        "facilityId": "SCOPE001",         # スコープID（必須）
                        "facilityName": "開発環境",        # スコープ名（必須）
                        "description": "開発チーム用スコープ", # 説明（任意）
                        "ownerRoleId": "ADMINISTRATORS"   # オーナーロールID（必須）
                    }
                }
        Returns:
            追加結果
        """
        return self._make_request('POST', 'RepositoryRestEndpoints/repository/scope', json=scope_info)

    def modify_scope(self, facility_id: str, scope_info: dict) -> Dict[str, Any]:
        """
        スコープ情報更新API (/repository/scope/{facilityId})
        Args:
            facility_id: スコープのfacilityId
            scope_info: スコープ情報(dict)。例:
                {
                    "facilityName": "開発環境",
                    "description": "開発チーム用スコープ",
                    "ownerRoleId": "ADMINISTRATORS"
                }
        Returns:
            更新結果
        """
        endpoint = f"RepositoryRestEndpoints/repository/scope/{facility_id}"
        return self._make_request('PUT', endpoint, json=scope_info)

    def delete_scope(self, facility_ids: list) -> Dict[str, Any]:
        """
        スコープ情報削除API (/repository/scope)
        Args:
            facility_ids: 削除するfacilityIdリスト
                例: ["SCOPE001", "SCOPE002"]
        Returns:
            削除結果
        """
        params = {"facilityIds": ",".join(facility_ids)}
        return self._make_request('DELETE', 'RepositoryRestEndpoints/repository/scope', params=params)

    def get_platform_list(self) -> Dict[str, Any]:
        """
        ノードへの設定可能なプラットフォーム一覧取得API (/repository/platform)
        Returns:
            プラットフォーム一覧
        """
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/platform')

    def get_subplatform_list(self) -> Dict[str, Any]:
        """
        ノードへの設定可能なサブプラットフォーム一覧取得API (/repository/subPlatform)
        Returns:
            サブプラットフォーム一覧
        """
        return self._make_request('GET', 'RepositoryRestEndpoints/repository/subPlatform')

