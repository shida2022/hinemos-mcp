from typing import Dict, Any, List, Optional
from .base import BaseClient

class MonitorResultClient(BaseClient):
    """
    Hinemos 7.1 監視結果 REST API クライアント
    仕様: spec/hinemos_monitor_result_api_spec.md を参照
    """

    def event_search(self, filter: Dict[str, Any], size: Optional[int] = None) -> Dict[str, Any]:
        """
        イベント一覧検索
        POST /monitorresult/event_search
        """
        body = {"filter": filter}
        if size is not None:
            body["size"] = size
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/event_search', json=body)

    def scope_list(
        self,
        facility_id: Optional[str] = None,
        status_flag: Optional[bool] = None,
        event_flag: Optional[bool] = None,
        order_flg: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        スコープ一覧取得
        GET /monitorresult/scope
        """
        params = {}
        if facility_id is not None:
            params["facilityId"] = facility_id
        if status_flag is not None:
            params["statusFlag"] = status_flag
        if event_flag is not None:
            params["eventFlag"] = event_flag
        if order_flg is not None:
            params["orderFlg"] = order_flg
        return self._make_request('GET', 'MonitorResultRestEndpoints/monitorresult/scope', params=params)

    def status_search(self, filter: Dict[str, Any], size: Optional[int] = None) -> Dict[str, Any]:
        """
        ステータス一覧検索
        POST /monitorresult/status_search
        """
        body = {"filter": filter}
        if size is not None:
            body["size"] = size
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/status_search', json=body)

    def status_delete(self, status_data_info_request_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        ステータス削除
        POST /monitorresult/status_delete
        """
        body = {"statusDataInfoRequestlist": status_data_info_request_list}
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/status_delete', json=body)

    def event_download(
        self,
        filter: Dict[str, Any],
        selected_events: Optional[List[Dict[str, Any]]] = None,
        filename: Optional[str] = None
    ) -> bytes:
        """
        イベントファイルダウンロード
        POST /monitorresult/event_download
        """
        body = {"filter": filter}
        if selected_events is not None:
            body["selectedEvents"] = selected_events
        if filename is not None:
            body["filename"] = filename
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/event_download', json=body, stream=True)

    def event_detail_search(
        self,
        monitorId: str,
        monitorDetailId: str,
        pluginId: str,
        facilityId: str,
        outputDate: str
    ) -> Dict[str, Any]:
        """
        イベント詳細検索
        POST /monitorresult/event_detail_search
        """
        body = {
            "monitorId": monitorId,
            "monitorDetailId": monitorDetailId,
            "pluginId": pluginId,
            "facilityId": facilityId,
            "outputDate": outputDate
        }
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/event_detail_search', json=body)

    def event_comment(
        self,
        monitorId: str,
        monitorDetailId: str,
        pluginId: str,
        facilityId: str,
        outputDate: str,
        comment: str,
        commentDate: str,
        commentUser: str
    ) -> Dict[str, Any]:
        """
        イベントコメント更新
        PUT /monitorresult/event_comment
        """
        body = {
            "monitorId": monitorId,
            "monitorDetailId": monitorDetailId,
            "pluginId": pluginId,
            "facilityId": facilityId,
            "outputDate": outputDate,
            "comment": comment,
            "commentDate": commentDate,
            "commentUser": commentUser
        }
        return self._make_request('PUT', 'MonitorResultRestEndpoints/monitorresult/event_comment', json=body)

    def event_confirm(
        self,
        list_: List[Dict[str, Any]],
        confirmType: int
    ) -> List[Dict[str, Any]]:
        """
        イベント確認状態更新
        PUT /monitorresult/event_confirm
        """
        body = {
            "list": list_,
            "confirmType": confirmType
        }
        return self._make_request('PUT', 'MonitorResultRestEndpoints/monitorresult/event_confirm', json=body)

    def event_multiConfirm(
        self,
        confirmType: int,
        filter: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        イベント一括確認更新
        PUT /monitorresult/event_multiConfirm
        """
        body = {
            "confirmType": confirmType,
            "filter": filter
        }
        return self._make_request('PUT', 'MonitorResultRestEndpoints/monitorresult/event_multiConfirm', json=body)

    def event_collectGraphFlg(
        self,
        list_: List[Dict[str, Any]],
        collectGraphFlg: bool
    ) -> List[Dict[str, Any]]:
        """
        性能グラフフラグ更新
        PUT /monitorresult/event_collectGraphFlg
        """
        body = {
            "list": list_,
            "collectGraphFlg": collectGraphFlg
        }
        return self._make_request('PUT', 'MonitorResultRestEndpoints/monitorresult/event_collectGraphFlg', json=body)

    def event_update(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        イベント情報更新
        PUT /monitorresult/event
        """
        body = {"info": info}
        return self._make_request('PUT', 'MonitorResultRestEndpoints/monitorresult/event', json=body)

    def eventCustomCommand_exec(
        self,
        commandNo: int,
        eventList: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        イベントカスタムコマンド実行
        POST /monitorresult/eventCustomCommand_exec
        """
        body = {
            "commandNo": commandNo,
            "eventList": eventList
        }
        return self._make_request('POST', 'MonitorResultRestEndpoints/monitorresult/eventCustomCommand_exec', json=body)

    def eventCustomCommand_result(self, uuid: str) -> Dict[str, Any]:
        """
        イベントカスタムコマンド結果取得
        GET /monitorresult/eventCustomCommand/{uuid}
        """
        endpoint = f"MonitorResultRestEndpoints/monitorresult/eventCustomCommand/{uuid}"
        return self._make_request('GET', endpoint)

    def event_collectValid_mapKeyFacility(self, facilityIdList: Optional[str] = None) -> Dict[str, Any]:
        """
        イベントデータマップ取得
        GET /monitorresult/event_collectValid_mapKeyFacility
        """
        params = {}
        if facilityIdList is not None:
            params["facilityIdList"] = facilityIdList
        return self._make_request('GET', 'MonitorResultRestEndpoints/monitorresult/event_collectValid_mapKeyFacility', params=params)