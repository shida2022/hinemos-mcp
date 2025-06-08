# Hinemos MCP Server 使用ガイド

## セットアップ手順

### 1. 環境構築

```bash
# リポジトリクローン
git clone <your-repo>/hinemos-mcp-server
cd hinemos-mcp-server

# 依存関係インストール
pip install -r requirements.txt

# 設定ファイル作成
cp .env.example .env
# .envファイルを編集してHinemos接続情報を設定
```

### 2. Hinemos接続設定

`.env`ファイルで以下を設定：

```env
HINEMOS_BASE_URL=http://your-hinemos-server:8080/HinemosWS/
HINEMOS_USERNAME=your_username
HINEMOS_PASSWORD=your_password
```

### 3. Claude Desktop との連携

Claude Desktop の設定ファイル（`claude_desktop_config.json`）に以下を追加：

```json
{
  "mcpServers": {
    "hinemos": {
      "command": "python",
      "args": ["/path/to/hinemos_mcp_server.py"],
      "env": {
        "HINEMOS_BASE_URL": "http://your-hinemos-server:8080/HinemosWS/",
        "HINEMOS_USERNAME": "your_username",
        "HINEMOS_PASSWORD": "your_password"
      }
    }
  }
}
```

## 利用可能な機能

### Tools（ツール）

1. **check_node_status(node_id: str)**
   - 指定ノードの監視ステータス確認
   - 例: `check_node_status("WEB-SERVER-01")`

2. **get_critical_events(hours: int = 24)**
   - 重要なイベント取得
   - 例: `get_critical_events(12)` # 過去12時間

3. **execute_hinemos_job(job_id: str, target_node: str)**
   - Hinemosジョブ実行
   - 例: `execute_hinemos_job("BACKUP_JOB", "DB-SERVER-01")`

4. **list_managed_nodes()**
   - 管理対象ノード一覧取得

### Resources（リソース）

1. **hinemos://monitor/status**
   - 現在の監視ステータス

2. **hinemos://events/recent**
   - 最新のイベント情報

### Prompts（プロンプト）

1. **system_health_report()**
   - システム全体の健全性レポート生成

2. **incident_investigation(event_id: str)**
   - インシデント詳細調査

## 使用例

### Claude Desktop での使用例

```
# ユーザー: システムの健全性レポートを作成してください

Claude: システム全体の健全性レポートを作成します。

[system_health_report() プロンプトを使用]
[check_node_status() で各ノードをチェック]
[get_critical_events() で重要なイベントを確認]

## システム健全性レポート

### 全体ステータス
- 総ノード数: 25台
- 正常稼働: 23台
- 警告状態: 2台
- エラー状態: 0台

### 重要なアラート
1. WEB-SERVER-02: CPU使用率 95% (警告)
2. DB-SERVER-01: ディスク使用率 88% (警告)

### 推奨アクション
1. WEB-SERVER-02のプロセス確認が必要
2. DB-SERVER-01のログクリーンアップ実行推奨
```

## テスト方法

### 1. 接続テスト

```python
# test_connection.py
import asyncio
from hinemos_mcp_server import HinemosClient, HinemosConfig
import aiohttp

async def test_connection():
    config = HinemosConfig(
        base_url="http://localhost:8080/HinemosWS/",
        username="hinemos",
        password="hinemos123"
    )
    
    async with aiohttp.ClientSession() as session:
        client = HinemosClient(config, session)
        try:
            nodes = await client.get_node_list()
            print(f"接続成功: {len(nodes)} ノード取得")
        except Exception as e:
            print(f"接続エラー: {e}")

asyncio.run(test_connection())
```

### 2. MCP Inspector でのテスト

```bash
# MCP Inspectorを使用してサーバーをテスト
npx @modelcontextprotocol/inspector python hinemos_mcp_server.py
```

### 3. 単体テスト

```python
# test_hinemos_mcp.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from hinemos_mcp_server import HinemosClient, HinemosConfig

@pytest.fixture
def mock_session():
    session = AsyncMock()
    response = AsyncMock()
    response.text = AsyncMock(return_value='<soap:Envelope>...</soap:Envelope>')
    response.raise_for_status = MagicMock()
    session.post.return_value.__aenter__.return_value = response
    return session

@pytest.mark.asyncio
async def test_get_node_list(mock_session):
    config = HinemosConfig("http://test", "user", "pass")
    client = HinemosClient(config, mock_session)
    
    result = await client.get_node_list()
    assert result is not None
    mock_session.post.assert_called_once()
```

## トラブルシューティング

### よくある問題

1. **認証エラー**
   ```
   Error: 401 Unauthorized
   解決: HINEMOS_USERNAME と HINEMOS_PASSWORD を確認
   ```

2. **接続タイムアウト**
   ```
   Error: Connection timeout
   解決: HINEMOS_BASE_URL とネットワーク接続を確認
   ```

3. **SOAP パースエラー**
   ```
   Error: XML parsing failed
   解決: Hinemosサーバーのレスポンス形式を確認
   ```

### ログ確認

```bash
# デバッグモードで実行
LOG_LEVEL=DEBUG python hinemos_mcp_server.py
```

### Hinemos API バージョン確認

```python
# Hinemos WebService APIのWSDLを確認
curl http://your-hinemos-server:8080/HinemosWS/MonitorEndpoint?wsdl
```

## カスタマイズ

### 新しいツールの追加

```python
@mcp.tool()
async def custom_monitoring_tool(parameter: str) -> List[TextContent]:
    """カスタム監視ツール"""
    ctx = mcp.get_context()
    client = HinemosClient(ctx.hinemos_config, ctx.session)
    
    # カスタムロジック実装
    result = await client.custom_api_call(parameter)
    
    return [TextContent(type="text", text=str(result))]
```

### 新しいリソースの追加

```python
@mcp.resource("hinemos://custom/data")
async def get_custom_data() -> Resource:
    """カスタムデータリソース"""
    # カスタムデータ取得ロジック
    return Resource(
        uri="hinemos://custom/data",
        name="Custom Hinemos Data",
        description="Custom data from Hinemos",
        mimeType="application/