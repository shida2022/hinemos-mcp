from typing import Dict, Any, List, Optional
from .base import BaseClient

class JobClient(BaseClient):
    """
    Hinemos 7.1 ジョブ管理 REST API クライアント
    仕様: spec/hinemos_job_api_spec.md を参照
    """
    NAME = 'JobRestEndpoints'
    # --- 1. ジョブツリー管理 ---
    def get_job_tree_simple(self, ownerRoleId: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if ownerRoleId:
            params["ownerRoleId"] = ownerRoleId
        return self._make_request('GET', self.NAME + '/job/setting/job_treeSimple', params=params)

    def get_job_tree_full(self, ownerRoleId: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if ownerRoleId:
            params["ownerRoleId"] = ownerRoleId
        return self._make_request('GET', self.NAME + '/job/setting/job_treeFull', params=params)

    def get_job_info(self, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/job_info/jobunit/{jobunitId}/job/{jobId}')

    def get_job_info_bulk(self, jobList: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        body = {"jobList": jobList}
        return self._make_request('POST', self.NAME + '/job/setting/job_info_search', json=body)

    # --- 2. ジョブユニット管理 ---
    def add_jobunit(self, jobunit: Dict[str, Any], isClient: bool = False) -> Dict[str, Any]:
        params = {"isClient": isClient}
        return self._make_request('POST', self.NAME + '/job/setting/jobunit', params=params, json=jobunit)

    def modify_jobunit(self, jobunitId: str, jobunit: Dict[str, Any], isClient: bool = False) -> Dict[str, Any]:
        params = {"isClient": isClient}
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}', params=params, json=jobunit)

    def delete_jobunit(self, jobunitId: str) -> Dict[str, Any]:
        return self._make_request('DELETE', self.NAME + f'/job/setting/jobunit/{jobunitId}')

    # --- 3. 編集ロック管理 ---
    def get_edit_lock(self, jobunitId: str, updateTime: str, forceFlag: bool) -> Dict[str, Any]:
        body = {"updateTime": updateTime, "forceFlag": forceFlag}
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/lock', json=body)

    def check_edit_lock(self, jobunitId: str, editSession: int) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/jobunit/{jobunitId}/lock/{editSession}')

    def release_edit_lock(self, jobunitId: str, editSession: int) -> Dict[str, Any]:
        return self._make_request('DELETE', self.NAME + f'/job/setting/jobunit/{jobunitId}/lock/{editSession}')

    # --- 4. ジョブ設定管理（全ジョブタイプ追加API） ---
    def add_jobnet(self, jobunitId: str, jobnet: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/jobnet', json=jobnet)

    def add_command_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/commandJob', json=job)

    def add_file_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/fileJob', json=job)

    def add_refer_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/referJob', json=job)

    def add_monitor_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/monitorJob', json=job)

    def add_approval_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/approvalJob', json=job)

    def add_joblinksend_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/joblinksendJob', json=job)

    def add_joblinkrcv_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/joblinkrcvJob', json=job)

    def add_filecheck_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/filecheckJob', json=job)

    def add_rpa_job(self, jobunitId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/setting/jobunit/{jobunitId}/rpaJob', json=job)

    def delete_job(self, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('DELETE', self.NAME + f'/job/setting/jobunit/{jobunitId}/job/{jobId}')

    # --- 5. ジョブ実行制御 ---
    def run_job(self, jobunitId: str, jobId: str, runJobRequest: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/session_exec/jobunit/{jobunitId}/job/{jobId}', json=runJobRequest)

    def run_job_kick(self, jobKickId: str, runJobKickRequest: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/session_exec/kick/{jobKickId}', json=runJobKickRequest)

    def session_job_operation(self, sessionId: str, jobunitId: str, jobId: str, operation: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/sessionJob_operation/{sessionId}/jobunit/{jobunitId}/job/{jobId}', json=operation)

    def session_node_operation(self, sessionId: str, jobunitId: str, jobId: str, facilityId: str, operation: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + f'/job/sessionNode_operation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facilityId/{facilityId}', json=operation)

    # --- 6. ジョブセッション監視 ---
    def get_session_job_detail(self, sessionId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/sessionJob_detail/{sessionId}')

    def get_session_node_detail(self, sessionId: str, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/sessionNode_detail/{sessionId}/jobunit/{jobunitId}/job/{jobId}')

    def get_session_file_detail(self, sessionId: str, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/sessionFile_detail/{sessionId}/jobunit/{jobunitId}/job/{jobId}')

    def get_session_job_jobInfo(self, sessionId: str, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/sessionJob_jobInfo/{sessionId}/jobunit/{jobunitId}/job/{jobId}')

    def get_session_job_allDetail(self, sessionId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/sessionJob_allDetail/{sessionId}')

    # --- 7. ジョブ履歴管理 ---
    def history_search(self, size: int, filter: Dict[str, Any]) -> Dict[str, Any]:
        body = {"size": size, "filter": filter}
        return self._make_request('POST', self.NAME + '/job/history_search', json=body)

    # --- 8. ジョブキック管理 ---
    def add_schedule(self, schedule: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/kick/schedule', json=schedule)

    def add_filecheck(self, filecheck: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/kick/filecheck', json=filecheck)

    def add_manual(self, manual: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/kick/manual', json=manual)

    def add_joblinkrcv(self, joblinkrcv: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/kick/joblinkrcv', json=joblinkrcv)

    def get_kick_list(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', self.NAME + '/job/setting/kick')

    def kick_search(self, condition: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/kick_search', json=condition)

    def set_kick_valid(self, setStatus: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._make_request('PUT', self.NAME + '/job/setting/kick_valid', json=setStatus)

    def delete_kick(self, jobkickIds: str) -> List[Dict[str, Any]]:
        params = {"jobkickIds": jobkickIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/kick', params=params)

    # --- 9. ジョブ承認管理 ---
    def session_approval_search(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._make_request('POST', self.NAME + '/job/session_approval_search', json=request)

    def modify_approval_info(self, sessionId: str, jobunitId: str, jobId: str, info: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/session_approval/{sessionId}/jobunit/{jobunitId}/job/{jobId}', json=info)

    # --- 10. ジョブキュー管理 ---
    def get_queue_list(self, roleId: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if roleId:
            params["roleId"] = roleId
        return self._make_request('GET', self.NAME + '/job/setting/queue', params=params)

    def get_queue_detail(self, queueId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/queue/{queueId}')

    def add_queue(self, queue: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/queue', json=queue)

    def modify_queue(self, queueId: str, queue: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/queue/{queueId}', json=queue)

    def delete_queue(self, queueIds: str) -> List[Dict[str, Any]]:
        params = {"queueIds": queueIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/queue', params=params)

    def queue_activity_search(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._make_request('POST', self.NAME + '/job/queueActivity_search', json=request)

    def queue_activity_detail(self, queueId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/queueActivity_detail/{queueId}')

    # --- 11. ジョブ連携送信設定 ---
    def get_joblinksend_setting_list(self, ownerRoleId: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if ownerRoleId:
            params["ownerRoleId"] = ownerRoleId
        return self._make_request('GET', self.NAME + '/job/joblinksend_setting', params=params)

    def get_joblinksend_setting_detail(self, joblinkSendSettingId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/joblinksend_setting/{joblinkSendSettingId}')

    def add_joblinksend_setting(self, setting: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/joblinksend_setting', json=setting)

    def modify_joblinksend_setting(self, joblinkSendSettingId: str, setting: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/joblinksend_setting/{joblinkSendSettingId}', json=setting)

    def delete_joblinksend_setting(self, joblinkSendSettingIds: str) -> List[Dict[str, Any]]:
        params = {"joblinkSendSettingIds": joblinkSendSettingIds}
        return self._make_request('DELETE', self.NAME + '/job/joblinksend_setting', params=params)

    # --- 12. ジョブ連携メッセージ管理 ---
    def regist_joblink_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/joblink_message', json=message)

    def send_joblink_message_manual(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/joblink_message_manual', json=message)

    def joblink_message_search(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/joblink_message_search', json=request)

    # --- 13. 操作権限確認 ---
    def available_start_operation(self, sessionId: str, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/operationProp_availableStartOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}')

    def available_start_operation_node(self, sessionId: str, jobunitId: str, jobId: str, facilityId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/operationProp_availableStartOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}')

    def available_stop_operation(self, sessionId: str, jobunitId: str, jobId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/operationProp_availableStopOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}')

    def available_stop_operation_node(self, sessionId: str, jobunitId: str, jobId: str, facilityId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/operationProp_availableStopOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}')

    # --- 14. RPAシナリオジョブ管理 ---
    def get_rpa_login_resolution(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', self.NAME + '/job/setting/rpa_login_resolution')

    def get_rpa_screenshot(self, sessionId: str, jobunitId: str, jobId: str, facilityId: str) -> List[Dict[str, Any]]:
        return self._make_request('GET', self.NAME + f'/job/sessionNode_operation/screenshot/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}')

    def get_rpa_screenshot_file(self, sessionId: str, jobunitId: str, jobId: str, facilityId: str, regDate: str) -> bytes:
        return self._make_request('GET', self.NAME + f'/job/sessionNode_operation/screenshot_file/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}/regdate/{regDate}', stream=True)

    # --- 15. その他 ---
    def get_jobmap_icon_image_iconId(self, ownerRoleId: Optional[str] = None) -> Dict[str, Any]:
        params = {}
        if ownerRoleId:
            params["ownerRoleId"] = ownerRoleId
        return self._make_request('GET', self.NAME + '/job/jobmap/iconImage_iconId', params=params)

    def delete_premakejobsession(self, jobkickId: str) -> Dict[str, Any]:
        params = {"jobkickId": jobkickId}
        return self._make_request('DELETE', self.NAME + '/job/setting/premakejobsession', params=params)

    def get_schedule_plan(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self._make_request('POST', self.NAME + '/job/setting/kick/schedule_plan', json=plan)

    def get_job_referrer_queue(self, queueId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/job_referrerQueue/{queueId}')

    def queue_search(self, search: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', self.NAME + '/job/setting/queue_search', json=search)

    # --- 16. ジョブ更新API（各ジョブタイプ） ---
    def modify_jobnet(self, jobunitId: str, jobId: str, jobnet: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/jobnet/{jobId}', json=jobnet)

    def modify_command_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/commandJob/{jobId}', json=job)

    def modify_file_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/fileJob/{jobId}', json=job)

    def modify_refer_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/referJob/{jobId}', json=job)

    def modify_monitor_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/monitorJob/{jobId}', json=job)

    def modify_approval_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/approvalJob/{jobId}', json=job)

    def modify_joblinksend_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/joblinkSendJob/{jobId}', json=job)

    def modify_joblinkrcv_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/joblinkRcvJob/{jobId}', json=job)

    def modify_filecheck_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/filecheckJob/{jobId}', json=job)

    def modify_rpa_job(self, jobunitId: str, jobId: str, job: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/jobunit/{jobunitId}/rpaJob/{jobId}', json=job)

    # --- 17. ジョブキック詳細取得・更新 ---
    def get_schedule_detail(self, jobKickId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/kick/schedule/{jobKickId}')

    def get_filecheck_detail(self, jobKickId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/kick/filecheck/{jobKickId}')

    def get_manual_detail(self, jobKickId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/kick/manual/{jobKickId}')

    def get_joblinkrcv_detail(self, jobKickId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/kick/joblinkrcv/{jobKickId}')

    def get_kick_detail(self, jobKickId: str) -> Dict[str, Any]:
        return self._make_request('GET', self.NAME + f'/job/setting/kick/{jobKickId}')

    def modify_schedule(self, jobKickId: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/kick/schedule/{jobKickId}', json=schedule)

    def modify_filecheck(self, jobKickId: str, filecheck: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/kick/filecheck/{jobKickId}', json=filecheck)

    def modify_manual(self, jobKickId: str, manual: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/kick/manual/{jobKickId}', json=manual)

    def modify_joblinkrcv(self, jobKickId: str, joblinkrcv: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', self.NAME + f'/job/setting/kick/joblinkrcv/{jobKickId}', json=joblinkrcv)

    # --- 18. ジョブキック削除API（タイプ別） ---
    def delete_schedule(self, jobkickIds: str) -> List[Dict[str, Any]]:
        params = {"jobkickIds": jobkickIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/kick/schedule', params=params)

    def delete_filecheck(self, jobkickIds: str) -> List[Dict[str, Any]]:
        params = {"jobkickIds": jobkickIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/kick/filecheck', params=params)

    def delete_manual(self, jobkickIds: str) -> List[Dict[str, Any]]:
        params = {"jobkickIds": jobkickIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/kick/manual', params=params)

    def delete_joblinkrcv(self, jobkickIds: str) -> List[Dict[str, Any]]:
        params = {"jobkickIds": jobkickIds}
        return self._make_request('DELETE', self.NAME + '/job/setting/kick/joblinkrcv', params=params)