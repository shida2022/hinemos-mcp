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
    
    def add_http_monitor(self, monitor_id: str, monitor_name: str, facility_id: str, 
                        url: str, interval: int = 300, timeout: int = 10000,
                        owner_role_id: str = "ADMINISTRATORS") -> Dict[str, Any]:
        """
        Add HTTP monitor setting
        
        Args:
            monitor_id: Unique monitor ID
            monitor_name: Display name for monitor
            facility_id: Target facility ID
            url: URL to monitor
            interval: Check interval in seconds (default: 300)
            timeout: Timeout in milliseconds (default: 10000)
            owner_role_id: Owner role ID (default: "ADMINISTRATORS")
            
        Returns:
            Response data
        """
        data = {
            "monitorId": monitor_id,
            "monitorName": monitor_name,
            "facilityId": facility_id,
            "url": url,
            "interval": interval,
            "timeout": timeout,
            "ownerRoleId": owner_role_id
        }
        
        return self._make_request('POST', 'MonitorRestEndpoints/monitor/http', json=data)
    
    def add_ping_monitor(self, monitor_id: str, monitor_name: str, facility_id: str,
                        interval: int = 300, timeout: int = 5000, run_count: int = 3,
                        owner_role_id: str = "ADMINISTRATORS") -> Dict[str, Any]:
        """
        Add Ping monitor setting
        
        Args:
            monitor_id: Unique monitor ID
            monitor_name: Display name for monitor
            facility_id: Target facility ID
            interval: Check interval in seconds (default: 300)
            timeout: Timeout in milliseconds (default: 5000)
            run_count: Number of ping attempts (default: 3)
            owner_role_id: Owner role ID (default: "ADMINISTRATORS")
            
        Returns:
            Response data
        """
        data = {
            "monitorId": monitor_id,
            "monitorName": monitor_name,
            "facilityId": facility_id,
            "interval": interval,
            "timeout": timeout,
            "runCount": run_count,
            "ownerRoleId": owner_role_id
        }
        
        return self._make_request('POST', 'MonitorRestEndpoints/monitor/ping', json=data)
    
    def get_monitor_list(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get monitor settings list
        
        Args:
            owner_role_id: Optional owner role ID filter
            
        Returns:
            Monitor list data
        """
        params = {}
        if owner_role_id:
            params['ownerRoleId'] = owner_role_id
        
        return self._make_request('GET', 'MonitorRestEndpoints/monitor', params=params)
    
    def delete_monitor(self, monitor_ids: list) -> Dict[str, Any]:
        """
        Delete monitor settings
        
        Args:
            monitor_ids: List of monitor IDs to delete
            
        Returns:
            Response data
        """
        data = {"monitorIds": monitor_ids}
        return self._make_request('DELETE', 'MonitorRestEndpoints/monitor', json=data)
    
    def get_event_list(self, limit: int = 100, start_date: Optional[str] = None,
                      end_date: Optional[str] = None, facility_id: Optional[str] = None,
                      priority: Optional[int] = None, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get event list
        
        Args:
            limit: Maximum number of events to retrieve (default: 100)
            start_date: Start date filter (YYYY-MM-DD format)
            end_date: End date filter (YYYY-MM-DD format)
            facility_id: Facility ID filter
            priority: Priority filter
            owner_role_id: Owner role ID filter
            
        Returns:
            Event list data
        """
        params = {"limit": limit}
        
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
        if facility_id:
            params['facilityId'] = facility_id
        if priority is not None:
            params['priority'] = priority
        if owner_role_id:
            params['ownerRoleId'] = owner_role_id
        
        return self._make_request('GET', 'EventRestEndpoints/event', params=params)
    
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