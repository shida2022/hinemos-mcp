# Hinemos 監視設定API仕様書

## 概要
このAPIはHinemos 7.1の監視設定を管理するためのREST APIです。様々な種類の監視設定の作成、更新、削除、取得が可能です。

## ベースパス
```
/monitorsetting
```

## 認証・認可
- REST APIの認証が必要
- システム権限（監視設定）が必要
- 一部のAPIはシステム管理者権限が必要

## 11. 監視設定共通データ項目

### 11.1 基本項目（全監視共通）

| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| monitorId | string | ○ | 監視設定ID（64文字以内の英数字） |
| monitorName | string | ○ | 監視設定名（最大256文字） |
| description | string | - | 説明（最大256文字） |
| monitorTypeId | string | ○ | 監視種別ID |
| facilityId | string | ○ | 監視対象ファシリティID |
| intervalSec | number | ○ | 監視間隔（秒） |
| validFlg | boolean | ○ | 監視有効フラグ |
| collectorFlg | boolean | - | 収集有効フラグ |
| ownerRoleId | string | ○ | オーナーロールID |
| notifyGroupId | string | - | 通知グループID |
| application | string | - | アプリケーション |
| calendarId | string | - | カレンダーID |

### 11.2 数値監視用項目

#### 収集設定
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| itemName | string | ○ | 収集値表示名 |
| measure | string | - | 収集値単位 |

#### 閾値設定（numericValueInfo配列）
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| monitorNumericType | string | ○ | 監視数値種別（"BASIC", "CHANGE", "PREDICTION"） |
| priority | string | ○ | 重要度（"CRITICAL", "WARNING", "INFO", "UNKNOWN"） |
| thresholdLowerLimit | number | - | 下限閾値 |
| thresholdUpperLimit | number | - | 上限閾値 |
| message | string | - | メッセージ |

#### 将来予測設定（predictionInfo）
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| predictionMethod | string | - | 予測手法（"POLYNOMIAL", "LINEAR"） |
| predictionAnalysysRange | number | - | 予測解析範囲（時間） |
| predictionTarget | number | - | 予測先（時間） |
| coefficientFlg | boolean | - | 回帰係数チェック |

#### 変化量設定（changeInfo）
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| changeAnalysysRange | number | - | 変化量解析範囲（時間） |
| changeApplication | number | - | 変化量適用率 |

### 11.3 文字列監視用項目

#### 文字列判定設定（stringValueInfo配列）
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| orderNo | number | ○ | 順序 |
| priority | string | ○ | 重要度 |
| pattern | string | ○ | 判定パターン |
| processType | string | ○ | 処理タイプ（"CONTAINS", "NOT_CONTAINS", "MATCHES"） |
| caseSensitivityFlg | boolean | - | 大文字小文字区別 |
| validFlg | boolean | ○ | 有効フラグ |
| message | string | - | メッセージ |

### 11.4 真偽値監視用項目

#### 真偽値判定設定（truthValueInfo配列）
| 項目名 | 型 | 必須 | 説明 |
|--------|-----|-----|------|
| priority | string | ○ | 重要度 |
| truthValue | string | ○ | 真偽値（"TRUE", "FALSE"） |
| message | string | - | メッセージ |

### 11.5 監視種別固有項目

#### HTTP監視
```json
"httpCheckInfo": {
  "url": "string",           // 監視URL（必須）
  "connectTimeout": number,  // 接続タイムアウト（ミリ秒）
  "requestTimeout": number,  // 要求タイムアウト（ミリ秒）
  "userAgent": "string",     // ユーザーエージェント
  "authType": "string",      // 認証タイプ（"NONE", "BASIC", "DIGEST"）
  "authUser": "string",      // 認証ユーザー
  "authPassword": "string",  // 認証パスワード
  "proxyFlg": boolean,      // プロキシ使用フラグ
  "proxyUrl": "string",     // プロキシURL
  "proxyPort": number,      // プロキシポート
  "proxyUser": "string",    // プロキシユーザー
  "proxyPassword": "string" // プロキシパスワード
}
```

#### JMX監視
```json
"jmxCheckInfo": {
  "port": number,           // JMXポート（必須）
  "authFlg": boolean,       // 認証フラグ
  "authUser": "string",     // 認証ユーザー
  "authPassword": "string", // 認証パスワード
  "masterId": "string",     // マスタID（必須）
  "url": "string",          // JMX URL
  "convertFlg": number      // 変換フラグ
}
```

#### PING監視
```json
"pingCheckInfo": {
  "runCount": number,       // 実行回数
  "runInterval": number,    // 実行間隔（ミリ秒）
  "timeout": number,        // タイムアウト（ミリ秒）
  "bytes": number           // パケットサイズ
}
```

#### カスタム監視
```json
"customCheckInfo": {
  "commandExecTypeCode": "string", // 実行種別（"INDIVIDUAL", "SELECTED"）
  "command": "string",             // コマンド（必須）
  "effectiveUser": "string",       // 実行ユーザー
  "timeout": number,               // タイムアウト（ミリ秒）
  "convertFlg": number             // 変換フラグ
}
```

#### リソース監視
```json
"perfCheckInfo": {
  "itemCode": "string",           // 項目コード（必須）
  "deviceDisplayName": "string",  // デバイス表示名
  "breakdownFlg": boolean         // 内訳フラグ
}
```

---

## 1. 監視設定一覧取得

### 全監視設定一覧取得
**GET** `/monitor`

監視設定の一覧を取得します。

#### レスポンス
- **200 OK**: 監視設定一覧（配列）
- **400 Bad Request**: リクエストエラー
- **401 Unauthorized**: 認証エラー
- **403 Forbidden**: 権限不足
- **500 Internal Server Error**: サーバーエラー

### 条件指定監視設定一覧取得
**POST** `/monitor_search`

条件に従って監視設定一覧を取得します。

#### リクエストボディ
```json
{
  "monitorFilterInfo": {
    // フィルター条件
  }
}
```

---

## 2. 監視設定の個別操作

### 監視設定取得
**GET** `/monitor/{monitorId}`

指定されたIDの監視設定を取得します。

#### パラメータ
- `monitorId` (path): 監視設定ID

### 監視設定削除
**DELETE** `/monitor`

指定された監視設定を削除します。

#### クエリパラメータ
- `monitorIds` (query): 削除する監視設定IDのカンマ区切り文字列

### 監視有効/無効切り替え
**PUT** `/monitor_monitorValid`

監視設定の監視有効/無効を切り替えます。

#### リクエストボディ
```json
{
  "monitorIds": ["string"],
  "validFlg": true
}
```

### 収集有効/無効切り替え
**PUT** `/monitor_collectorValid`

監視設定の収集有効/無効を切り替えます。

---

## 3. 監視種別ごとのAPI

### 3.1 HTTPシナリオ監視

#### 作成
**POST** `/httpScenario`

**リクエストボディ例:**
```json
{
  "monitorId": "HTTP_SCENARIO_001",
  "monitorName": "Webサイト監視",
  "description": "ECサイトのシナリオ監視",
  "monitorTypeId": "MON_HTP_SCE",
  "facilityId": "ROOT",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": false,
  "ownerRoleId": "ALL_USERS",
  "notifyGroupId": "NOTIFY_GROUP_001",
  "application": "EC_SITE",
  "calendarId": "CALENDAR_001",
  "httpScenarioCheckInfo": {
    "monitorTypeId": "MON_HTP_SCE",
    "monitorId": "HTTP_SCENARIO_001",
    "urlList": [
      {
        "id": 1,
        "url": "https://example.com/login",
        "description": "ログインページ",
        "statusCode": "200",
        "post": "username=test&password=test",
        "connectTimeout": 10000,
        "requestTimeout": 60000
      },
      {
        "id": 2,
        "url": "https://example.com/dashboard",
        "description": "ダッシュボード",
        "statusCode": "200",
        "connectTimeout": 10000,
        "requestTimeout": 60000
      }
    ],
    "userAgent": "Hinemos HTTP Monitor",
    "connectTimeout": 10000,
    "requestTimeout": 60000,
    "authType": "NONE",
    "authUser": "",
    "authPassword": ""
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 30000.0
    }
  ]
}
```

#### 更新
**PUT** `/httpScenario/{monitorId}`

#### 一覧取得
**GET** `/httpScenario`

### 3.2 HTTP監視（数値）

#### 作成
**POST** `/httpNumeric`

**リクエストボディ例:**
```json
{
  "monitorId": "HTTP_NUMERIC_001",
  "monitorName": "レスポンス時間監視",
  "description": "HTTPレスポンス時間の数値監視",
  "monitorTypeId": "MON_HTP_N",
  "facilityId": "ROOT",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": true,
  "ownerRoleId": "ALL_USERS",
  "itemName": "レスポンス時間",
  "measure": "msec",
  "httpCheckInfo": {
    "monitorTypeId": "MON_HTP_N",
    "monitorId": "HTTP_NUMERIC_001",
    "url": "https://example.com/api/health",
    "connectTimeout": 10000,
    "requestTimeout": 60000,
    "userAgent": "Hinemos HTTP Monitor",
    "authType": "NONE",
    "authUser": "",
    "authPassword": "",
    "proxyFlg": false,
    "proxyUrl": "",
    "proxyPort": 8080,
    "proxyUser": "",
    "proxyPassword": ""
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "WARNING",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 5000.0
    },
    {
      "monitorNumericType": "BASIC",
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 10000.0
    }
  ],
  "predictionInfo": {
    "predictionMethod": "POLYNOMIAL",
    "predictionAnalysysRange": 24,
    "predictionTarget": 6,
    "coefficientFlg": false
  },
  "changeInfo": {
    "changeAnalysysRange": 24,
    "changeApplication": 1.0
  }
}
```

#### 更新
**PUT** `/httpNumeric/{monitorId}`

#### 一覧取得
**GET** `/httpNumeric`

### 3.3 HTTP監視（文字列）

#### 作成
**POST** `/httpString`

**リクエストボディ例:**
```json
{
  "monitorId": "HTTP_STRING_001",
  "monitorName": "レスポンス内容監視",
  "description": "HTTPレスポンス内容の文字列監視",
  "monitorTypeId": "MON_HTP_S",
  "facilityId": "ROOT",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": false,
  "ownerRoleId": "ALL_USERS",
  "httpCheckInfo": {
    "monitorTypeId": "MON_HTP_S",
    "monitorId": "HTTP_STRING_001",
    "url": "https://example.com/api/status",
    "connectTimeout": 10000,
    "requestTimeout": 60000,
    "userAgent": "Hinemos HTTP Monitor",
    "authType": "BASIC",
    "authUser": "username",
    "authPassword": "password",
    "proxyFlg": false
  },
  "stringValueInfo": [
    {
      "orderNo": 1,
      "priority": "CRITICAL",
      "pattern": "ERROR",
      "processType": "CONTAINS",
      "caseSensitivityFlg": false,
      "validFlg": true,
      "message": "エラー検出"
    },
    {
      "orderNo": 2,
      "priority": "NORMAL",
      "pattern": "OK",
      "processType": "CONTAINS",
      "caseSensitivityFlg": false,
      "validFlg": true,
      "message": "正常"
    }
  ]
}
```

#### 更新
**PUT** `/httpString/{monitorId}`

#### 一覧取得
**GET** `/httpString`

### 3.4 エージェント監視

#### 作成
**POST** `/agent`

**リクエストボディ例:**
```json
{
  "monitorId": "AGENT_001",
  "monitorName": "エージェント生存監視",
  "description": "Hinemosエージェントの生存確認",
  "monitorTypeId": "MON_AGT",
  "facilityId": "SERVER_001",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": false,
  "ownerRoleId": "ALL_USERS",
  "truthValueInfo": [
    {
      "priority": "CRITICAL",
      "truthValue": "FALSE",
      "message": "エージェント停止"
    }
  ]
}
```

#### 更新
**PUT** `/agent/{monitorId}`

#### 一覧取得
**GET** `/agent`

### 3.5 JMX監視

#### 作成
**POST** `/jmx`

**リクエストボディ例:**
```json
{
  "monitorId": "JMX_001",
  "monitorName": "JVMヒープメモリ監視",
  "description": "JVMのヒープメモリ使用量監視",
  "monitorTypeId": "MON_JMX",
  "facilityId": "APP_SERVER_001",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": true,
  "ownerRoleId": "ALL_USERS",
  "itemName": "ヒープメモリ使用量",
  "measure": "MB",
  "jmxCheckInfo": {
    "monitorTypeId": "MON_JMX",
    "monitorId": "JMX_001",
    "port": 9999,
    "authFlg": false,
    "authUser": "",
    "authPassword": "",
    "masterId": "java.lang:type=Memory:HeapMemoryUsage:used",
    "url": "service:jmx:rmi:///jndi/rmi://#[HOST]#:#[PORT]#/jmxrmi",
    "convertFlg": 1
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "WARNING",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 2147483648.0
    },
    {
      "monitorNumericType": "BASIC", 
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 4294967296.0
    }
  ]
}
```

#### 更新
**PUT** `/jmx/{monitorId}`

#### 一覧取得
**GET** `/jmx`

#### JMXフォーマット一覧取得
**GET** `/jmx/jmxFormat`

### 3.6 PING監視

#### 作成
**POST** `/ping`

**リクエストボディ例:**
```json
{
  "monitorId": "PING_001",
  "monitorName": "サーバー疎通監視",
  "description": "サーバーへのPing疎通確認",
  "monitorTypeId": "MON_PING",
  "facilityId": "SERVER_001",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": true,
  "ownerRoleId": "ALL_USERS",
  "itemName": "応答時間",
  "measure": "msec",
  "pingCheckInfo": {
    "monitorTypeId": "MON_PING",
    "monitorId": "PING_001",
    "runCount": 1,
    "runInterval": 1000,
    "timeout": 5000,
    "bytes": 56
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "WARNING",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 3000.0
    },
    {
      "monitorNumericType": "BASIC",
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 5000.0
    }
  ]
}
```

#### 更新
**PUT** `/ping/{monitorId}`

#### 一覧取得
**GET** `/ping`

### 3.7 SNMPトラップ監視

#### 作成
**POST** `/snmptrap`

#### 更新
**PUT** `/snmptrap/{monitorId}`

#### 一覧取得
**GET** `/snmptrap`

### 3.8 SNMP監視（数値）

#### 作成
**POST** `/snmpNumeric`

#### 更新
**PUT** `/snmpNumeric/{monitorId}`

#### 一覧取得
**GET** `/snmpNumeric`

### 3.9 SNMP監視（文字列）

#### 作成
**POST** `/snmpString`

#### 更新
**PUT** `/snmpString/{monitorId}`

#### 一覧取得
**GET** `/snmpString`

### 3.10 SQL監視（数値）

#### 作成
**POST** `/sqlNumeric`

#### 更新
**PUT** `/sqlNumeric/{monitorId}`

#### 一覧取得
**GET** `/sqlNumeric`

### 3.11 SQL監視（文字列）

#### 作成
**POST** `/sqlString`

#### 更新
**PUT** `/sqlString/{monitorId}`

#### 一覧取得
**GET** `/sqlString`

### 3.12 Windowsイベント監視

#### 作成
**POST** `/winevent`

#### 更新
**PUT** `/winevent/{monitorId}`

#### 一覧取得
**GET** `/winevent`

### 3.13 Windowsサービス監視

#### 作成
**POST** `/winservice`

#### 更新
**PUT** `/winservice/{monitorId}`

#### 一覧取得
**GET** `/winservice`

### 3.14 カスタムトラップ監視（数値）

#### 作成
**POST** `/customtrapNumeric`

#### 更新
**PUT** `/customtrapNumeric/{monitorId}`

#### 一覧取得
**GET** `/customtrapNumeric`

### 3.15 カスタムトラップ監視（文字列）

#### 作成
**POST** `/customtrapString`

#### 更新
**PUT** `/customtrapString/{monitorId}`

#### 一覧取得
**GET** `/customtrapString`

### 3.16 カスタム監視（数値）

#### 作成
**POST** `/customNumeric`

**リクエストボディ例:**
```json
{
  "monitorId": "CUSTOM_NUMERIC_001",
  "monitorName": "カスタム数値監視",
  "description": "シェルスクリプトによる数値監視",
  "monitorTypeId": "MON_CUSTOM_N",
  "facilityId": "SERVER_001",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": true,
  "ownerRoleId": "ALL_USERS",
  "itemName": "カスタム値",
  "measure": "個",
  "customCheckInfo": {
    "monitorTypeId": "MON_CUSTOM_N",
    "monitorId": "CUSTOM_NUMERIC_001",
    "commandExecTypeCode": "INDIVIDUAL",
    "command": "/opt/hinemos/bin/custom_check.sh",
    "effectiveUser": "hinemos",
    "timeout": 15000,
    "convertFlg": 2
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "WARNING",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 80.0
    },
    {
      "monitorNumericType": "BASIC",
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 95.0
    }
  ]
}
```

#### 更新
**PUT** `/customNumeric/{monitorId}`

#### 一覧取得
**GET** `/customNumeric`

### 3.17 カスタム監視（文字列）

#### 作成
**POST** `/customString`

#### 更新
**PUT** `/customString/{monitorId}`

#### 一覧取得
**GET** `/customString`

### 3.18 クラウドログ監視

#### 作成
**POST** `/cloudlog`

#### 更新
**PUT** `/cloudlog/{monitorId}`

#### 一覧取得
**GET** `/cloudlog`

### 3.19 クラウドサービス監視

#### 作成
**POST** `/cloudservice`

#### 更新
**PUT** `/cloudservice/{monitorId}`

#### 一覧取得
**GET** `/cloudservice`

### 3.20 クラウド課金監視

#### 作成
**POST** `/cloudservicebilling`

#### 更新
**PUT** `/cloudservicebilling/{monitorId}`

#### 一覧取得
**GET** `/cloudservicebilling`

### 3.21 クラウド課金詳細監視

#### 作成
**POST** `/cloudservicebillingdetail`

#### 更新
**PUT** `/cloudservicebillingdetail/{monitorId}`

#### 一覧取得
**GET** `/cloudservicebillingdetail`

### 3.22 サービス・ポート監視

#### 作成
**POST** `/serviceport`

#### 更新
**PUT** `/serviceport/{monitorId}`

#### 一覧取得
**GET** `/serviceport`

### 3.23 システムログ監視

#### 作成
**POST** `/systemlog`

#### 更新
**PUT** `/systemlog/{monitorId}`

#### 一覧取得
**GET** `/systemlog`

### 3.24 バイナリファイル監視

#### 作成
**POST** `/binaryfile`

#### 更新
**PUT** `/binaryfile/{monitorId}`

#### 一覧取得
**GET** `/binaryfile`

### 3.25 パケットキャプチャ監視

#### 作成
**POST** `/packetCapture`

#### 更新
**PUT** `/packetcapture/{monitorId}`

#### 一覧取得
**GET** `/packetcapture`

### 3.26 プロセス監視

#### 作成
**POST** `/process`

#### 更新
**PUT** `/process/{monitorId}`

#### 一覧取得
**GET** `/process`

### 3.27 リソース監視

#### 作成
**POST** `/performance`

**リクエストボディ例:**
```json
{
  "monitorId": "PERFORMANCE_001",
  "monitorName": "CPU使用率監視",
  "description": "サーバーのCPU使用率監視",
  "monitorTypeId": "MON_PERF",
  "facilityId": "SERVER_001",
  "intervalSec": 300,
  "validFlg": true,
  "collectorFlg": true,
  "ownerRoleId": "ALL_USERS",
  "itemName": "CPU使用率",
  "measure": "%",
  "perfCheckInfo": {
    "monitorTypeId": "MON_PERF",
    "monitorId": "PERFORMANCE_001",
    "itemCode": "system.cpu.usage",
    "deviceDisplayName": "",
    "breakdownFlg": false
  },
  "numericValueInfo": [
    {
      "monitorNumericType": "BASIC",
      "priority": "WARNING",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 80.0
    },
    {
      "monitorNumericType": "BASIC",
      "priority": "CRITICAL",
      "thresholdLowerLimit": 0.0,
      "thresholdUpperLimit": 95.0
    }
  ]
}
```

#### 更新
**PUT** `/performance/{monitorId}`

#### 一覧取得
**GET** `/performance`

### 3.28 ログファイル監視

#### 作成
**POST** `/logfile`

#### 更新
**PUT** `/logfile/{monitorId}`

#### 一覧取得
**GET** `/logfile`

### 3.29 ログ件数監視

#### 作成
**POST** `/logcount`

#### 更新
**PUT** `/logcount/{monitorId}`

#### 一覧取得
**GET** `/logcount`

### 3.30 相関係数監視

#### 作成
**POST** `/correlation`

#### 更新
**PUT** `/correlation/{monitorId}`

#### 一覧取得
**GET** `/correlation`

### 3.31 収集値統合監視

#### 作成
**POST** `/integration`

#### 更新
**PUT** `/integration/{monitorId}`

#### 一覧取得
**GET** `/integration`

### 3.32 RPAログファイル監視

#### 作成
**POST** `/rpalogfile`

#### 更新
**PUT** `/rpalogfile/{monitorId}`

#### 一覧取得
**GET** `/rpalogfile`

### 3.33 RPA管理ツール監視

#### 作成
**POST** `/rpaManagementTool`

#### 更新
**PUT** `/rpaManagementTool/{monitorId}`

#### 一覧取得
**GET** `/rpaManagementTool`

---

## 4. 特殊な取得API

### 文字列監視設定一覧取得
**GET** `/monitor_string`

分析用の文字列監視設定一覧を取得します。

#### クエリパラメータ
- `facilityId` (query): ファシリティID
- `ownerRoleId` (query): オーナーロールID

### 文字列・トラップ監視一覧取得
**GET** `/monitor_stringAndTrap`

文字列監視とトラップ監視の一覧を取得します。

### 監視ジョブ用監視設定一覧取得
**GET** `/monitor_withoutCheckInfo_forJob`

監視ジョブで使用可能な監視設定一覧を取得します。

#### クエリパラメータ
- `ownerRoleId` (query): オーナーロールID

### 監視設定簡易一覧取得
**GET** `/monitor_withoutCheckInfo`

チェック情報を含まない監視設定一覧を取得します。

### 条件指定監視設定簡易一覧取得
**POST** `/monitor_withoutCheckInfo_search`

条件に従ってチェック情報を含まない監視設定一覧を取得します。

### 性能グラフ用監視設定取得
**GET** `/monitor_graphInfo_forCollect/{monitorId}`

性能グラフ表示用の監視設定情報を取得します。

### 監視文字列タグ一覧取得
**GET** `/monitor_string_tag/{monitorId}`

指定された監視の文字列タグ一覧を取得します。

#### クエリパラメータ
- `ownerRoleId` (query): オーナーロールID

---

## 5. マスタ管理API

### 5.1 JMXマスタ

#### JMXマスタ一覧取得
**GET** `/jmxmaster_all`

システム管理者権限が必要です。

#### JMXマスタ追加
**POST** `/jmxmaster`

#### JMXマスタ削除
**DELETE** `/jmxmaster`

#### クエリパラメータ
- `jmxMasterIds` (query): 削除するJMXマスタIDのカンマ区切り文字列

#### JMXマスタ全削除
**DELETE** `/jmxmaster_all`

#### JMX監視項目一覧取得
**GET** `/jmxmonitoritem_all`

### 5.2 SQL関連

#### JDBCドライバ一覧取得
**GET** `/sql/jdbcDriver`

### 5.3 バイナリ監視

#### バイナリプリセット一覧取得
**GET** `/binaryCheckInfo`

---

## 6. エラーレスポンス

全てのAPIで共通のエラーレスポンスコードを返します。

### ステータスコード
- **400 Bad Request**: リクエストパラメータエラー
- **401 Unauthorized**: 認証エラー
- **403 Forbidden**: 権限不足
- **404 Not Found**: リソースが見つからない
- **500 Internal Server Error**: サーバー内部エラー

### エラーレスポンス例
```json
{
  "errorCode": "string",
  "message": "string",
  "errorArgs": ["string"]
}
```

---

## 7. 注意事項

1. **認証**: 全てのAPIでHinemosの認証が必要です
2. **権限**: 監視設定権限（読み取り/変更）が必要です
3. **システム管理者権限**: JMXマスタ管理APIはシステム管理者権限が必要です
4. **オーナーロール**: 一部のAPIではオーナーロールの所属チェックが行われます
5. **監視種別**: 各監視種別ごとに専用のエンドポイントが用意されています
6. **バージョン**: このAPIはHinemos 7.1用です

---

## 8. データ形式

- **Content-Type**: `application/json`
- **文字コード**: UTF-8
- **日時形式**: ISO 8601形式またはHinemos独自形式
- **配列**: 複数のリソースを扱う場合は配列形式で返却

---

## 9. パフォーマンス考慮

- 大量データの取得時はページネーション対応
- フィルタリング機能による絞り込み可能
- 必要最小限のデータのみ取得するための専用エンドポイント

---

## 10. セキュリティ

- 全てのAPIでログ出力対応
- 操作ログの記録
- ロールベースアクセス制御
- 入力値検証の実装