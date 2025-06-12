from typing import Optional, Dict, Any
from .base import BaseClient

class CollectClient(BaseClient):

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