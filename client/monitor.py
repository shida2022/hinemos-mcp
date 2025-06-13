from typing import Dict, Any, List, Optional
from .base import BaseClient

class MonitorClient(BaseClient):
    """
    Hinemos 7.1 監視設定 REST API クライアント
    仕様: spec/hinemos_monitor_api_spec.md を参照
    """

    # --- 共通・一覧・取得・削除 ---
    def get_monitor_list(self) -> List[Dict[str, Any]]:
        """
        監視設定一覧取得API (/monitorsetting/monitor)
        Returns:
            監視設定一覧（配列）
        """
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor')

    def search_monitor_list(self, monitor_filter_info: dict) -> List[Dict[str, Any]]:
        """
        条件指定監視設定一覧取得API (/monitorsetting/monitor_search)
        Args:
            monitor_filter_info: フィルター条件(dict)
        Returns:
            監視設定一覧（配列）
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/monitor_search', json={"monitorFilterInfo": monitor_filter_info})

    def get_monitor(self, monitor_id: str) -> Dict[str, Any]:
        """
        監視設定取得API (/monitorsetting/monitor/{monitorId})
        Args:
            monitor_id: 監視設定ID
        Returns:
            監視設定情報
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/monitor/{monitor_id}"
        return self._make_request('GET', endpoint)

    def delete_monitor(self, monitor_ids: List[str]) -> Dict[str, Any]:
        """
        監視設定削除API (/monitorsetting/monitor)
        Args:
            monitor_ids: 削除する監視設定IDリスト
        Returns:
            削除結果
        """
        params = {"monitorIds": ",".join(monitor_ids)}
        return self._make_request('DELETE', 'MonitorsettingRestEndpoints/monitorsetting/monitor', params=params)

    def set_status_monitor(self, monitor_ids: List[str], valid_flg: bool) -> Dict[str, Any]:
        """
        監視有効/無効切り替えAPI (/monitorsetting/monitor_monitorValid)
        Args:
            monitor_ids: 監視設定IDリスト
            valid_flg: 有効(True)/無効(False)
        Returns:
            結果
        """
        body = {"monitorIds": monitor_ids, "validFlg": valid_flg}
        return self._make_request('PUT', 'MonitorsettingRestEndpoints/monitorsetting/monitor_monitorValid', json=body)

    def set_status_collector(self, monitor_ids: List[str], collector_flg: bool) -> Dict[str, Any]:
        """
        収集有効/無効切り替えAPI (/monitorsetting/monitor_collectorValid)
        Args:
            monitor_ids: 監視設定IDリスト
            collector_flg: 有効(True)/無効(False)
        Returns:
            結果
        """
        body = {"monitorIds": monitor_ids, "collectorFlg": collector_flg}
        return self._make_request('PUT', 'MonitorsettingRestEndpoints/monitorsetting/monitor_collectorValid', json=body)

    def get_monitor_info_for_graph(self, monitor_id: str) -> Dict[str, Any]:
        """
        性能グラフ用監視設定取得API (/monitorsetting/monitor_graphInfo_forCollect/{monitorId})
        Args:
            monitor_id: 監視設定ID
        Returns:
            監視設定情報
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/monitor_graphInfo_forCollect/{monitor_id}"
        return self._make_request('GET', endpoint)

    # --- 監視種別ごとの追加・更新 ---
    def add_http_numeric_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定追加API (/monitorsetting/httpNumeric)
        Args:
            monitor_info: 監視設定情報(dict)。例は仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/httpNumeric', json=monitor_info)

    def modify_http_numeric_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定更新API (/monitorsetting/httpNumeric/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/httpNumeric/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_ping_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        PING監視設定追加API (/monitorsetting/ping)
        Args:
            monitor_info: 監視設定情報(dict)。例は仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/ping', json=monitor_info)

    def modify_ping_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        PING監視設定更新API (/monitorsetting/ping/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/ping/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_agent_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        エージェント監視設定追加API (/monitorsetting/agent)
        Args:
            monitor_info: 監視設定情報(dict)。例は仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/agent', json=monitor_info)

    def modify_agent_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        エージェント監視設定更新API (/monitorsetting/agent/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/agent/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_jmx_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        JMX監視設定追加API (/monitorsetting/jmx)
        Args:
            monitor_info: 監視設定情報(dict)。例は仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/jmx', json=monitor_info)

    def modify_jmx_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        JMX監視設定更新API (/monitorsetting/jmx/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/jmx/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_snmp_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視設定追加API (/monitorsetting/snmp)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/snmp', json=monitor_info)

    def modify_snmp_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視設定更新API (/monitorsetting/snmp/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/snmp/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_sql_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SQL監視設定追加API (/monitorsetting/sql)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/sql', json=monitor_info)

    def modify_sql_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SQL監視設定更新API (/monitorsetting/sql/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/sql/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_logfile_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        ログファイル監視設定追加API (/monitorsetting/logfile)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/logfile', json=monitor_info)

    def modify_logfile_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        ログファイル監視設定更新API (/monitorsetting/logfile/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/logfile/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_command_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        コマンド監視設定追加API (/monitorsetting/command)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/command', json=monitor_info)

    def modify_command_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        コマンド監視設定更新API (/monitorsetting/command/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/command/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_custom_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視設定追加API (/monitorsetting/custom)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/custom', json=monitor_info)

    def modify_custom_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視設定更新API (/monitorsetting/custom/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/custom/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def add_custom_numeric_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視（数値）設定追加API (/monitorsetting/customNumeric)
        Args:
            monitor_info: カスタム数値監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/customNumeric', json=monitor_info)

    def modify_custom_numeric_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視（数値）設定更新API (/monitorsetting/customNumeric/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: カスタム数値監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/customNumeric/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_custom_numeric_list(self) -> List[Dict[str, Any]]:
        """
        カスタム監視（数値）設定一覧取得API (/monitorsetting/customNumeric)
        Returns:
            カスタム数値監視設定一覧（配列）
        """
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/customNumeric')

    def add_custom_string_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視（文字列）設定追加API (/monitorsetting/customString)
        Args:
            monitor_info: カスタム文字列監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/customString', json=monitor_info)

    def modify_custom_string_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視（文字列）設定更新API (/monitorsetting/customString/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: カスタム文字列監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/customString/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_custom_string_list(self) -> List[Dict[str, Any]]:
        """
        カスタム監視（文字列）設定一覧取得API (/monitorsetting/customString)
        Returns:
            カスタム文字列監視設定一覧（配列）
        """
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/customString')

    # --- 追加: 監視設定簡易一覧・その他 ---
    def get_monitor_list_without_checkinfo(self, owner_role_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        監視設定簡易一覧取得API (/monitorsetting/monitor_withoutCheckInfo)
        Args:
            owner_role_id: オーナーロールID（オプション）
        Returns:
            監視設定一覧（配列）
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor_withoutCheckInfo', params=params)

    def search_monitor_list_without_checkinfo(self, monitor_filter_info: dict) -> List[Dict[str, Any]]:
        """
        条件指定監視設定簡易一覧取得API (/monitorsetting/monitor_withoutCheckInfo_search)
        Args:
            monitor_filter_info: フィルター条件(dict)
        Returns:
            監視設定一覧（配列）
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/monitor_withoutCheckInfo_search', json={"monitorFilterInfo": monitor_filter_info})

    def get_monitor_string_list(self, facility_id: Optional[str] = None, owner_role_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        文字列監視設定一覧取得API (/monitorsetting/monitor_string)
        Args:
            facility_id: ファシリティID（オプション）
            owner_role_id: オーナーロールID（オプション）
        Returns:
            監視設定一覧（配列）
        """
        params = {}
        if facility_id:
            params["facilityId"] = facility_id
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor_string', params=params)

    def get_monitor_string_and_trap_list(self) -> List[Dict[str, Any]]:
        """
        文字列・トラップ監視一覧取得API (/monitorsetting/monitor_stringAndTrap)
        Returns:
            監視設定一覧（配列）
        """
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor_stringAndTrap')

    def get_monitor_list_for_job(self, owner_role_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        監視ジョブ用監視設定一覧取得API (/monitorsetting/monitor_withoutCheckInfo_forJob)
        Args:
            owner_role_id: オーナーロールID（オプション）
        Returns:
            監視設定一覧（配列）
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor_withoutCheckInfo_forJob', params=params)

    def get_monitor_string_tag(self, monitor_id: str, owner_role_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        監視文字列タグ一覧取得API (/monitorsetting/monitor_string_tag/{monitorId})
        Args:
            monitor_id: 監視設定ID
            owner_role_id: オーナーロールID（オプション）
        Returns:
            タグ一覧
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/monitor_string_tag/{monitor_id}"
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', endpoint, params=params)

    def add_performance_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        リソース監視設定追加API (/monitorsetting/performance)
        Args:
            monitor_info: リソース監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/performance', json=monitor_info)

    def modify_performance_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        リソース監視設定更新API (/monitorsetting/performance/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: リソース監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/performance/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_performance_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        リソース監視設定一覧取得API (/monitorsetting/performance)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            リソース監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/performance', params=params)

    def add_snmp_numeric_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視（数値）設定追加API (/monitorsetting/snmpNumeric)
        Args:
            monitor_info: SNMP数値監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/snmpNumeric', json=monitor_info)

    def modify_snmp_numeric_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視（数値）設定更新API (/monitorsetting/snmpNumeric/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: SNMP数値監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/snmpNumeric/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_snmp_numeric_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        SNMP監視（数値）設定一覧取得API (/monitorsetting/snmpNumeric)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            SNMP数値監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/snmpNumeric', params=params)

    def add_snmp_string_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視（文字列）設定追加API (/monitorsetting/snmpString)
        Args:
            monitor_info: SNMP文字列監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/snmpString', json=monitor_info)

    def modify_snmp_string_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視（文字列）設定更新API (/monitorsetting/snmpString/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: SNMP文字列監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/snmpString/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_snmp_string_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        SNMP監視（文字列）設定一覧取得API (/monitorsetting/snmpString)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            SNMP文字列監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/snmpString', params=params)

    def add_process_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        プロセス監視設定追加API (/monitorsetting/process)
        Args:
            monitor_info: プロセス監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/process', json=monitor_info)

    def modify_process_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        プロセス監視設定更新API (/monitorsetting/process/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: プロセス監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/process/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_process_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        プロセス監視設定一覧取得API (/monitorsetting/process)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            プロセス監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/process', params=params)

    def add_http_numeric_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定追加API (/monitorsetting/httpNumeric)
        Args:
            monitor_info: HTTP数値監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/httpNumeric', json=monitor_info)

    def modify_http_numeric_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定更新API (/monitorsetting/httpNumeric/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: HTTP数値監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/httpNumeric/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_http_numeric_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        HTTP監視（数値）設定一覧取得API (/monitorsetting/httpNumeric)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            HTTP数値監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/httpNumeric', params=params)

    def add_http_string_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（文字列）設定追加API (/monitorsetting/httpString)
        Args:
            monitor_info: HTTP文字列監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/httpString', json=monitor_info)

    def modify_http_string_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（文字列）設定更新API (/monitorsetting/httpString/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: HTTP文字列監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/httpString/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_http_string_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        HTTP監視（文字列）設定一覧取得API (/monitorsetting/httpString)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            HTTP文字列監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/httpString', params=params)

    def add_http_scenario_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTPシナリオ監視設定追加API (/monitorsetting/httpScenario)
        Args:
            monitor_info: HTTPシナリオ監視設定情報(dict)。例はAPI仕様書参照
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/httpScenario', json=monitor_info)

    def modify_http_scenario_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTPシナリオ監視設定更新API (/monitorsetting/httpScenario/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: HTTPシナリオ監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/httpScenario/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def get_http_scenario_list(self, monitor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        HTTPシナリオ監視設定一覧取得API (/monitorsetting/httpScenario)
        Args:
            monitor_id: 監視設定ID（オプション）
        Returns:
            HTTPシナリオ監視設定一覧（配列）
        """
        params = {}
        if monitor_id:
            params["monitorId"] = monitor_id
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/httpScenario', params=params)