import os
import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

class HinemosClient:
    """
    Hinemos REST API Client
    
    Usage:
        client = HinemosClient()
        client.login()
        
        # Get facility tree
        facility_tree = client.get_facility_tree()
        
        # Other API calls...
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Hinemos client
        
        Args:
            base_url: Base URL of Hinemos server (optional, will use HINEMOS_ENDPOINT env if not provided)
        """
        if base_url is None:
            base_url = os.getenv("HINEMOS_ENDPOINT", "http://localhost:8080")
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token_id: Optional[str] = None
        self.token_expiration: Optional[datetime] = None
        self.logger = logging.getLogger(__name__)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def login(self, user_id: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Login to Hinemos and obtain access token
        
        Args:
            user_id: Username (optional, will use HINEMOS_USERNAME env if not provided)
            password: Password (optional, will use HINEMOS_PASSWORD env if not provided)
            
        Returns:
            Login response containing token and manager info
            
        Raises:
            requests.RequestException: If login fails
        """
        if user_id is None:
            user_id = os.getenv("HINEMOS_USERNAME", "")
        if password is None:
            password = os.getenv("HINEMOS_PASSWORD", "")

        login_url = f"{self.base_url}/HinemosWeb/api/AccessRestEndpoints/access/login"
        login_data = {
            "userId": user_id,
            "password": password
        }

        try:
            response = self.session.post(login_url, json=login_data)
            response.raise_for_status()

            login_response = response.json()

            # Extract token information
            token_info = login_response.get('token', {})
            self.token_id = token_info.get('tokenId')

            # Parse expiration date
            expiration_str = token_info.get('expirationDate')
            if expiration_str:
                self.token_expiration = datetime.strptime(
                    expiration_str, "%Y-%m-%d %H:%M:%S.%f"
                )

            # Set authorization header for subsequent requests
            if self.token_id:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token_id}'
                })

            self.logger.info(f"Successfully logged in. Token expires at: {self.token_expiration}")
            return login_response

        except requests.RequestException as e:
            self.logger.error(f"Login failed: {e}")
            raise
    
    def is_token_valid(self) -> bool:
        """
        Check if current token is still valid
        
        Returns:
            True if token is valid, False otherwise
        """
        if not self.token_id or not self.token_expiration:
            return False
        
        # Add 5 minute buffer before expiration
        return datetime.now() < (self.token_expiration - timedelta(minutes=5))
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make authenticated request to Hinemos API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response
            
        Raises:
            requests.RequestException: If request fails
            ValueError: If token is invalid
        """
        if not self.is_token_valid():
            raise ValueError("Token is invalid or expired. Please login again.")
        
        url = f"{self.base_url}/HinemosWeb/api/{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {method} {url} - {e}")
            raise
    
    # --- RepositoryRestEndpoints対応 Hinemos REST APIクライアントメソッド ---

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
        ノード情報取得API (/repository/node/{facilityId})
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

    def add_node(self, node_info: dict) -> Dict[str, Any]:
        """
        ノード情報追加API (/repository/node)
        Args:
            node_info: ノード情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'RepositoryRestEndpoints/repository/node', json=node_info)

    def modify_node(self, facility_id: str, node_info: dict) -> Dict[str, Any]:
        """
        ノード情報更新API (/repository/node/{facilityId})
        Args:
            facility_id: ノードのfacilityId
            node_info: ノード情報(dict)
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
        Returns:
            削除結果
        """
        # facilityIdsはカンマ区切りでクエリパラメータ
        params = {"facilityIds": ",".join(facility_ids)}
        return self._make_request('DELETE', 'RepositoryRestEndpoints/repository/node', params=params)

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
            scope_info: スコープ情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'RepositoryRestEndpoints/repository/scope', json=scope_info)

    def modify_scope(self, facility_id: str, scope_info: dict) -> Dict[str, Any]:
        """
        スコープ情報更新API (/repository/scope/{facilityId})
        Args:
            facility_id: スコープのfacilityId
            scope_info: スコープ情報(dict)
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
    
    # --- MonitorsettingRestEndpoints対応 Hinemos REST APIクライアントメソッド ---

    def get_monitor_list(self) -> Dict[str, Any]:
        """
        監視設定一覧の取得API (/monitorsetting/monitor)
        Returns:
            監視設定一覧
        """
        return self._make_request('GET', 'MonitorsettingRestEndpoints/monitorsetting/monitor')

    def get_monitor(self, monitor_id: str) -> Dict[str, Any]:
        """
        監視設定の取得API (/monitorsetting/monitor/{monitorId})
        Args:
            monitor_id: 監視設定ID
        Returns:
            監視設定情報
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/monitor/{monitor_id}"
        return self._make_request('GET', endpoint)

    def add_http_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定の追加API (/monitorsetting/httpNumeric)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/httpNumeric', json=monitor_info)

    def add_ping_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        PING監視設定の追加API (/monitorsetting/ping)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/ping', json=monitor_info)

    def add_agent_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        エージェント監視設定の追加API (/monitorsetting/agent)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/agent', json=monitor_info)

    def add_jmx_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        JMX監視設定の追加API (/monitorsetting/jmx)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/jmx', json=monitor_info)

    def add_snmp_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視設定の追加API (/monitorsetting/snmp)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/snmp', json=monitor_info)

    def add_sql_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        SQL監視設定の追加API (/monitorsetting/sql)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/sql', json=monitor_info)

    def add_logfile_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        ログファイル監視設定の追加API (/monitorsetting/logfile)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/logfile', json=monitor_info)

    def add_command_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        コマンド監視設定の追加API (/monitorsetting/command)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/command', json=monitor_info)

    def add_custom_monitor(self, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視設定の追加API (/monitorsetting/custom)
        Args:
            monitor_info: 監視設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'MonitorsettingRestEndpoints/monitorsetting/custom', json=monitor_info)

    def modify_http_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        HTTP監視（数値）設定の更新API (/monitorsetting/httpNumeric/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/httpNumeric/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_ping_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        PING監視設定の更新API (/monitorsetting/ping/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/ping/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_agent_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        エージェント監視設定の更新API (/monitorsetting/agent/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/agent/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_jmx_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        JMX監視設定の更新API (/monitorsetting/jmx/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/jmx/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_snmp_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SNMP監視設定の更新API (/monitorsetting/snmp/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/snmp/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_sql_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        SQL監視設定の更新API (/monitorsetting/sql/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/sql/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_logfile_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        ログファイル監視設定の更新API (/monitorsetting/logfile/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/logfile/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_command_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        コマンド監視設定の更新API (/monitorsetting/command/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/command/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def modify_custom_monitor(self, monitor_id: str, monitor_info: dict) -> Dict[str, Any]:
        """
        カスタム監視設定の更新API (/monitorsetting/custom/{monitorId})
        Args:
            monitor_id: 監視設定ID
            monitor_info: 監視設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/custom/{monitor_id}"
        return self._make_request('PUT', endpoint, json=monitor_info)

    def delete_monitor(self, monitor_ids: list) -> Dict[str, Any]:
        """
        監視設定の削除API (/monitorsetting/monitor)
        Args:
            monitor_ids: 削除する監視設定IDリスト
        Returns:
            削除結果
        """
        params = {"monitorIds": ",".join(monitor_ids)}
        return self._make_request('DELETE', 'MonitorsettingRestEndpoints/monitorsetting/monitor', params=params)

    def get_monitor_info_for_graph(self, monitor_id: str) -> Dict[str, Any]:
        """
        性能グラフ表示への対象である監視設定の取得API (/monitorsetting/monitor_graphInfo_forCollect/{monitorId})
        Args:
            monitor_id: 監視設定ID
        Returns:
            監視設定情報
        """
        endpoint = f"MonitorsettingRestEndpoints/monitorsetting/monitor_graphInfo_forCollect/{monitor_id}"
        return self._make_request('GET', endpoint)

    def set_status_monitor(self, status_info: dict) -> Dict[str, Any]:
        """
        監視設定の監視有効／無効の切り替えAPI (/monitorsetting/monitor_monitorValid)
        Args:
            status_info: ステータス情報(dict)
        Returns:
            結果
        """
        return self._make_request('PUT', 'MonitorsettingRestEndpoints/monitorsetting/monitor_monitorValid', json=status_info)

    def set_status_collector(self, status_info: dict) -> Dict[str, Any]:
        """
        監視設定の収集有効／無効の切り替えAPI (/monitorsetting/monitor_collectorValid)
        Args:
            status_info: ステータス情報(dict)
        Returns:
            結果
        """
        return self._make_request('PUT', 'MonitorsettingRestEndpoints/monitorsetting/monitor_collectorValid', json=status_info)
    
    def logout(self) -> None:
        """
        Logout and clean up session
        """
        # Clear token information
        self.token_id = None
        self.token_expiration = None
        
        # Remove authorization header
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        
        self.logger.info("Logged out successfully")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - logout automatically"""
        self.logout()


    # --- CalendarRestEndpoints対応 Hinemos REST APIクライアントメソッド ---

    def get_calendar_list(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        カレンダー一覧取得API (/calendar/calendar)
        Args:
            owner_role_id: オーナーロールID (任意)
        Returns:
            カレンダー一覧
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'CalendarRestEndpoints/calendar/calendar', params=params)

    def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """
        カレンダー情報取得API (/calendar/calendar/{calendarId})
        Args:
            calendar_id: カレンダーID
        Returns:
            カレンダー情報
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}"
        return self._make_request('GET', endpoint)

    def add_calendar(self, calendar_info: dict) -> Dict[str, Any]:
        """
        カレンダー追加API (/calendar/calendar)
        Args:
            calendar_info: カレンダー情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'CalendarRestEndpoints/calendar/calendar', json=calendar_info)

    def modify_calendar(self, calendar_id: str, calendar_info: dict) -> Dict[str, Any]:
        """
        カレンダー更新API (/calendar/calendar/{calendarId})
        Args:
            calendar_id: カレンダーID
            calendar_info: カレンダー情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}"
        return self._make_request('PUT', endpoint, json=calendar_info)

    def delete_calendar(self, calendar_ids: list) -> Dict[str, Any]:
        """
        カレンダー削除API (/calendar/calendar)
        Args:
            calendar_ids: 削除するカレンダーIDリスト
        Returns:
            削除結果
        """
        params = {"calendarIds": ",".join(calendar_ids)}
        return self._make_request('DELETE', 'CalendarRestEndpoints/calendar/calendar', params=params)

    def get_calendar_month(self, calendar_id: str, year: int, month: int) -> Dict[str, Any]:
        """
        カレンダー月別稼働状態取得API (/calendar/calendar/{calendarId}/calendarDetail_monthOperationState)
        Args:
            calendar_id: カレンダーID
            year: 年 (int)
            month: 月 (int)
        Returns:
            月別稼働状態リスト
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}/calendarDetail_monthOperationState"
        params = {"year": str(year), "month": str(month)}
        return self._make_request('GET', endpoint, params=params)

    def get_calendar_week(self, calendar_id: str, year: int, month: int, day: int) -> Dict[str, Any]:
        """
        カレンダー週情報取得API (/calendar/calendar/{calendarId}/calendarDetail_week)
        Args:
            calendar_id: カレンダーID
            year: 年 (int)
            month: 月 (int)
            day: 日 (int)
        Returns:
            週情報リスト
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}/calendarDetail_week"
        params = {"year": str(year), "month": str(month), "day": str(day)}
        return self._make_request('GET', endpoint, params=params)

    def get_calendar_pattern_list(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        カレンダパターン一覧取得API (/calendar/pattern)
        Args:
            owner_role_id: オーナーロールID (任意)
        Returns:
            カレンダパターン一覧
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'CalendarRestEndpoints/calendar/pattern', params=params)

    def get_calendar_pattern(self, calendar_pattern_id: str) -> Dict[str, Any]:
        """
        カレンダパターン情報取得API (/calendar/pattern/{calendarPatternId})
        Args:
            calendar_pattern_id: カレンダパターンID
        Returns:
            カレンダパターン情報
        """
        endpoint = f"CalendarRestEndpoints/calendar/pattern/{calendar_pattern_id}"
        return self._make_request('GET', endpoint)

    def add_calendar_pattern(self, pattern_info: dict) -> Dict[str, Any]:
        """
        カレンダパターン追加API (/calendar/pattern)
        Args:
            pattern_info: カレンダパターン情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'CalendarRestEndpoints/calendar/pattern', json=pattern_info)

    def modify_calendar_pattern(self, calendar_pattern_id: str, pattern_info: dict) -> Dict[str, Any]:
        """
        カレンダパターン更新API (/calendar/pattern/{calendarPatternId})
        Args:
            calendar_pattern_id: カレンダパターンID
            pattern_info: カレンダパターン情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"CalendarRestEndpoints/calendar/pattern/{calendar_pattern_id}"
        return self._make_request('PUT', endpoint, json=pattern_info)

    def delete_calendar_pattern(self, calendar_pattern_ids: list) -> Dict[str, Any]:
        """
        カレンダパターン削除API (/calendar/pattern)
        Args:
            calendar_pattern_ids: 削除するカレンダパターンIDリスト
        Returns:
            削除結果
        """
        params = {"calendarPatternIds": ",".join(calendar_pattern_ids)}
        return self._make_request('DELETE', 'CalendarRestEndpoints/calendar/pattern', params=params)

    # --- CollectRestEndpoints対応 Hinemos REST APIクライアントメソッド ---

    def get_collect_id(self, monitor_id: str, item_name: str, display_name: str, facility_ids: list, size: Optional[int] = None) -> Dict[str, Any]:
        """
        収集IDリスト取得API (/collect/key/{monitorId})
        Args:
            monitor_id: 監視設定ID
            item_name: 収集項目コード
            display_name: 表示名
            facility_ids: ファシリティIDリスト
            size: 取得件数（任意）
        Returns:
            収集IDリスト
        """
        params = {
            "itemName": item_name,
            "displayName": display_name,
            "facilityIds": ",".join(facility_ids)
        }
        if size is not None:
            params["size"] = str(size)
        endpoint = f"CollectRestEndpoints/collect/key/{monitor_id}"
        return self._make_request('GET', endpoint, params=params)

    def get_collect_data(self, id_list: list, summary_type: str, from_time: str, to_time: str, size: Optional[int] = None) -> Dict[str, Any]:
        """
        収集データ取得API (/collect/data)
        Args:
            id_list: 収集IDリスト
            summary_type: サマリタイプ
            from_time: 取得開始日時 (yyyy-MM-dd HH:mm:ss)
            to_time: 取得終了日時 (yyyy-MM-dd HH:mm:ss)
            size: 取得件数（任意）
        Returns:
            収集データリスト
        """
        params = {
            "idList": ",".join(str(i) for i in id_list),
            "summaryType": summary_type,
            "fromTime": from_time,
            "toTime": to_time
        }
        if size is not None:
            params["size"] = str(size)
        return self._make_request('GET', 'CollectRestEndpoints/collect/data', params=params)

    def get_item_code_list(self, facility_ids: list, size: Optional[int] = None) -> Dict[str, Any]:
        """
        収集項目コードリスト取得API (/collect/key)
        Args:
            facility_ids: ファシリティIDリスト
            size: 取得件数（任意）
        Returns:
            収集項目コードリスト
        """
        params = {
            "facilityIds": ",".join(facility_ids)
        }
        if size is not None:
            params["size"] = str(size)
        return self._make_request('GET', 'CollectRestEndpoints/collect/key', params=params)

    def get_collect_item_code_master_list(self) -> Dict[str, Any]:
        """
        収集項目コードマスタ一覧取得API (/collect/itemCodeMst)
        Returns:
            収集項目コードマスタ一覧
        """
        return self._make_request('GET', 'CollectRestEndpoints/collect/itemCodeMst')

    def get_collect_key_map_for_analytics(self, facility_id: str, owner_role_id: str) -> Dict[str, Any]:
        """
        収集値キーの一覧取得API (/collect/key_mapKeyItemName/{facilityId})
        Args:
            facility_id: ファシリティID
            owner_role_id: オーナーロールID
        Returns:
            収集値キーの一覧
        """
        params = {"ownerRoleId": owner_role_id}
        endpoint = f"CollectRestEndpoints/collect/key_mapKeyItemName/{facility_id}"
        return self._make_request('GET', endpoint, params=params)

    def get_available_collector_item_list(self, facility_id: str) -> Dict[str, Any]:
        """
        収集可能な項目のリスト取得API (/collect/itemCodeMst_availableItem)
        Args:
            facility_id: ファシリティID
        Returns:
            収集可能な項目リスト
        """
        params = {"facilityId": facility_id}
        return self._make_request('GET', 'CollectRestEndpoints/collect/itemCodeMst_availableItem', params=params)

    def get_collect_master_info(self) -> Dict[str, Any]:
        """
        収集マスタ情報一括取得API (/collect/master)
        Returns:
            収集マスタ情報
        """
        return self._make_request('GET', 'CollectRestEndpoints/collect/master')

    def add_collect_setting(self, collect_info: dict) -> Dict[str, Any]:
        """
        収集設定追加API (/collect/setting)
        Args:
            collect_info: 収集設定情報(dict)
        Returns:
            追加結果
        """
        return self._make_request('POST', 'CollectRestEndpoints/collect/setting', json=collect_info)

    def modify_collect_setting(self, collect_id: str, collect_info: dict) -> Dict[str, Any]:
        """
        収集設定更新API (/collect/setting/{collectId})
        Args:
            collect_id: 収集設定ID
            collect_info: 収集設定情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"CollectRestEndpoints/collect/setting/{collect_id}"
        return self._make_request('PUT', endpoint, json=collect_info)

    def delete_collect_setting(self, collect_ids: list) -> Dict[str, Any]:
        """
        収集設定削除API (/collect/setting)
        Args:
            collect_ids: 削除する収集設定IDリスト
        Returns:
            削除結果
        """
        params = {"collectIds": ",".join(collect_ids)}
        return self._make_request('DELETE', 'CollectRestEndpoints/collect/setting', params=params)

# Usage example
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client (base_url will be taken from env if not provided)
    client = HinemosClient()
    
    try:
        # Login (user/pass will be taken from env if not provided)
        login_response = client.login()
        print("Login successful:", json.dumps(login_response, indent=2, ensure_ascii=False))
        
        # Get facility tree
        facility_tree = client.get_facility_tree()
        print("Facility tree:", json.dumps(facility_tree, indent=2, ensure_ascii=False))

        # Get exec target facility tree (例: facility_id="root")
        exec_tree = client.get_exec_target_facility_tree("root")
        print("Exec target facility tree:", json.dumps(exec_tree, indent=2, ensure_ascii=False))

        # Get node facility tree
        node_facility_tree = client.get_node_facility_tree()
        print("Node facility tree:", json.dumps(node_facility_tree, indent=2, ensure_ascii=False))

        # Get node list
        node_list = client.get_node_list()
        print("Node list:", json.dumps(node_list, indent=2, ensure_ascii=False))

        # Get node (例: facility_id="root")
        node = client.get_node("TEST_LOCAL")
        print("Node:", json.dumps(node, indent=2, ensure_ascii=False))

        # Get node full (例: facility_id="root")
        node_full = client.get_node_full("TEST_LOCAL")
        print("Node full:", json.dumps(node_full, indent=2, ensure_ascii=False))

        # Get facility list
        facility_list = client.get_facility_list()
        print("Facility list:", json.dumps(facility_list, indent=2, ensure_ascii=False))

        # 最初のfacilityIdを使ってノード情報を取得
        first_facility_id = None
        if facility_list and "facilityList" in facility_list and facility_list["facilityList"]:
            first_facility_id = facility_list["facilityList"][0].get("facilityId")
            print(f"First facilityId: {first_facility_id}")

        if first_facility_id:
            node = client.get_node("TEST_LOCAL")
            print("Node:", json.dumps(node, indent=2, ensure_ascii=False))

            node_full = client.get_node_full("TEST_LOCAL")
            print("Node full:", json.dumps(node_full, indent=2, ensure_ascii=False))

            scope = client.get_scope("TEST_LOCAL")
            print("Scope:", json.dumps(scope, indent=2, ensure_ascii=False))
        else:
            print("No facilityId found in facility list.")

        # Get scope default
        scope_default = client.get_scope_default()
        print("Scope default:", json.dumps(scope_default, indent=2, ensure_ascii=False))

        # Get platform list
        platform_list = client.get_platform_list()
        print("Platform list:", json.dumps(platform_list, indent=2, ensure_ascii=False))

        # Get subplatform list
        subplatform_list = client.get_subplatform_list()
        print("Subplatform list:", json.dumps(subplatform_list, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Logout
        client.logout()