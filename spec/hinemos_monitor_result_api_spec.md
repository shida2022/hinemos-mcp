# Hinemos 7.1 Monitor Result REST API 仕様書

## 概要
本仕様書は、Hinemos 7.1の監視結果（Monitor Result）に関するREST APIエンドポイントの仕様を定義します。この仕様は実際のMonitorResultRestEndpoints.javaファイルを基に作成されています。

## ベースURL
```
https://{hinemos-server}:{port}/HinemosWS/rest/monitorresult
```

## 認証
- 基本認証（Basic Authentication）を使用
- または、Hinemos WebサービスのAPIキー認証

---

## エンドポイント一覧

### 1. イベント一覧検索

#### エンドポイント
```http
POST /monitorresult/event_search
```

#### 概要
指定された条件に一致するイベント一覧情報を取得します（クライアントview用）。

#### 権限
- MonitorResultRead権限が必要

#### リクエストボディ
```json
{
  "filter": {
    "facilityId": "ROOT",
    "priority": ["INFO", "WARNING", "CRITICAL"],
    "generationDateFrom": "2025-06-01T00:00:00.000Z",
    "generationDateTo": "2025-06-13T23:59:59.999Z",
    "outputDateFrom": "2025-06-01T00:00:00.000Z",
    "outputDateTo": "2025-06-13T23:59:59.999Z",
    "monitorId": "PING_SUCCESS_001",
    "monitorDetailId": "",
    "application": "ping_app",
    "message": "",
    "confirmType": [0, 1, 2],
    "confirmUser": "",
    "comment": "",
    "commentUser": "",
    "collectGraphFlg": true,
    "ownerRoleId": "ALL_USERS"
  },
  "size": 1000
}
```

#### レスポンス例
```json
{
  "total": 150,
  "eventList": [
    {
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "facilityId": "WEB_SERVER_01",
      "facilityName": "Webサーバー01",
      "priority": "INFO",
      "message": "応答時間: 15.2ms",
      "messageOrg": "Ping response time: 15.2ms",
      "generationDate": "2025-06-13T07:30:00.000Z",
      "outputDate": "2025-06-13T07:30:05.123Z",
      "confirmType": 0,
      "confirmDate": null,
      "confirmUser": "",
      "duplicationCount": 1,
      "comment": "",
      "commentDate": null,
      "commentUser": "",
      "collectGraphFlg": false,
      "ownerRoleId": "ALL_USERS",
      "application": "ping_app",
      "scopeText": "ROOT > アプリケーションサーバ > WEB_SERVER_01"
    }
  ]
}
```

---

### 2. スコープ一覧取得

#### エンドポイント
```http
GET /monitorresult/scope
```

#### 概要
スコープ情報一覧を取得します。指定されたファシリティの配下全てのファシリティのスコープ情報一覧を返します。

#### 権限
- MonitorResultRead権限が必要

#### クエリパラメータ
| パラメータ名 | タイプ | 必須 | 説明 |
|-------------|--------|------|------|
| facilityId | String | - | 取得対象の親ファシリティID |
| statusFlag | Boolean | - | ステータス情報取得フラグ |
| eventFlag | Boolean | - | イベント情報取得フラグ |
| orderFlg | Boolean | - | ソート順フラグ |

#### レスポンス例
```json
[
  {
    "facilityId": "ROOT",
    "facilityName": "ROOT",
    "facilityType": "SCOPE",
    "description": "ルートスコープ",
    "displaySortOrder": 0,
    "iconImage": "",
    "valid": true,
    "priority": "UNKNOWN",
    "statusCount": {
      "unknown": 0,
      "normal": 15,
      "warning": 3,
      "critical": 1
    },
    "eventCount": {
      "unknown": 2,
      "info": 120,
      "warning": 15,
      "critical": 5
    }
  }
]
```

---

### 3. ステータス一覧検索

#### エンドポイント
```http
POST /monitorresult/status_search
```

#### 概要
指定された条件に一致するステータス情報一覧を取得します。

#### 権限
- MonitorResultRead権限が必要

#### リクエストボディ
```json
{
  "filter": {
    "facilityId": "ROOT",
    "priority": ["WARNING", "CRITICAL"],
    "monitorId": "",
    "application": "",
    "ownerRoleId": "ALL_USERS"
  },
  "size": 500
}
```

#### レスポンス例
```json
{
  "total": 25,
  "countAll": 150,
  "statusList": [
    {
      "facilityId": "WEB_SERVER_01",
      "facilityName": "Webサーバー01",
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "priority": "WARNING",
      "message": "応答時間が閾値を超過: 3.2秒",
      "outputDate": "2025-06-13T07:30:00.000Z",
      "generationDate": "2025-06-13T07:29:55.000Z",
      "application": "ping_app",
      "value": 3200.0,
      "ownerRoleId": "ALL_USERS",
      "collectGraphFlg": false
    }
  ]
}
```

---

### 4. ステータス削除

#### エンドポイント
```http
POST /monitorresult/status_delete
```

#### 概要
指定されたステータス情報を削除します。

#### 権限
- MonitorResultRead権限とMODIFY権限が必要

#### リクエストボディ
```json
{
  "statusDataInfoRequestlist": [
    {
      "facilityId": "WEB_SERVER_01",
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "outputDate": "2025-06-13T07:30:00.000Z"
    }
  ]
}
```

#### レスポンス例
```json
[
  {
    "facilityId": "WEB_SERVER_01",
    "facilityName": "Webサーバー01",
    "monitorId": "PING_SUCCESS_001",
    "monitorDetailId": "",
    "pluginId": "MON_PNG_N",
    "priority": "WARNING",
    "message": "削除済み",
    "outputDate": "2025-06-13T07:30:00.000Z"
  }
]
```

---

### 5. イベントファイルダウンロード

#### エンドポイント
```http
POST /monitorresult/event_download
```

#### 概要
指定された条件に一致する帳票出力用イベント情報一覧をCSVファイルとしてダウンロードします。

#### 権限
- MonitorResultRead権限が必要

#### リクエストボディ
```json
{
  "filter": {
    "facilityId": "ROOT",
    "priority": ["WARNING", "CRITICAL"],
    "generationDateFrom": "2025-06-01T00:00:00.000Z",
    "generationDateTo": "2025-06-13T23:59:59.999Z"
  },
  "selectedEvents": [
    {
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "facilityId": "WEB_SERVER_01",
      "outputDate": "2025-06-13T07:30:00.000Z"
    }
  ],
  "filename": "event_report_20250613.csv"
}
```

#### レスポンス
- Content-Type: application/octet-stream
- バイナリCSVファイル

---

### 6. イベント詳細検索

#### エンドポイント
```http
POST /monitorresult/event_detail_search
```

#### 概要
イベント詳細情報を取得します。

#### 権限
- MonitorResultRead権限が必要

#### リクエストボディ
```json
{
  "monitorId": "PING_SUCCESS_001",
  "monitorDetailId": "",
  "pluginId": "MON_PNG_N",
  "facilityId": "WEB_SERVER_01",
  "outputDate": "2025-06-13T07:30:00.000Z"
}
```

#### レスポンス例
```json
{
  "monitorId": "PING_SUCCESS_001",
  "monitorDetailId": "",
  "pluginId": "MON_PNG_N",
  "facilityId": "WEB_SERVER_01",
  "facilityName": "Webサーバー01",
  "priority": "WARNING",
  "message": "応答時間が閾値を超過",
  "messageOrg": "Ping response time exceeded threshold",
  "generationDate": "2025-06-13T07:30:00.000Z",
  "outputDate": "2025-06-13T07:30:05.123Z",
  "confirmType": 0,
  "application": "ping_app",
  "value": 3200.0,
  "eventLogHitory": [
    {
      "operationHistoryType": "CREATE",
      "operationDate": "2025-06-13T07:30:05.123Z",
      "operationUser": "system",
      "detail": "イベント作成"
    }
  ]
}
```

---

### 7. イベントコメント更新

#### エンドポイント
```http
PUT /monitorresult/event_comment
```

#### 概要
指定されたイベント情報のコメントを更新します。

#### 権限
- MonitorResultMODIFY権限が必要

#### リクエストボディ
```json
{
  "monitorId": "PING_SUCCESS_001",
  "monitorDetailId": "",
  "pluginId": "MON_PNG_N",
  "facilityId": "WEB_SERVER_01",
  "outputDate": "2025-06-13T07:30:00.000Z",
  "comment": "調査完了、ネットワーク遅延が原因でした",
  "commentDate": "2025-06-13T08:00:00.000Z",
  "commentUser": "admin"
}
```

#### レスポンス例
```json
{
  "monitorId": "PING_SUCCESS_001",
  "monitorDetailId": "",
  "pluginId": "MON_PNG_N",
  "facilityId": "WEB_SERVER_01",
  "facilityName": "Webサーバー01",
  "priority": "WARNING",
  "message": "応答時間が閾値を超過",
  "comment": "調査完了、ネットワーク遅延が原因でした",
  "commentDate": "2025-06-13T08:00:00.000Z",
  "commentUser": "admin",
  "outputDate": "2025-06-13T07:30:00.000Z"
}
```

---

### 8. イベント確認状態更新

#### エンドポイント
```http
PUT /monitorresult/event_confirm
```

#### 概要
指定されたイベント情報一覧の確認状態を更新します。

#### 権限
- MonitorResultMODIFY権限が必要

#### リクエストボディ
```json
{
  "list": [
    {
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "facilityId": "WEB_SERVER_01",
      "outputDate": "2025-06-13T07:30:00.000Z"
    }
  ],
  "confirmType": 2
}
```

#### 確認タイプ
- 0: 未確認
- 1: 確認中
- 2: 確認済

#### レスポンス例
```json
[
  {
    "monitorId": "PING_SUCCESS_001",
    "monitorDetailId": "",
    "pluginId": "MON_PNG_N",
    "facilityId": "WEB_SERVER_01",
    "facilityName": "Webサーバー01",
    "priority": "WARNING",
    "confirmType": 2,
    "confirmDate": "2025-06-13T08:00:00.000Z",
    "confirmUser": "admin",
    "outputDate": "2025-06-13T07:30:00.000Z"
  }
]
```

---

### 9. イベント一括確認更新

#### エンドポイント
```http
PUT /monitorresult/event_multiConfirm
```

#### 概要
指定された条件に一致するイベント情報の確認状態を一括更新します。

#### 権限
- MonitorResultMODIFY権限が必要

#### リクエストボディ
```json
{
  "confirmType": 2,
  "filter": {
    "facilityId": "ROOT",
    "priority": ["WARNING", "CRITICAL"],
    "generationDateFrom": "2025-06-13T00:00:00.000Z",
    "generationDateTo": "2025-06-13T23:59:59.999Z",
    "confirmType": [0]
  }
}
```

#### レスポンス例
```json
[
  {
    "monitorId": "PING_SUCCESS_001",
    "facilityId": "WEB_SERVER_01",
    "confirmType": 2,
    "confirmDate": "2025-06-13T08:00:00.000Z",
    "confirmUser": "admin"
  }
]
```

---

### 10. 性能グラフフラグ更新

#### エンドポイント
```http
PUT /monitorresult/event_collectGraphFlg
```

#### 概要
指定されたイベント情報一覧の性能グラフ用フラグを更新します。

#### 権限
- MonitorResultMODIFY権限が必要

#### リクエストボディ
```json
{
  "list": [
    {
      "monitorId": "HTTP_NUMERIC_SUCCESS_002",
      "monitorDetailId": "",
      "pluginId": "MON_HTP_N",
      "facilityId": "WEB_SERVER_01",
      "outputDate": "2025-06-13T07:30:00.000Z"
    }
  ],
  "collectGraphFlg": true
}
```

#### レスポンス例
```json
[
  {
    "monitorId": "HTTP_NUMERIC_SUCCESS_002",
    "facilityId": "WEB_SERVER_01",
    "collectGraphFlg": true,
    "outputDate": "2025-06-13T07:30:00.000Z"
  }
]
```

---

### 11. イベント情報更新

#### エンドポイント
```http
PUT /monitorresult/event
```

#### 概要
指定されたイベント情報を更新します。

#### 権限
- MonitorResultMODIFY権限が必要

#### リクエストボディ
```json
{
  "info": {
    "monitorId": "PING_SUCCESS_001",
    "monitorDetailId": "",
    "pluginId": "MON_PNG_N",
    "facilityId": "WEB_SERVER_01",
    "outputDate": "2025-06-13T07:30:00.000Z",
    "priority": "INFO",
    "message": "正常に復旧しました",
    "comment": "ネットワーク問題が解決"
  }
}
```

#### レスポンス例
```json
{
  "monitorId": "PING_SUCCESS_001",
  "facilityId": "WEB_SERVER_01",
  "priority": "INFO",
  "message": "正常に復旧しました",
  "comment": "ネットワーク問題が解決",
  "outputDate": "2025-06-13T07:30:00.000Z"
}
```

---

### 12. イベントカスタムコマンド実行

#### エンドポイント
```http
POST /monitorresult/eventCustomCommand_exec
```

#### 概要
指定されたイベント情報に対してカスタムコマンドを実行します。

#### 権限
- MonitorResultEXEC権限が必要

#### リクエストボディ
```json
{
  "commandNo": 1,
  "eventList": [
    {
      "monitorId": "PING_SUCCESS_001",
      "monitorDetailId": "",
      "pluginId": "MON_PNG_N",
      "facilityId": "WEB_SERVER_01",
      "outputDate": "2025-06-13T07:30:00.000Z"
    }
  ]
}
```

#### レスポンス例
```json
{
  "commandResultID": "uuid-12345678-1234-1234-1234-123456789abc"
}
```

---

### 13. イベントカスタムコマンド結果取得

#### エンドポイント
```http
GET /monitorresult/eventCustomCommand/{uuid}
```

#### 概要
イベントカスタムコマンドの実行結果を取得します。

#### 権限
- MonitorResultEXEC権限が必要

#### パスパラメータ
| パラメータ名 | タイプ | 必須 | 説明 |
|-------------|--------|------|------|
| uuid | String | ✓ | コマンド結果ID |

#### レスポンス例
```json
{
  "eventCustomCommandResultRoot": {
    "commandResultID": "uuid-12345678-1234-1234-1234-123456789abc",
    "status": "COMPLETED",
    "startTime": "2025-06-13T08:00:00.000Z",
    "endTime": "2025-06-13T08:00:30.000Z",
    "results": [
      {
        "facilityId": "WEB_SERVER_01",
        "exitCode": 0,
        "stdout": "コマンド実行成功",
        "stderr": "",
        "executeTime": "2025-06-13T08:00:15.000Z"
      }
    ]
  }
}
```

---

### 14. イベントデータマップ取得

#### エンドポイント
```http
GET /monitorresult/event_collectValid_mapKeyFacility
```

#### 概要
イベント履歴のフラグ情報をファシリティIDごとのマップで取得します。

#### クエリパラメータ
| パラメータ名 | タイプ | 必須 | 説明 |
|-------------|--------|------|------|
| facilityIdList | String | - | カンマ区切りのファシリティIDリスト |

#### レスポンス例
```json
{
  "map": {
    "WEB_SERVER_01": [
      {
        "monitorId": "PING_SUCCESS_001",
        "facilityId": "WEB_SERVER_01",
        "priority": "WARNING",
        "collectGraphFlg": true,
        "outputDate": "2025-06-13T07:30:00.000Z"
      }
    ],
    "DB_SERVER_01": [
      {
        "monitorId": "CUSTOM_TEST_007",
        "facilityId": "DB_SERVER_01",
        "priority": "INFO",
        "collectGraphFlg": false,
        "outputDate": "2025-06-13T07:25:00.000Z"
      }
    ]
  }
}
```

---

## DTOクラス定義

### EventLogInfoResponse
```java
public class EventLogInfoResponse {
    private String monitorId;
    private String monitorDetailId;
    private String pluginId;
    private String facilityId;
    private String facilityName;
    private String priority;
    private String message;
    private String messageOrg;
    private String generationDate;
    private String outputDate;
    private Integer confirmType;
    private String confirmDate;
    private String confirmUser;
    private Integer duplicationCount;
    private String comment;
    private String commentDate;
    private String commentUser;
    private Boolean collectGraphFlg;
    private String ownerRoleId;
    private String application;
    private String scopeText;
    private Double value;
    
    // getters and setters
}
```

### StatusInfoResponse
```java
public class StatusInfoResponse {
    private String facilityId;
    private String facilityName;
    private String monitorId;
    private String monitorDetailId;
    private String pluginId;
    private String priority;
    private String message;
    private String outputDate;
    private String generationDate;
    private String application;
    private Double value;
    private String ownerRoleId;
    private Boolean collectGraphFlg;
    
    // getters and setters
}
```

### ScopeDataInfoResponse
```java
public class ScopeDataInfoResponse {
    private String facilityId;
    private String facilityName;
    private String facilityType;
    private String description;
    private Integer displaySortOrder;
    private String iconImage;
    private Boolean valid;
    private String priority;
    private Map<String, Integer> statusCount;
    private Map<String, Integer> eventCount;
    
    // getters and setters
}
```

---

## エラーレスポンス

### 標準エラーレスポンス
```json
{
  "errorCode": "MONITOR_NOT_FOUND",
  "message": "指定された監視設定が見つかりません",
  "errorArgs": ["INVALID_MONITOR_001"]
}
```

### エラーコード一覧
| エラーコード | HTTPステータス | 説明 |
|-------------|---------------|------|
| MONITOR_NOT_FOUND | 404 | 監視設定が存在しない |
| EVENT_LOG_NOT_FOUND | 404 | イベントログが存在しない |
| FACILITY_NOT_FOUND | 404 | ファシリティが存在しない |
| INVALID_ROLE | 403 | アクセス権限がない |
| INVALID_SETTING | 400 | パラメータが不正 |
| INVALID_USER_PASS | 401 | 認証エラー |
| HINEMOS_UNKNOWN | 500 | 内部エラー |

---

## 権限について

### 必要な権限
- **MonitorResultRead**: 参照系API（GET, POST（検索系））
- **MonitorResultMODIFY**: 更新系API（PUT）
- **MonitorResultEXEC**: 実行系API（カスタムコマンド）

### 権限の組み合わせ
- 削除API: READ + MODIFY
- コメント・確認状態更新: MODIFY
- カスタムコマンド: EXEC

---

## 注意事項

1. **日時形式**: すべての日時はISO 8601形式（UTC）で指定
2. **確認タイプ**: 0=未確認、1=確認中、2=確認済
3. **優先度**: INFO, WARNING, CRITICAL, UNKNOWN
4. **ファイルダウンロード**: CSVファイルはUTF-8エンコード
5. **一括操作**: 大量データ処理時はタイムアウトに注意

---

## 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|----------|
| 1.0 | 2025-06-13 | 初版作成（実際のソースコードベース） |