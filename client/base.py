import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class BaseClient:
    def __init__(self, base_url: Optional[str] = None):
        if base_url is None:
            base_url = os.getenv("HINEMOS_ENDPOINT", "http://localhost:8080")
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token_id: Optional[str] = None
        self.token_expiration: Optional[datetime] = None
        self.logger = logging.getLogger(__name__)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def login(self, user_id: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        if user_id is None:
            user_id = os.getenv("HINEMOS_USERNAME", "")
        if password is None:
            password = os.getenv("HINEMOS_PASSWORD", "")
        login_url = f"{self.base_url}/HinemosWeb/api/AccessRestEndpoints/access/login"
        login_data = {"userId": user_id, "password": password}
        response = self.session.post(login_url, json=login_data)
        response.raise_for_status()
        login_response = response.json()
        token_info = login_response.get('token', {})
        self.token_id = token_info.get('tokenId')
        expiration_str = token_info.get('expirationDate')
        if expiration_str:
            self.token_expiration = datetime.strptime(expiration_str, "%Y-%m-%d %H:%M:%S.%f")
        if self.token_id:
            self.session.headers.update({'Authorization': f'Bearer {self.token_id}'})
        return login_response

    def is_token_valid(self) -> bool:
        if not self.token_id or not self.token_expiration:
            return False
        return datetime.now() < (self.token_expiration - timedelta(minutes=5))

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        logging.info(f"Making {method} request to {endpoint} with params: {kwargs.get('params', {})} and data: {kwargs.get('json', {})}")
        if not self.is_token_valid():
            self.login()
            if not self.is_token_valid():
                raise ValueError("Token is invalid or expired. Please login again.")
        url = f"{self.base_url}/HinemosWeb/api/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def logout(self) -> None:
        self.token_id = None
        self.token_expiration = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()