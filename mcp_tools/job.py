from mcp.types import Tool

def get_tools():
    return [
        # --- 1. ジョブツリー管理 ---
        Tool(
            name="get_job_tree_simple",
            description="ジョブツリー情報取得（簡易版）",
            inputSchema={
                "type": "object",
                "properties": {
                    "ownerRoleId": {"type": "string", "description": "オーナーロールID"}
                }
            }
        ),
        Tool(
            name="get_job_tree_full",
            description="ジョブツリー情報取得（完全版）",
            inputSchema={
                "type": "object",
                "properties": {
                    "ownerRoleId": {"type": "string", "description": "オーナーロールID"}
                }
            }
        ),
        Tool(
            name="get_job_info",
            description="ジョブ詳細情報取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["jobunitId", "jobId"]
            }
        ),
        Tool(
            name="get_job_info_bulk",
            description="ジョブ情報一括取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobList": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "jobunitId": {"type": "string"},
                                "id": {"type": "string"}
                            },
                            "required": ["jobunitId", "id"]
                        }
                    }
                },
                "required": ["jobList"]
            }
        ),
        # --- 2. ジョブユニット管理 ---
        Tool(
            name="add_jobunit",
            description="ジョブユニット登録",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunit": {
                        "type": "object",
                        "properties": {
                            "jobTreeItem": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string", "description": "ジョブユニットID"},
                                            "jobunitId": {"type": "string", "description": "ジョブユニットID（idと同じ値）"},
                                            "name": {"type": "string", "description": "ジョブユニット名"},
                                            "type": {"type": "string", "description": "ジョブタイプ（JOBUNIT固定）", "default": "JOBUNIT"},
                                            "description": {"type": "string", "description": "説明", "default": ""},
                                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                                            "registered": {"type": "boolean", "description": "登録フラグ", "default": false},
                                            "isUseApprovalReqSentence": {"type": "boolean", "description": "承認要求文使用フラグ", "default": false},
                                            "expNodeRuntimeFlg": {"type": "boolean", "description": "ノード実行時展開フラグ", "default": false},
                                            "beginPriority": {"type": "string", "description": "開始優先度", "default": "INFO"},
                                            "normalPriority": {"type": "string", "description": "正常優先度", "default": "INFO"},
                                            "warnPriority": {"type": "string", "description": "警告優先度", "default": "WARNING"},
                                            "abnormalPriority": {"type": "string", "description": "異常優先度", "default": "CRITICAL"},
                                            "updateTaget": {"type": "boolean", "description": "更新対象フラグ", "default": true},
                                            "endStatus": {
                                                "type": "array",
                                                "description": "終了ステータス定義",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "type": {"type": "string", "description": "ステータスタイプ（NORMAL/WARNING/ABNORMAL）"},
                                                        "value": {"type": "integer", "description": "終了値"},
                                                        "startRangeValue": {"type": "integer", "description": "開始範囲値"},
                                                        "endRangeValue": {"type": "integer", "description": "終了範囲値"}
                                                    }
                                                },
                                                "default": [
                                                    {"type": "NORMAL", "value": 0, "startRangeValue": 0, "endRangeValue": 0},
                                                    {"type": "WARNING", "value": 1, "startRangeValue": 1, "endRangeValue": 1},
                                                    {"type": "ABNORMAL", "value": -1}
                                                ]
                                            },
                                            "param": {"type": "array", "description": "パラメータリスト", "default": []},
                                            "notifyRelationInfos": {"type": "array", "description": "通知関連情報", "default": []}
                                        },
                                        "required": ["id", "jobunitId", "name", "type", "ownerRoleId"]
                                    },
                                    "children": {"type": "array", "description": "子要素リスト", "default": []}
                                },
                                "required": ["data", "children"]
                            }
                        },
                        "required": ["jobTreeItem"]
                    },
                    "isClient": {"type": "boolean", "description": "クライアント用モード", "default": true}
                },
                "required": ["jobunit"]
            }
        ),
        Tool(
            name="modify_jobunit",
            description="ジョブユニット更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "jobunit": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "ジョブユニットID"},
                            "name": {"type": "string", "description": "ジョブユニット名"},
                            "description": {"type": "string", "description": "説明"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "parentJobunitId": {"type": "string", "description": "親ジョブユニットID"},
                            "jobunitType": {"type": "integer", "description": "ジョブユニット種別(1:通常, 2:テンプレート)"},
                            "updateTime": {"type": "string", "description": "更新日時(yyyy-MM-dd HH:mm:ss)"},
                            "editSession": {"type": "integer", "description": "編集セッションID"}
                        },
                        "required": ["id", "name", "ownerRoleId"]
                    },
                    "isClient": {"type": "boolean", "description": "クライアント用モード"}
                },
                "required": ["jobunitId", "jobunit"]
            }
        ),
        Tool(
            name="delete_jobunit",
            description="ジョブユニット削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"}
                },
                "required": ["jobunitId"]
            }
        ),
        # --- 3. 編集ロック管理 ---
        Tool(
            name="get_edit_lock",
            description="編集ロック取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "updateTime": {"type": "string"},
                    "forceFlag": {"type": "boolean"}
                },
                "required": ["jobunitId", "updateTime", "forceFlag"]
            }
        ),
        Tool(
            name="check_edit_lock",
            description="編集ロック確認",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "editSession": {"type": "integer"}
                },
                "required": ["jobunitId", "editSession"]
            }
        ),
        Tool(
            name="release_edit_lock",
            description="編集ロック解放",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "editSession": {"type": "integer"}
                },
                "required": ["jobunitId", "editSession"]
            }
        ),
        # --- 4. ジョブ設定管理（全ジョブタイプ追加API） ---
        Tool(
            name="add_jobnet",
            description="ジョブネット追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "jobnet": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブネットID"},
                            "name": {"type": "string", "description": "ジョブネット名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(0:ジョブネット)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "jobnet": {
                                "type": "object",
                                "properties": {
                                    "startCondition": {"type": "integer", "description": "開始条件"},
                                    "endCondition": {"type": "integer", "description": "終了条件"},
                                    "timeout": {"type": "integer", "description": "タイムアウト(秒)"},
                                    "jobList": {
                                        "type": "array",
                                        "description": "子ジョブリスト",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string", "description": "子ジョブID"},
                                                "type": {"type": "integer", "description": "子ジョブタイプ"},
                                                "name": {"type": "string", "description": "子ジョブ名"}
                                            },
                                            "required": ["id", "type", "name"]
                                        }
                                    }
                                }
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "jobnet"]
                    }
                },
                "required": ["jobunitId", "jobnet"]
            }
        ),
        Tool(
            name="add_command_job",
            description="コマンドジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(1:コマンド)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "command": {
                                "type": "object",
                                "properties": {
                                    "startCommand": {"type": "string", "description": "開始コマンド"},
                                    "stopType": {"type": "integer", "description": "停止タイプ"},
                                    "stopCommand": {"type": "string", "description": "停止コマンド"},
                                    "specifyUser": {"type": "boolean", "description": "ユーザ指定"},
                                    "effectiveUser": {"type": "string", "description": "実行ユーザ"},
                                    "messageRetry": {"type": "integer", "description": "メッセージリトライ回数"},
                                    "messageRetryEndFlg": {"type": "boolean", "description": "メッセージリトライ終了フラグ"},
                                    "messageRetryEndValue": {"type": "integer", "description": "メッセージリトライ終了値"},
                                    "commandRetry": {"type": "integer", "description": "コマンドリトライ回数"},
                                    "commandRetryFlg": {"type": "boolean", "description": "コマンドリトライフラグ"},
                                    "commandRetryEndStatus": {"type": "integer", "description": "コマンドリトライ終了ステータス"},
                                    "facilityID": {"type": "string", "description": "実行先ファシリティID"},
                                    "processingMethod": {"type": "integer", "description": "処理方式"},
                                    "scriptName": {"type": "string", "description": "スクリプト名"},
                                    "scriptEncoding": {"type": "string", "description": "スクリプトエンコーディング"},
                                    "scriptContent": {"type": "string", "description": "スクリプト内容"},
                                    "envVariableInfo": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "key": {"type": "string"},
                                                "value": {"type": "string"}
                                            }
                                        },
                                        "description": "環境変数リスト"
                                    },
                                    "normalJobPriority": {"type": "integer", "description": "正常時優先度"},
                                    "abnormalJobPriority": {"type": "integer", "description": "異常時優先度"},
                                    "jobReturnCodeList": {
                                        "type": "array",
                                        "items": {"type": "integer"},
                                        "description": "正常終了コードリスト"
                                    }
                                },
                                "required": ["startCommand"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "command"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_file_job",
            description="ファイル転送ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(2:ファイル転送)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "file": {
                                "type": "object",
                                "properties": {
                                    "srcFacilityId": {"type": "string", "description": "送信元ファシリティID"},
                                    "srcPath": {"type": "string", "description": "送信元パス"},
                                    "dstFacilityId": {"type": "string", "description": "送信先ファシリティID"},
                                    "dstPath": {"type": "string", "description": "送信先パス"},
                                    "overwrite": {"type": "boolean", "description": "上書きフラグ"},
                                    "deleteAfterTransfer": {"type": "boolean", "description": "転送後削除フラグ"},
                                    "transferType": {"type": "integer", "description": "転送タイプ"},
                                    "encoding": {"type": "string", "description": "エンコーディング"}
                                },
                                "required": ["srcFacilityId", "srcPath", "dstFacilityId", "dstPath"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "file"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_refer_job",
            description="参照ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(3:参照)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "refer": {
                                "type": "object",
                                "properties": {
                                    "referJobunitId": {"type": "string", "description": "参照先ジョブユニットID"},
                                    "referJobId": {"type": "string", "description": "参照先ジョブID"}
                                },
                                "required": ["referJobunitId", "referJobId"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "refer"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_monitor_job",
            description="監視ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(4:監視)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "monitor": {
                                "type": "object",
                                "properties": {
                                    "monitorId": {"type": "string", "description": "監視ID"},
                                    "monitorType": {"type": "integer", "description": "監視タイプ"},
                                    "facilityId": {"type": "string", "description": "監視対象ファシリティID"},
                                    "monitorDetailId": {"type": "string", "description": "監視詳細ID"},
                                    "pluginId": {"type": "string", "description": "プラグインID"},
                                    "outputDate": {"type": "string", "description": "出力日時"}
                                },
                                "required": ["monitorId", "monitorType", "facilityId"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "monitor"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_approval_job",
            description="承認ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(5:承認)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "approval": {
                                "type": "object",
                                "properties": {
                                    "approverRoleId": {"type": "string", "description": "承認者ロールID"},
                                    "approvalType": {"type": "integer", "description": "承認タイプ"},
                                    "approvalTimeout": {"type": "integer", "description": "承認タイムアウト(秒)"}
                                },
                                "required": ["approverRoleId", "approvalType"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "approval"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_joblinksend_job",
            description="ジョブ連携送信ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(6:ジョブ連携送信)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "joblinksend": {
                                "type": "object",
                                "properties": {
                                    "joblinkSendSettingId": {"type": "string", "description": "ジョブ連携送信設定ID"},
                                    "message": {"type": "string", "description": "送信メッセージ"},
                                    "timeout": {"type": "integer", "description": "タイムアウト(秒)"}
                                },
                                "required": ["joblinkSendSettingId"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "joblinksend"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_joblinkrcv_job",
            description="ジョブ連携待機ジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(7:ジョブ連携待機)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "joblinkrcv": {
                                "type": "object",
                                "properties": {
                                    "joblinkRcvSettingId": {"type": "string", "description": "ジョブ連携待機設定ID"},
                                    "timeout": {"type": "integer", "description": "タイムアウト(秒)"}
                                },
                                "required": ["joblinkRcvSettingId"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "joblinkrcv"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_filecheck_job",
            description="ファイルチェックジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(8:ファイルチェック)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "filecheck": {
                                "type": "object",
                                "properties": {
                                    "facilityId": {"type": "string", "description": "ファシリティID"},
                                    "path": {"type": "string", "description": "チェック対象パス"},
                                    "filePattern": {"type": "string", "description": "ファイルパターン"},
                                    "timeout": {"type": "integer", "description": "タイムアウト(秒)"}
                                },
                                "required": ["facilityId", "path", "filePattern"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "filecheck"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="add_rpa_job",
            description="RPAシナリオジョブ追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "job": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "id": {"type": "string", "description": "ジョブID"},
                            "name": {"type": "string", "description": "ジョブ名"},
                            "description": {"type": "string", "description": "説明"},
                            "type": {"type": "integer", "description": "ジョブタイプ(9:RPAシナリオ)"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "iconId": {"type": "string", "description": "アイコンID"},
                            "rpa": {
                                "type": "object",
                                "properties": {
                                    "scenarioId": {"type": "string", "description": "RPAシナリオID"},
                                    "facilityId": {"type": "string", "description": "実行先ファシリティID"},
                                    "loginUser": {"type": "string", "description": "ログインユーザ"},
                                    "loginPassword": {"type": "string", "description": "ログインパスワード"},
                                    "timeout": {"type": "integer", "description": "タイムアウト(秒)"}
                                },
                                "required": ["scenarioId", "facilityId"]
                            }
                        },
                        "required": ["jobunitId", "id", "name", "type", "ownerRoleId", "rpa"]
                    }
                },
                "required": ["jobunitId", "job"]
            }
        ),
        Tool(
            name="delete_job",
            description="ジョブ削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["jobunitId", "jobId"]
            }
        ),
        # --- 5. ジョブ実行制御 ---
        Tool(
            name="run_job",
            description="ジョブ実行",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "jobId": {"type": "string", "description": "ジョブID"},
                    "runJobRequest": {
                        "type": "object",
                        "properties": {
                            "parameterList": {
                                "type": "array",
                                "description": "パラメータリスト",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "value": {"type": "string"}
                                    },
                                    "required": ["key", "value"]
                                }
                            },
                            "scheduleDate": {"type": "string", "description": "スケジュール日時(yyyy-MM-dd HH:mm:ss)"},
                            "comment": {"type": "string", "description": "コメント"}
                        }
                    }
                },
                "required": ["jobunitId", "jobId", "runJobRequest"]
            }
        ),
        Tool(
            name="run_job_kick",
            description="ジョブキック実行",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string", "description": "ジョブキックID"},
                    "runJobKickRequest": {
                        "type": "object",
                        "properties": {
                            "parameterList": {
                                "type": "array",
                                "description": "パラメータリスト",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "value": {"type": "string"}
                                    },
                                    "required": ["key", "value"]
                                }
                            },
                            "scheduleDate": {"type": "string", "description": "スケジュール日時(yyyy-MM-dd HH:mm:ss)"},
                            "comment": {"type": "string", "description": "コメント"}
                        }
                    }
                },
                "required": ["jobKickId", "runJobKickRequest"]
            }
        ),
        Tool(
            name="session_job_operation",
            description="セッションジョブ操作",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string", "description": "セッションID"},
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "jobId": {"type": "string", "description": "ジョブID"},
                    "operation": {
                        "type": "object",
                        "properties": {
                            "operationType": {"type": "integer", "description": "操作種別(1:停止, 2:再実行, 3:スキップ等)"},
                            "comment": {"type": "string", "description": "コメント"}
                        },
                        "required": ["operationType"]
                    }
                },
                "required": ["sessionId", "jobunitId", "jobId", "operation"]
            }
        ),
        Tool(
            name="session_node_operation",
            description="セッションノード操作",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string", "description": "セッションID"},
                    "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                    "jobId": {"type": "string", "description": "ジョブID"},
                    "facilityId": {"type": "string", "description": "ファシリティID"},
                    "operation": {
                        "type": "object",
                        "properties": {
                            "operationType": {"type": "integer", "description": "操作種別(1:停止, 2:再実行, 3:スキップ等)"},
                            "comment": {"type": "string", "description": "コメント"}
                        },
                        "required": ["operationType"]
                    }
                },
                "required": ["sessionId", "jobunitId", "jobId", "facilityId", "operation"]
            }
        ),
        # --- 6. ジョブセッション監視 ---
        Tool(
            name="get_session_job_detail",
            description="ジョブ詳細一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"}
                },
                "required": ["sessionId"]
            }
        ),
        Tool(
            name="get_session_node_detail",
            description="ノード詳細一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId"]
            }
        ),
        Tool(
            name="get_session_file_detail",
            description="ファイル転送一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId"]
            }
        ),
        Tool(
            name="get_session_job_jobInfo",
            description="セッションジョブ情報取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId"]
            }
        ),
        Tool(
            name="get_session_job_allDetail",
            description="セッションジョブ全詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"}
                },
                "required": ["sessionId"]
            }
        ),
        # --- 7. ジョブ履歴管理 ---
        Tool(
            name="history_search",
            description="ジョブ履歴一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "size": {"type": "integer"},
                    "filter": {"type": "object"}
                },
                "required": ["size", "filter"]
            }
        ),
        # --- 8. ジョブキック管理 ---
        Tool(
            name="add_schedule",
            description="スケジュールジョブキック追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "schedule": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "jobId": {"type": "string", "description": "ジョブID"},
                            "scheduleType": {"type": "integer", "description": "スケジュールタイプ(1:日次,2:週次,3:月次,4:cron)"},
                            "startDate": {"type": "string", "description": "開始日(yyyy-MM-dd)"},
                            "endDate": {"type": "string", "description": "終了日(yyyy-MM-dd)"},
                            "startTime": {"type": "string", "description": "開始時刻(HH:mm:ss)"},
                            "cronExpression": {"type": "string", "description": "cron式"},
                            "parameterList": {
                                "type": "array",
                                "description": "パラメータリスト",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "value": {"type": "string"}
                                    },
                                    "required": ["key", "value"]
                                }
                            },
                            "comment": {"type": "string", "description": "コメント"}
                        },
                        "required": ["jobunitId", "jobId", "scheduleType", "startDate", "startTime"]
                    }
                },
                "required": ["schedule"]
            }
        ),
        Tool(
            name="add_filecheck",
            description="ファイルチェックジョブキック追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "filecheck": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "jobId": {"type": "string", "description": "ジョブID"},
                            "facilityId": {"type": "string", "description": "ファシリティID"},
                            "path": {"type": "string", "description": "監視パス"},
                            "filePattern": {"type": "string", "description": "ファイルパターン"},
                            "timeout": {"type": "integer", "description": "タイムアウト(秒)"},
                            "parameterList": {
                                "type": "array",
                                "description": "パラメータリスト",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "value": {"type": "string"}
                                    },
                                    "required": ["key", "value"]
                                }
                            },
                            "comment": {"type": "string", "description": "コメント"}
                        },
                        "required": ["jobunitId", "jobId", "facilityId", "path", "filePattern"]
                    }
                },
                "required": ["filecheck"]
            }
        ),
        Tool(
            name="add_manual",
            description="手動ジョブキック追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "manual": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "jobId": {"type": "string", "description": "ジョブID"},
                            "parameterList": {
                                "type": "array",
                                "description": "パラメータリスト",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "value": {"type": "string"}
                                    },
                                    "required": ["key", "value"]
                                }
                            },
                            "comment": {"type": "string", "description": "コメント"}
                        },
                        "required": ["jobunitId", "jobId"]
                    }
                },
                "required": ["manual"]
            }
        ),
        Tool(
            name="add_joblinkrcv_job",
            description="ジョブ連携受信ジョブキック追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "joblinkrcv": {
                        "type": "object",
                        "properties": {
                            "jobunitId": {"type": "string", "description": "ジョブユニットID"},
                            "jobId": {"type": "string", "description": "ジョブID"},
                            "joblinkRcvSettingId": {"type": "string", "description": "ジョブ連携待機設定ID"},
                            "timeout": {"type": "integer", "description": "タイムアウト(秒)"}
                        },
                        "required": ["jobunitId", "jobId", "joblinkRcvSettingId"]
                    }
                },
                "required": ["joblinkrcv"]
            }
        ),
        Tool(
            name="get_kick_list",
            description="ジョブキック一覧取得",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="kick_search",
            description="条件付きジョブキック検索",
            inputSchema={
                "type": "object",
                "properties": {
                    "condition": {"type": "object"}
                },
                "required": ["condition"]
            }
        ),
        Tool(
            name="set_kick_valid",
            description="ジョブキック状態変更",
            inputSchema={
                "type": "object",
                "properties": {
                    "setStatus": {"type": "object"}
                },
                "required": ["setStatus"]
            }
        ),
        Tool(
            name="delete_kick",
            description="ジョブキック削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickIds": {"type": "string"}
                },
                "required": ["jobkickIds"]
            }
        ),
        # --- 9. ジョブ承認管理 ---
        Tool(
            name="session_approval_search",
            description="承認対象ジョブ一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "request": {"type": "object"}
                },
                "required": ["request"]
            }
        ),
        Tool(
            name="modify_approval_info",
            description="承認情報更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "info": {"type": "object"}
                },
                "required": ["sessionId", "jobunitId", "jobId", "info"]
            }
        ),
        # --- 10. ジョブキュー管理 ---
        Tool(
            name="get_queue_list",
            description="ジョブキュー一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "roleId": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_queue_detail",
            description="ジョブキュー詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "queueId": {"type": "string"}
                },
                "required": ["queueId"]
            }
        ),
        Tool(
            name="add_queue",
            description="ジョブキュー追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "queue": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "キューID"},
                            "name": {"type": "string", "description": "キュー名"},
                            "description": {"type": "string", "description": "説明"},
                            "ownerRoleId": {"type": "string", "description": "オーナーロールID"},
                            "maxJobNum": {"type": "integer", "description": "最大同時実行数"},
                            "priority": {"type": "integer", "description": "優先度"},
                            "validFlg": {"type": "boolean", "description": "有効フラグ"}
                        },
                        "required": ["id", "name", "ownerRoleId", "maxJobNum"]
                    }
                },
                "required": ["queue"]
            }
        ),
        Tool(
            name="modify_queue",
            description="ジョブキュー更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "queueId": {"type": "string"},
                    "queue": {"type": "object"}
                },
                "required": ["queueId", "queue"]
            }
        ),
        Tool(
            name="delete_queue",
            description="ジョブキュー削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "queueIds": {"type": "string"}
                },
                "required": ["queueIds"]
            }
        ),
        Tool(
            name="queue_activity_search",
            description="キューアクティビティ検索",
            inputSchema={
                "type": "object",
                "properties": {
                    "request": {"type": "object"}
                },
                "required": ["request"]
            }
        ),
        Tool(
            name="queue_activity_detail",
            description="キュー内容詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "queueId": {"type": "string"}
                },
                "required": ["queueId"]
            }
        ),
        # --- 11. ジョブ連携送信設定 ---
        Tool(
            name="get_joblinksend_setting_list",
            description="送信設定一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "ownerRoleId": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_joblinksend_setting_detail",
            description="送信設定詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "joblinkSendSettingId": {"type": "string"}
                },
                "required": ["joblinkSendSettingId"]
            }
        ),
        Tool(
            name="add_joblinksend_setting",
            description="送信設定追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "setting": {"type": "object"}
                },
                "required": ["setting"]
            }
        ),
        Tool(
            name="modify_joblinksend_setting",
            description="送信設定更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "joblinkSendSettingId": {"type": "string"},
                    "setting": {"type": "object"}
                },
                "required": ["joblinkSendSettingId", "setting"]
            }
        ),
        Tool(
            name="delete_joblinksend_setting",
            description="送信設定削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "joblinkSendSettingIds": {"type": "string"}
                },
                "required": ["joblinkSendSettingIds"]
            }
        ),
        # --- 12. ジョブ連携メッセージ管理 ---
        Tool(
            name="regist_joblink_message",
            description="メッセージ登録",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "object"}
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="send_joblink_message_manual",
            description="手動メッセージ送信",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "object"}
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="joblink_message_search",
            description="メッセージ一覧検索",
            inputSchema={
                "type": "object",
                "properties": {
                    "request": {"type": "object"}
                },
                "required": ["request"]
            }
        ),
        # --- 13. 操作権限確認 ---
        Tool(
            name="available_start_operation",
            description="ジョブ開始操作権限確認",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId"]
            }
        ),
        Tool(
            name="available_start_operation_node",
            description="ノード開始操作権限確認",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "facilityId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId", "facilityId"]
            }
        ),
        Tool(
            name="available_stop_operation",
            description="ジョブ停止操作権限確認",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId"]
            }
        ),
        Tool(
            name="available_stop_operation_node",
            description="ノード停止操作権限確認",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "facilityId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId", "facilityId"]
            }
        ),
        # --- 14. RPAシナリオジョブ管理 ---
        Tool(
            name="get_rpa_login_resolution",
            description="RPAログイン解像度一覧取得",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_rpa_screenshot",
            description="RPAスクリーンショット取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "facilityId": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId", "facilityId"]
            }
        ),
        Tool(
            name="get_rpa_screenshot_file",
            description="RPAスクリーンショットファイルダウンロード",
            inputSchema={
                "type": "object",
                "properties": {
                    "sessionId": {"type": "string"},
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "facilityId": {"type": "string"},
                    "regDate": {"type": "string"}
                },
                "required": ["sessionId", "jobunitId", "jobId", "facilityId", "regDate"]
            }
        ),
        # --- 15. その他 ---
        Tool(
            name="get_jobmap_icon_image_iconId",
            description="ジョブマップアイコン一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "ownerRoleId": {"type": "string"}
                }
            }
        ),
        Tool(
            name="delete_premakejobsession",
            description="プリメイクジョブセッション削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickId": {"type": "string"}
                },
                "required": ["jobkickId"]
            }
        ),
        Tool(
            name="get_schedule_plan",
            description="スケジュール計画一覧取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "plan": {"type": "object"}
                },
                "required": ["plan"]
            }
        ),
        Tool(
            name="get_job_referrer_queue",
            description="ジョブキューの参照情報取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "queueId": {"type": "string"}
                },
                "required": ["queueId"]
            }
        ),
        Tool(
            name="queue_search",
            description="ジョブキュー設定検索",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {"type": "object"}
                },
                "required": ["search"]
            }
        ),
        # --- 16. ジョブ更新API（各ジョブタイプ） ---
        Tool(
            name="modify_jobnet",
            description="ジョブネット更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "jobnet": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "jobnet"]
            }
        ),
        Tool(
            name="modify_command_job",
            description="コマンドジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_file_job",
            description="ファイル転送ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_refer_job",
            description="参照ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_monitor_job",
            description="監視ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_approval_job",
            description="承認ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_joblinksend_job",
            description="ジョブ連携送信ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_joblinkrcv_job",
            description="ジョブ連携待機ジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_filecheck_job",
            description="ファイルチェックジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        Tool(
            name="modify_rpa_job",
            description="RPAシナリオジョブ更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobunitId": {"type": "string"},
                    "jobId": {"type": "string"},
                    "job": {"type": "object"}
                },
                "required": ["jobunitId", "jobId", "job"]
            }
        ),
        # --- 17. ジョブキック詳細取得・更新API ---
        Tool(
            name="get_schedule_detail",
            description="スケジュール詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"}
                },
                "required": ["jobKickId"]
            }
        ),
        Tool(
            name="get_filecheck_detail",
            description="ファイルチェック詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"}
                },
                "required": ["jobKickId"]
            }
        ),
        Tool(
            name="get_manual_detail",
            description="手動実行契機詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"}
                },
                "required": ["jobKickId"]
            }
        ),
        Tool(
            name="get_joblinkrcv_detail",
            description="ジョブ連携受信契機詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"}
                },
                "required": ["jobKickId"]
            }
        ),
        Tool(
            name="get_kick_detail",
            description="ジョブキック詳細取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"}
                },
                "required": ["jobKickId"]
            }
        ),
        Tool(
            name="modify_schedule",
            description="スケジュール更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"},
                    "schedule": {"type": "object"}
                },
                "required": ["jobKickId", "schedule"]
            }
        ),
        Tool(
            name="modify_filecheck",
            description="ファイルチェック更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"},
                    "filecheck": {"type": "object"}
                },
                "required": ["jobKickId", "filecheck"]
            }
        ),
        Tool(
            name="modify_manual",
            description="手動実行契機更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"},
                    "manual": {"type": "object"}
                },
                "required": ["jobKickId", "manual"]
            }
        ),
        Tool(
            name="modify_joblinkrcv",
            description="ジョブ連携受信契機更新",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobKickId": {"type": "string"},
                    "joblinkrcv": {"type": "object"}
                },
                "required": ["jobKickId", "joblinkrcv"]
            }
        ),
        Tool(
            name="delete_schedule",
            description="スケジュール削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickIds": {"type": "string"}
                },
                "required": ["jobkickIds"]
            }
        ),
        Tool(
            name="delete_filecheck",
            description="ファイルチェック削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickIds": {"type": "string"}
                },
                "required": ["jobkickIds"]
            }
        ),
        Tool(
            name="delete_manual",
            description="手動実行契機削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickIds": {"type": "string"}
                },
                "required": ["jobkickIds"]
            }
        ),
        Tool(
            name="delete_joblinkrcv",
            description="ジョブ連携受信契機削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobkickIds": {"type": "string"}
                },
                "required": ["jobkickIds"]
            }
        ),
    ]

async def dispatch(name, manager, arguments):
    # 省略: 既存のAPI名に合わせて manager.XXX(**arguments) を呼び出す分岐を追加してください
    # 例:
    if name == "get_job_tree_simple":
        return await manager.get_job_tree_simple(ownerRoleId=arguments.get("ownerRoleId"))
    elif name == "get_job_tree_full":
        return await manager.get_job_tree_full(ownerRoleId=arguments.get("ownerRoleId"))
    elif name == "get_job_info":
        return await manager.get_job_info(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "get_job_info_bulk":
        return await manager.get_job_info_bulk(jobList=arguments.get("jobList"))
    elif name == "add_jobunit":
        return await manager.add_jobunit(jobunit=arguments.get("jobunit"), isClient=arguments.get("isClient"))
    elif name == "modify_jobunit":
        return await manager.modify_jobunit(jobunitId=arguments.get("jobunitId"), jobunit=arguments.get("jobunit"), isClient=arguments.get("isClient"))
    elif name == "delete_jobunit":
        return await manager.delete_jobunit(jobunitId=arguments.get("jobunitId"))
    elif name == "get_edit_lock":
        return await manager.get_edit_lock(jobunitId=arguments.get("jobunitId"), updateTime=arguments.get("updateTime"), forceFlag=arguments.get("forceFlag"))
    elif name == "check_edit_lock":
        return await manager.check_edit_lock(jobunitId=arguments.get("jobunitId"), editSession=arguments.get("editSession"))
    elif name == "release_edit_lock":
        return await manager.release_edit_lock(jobunitId=arguments.get("jobunitId"), editSession=arguments.get("editSession"))
    elif name == "add_jobnet":
        return await manager.add_jobnet(jobunitId=arguments.get("jobunitId"), jobnet=arguments.get("jobnet"))
    elif name == "add_command_job":
        return await manager.add_command_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_file_job":
        return await manager.add_file_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_refer_job":
        return await manager.add_refer_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_monitor_job":
        return await manager.add_monitor_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_approval_job":
        return await manager.add_approval_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_joblinksend_job":
        return await manager.add_joblinksend_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_joblinkrcv_job":
        return await manager.add_joblinkrcv_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_filecheck_job":
        return await manager.add_filecheck_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "add_rpa_job":
        return await manager.add_rpa_job(jobunitId=arguments.get("jobunitId"), job=arguments.get("job"))
    elif name == "delete_job":
        return await manager.delete_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "run_job":
        return await manager.run_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), runJobRequest=arguments.get("runJobRequest"))
    elif name == "run_job_kick":
        return await manager.run_job_kick(jobKickId=arguments.get("jobKickId"), runJobKickRequest=arguments.get("runJobKickRequest"))
    elif name == "session_job_operation":
        return await manager.session_job_operation(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), operation=arguments.get("operation"))
    elif name == "session_node_operation":
        return await manager.session_node_operation(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), facilityId=arguments.get("facilityId"), operation=arguments.get("operation"))
    elif name == "get_session_job_detail":
        return await manager.get_session_job_detail(sessionId=arguments.get("sessionId"))
    elif name == "get_session_node_detail":
        return await manager.get_session_node_detail(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "get_session_file_detail":
        return await manager.get_session_file_detail(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "get_session_job_jobInfo":
        return await manager.get_session_job_jobInfo(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "get_session_job_allDetail":
        return await manager.get_session_job_allDetail(sessionId=arguments.get("sessionId"))
    elif name == "history_search":
        return await manager.history_search(size=arguments.get("size"), filter=arguments.get("filter"))
    elif name == "add_schedule":
        return await manager.add_schedule(schedule=arguments.get("schedule"))
    elif name == "add_filecheck":
        return await manager.add_filecheck(filecheck=arguments.get("filecheck"))
    elif name == "add_manual":
        return await manager.add_manual(manual=arguments.get("manual"))
    elif name == "add_joblinkrcv":
        return await manager.add_joblinkrcv(joblinkrcv=arguments.get("joblinkrcv"))
    elif name == "get_kick_list":
        return await manager.get_kick_list()
    elif name == "kick_search":
        return await manager.kick_search(condition=arguments.get("condition"))
    elif name == "set_kick_valid":
        return await manager.set_kick_valid(setStatus=arguments.get("setStatus"))
    elif name == "delete_kick":
        return await manager.delete_kick(jobkickIds=arguments.get("jobkickIds"))
    elif name == "session_approval_search":
        return await manager.session_approval_search(request=arguments.get("request"))
    elif name == "modify_approval_info":
        return await manager.modify_approval_info(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), info=arguments.get("info"))
    elif name == "get_queue_list":
        return await manager.get_queue_list(roleId=arguments.get("roleId"))
    elif name == "get_queue_detail":
        return await manager.get_queue_detail(queueId=arguments.get("queueId"))
    elif name == "add_queue":
        return await manager.add_queue(queue=arguments.get("queue"))
    elif name == "modify_queue":
        return await manager.modify_queue(queueId=arguments.get("queueId"), queue=arguments.get("queue"))
    elif name == "delete_queue":
        return await manager.delete_queue(queueIds=arguments.get("queueIds"))
    elif name == "queue_activity_search":
        return await manager.queue_activity_search(request=arguments.get("request"))
    elif name == "queue_activity_detail":
        return await manager.queue_activity_detail(queueId=arguments.get("queueId"))
    elif name == "get_joblinksend_setting_list":
        return await manager.get_joblinksend_setting_list(ownerRoleId=arguments.get("ownerRoleId"))
    elif name == "get_joblinksend_setting_detail":
        return await manager.get_joblinksend_setting_detail(joblinkSendSettingId=arguments.get("joblinkSendSettingId"))
    elif name == "add_joblinksend_setting":
        return await manager.add_joblinksend_setting(setting=arguments.get("setting"))
    elif name == "modify_joblinksend_setting":
        return await manager.modify_joblinksend_setting(joblinkSendSettingId=arguments.get("joblinkSendSettingId"), setting=arguments.get("setting"))
    elif name == "delete_joblinksend_setting":
        return await manager.delete_joblinksend_setting(joblinkSendSettingIds=arguments.get("joblinkSendSettingIds"))
    elif name == "regist_joblink_message":
        return await manager.regist_joblink_message(message=arguments.get("message"))
    elif name == "send_joblink_message_manual":
        return await manager.send_joblink_message_manual(message=arguments.get("message"))
    elif name == "joblink_message_search":
        return await manager.joblink_message_search(request=arguments.get("request"))
    elif name == "available_start_operation":
        return await manager.available_start_operation(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "available_start_operation_node":
        return await manager.available_start_operation_node(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), facilityId=arguments.get("facilityId"))
    elif name == "available_stop_operation":
        return await manager.available_stop_operation(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"))
    elif name == "available_stop_operation_node":
        return await manager.available_stop_operation_node(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), facilityId=arguments.get("facilityId"))
    elif name == "get_rpa_login_resolution":
        return await manager.get_rpa_login_resolution()
    elif name == "get_rpa_screenshot":
        return await manager.get_rpa_screenshot(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), facilityId=arguments.get("facilityId"))
    elif name == "get_rpa_screenshot_file":
        return await manager.get_rpa_screenshot_file(sessionId=arguments.get("sessionId"), jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), facilityId=arguments.get("facilityId"), regDate=arguments.get("regDate"))
    elif name == "get_jobmap_icon_image_iconId":
        return await manager.get_jobmap_icon_image_iconId(ownerRoleId=arguments.get("ownerRoleId"))
    elif name == "delete_premakejobsession":
        return await manager.delete_premakejobsession(jobkickId=arguments.get("jobkickId"))
    elif name == "get_schedule_plan":
        return await manager.get_schedule_plan(plan=arguments.get("plan"))
    elif name == "get_job_referrer_queue":
        return await manager.get_job_referrer_queue(queueId=arguments.get("queueId"))
    elif name == "queue_search":
        return await manager.queue_search(search=arguments.get("search"))
    elif name == "modify_jobnet":
        return await manager.modify_jobnet(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), jobnet=arguments.get("jobnet"))
    elif name == "modify_command_job":
        return await manager.modify_command_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_file_job":
        return await manager.modify_file_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_refer_job":
        return await manager.modify_refer_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_monitor_job":
        return await manager.modify_monitor_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_approval_job":
        return await manager.modify_approval_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_joblinksend_job":
        return await manager.modify_joblinksend_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_joblinkrcv_job":
        return await manager.modify_joblinkrcv_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_filecheck_job":
        return await manager.modify_filecheck_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "modify_rpa_job":
        return await manager.modify_rpa_job(jobunitId=arguments.get("jobunitId"), jobId=arguments.get("jobId"), job=arguments.get("job"))
    elif name == "get_schedule_detail":
        return await manager.get_schedule_detail(jobKickId=arguments.get("jobKickId"))
    elif name == "get_filecheck_detail":
        return await manager.get_filecheck_detail(jobKickId=arguments.get("jobKickId"))
    elif name == "get_manual_detail":
        return await manager.get_manual_detail(jobKickId=arguments.get("jobKickId"))
    elif name == "get_joblinkrcv_detail":
        return await manager.get_joblinkrcv_detail(jobKickId=arguments.get("jobKickId"))
    elif name == "get_kick_detail":
        return await manager.get_kick_detail(jobKickId=arguments.get("jobKickId"))
    elif name == "modify_schedule":
        return await manager.modify_schedule(jobKickId=arguments.get("jobKickId"), schedule=arguments.get("schedule"))
    elif name == "modify_filecheck":
        return await manager.modify_filecheck(jobKickId=arguments.get("jobKickId"), filecheck=arguments.get("filecheck"))
    elif name == "modify_manual":
        return await manager.modify_manual(jobKickId=arguments.get("jobKickId"), manual=arguments.get("manual"))
    elif name == "modify_joblinkrcv":
        return await manager.modify_joblinkrcv(jobKickId=arguments.get("jobKickId"), joblinkrcv=arguments.get("joblinkrcv"))
    elif name == "delete_schedule":
        return await manager.delete_schedule(jobkickIds=arguments.get("jobkickIds"))
    elif name == "delete_filecheck":
        return await manager.delete_filecheck(jobkickIds=arguments.get("jobkickIds"))
    elif name == "delete_manual":
        return await manager.delete_manual(jobkickIds=arguments.get("jobkickIds"))
    elif name == "delete_joblinkrcv":
        return await manager.delete_joblinkrcv(jobkickIds=arguments.get("jobkickIds"))