# Hinemosジョブ管理API仕様書

## 概要
Hinemosジョブ管理APIは、ジョブの設定、実行、監視、スケジューリングなどの包括的なジョブ管理機能を提供するREST APIです。

## ベースURL
```
/job
```

## 認証・認可
- **権限**: JobManagement機能のシステム権限が必要
- **権限モード**: READ, ADD, MODIFY, EXEC, APPROVAL
- **認証**: Bearerトークン認証

---

## 1. ジョブツリー管理

### 1.1 ジョブツリー情報取得（簡易版）
**GET** `/setting/job_treeSimple`

ジョブツリーの基本情報を取得します。

**権限**: JobManagement READ

**クエリパラメータ**:
- `ownerRoleId` (string): オーナーロールID

**レスポンス**: `JobTreeItemResponseP1`

### 1.2 ジョブツリー情報取得（完全版）
**GET** `/setting/job_treeFull`

ジョブツリーの詳細情報を取得します。

**権限**: JobManagement READ

**クエリパラメータ**:
- `ownerRoleId` (string): オーナーロールID

**レスポンス**: `JobTreeItemResponseP2`

### 1.3 ジョブ詳細情報取得
**GET** `/setting/job_info/jobunit/{jobunitId}/job/{jobId}`

指定されたジョブの詳細情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobInfoResponse`

### 1.4 ジョブ情報一括取得
**POST** `/setting/job_info_search`

複数のジョブの詳細情報を一括取得します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobFullListRequest`
```json
{
  "jobList": [
    {
      "jobunitId": "string",
      "id": "string"
    }
  ]
}
```

**レスポンス**: `JobInfoResponse[]`

---

## 2. ジョブユニット管理

### 2.1 ジョブユニット登録
**POST** `/setting/jobunit`

新しいジョブユニットを登録します。

**権限**: JobManagement READ, ADD

**クエリパラメータ**:
- `isClient` (boolean, default: false): クライアント用モード

**リクエストボディ**: `RegisterJobunitRequest`

**レスポンス**: `JobTreeItemResponseP2`

### 2.2 ジョブユニット更新
**PUT** `/setting/jobunit/{jobunitId}`

既存のジョブユニットを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**クエリパラメータ**:
- `isClient` (boolean, default: false): クライアント用モード

**リクエストボディ**: `ReplaceJobunitRequest`

**レスポンス**: `JobTreeItemResponseP2`

### 2.3 ジョブユニット削除
**DELETE** `/setting/jobunit/{jobunitId}`

指定されたジョブユニットを削除します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**レスポンス**: `JobTreeItemResponseP2`

---

## 3. 編集ロック管理

### 3.1 編集ロック取得
**POST** `/setting/jobunit/{jobunitId}/lock`

ジョブユニットの編集ロックを取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `GetEditLockRequest`
```json
{
  "updateTime": "string",
  "forceFlag": "boolean"
}
```

**レスポンス**: `EditLockResponse`

### 3.2 編集ロック確認
**GET** `/setting/jobunit/{jobunitId}/lock/{editSession}`

編集ロックの有効性を確認します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `editSession` (integer): セッションID

**レスポンス**: `EditLockResponse`

### 3.3 編集ロック解放
**DELETE** `/setting/jobunit/{jobunitId}/lock/{editSession}`

編集ロックを解放します。

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `editSession` (integer): セッションID

---

## 4. ジョブ設定管理

### 4.1 ジョブネット追加
**POST** `/setting/jobunit/{jobunitId}/jobnet`

ジョブネットを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddJobnetRequest`

**レスポンス**: `JobnetInfoResponse`

### 4.2 コマンドジョブ追加
**POST** `/setting/jobunit/{jobunitId}/commandJob`

コマンドジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddCommandJobRequest`

**レスポンス**: `CommandJobInfoResponse`

### 4.3 ファイル転送ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/fileJob`

ファイル転送ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddFileTransferJobRequest`

**レスポンス**: `FileJobInfoResponse`

### 4.4 参照ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/referJob`

参照ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddReferJobRequest`

**レスポンス**: `ReferJobInfoResponse`

### 4.5 監視ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/monitorJob`

監視ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddMonitorJobRequest`

**レスポンス**: `MonitorJobInfoResponse`

### 4.6 承認ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/approvalJob`

承認ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddApprovalJobRequest`

**レスポンス**: `ApprovalJobInfoResponse`

### 4.7 ジョブ連携送信ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/joblinksendJob`

ジョブ連携送信ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddJobLinkSendJobRequest`

**レスポンス**: `JobLinkSendJobInfoResponse`

### 4.8 ジョブ連携待機ジョブ追加
**POST** `/setting/jobunit/{jobunitId}/joblinkrcvJob`

ジョブ連携待機ジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddJobLinkRcvJobRequest`

**レスポンス**: `JobLinkRcvJobInfoResponse`

### 4.9 ファイルチェックジョブ追加
**POST** `/setting/jobunit/{jobunitId}/filecheckJob`

ファイルチェックジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddFileCheckJobRequest`

**レスポンス**: `FileCheckJobInfoResponse`

### 4.10 RPAシナリオジョブ追加
**POST** `/setting/jobunit/{jobunitId}/rpaJob`

RPAシナリオジョブを追加します。

**権限**: JobManagement READ, ADD

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID

**リクエストボディ**: `AddRpaJobRequest`

**レスポンス**: `RpaJobInfoResponse`

### 4.11 ジョブ削除
**DELETE** `/setting/jobunit/{jobunitId}/job/{jobId}`

指定されたジョブを削除します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobInfoResponseP1`

---

## 5. ジョブ実行制御

### 5.1 ジョブ実行
**POST** `/session_exec/jobunit/{jobunitId}/job/{jobId}`

指定されたジョブを実行します。

**権限**: JobManagement EXEC, READ

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `RunJobRequest`
```json
{
  "jobWaitTime": "boolean",
  "jobWaitMinute": "boolean",
  "jobCommand": "boolean",
  "jobRuntimeParamList": [
    {
      "paramId": "string",
      "paramType": "integer",
      "value": "string"
    }
  ]
}
```

**レスポンス**: `RunJobResponse`

### 5.2 ジョブキック実行
**POST** `/session_exec/kick/{jobKickId}`

ジョブ実行契機を直接実行します。

**権限**: JobManagement EXEC, MODIFY, READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**リクエストボディ**: `RunJobKickRequest`

**レスポンス**: `RunJobResponse`

### 5.3 セッションジョブ操作
**POST** `/sessionJob_operation/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

実行中のジョブに対して操作を行います。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `JobOperationRequest`
```json
{
  "control": "string",
  "endStatus": "integer",
  "endValue": "integer"
}
```

### 5.4 セッションノード操作
**POST** `/sessionNode_operation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facilityId/{facilityId}`

実行中のジョブの特定ノードに対して操作を行います。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID
- `facilityId` (string): ファシリティID

**リクエストボディ**: `JobOperationRequest`

---

## 6. ジョブセッション監視

### 6.1 ジョブ詳細一覧取得
**GET** `/sessionJob_detail/{sessionId}`

セッションジョブの詳細一覧を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID

**レスポンス**: `JobTreeItemResponseP4`

### 6.2 ノード詳細一覧取得
**GET** `/sessionNode_detail/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

ノードの詳細一覧を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobNodeDetailResponse[]`

### 6.3 ファイル転送一覧取得
**GET** `/sessionFile_detail/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

ファイル転送の詳細一覧を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobForwardFileResponse[]`

### 6.4 セッションジョブ情報取得
**GET** `/sessionJob_jobInfo/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

セッションジョブの情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobTreeItemResponseP3`

### 6.5 セッションジョブ全詳細取得
**GET** `/sessionJob_allDetail/{sessionId}`

セッションジョブの全詳細情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID

**レスポンス**: `JobSessionJobDetailResponse`

---

## 7. ジョブ履歴管理

### 7.1 ジョブ履歴一覧取得
**POST** `/history_search`

ジョブの実行履歴を検索・取得します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobHistoryListRequest`
```json
{
  "size": "integer",
  "filter": {
    "sessionId": "string",
    "jobunitId": "string",
    "jobId": "string",
    "startFromDate": "string",
    "startToDate": "string",
    "endFromDate": "string",
    "endToDate": "string",
    "status": "integer",
    "endStatus": "integer",
    "triggerType": "integer",
    "ownerRoleId": "string"
  }
}
```

**レスポンス**: `GetJobHistoryListResponse`

---

## 8. ジョブキック管理（実行契機）

### 8.1 スケジュール追加
**POST** `/setting/kick/schedule`

スケジュール実行契機を追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddScheduleRequest`
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "jobunitId": "string",
  "jobId": "string",
  "valid": "boolean",
  "ownerRoleId": "string",
  "calendarId": "string",
  "scheduleType": "integer",
  "week": "integer",
  "hour": "integer",
  "minute": "integer"
}
```

**レスポンス**: `JobKickResponse`

### 8.2 ファイルチェック追加
**POST** `/setting/kick/filecheck`

ファイルチェック実行契機を追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddFileCheckRequest`

**レスポンス**: `JobKickResponse`

### 8.3 手動実行契機追加
**POST** `/setting/kick/manual`

手動実行契機を追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddJobManualRequest`

**レスポンス**: `JobKickResponse`

### 8.4 ジョブ連携受信契機追加
**POST** `/setting/kick/joblinkrcv`

ジョブ連携受信契機を追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddJobLinkRcvRequest`

**レスポンス**: `JobKickResponse`

### 8.5 ジョブキック一覧取得
**GET** `/setting/kick`

すべてのジョブ実行契機の一覧を取得します。

**権限**: JobManagement READ

**レスポンス**: `JobKickResponse[]`

### 8.6 条件付きジョブキック検索
**POST** `/setting/kick_search`

条件を指定してジョブ実行契機を検索します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobKickListByConditionRequest`

**レスポンス**: `GetJobKickListByConditionResponse`

### 8.7 ジョブキック状態変更
**PUT** `/setting/kick_valid`

ジョブ実行契機の有効/無効状態を変更します。

**権限**: JobManagement READ, MODIFY

**リクエストボディ**: `SetJobKickStatusRequest`
```json
{
  "jobKickId": ["string"],
  "validFlag": "boolean"
}
```

**レスポンス**: `JobKickResponse[]`

### 8.8 ジョブキック削除
**DELETE** `/setting/kick`

ジョブ実行契機を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickIds` (string): カンマ区切りのジョブキックIDリスト

**レスポンス**: `JobKickResponse[]`

---

## 9. ジョブ承認管理

### 9.1 承認対象ジョブ一覧取得
**POST** `/session_approval_search`

承認が必要なジョブの一覧を取得します。

**権限**: JobManagement READ

**リクエストボディ**: `GetApprovalJobListRequest`
```json
{
  "size": "integer",
  "sessionId": "string",
  "jobunitId": "string",
  "jobId": "string",
  "targetStatusList": ["PENDING", "APPROVED", "REJECTED"],
  "requestUser": "string",
  "approvalUser": "string"
}
```

**レスポンス**: `JobApprovalInfoResponse[]`

### 9.2 承認情報更新
**PUT** `/session_approval/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

ジョブの承認状態を更新します。

**権限**: JobManagement READ, APPROVAL

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyApprovalInfoRequest`
```json
{
  "result": "integer",
  "comment": "string"
}
```

**レスポンス**: `JobApprovalInfoResponse`

---

## 10. ジョブキュー管理

### 10.1 ジョブキュー一覧取得
**GET** `/setting/queue`

ジョブキューの一覧を取得します。

**権限**: JobManagement READ

**クエリパラメータ**:
- `roleId` (string): ロールID

**レスポンス**: `JobQueueResponse[]`

### 10.2 ジョブキュー詳細取得
**GET** `/setting/queue/{queueId}`

指定されたジョブキューの詳細情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `queueId` (string): キューID

**レスポンス**: `JobQueueResponse`

### 10.3 ジョブキュー追加
**POST** `/setting/queue`

新しいジョブキューを追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddJobQueueRequest`
```json
{
  "queueId": "string",
  "name": "string",
  "concurrency": "integer",
  "ownerRoleId": "string"
}
```

**レスポンス**: `JobQueueResponse`

### 10.4 ジョブキュー更新
**PUT** `/setting/queue/{queueId}`

既存のジョブキューを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `queueId` (string): キューID

**リクエストボディ**: `ModifyJobQueueRequest`

**レスポンス**: `JobQueueResponse`

### 10.5 ジョブキュー削除
**DELETE** `/setting/queue`

ジョブキューを削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `queueIds` (string): カンマ区切りのキューIDリスト

**レスポンス**: `JobQueueResponse[]`

### 10.6 キューアクティビティ検索
**POST** `/queueActivity_search`

キューの活動状況を検索します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobQueueActivityInfoRequest`

**レスポンス**: `JobQueueItemInfoResponse[]`

### 10.7 キュー内容詳細取得
**GET** `/queueActivity_detail/{queueId}`

キューの詳細内容を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `queueId` (string): キューID

**レスポンス**: `JobQueueItemContentResponse`

---

## 11. ジョブ連携送信設定

### 11.1 送信設定一覧取得
**GET** `/joblinksend_setting`

ジョブ連携送信設定の一覧を取得します。

**権限**: JobManagement READ

**クエリパラメータ**:
- `ownerRoleId` (string): オーナーロールID

**レスポンス**: `JobLinkSendSettingResponse[]`

### 11.2 送信設定詳細取得
**GET** `/joblinksend_setting/{joblinkSendSettingId}`

指定された送信設定の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `joblinkSendSettingId` (string): 送信設定ID

**レスポンス**: `JobLinkSendSettingResponse`

### 11.3 送信設定追加
**POST** `/joblinksend_setting`

新しい送信設定を追加します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `AddJobLinkSendSettingRequest`
```json
{
  "joblinkSendSettingId": "string",
  "description": "string",
  "facilityId": "string",
  "protocol": "string",
  "port": "integer",
  "resourcePath": "string",
  "proxyFlg": "boolean",
  "proxyUrl": "string",
  "proxyPort": "integer",
  "proxyUser": "string",
  "proxyPassword": "string"
}
```

**レスポンス**: `JobLinkSendSettingResponse`

### 11.4 送信設定更新
**PUT** `/joblinksend_setting/{joblinkSendSettingId}`

既存の送信設定を更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `joblinkSendSettingId` (string): 送信設定ID

**リクエストボディ**: `ModifyJobLinkSendSettingRequest`

**レスポンス**: `JobLinkSendSettingResponse`

### 11.5 送信設定削除
**DELETE** `/joblinksend_setting`

送信設定を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `joblinkSendSettingIds` (string): カンマ区切りの送信設定IDリスト

**レスポンス**: `JobLinkSendSettingResponse[]`

---

## 12. ジョブ連携メッセージ管理

### 12.1 メッセージ登録
**POST** `/joblink_message`

外部マネージャからジョブ連携メッセージを登録します。

**権限**: JobManagement READ, ADD

**リクエストボディ**: `RegistJobLinkMessageRequest`
```json
{
  "joblinkMessageId": "string",
  "sourceIpAddressList": ["string"],
  "sendDate": "string",
  "facilityId": "string",
  "monitorDetailId": "string",
  "application": "string",
  "priority": "INFO",
  "message": "string",
  "messageOrg": "string",
  "jobLinkExpInfoList": [
    {
      "key": "string",
      "value": "string"
    }
  ]
}
```

**レスポンス**: `RegistJobLinkMessageResponse`

### 12.2 手動メッセージ送信
**POST** `/joblink_message_manual`

手動でジョブ連携メッセージを送信します。

**権限**: JobManagement READ, EXEC

**リクエストボディ**: `SendJobLinkMessageManualRequest`

**レスポンス**: `SendJobLinkMessageManualResponse`

### 12.3 メッセージ一覧検索
**POST** `/joblink_message_search`

受信ジョブ連携メッセージの一覧を検索します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobLinkMessageListRequest`
```json
{
  "size": "integer",
  "filterInfo": {
    "joblinkMessageId": "string",
    "facilityId": "string",
    "application": "string",
    "priorityList": ["INFO", "WARNING", "CRITICAL"],
    "message": "string",
    "sendDateFrom": "string",
    "sendDateTo": "string",
    "acceptDateFrom": "string",
    "acceptDateTo": "string"
  }
}
```

**レスポンス**: `GetJobLinkMessageListResponse`

---

## 13. 操作権限確認

### 13.1 ジョブ開始操作権限確認
**GET** `/operationProp_availableStartOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

ジョブに対して実行可能な開始操作を確認します。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobOperationPropResponse`

### 13.2 ノード開始操作権限確認
**GET** `/operationProp_availableStartOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}`

ノードに対して実行可能な開始操作を確認します。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID
- `facilityId` (string): ファシリティID

**レスポンス**: `JobOperationPropResponse`

### 13.3 ジョブ停止操作権限確認
**GET** `/operationProp_availableStopOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}`

ジョブに対して実行可能な停止操作を確認します。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**レスポンス**: `JobOperationPropResponse`

### 13.4 ノード停止操作権限確認
**GET** `/operationProp_availableStopOperation/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}`

ノードに対して実行可能な停止操作を確認します。

**権限**: JobManagement EXEC

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID
- `facilityId` (string): ファシリティID

**レスポンス**: `JobOperationPropResponse`

---

## 14. RPAシナリオジョブ管理

### 14.1 RPAログイン解像度一覧取得
**GET** `/setting/rpa_login_resolution`

RPAシナリオジョブで使用可能なログイン解像度の一覧を取得します。

**権限**: JobManagement READ

**レスポンス**: `JobRpaLoginResolutionResponse[]`

### 14.2 RPAスクリーンショット取得
**GET** `/sessionNode_operation/screenshot/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}`

RPAシナリオジョブのスクリーンショット情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID
- `facilityId` (string): ファシリティID

**レスポンス**: `JobRpaScreenshotResponse[]`

### 14.3 RPAスクリーンショットファイルダウンロード
**GET** `/sessionNode_operation/screenshot_file/{sessionId}/jobunit/{jobunitId}/job/{jobId}/facility/{facilityId}/regdate/{regDate}`

RPAスクリーンショットファイルをダウンロードします。

**権限**: JobManagement READ

**パスパラメータ**:
- `sessionId` (string): セッションID
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID
- `facilityId` (string): ファシリティID
- `regDate` (string): 登録日時

**レスポンス**: バイナリファイル (application/octet-stream)

---

## 15. その他の管理機能

### 15.1 ジョブマップアイコン一覧取得
**GET** `/jobmap/iconImage_iconId`

ジョブマップで使用可能なアイコンIDの一覧を取得します。

**権限**: JobManagement READ

**クエリパラメータ**:
- `ownerRoleId` (string): オーナーロールID

**レスポンス**: `JobmapIconImageInfoResponseP1`

### 15.2 プリメイクジョブセッション削除
**DELETE** `/setting/premakejobsession`

事前作成されたジョブセッションを削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickId` (string): ジョブキックID

**レスポンス**: `PremakeJobsessionResponse`

### 15.3 スケジュール計画一覧取得
**POST** `/setting/kick/schedule_plan`

スケジュール実行の計画一覧を取得します。

**権限**: JobManagement READ

**リクエストボディ**: `GetPlanListRequest`
```json
{
  "size": "integer",
  "jobunitId": "string",
  "jobId": "string",
  "facilityId": "string",
  "fromDate": "string",
  "toDate": "string",
  "ownerRoleId": "string"
}
```

**レスポンス**: `JobPlanResponse[]`

### 15.4 ジョブキューの参照情報取得
**GET** `/setting/job_referrerQueue/{queueId}`

指定されたキューを参照しているジョブ情報を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `queueId` (string): キューID

**レスポンス**: `JobInfoReferrerQueueResponse`

### 15.5 ジョブキュー設定検索
**POST** `/setting/queue_search`

条件を指定してジョブキュー設定を検索します。

**権限**: JobManagement READ

**リクエストボディ**: `GetJobQueueListSearchRequest`
```json
{
  "queueId": "string",
  "name": "string",
  "ownerRoleId": "string"
}
```

**レスポンス**: `JobQueueSettingViewInfoResponse`

---

## 16. ジョブ更新API（各ジョブタイプ）

### 16.1 ジョブネット更新
**PUT** `/setting/jobunit/{jobunitId}/jobnet/{jobId}`

既存のジョブネットを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyJobnetRequest`

**レスポンス**: `JobnetInfoResponse`

### 16.2 コマンドジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/commandJob/{jobId}`

既存のコマンドジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyCommandJobRequest`

**レスポンス**: `CommandJobInfoResponse`

### 16.3 ファイル転送ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/fileJob/{jobId}`

既存のファイル転送ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyFileTransferJobRequest`

**レスポンス**: `FileJobInfoResponse`

### 16.4 参照ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/referJob/{jobId}`

既存の参照ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyReferJobRequest`

**レスポンス**: `ReferJobInfoResponse`

### 16.5 監視ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/monitorJob/{jobId}`

既存の監視ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyMonitorJobRequest`

**レスポンス**: `MonitorJobInfoResponse`

### 16.6 承認ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/approvalJob/{jobId}`

既存の承認ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyApprovalJobRequest`

**レスポンス**: `ApprovalJobInfoResponse`

### 16.7 ジョブ連携送信ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/joblinkSendJob/{jobId}`

既存のジョブ連携送信ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyJobLinkSendJobRequest`

**レスポンス**: `JobLinkSendJobInfoResponse`

### 16.8 ジョブ連携待機ジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/joblinkRcvJob/{jobId}`

既存のジョブ連携待機ジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyJobLinkRcvJobRequest`

**レスポンス**: `JobLinkRcvJobInfoResponse`

### 16.9 ファイルチェックジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/filecheckJob/{jobId}`

既存のファイルチェックジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyFileCheckJobRequest`

**レスポンス**: `FileCheckJobInfoResponse`

### 16.10 RPAシナリオジョブ更新
**PUT** `/setting/jobunit/{jobunitId}/rpaJob/{jobId}`

既存のRPAシナリオジョブを更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobunitId` (string): ジョブユニットID
- `jobId` (string): ジョブID

**リクエストボディ**: `ModifyRpaJobRequest`

**レスポンス**: `RpaJobInfoResponse`

---

## 17. ジョブキック詳細取得・更新API

### 17.1 スケジュール詳細取得
**GET** `/setting/kick/schedule/{jobKickId}`

指定されたスケジュール実行契機の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**レスポンス**: `JobScheduleResponse`

### 17.2 ファイルチェック詳細取得
**GET** `/setting/kick/filecheck/{jobKickId}`

指定されたファイルチェック実行契機の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**レスポンス**: `JobFileCheckResponse`

### 17.3 手動実行契機詳細取得
**GET** `/setting/kick/manual/{jobKickId}`

指定された手動実行契機の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**レスポンス**: `JobManualResponse`

### 17.4 ジョブ連携受信契機詳細取得
**GET** `/setting/kick/joblinkrcv/{jobKickId}`

指定されたジョブ連携受信契機の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**レスポンス**: `JobLinkRcvResponse`

### 17.5 ジョブキック詳細取得
**GET** `/setting/kick/{jobKickId}`

指定されたジョブ実行契機の詳細を取得します。

**権限**: JobManagement READ

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**レスポンス**: `JobKickResponse`

### 17.6 スケジュール更新
**PUT** `/setting/kick/schedule/{jobKickId}`

既存のスケジュール実行契機を更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**リクエストボディ**: `ModifyScheduleRequest`

**レスポンス**: `JobKickResponse`

### 17.7 ファイルチェック更新
**PUT** `/setting/kick/filecheck/{jobKickId}`

既存のファイルチェック実行契機を更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**リクエストボディ**: `ModifyFileCheckRequest`

**レスポンス**: `JobKickResponse`

### 17.8 手動実行契機更新
**PUT** `/setting/kick/manual/{jobKickId}`

既存の手動実行契機を更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**リクエストボディ**: `ModifyJobManualRequest`

**レスポンス**: `JobKickResponse`

### 17.9 ジョブ連携受信契機更新
**PUT** `/setting/kick/joblinkrcv/{jobKickId}`

既存のジョブ連携受信契機を更新します。

**権限**: JobManagement READ, MODIFY

**パスパラメータ**:
- `jobKickId` (string): ジョブキックID

**リクエストボディ**: `ModifyJobLinkRcvRequest`

**レスポンス**: `JobKickResponse`

---

## 18. ジョブキック削除API（タイプ別）

### 18.1 スケジュール削除
**DELETE** `/setting/kick/schedule`

スケジュール実行契機を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickIds` (string): カンマ区切りのジョブキックIDリスト

**レスポンス**: `JobKickResponse[]`

### 18.2 ファイルチェック削除
**DELETE** `/setting/kick/filecheck`

ファイルチェック実行契機を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickIds` (string): カンマ区切りのジョブキックIDリスト

**レスポンス**: `JobKickResponse[]`

### 18.3 手動実行契機削除
**DELETE** `/setting/kick/manual`

手動実行契機を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickIds` (string): カンマ区切りのジョブキックIDリスト

**レスポンス**: `JobKickResponse[]`

### 18.4 ジョブ連携受信契機削除
**DELETE** `/setting/kick/joblinkrcv`

ジョブ連携受信契機を削除します。

**権限**: JobManagement READ, MODIFY

**クエリパラメータ**:
- `jobkickIds` (string): カンマ区切りのジョブキックIDリスト

**レスポンス**: `JobKickResponse[]`

---

## 19. 共通データ構造

### 19.1 JobInfo（ジョブ情報）
```json
{
  "jobunitId": "string",
  "id": "string",
  "name": "string",
  "description": "string",
  "type": "integer",
  "ownerRoleId": "string",
  "iconId": "string",
  "registeredModule": "boolean",
  "createTime": "string",
  "updateTime": "string",
  "createUser": "string",
  "updateUser": "string",
  "waitRule": {
    "condition": "integer",
    "endCondition": "integer",
    "endStatus": "integer",
    "endValue": "integer",
    "skipCondition": "integer",
    "skipEndStatus": "integer",
    "skipEndValue": "integer",
    "exclusiveBranch": "boolean",
    "exclusiveBranchNextJobOrderList": ["integer"],
    "calendar": "boolean",
    "calendarId": "string",
    "calendarEndStatus": "integer",
    "calendarEndValue": "integer",
    "jobRetryFlg": "boolean",
    "jobRetry": "integer",
    "jobRetryEndStatus": "integer",
    "queueFlg": "boolean",
    "queueId": "string",
    "startDelayTime": "boolean",
    "startDelayTimeValue": "string",
    "endDelayTime": "boolean",
    "endDelayTimeValue": "string",
    "multiplicityNotify": "boolean",
    "multiplicityNotifyPriority": "string",
    "multiplicityOperation": "integer",
    "multiplicityEndValue": "integer",
    "objectGroup": []
  },
  "command": {
    "startCommand": "string",
    "stopType": "integer",
    "stopCommand": "string",
    "specifyUser": "boolean",
    "effectiveUser": "string",
    "messageRetry": "integer",
    "messageRetryEndFlg": "boolean",
    "messageRetryEndValue": "integer",
    "commandRetry": "integer",
    "commandRetryFlg": "boolean",
    "commandRetryEndStatus": "integer",
    "facilityID": "string",
    "processingMethod": "integer",
    "scriptName": "string",
    "scriptEncoding": "string",
    "scriptContent": "string",
    "envVariableInfo": [],
    "normalJobPriority": "integer",
    "abnormalJobPriority": "integer",
    "jobReturnCodeList": []
  },
  "file": {
    "processMode": "integer",
    "srcFacilityID": "string",
    "destFacilityID": "string",
    "srcFile": "string",
    "destDirectory": "string",
    "destWorkDir": "string",
    "compressionFlg": "boolean",
    "checkFlg": "boolean",
    "specifyUser": "boolean",
    "effectiveUser": "string",
    "messageRetry": "integer",
    "messageRetryEndFlg": "boolean",
    "messageRetryEndValue": "integer",
    "commandRetry": "integer",
    "commandRetryFlg": "boolean",
    "commandRetryEndStatus": "integer"
  },
  "monitor": {
    "facilityID": "string",
    "monitorId": "string",
    "monitorInfoEndValue": "integer",
    "monitorWarnEndValue": "integer",
    "monitorCriticalEndValue": "integer",
    "monitorUnknownEndValue": "integer",
    "monitorWaitTime": "integer",
    "monitorWaitEndValue": "integer",
    "processMode": "integer"
  },
  "approval": {
    "approvalReqRoleId": "string",
    "approvalReqUserId": "string",
    "approvalReqSentence": "string",
    "approvalReqMailTitle": "string",
    "approvalReqMailBody": "string",
    "useApprovalReqSentence": "boolean"
  },
  "refer": {
    "referJobunitId": "string",
    "referJobId": "string",
    "referJobSelectType": "integer"
  },
  "param": [],
  "startJobId": "string",
  "ownerRoleId": "string",
  "exclusive": "boolean",
  "exclusiveBranch": "boolean",
  "propertyFull": "boolean"
}
```

### 19.2 JobKick（実行契機情報）
```json
{
  "id": "string",
  "name": "string",
  "type": "integer",
  "jobunitId": "string",
  "jobId": "string",
  "calendarId": "string",
  "valid": "boolean",
  "ownerRoleId": "string",
  "createTime": "string",
  "updateTime": "string",
  "createUser": "string",
  "updateUser": "string",
  "jobRuntimeParamList": []
}
```

### 19.3 JobDetailInfo（ジョブ実行詳細情報）
```json
{
  "sessionId": "string",
  "jobunitId": "string",
  "jobId": "string",
  "facilityId": "string",
  "status": "integer",
  "endStatus": "integer",
  "endValue": "integer",
  "startDate": "string",
  "endDate": "string",
  "sessionTime": "string",
  "instanceTime": "string",
  "priority": "integer",
  "scope": "string",
  "ownerRoleId": "string",
  "waitRuleTimeList": ["string"]
}
```

---

## 20. エラーレスポンス

APIはHTTPステータスコードとともに、詳細なエラー情報を返します。

### 20.1 共通エラーレスポンス
```json
{
  "errorCode": "string",
  "message": "string",
  "errorArgs": ["string"]
}
```

### 20.2 エラーステータスコード
- **400 Bad Request**: リクエストパラメータエラー
- **401 Unauthorized**: 認証エラー
- **403 Forbidden**: 権限不足
- **404 Not Found**: リソースが見つからない
- **409 Conflict**: 重複エラー
- **500 Internal Server Error**: サーバー内部エラー

---

## 21. 使用例

### 21.1 ジョブユニット作成からジョブ実行まで
```bash
# 1. ジョブユニット作成
curl -X POST /job/setting/jobunit \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jobTreeItem": {
      "data": {
        "jobunitId": "TEST_UNIT",
        "id": "TEST_UNIT",
        "name": "テストジョブユニット",
        "type": 0,
        "ownerRoleId": "ADMINISTRATORS"
      },
      "children": []
    }
  }'

# 2. コマンドジョブ追加
curl -X POST /job/setting/jobunit/TEST_UNIT/commandJob \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "TEST_JOB",
    "name": "テストコマンドジョブ",
    "command": {
      "startCommand": "echo hello",
      "facilityID": "localhost"
    }
  }'

# 3. ジョブ実行
curl -X POST /job/session_exec/jobunit/TEST_UNIT/job/TEST_JOB \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 21.2 ジョブ履歴検索
```bash
curl -X POST /job/history_search \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 100,
    "filter": {
      "jobunitId": "TEST_UNIT",
      "startFromDate": "2024-01-01 00:00:00",
      "startToDate": "2024-12-31 23:59:59"
    }
  }'
```

---

## 22. 注意事項

1. **ロック機能**: ジョブユニット編集時は適切に編集ロックを取得・解放してください
2. **権限管理**: 各APIは適切なシステム権限が必要です
3. **日時形式**: 日時は "yyyy/MM/dd HH:mm:ss" 形式で指定してください
4. **オーナーロール**: ユーザーは指定したオーナーロールに所属している必要があります
5. **バッチ処理**: 大量のデータ取得時はサイズ制限パラメータを適切に設定してください

---

この仕様書は、Hinemosジョブ管理APIの包括的なガイドです。実際の利用時は、認証トークンの取得やエラーハンドリングも適切に実装してください。