from typing import Optional, Dict, Any
from .base import BaseClient

class JobClient(BaseClient):

    def get_job_tree(self, owner_role_id: Optional[str] = None, tree_only: Optional[bool] = None, locale: Optional[str] = None) -> Dict[str, Any]:
        """
        ジョブツリー取得API (/jobmanagement/jobTree)
        Args:
            owner_role_id: オーナーロールID (任意)
            tree_only: ツリー構造のみ取得するか (任意)
            locale: ロケール (任意)
        Returns:
            ジョブツリー情報
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        if tree_only is not None:
            params["treeOnly"] = str(tree_only).lower()
        if locale:
            params["locale"] = locale
        return self._make_request('GET', 'jobmanagement/jobTree', params=params)

    def get_job_detail(self, jobunit_id: str, job_id: str) -> Dict[str, Any]:
        """
        ジョブ詳細情報取得API (/jobmanagement/job/{jobunitId}/{jobId})
        Args:
            jobunit_id: ジョブユニットID
            job_id: ジョブID
        Returns:
            ジョブ詳細情報
        """
        endpoint = f"jobmanagement/job/{jobunit_id}/{job_id}"
        return self._make_request('GET', endpoint)

    def run_job(self, jobunit_id: str, job_id: str, trigger_type: int = 1, trigger_info: str = "API実行", job_variable_list: Optional[list] = None) -> Dict[str, Any]:
        """
        ジョブ実行API (/jobmanagement/job/run)
        Args:
            jobunit_id: ジョブユニットID
            job_id: ジョブID
            trigger_type: トリガー種別 (デフォルト: 1)
            trigger_info: トリガー情報 (デフォルト: "API実行")
            job_variable_list: ジョブ変数リスト (例: [{"name": "PARAM1", "value": "value1"}])
        Returns:
            実行結果（セッションID等）
        """
        data = {
            "jobunitId": jobunit_id,
            "jobId": job_id,
            "triggerType": trigger_type,
            "triggerInfo": trigger_info
        }
        if job_variable_list is not None:
            data["jobVariableList"] = job_variable_list
        return self._make_request('POST', 'jobmanagement/job/run', json=data)

    def get_job_history(self, owner_role_id: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None,
                        jobunit_id: Optional[str] = None, job_id: Optional[str] = None, status: Optional[int] = None,
                        limit: Optional[int] = None) -> Dict[str, Any]:
        """
        ジョブ履歴取得API (/jobmanagement/jobHistory)
        Args:
            owner_role_id: オーナーロールIDフィルタ (任意)
            from_date: 開始日時(YYYY-MM-DD HH:MM:SS) (任意)
            to_date: 終了日時(YYYY-MM-DD HH:MM:SS) (任意)
            jobunit_id: ジョブユニットID (任意)
            job_id: ジョブID (任意)
            status: 実行状態 (任意)
            limit: 取得件数上限 (任意)
        Returns:
            ジョブ履歴リスト
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if jobunit_id:
            params["jobunitId"] = jobunit_id
        if job_id:
            params["jobId"] = job_id
        if status is not None:
            params["status"] = str(status)
        if limit is not None:
            params["limit"] = str(limit)
        return self._make_request('GET', 'jobmanagement/jobHistory', params=params)

    def operate_job(self, session_id: str, jobunit_id: str, job_id: str, facility_id: str, control: int, end_value: Optional[int] = None) -> Dict[str, Any]:
        """
        ジョブ操作API (/jobmanagement/job/operation)
        Args:
            session_id: セッションID
            jobunit_id: ジョブユニットID
            job_id: ジョブID
            facility_id: ファシリティID
            control: 操作種別 (1:開始, 2:停止, 3:強制停止, 4:中断, 5:再実行)
            end_value: 終了値 (任意)
        Returns:
            操作結果
        """
        data = {
            "sessionId": session_id,
            "jobunitId": jobunit_id,
            "jobId": job_id,
            "facilityId": facility_id,
            "control": control
        }
        if end_value is not None:
            data["endValue"] = end_value
        return self._make_request('POST', 'jobmanagement/job/operation', json=data)

    def create_job(self, job_info: dict) -> Dict[str, Any]:
        """
        ジョブ作成API (/jobmanagement/job)
        Args:
            job_info: ジョブ情報(dict)
        Returns:
            作成結果
        """
        data = {"jobInfo": job_info}
        return self._make_request('POST', 'jobmanagement/job', json=data)

    def update_job(self, jobunit_id: str, job_id: str, job_info: dict) -> Dict[str, Any]:
        """
        ジョブ更新API (/jobmanagement/job/{jobunitId}/{jobId})
        Args:
            jobunit_id: ジョブユニットID
            job_id: ジョブID
            job_info: ジョブ情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"jobmanagement/job/{jobunit_id}/{job_id}"
        data = {"jobInfo": job_info}
        return self._make_request('PUT', endpoint, json=data)

    def delete_job(self, jobunit_id: str, job_id: str) -> Dict[str, Any]:
        """
        ジョブ削除API (/jobmanagement/job/{jobunitId}/{jobId})
        Args:
            jobunit_id: ジョブユニットID
            job_id: ジョブID
        Returns:
            削除結果
        """
        endpoint = f"jobmanagement/job/{jobunit_id}/{job_id}"
        return self._make_request('DELETE', endpoint)

    def get_job_kick_list(self) -> Dict[str, Any]:
        """
        ジョブキック一覧取得API (/jobmanagement/jobKick)
        Returns:
            ジョブキック一覧
        """
        return self._make_request('GET', 'jobmanagement/jobKick')

    def create_job_kick(self, job_kick_info: dict) -> Dict[str, Any]:
        """
        ジョブキック作成API (/jobmanagement/jobKick)
        Args:
            job_kick_info: ジョブキック情報(dict)
        Returns:
            作成結果
        """
        return self._make_request('POST', 'jobmanagement/jobKick', json=job_kick_info)

    def update_job_kick(self, job_kick_id: str, job_kick_info: dict) -> Dict[str, Any]:
        """
        ジョブキック更新API (/jobmanagement/jobKick/{jobKickId})
        Args:
            job_kick_id: ジョブキックID
            job_kick_info: ジョブキック情報(dict)
        Returns:
            更新結果
        """
        endpoint = f"jobmanagement/jobKick/{job_kick_id}"
        return self._make_request('PUT', endpoint, json=job_kick_info)

    def delete_job_kick(self, job_kick_id: str) -> Dict[str, Any]:
        """
        ジョブキック削除API (/jobmanagement/jobKick/{jobKickId})
        Args:
            job_kick_id: ジョブキックID
        Returns:
            削除結果
        """
        endpoint = f"jobmanagement/jobKick/{job_kick_id}"
        return self._make_request('DELETE', endpoint)