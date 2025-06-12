from typing import Optional, Dict, Any
from .base import BaseClient

class CalendarClient(BaseClient):

    # 日時フォーマットの変換処理
    def format_hinemos_datetime(iso_datetime: str) -> str:
        """ISO8601形式をHinemos形式（yyyy-MM-dd HH:mm:ss.SSS）に変換"""
        if not iso_datetime:
            return iso_datetime
            
        try:
            from datetime import datetime
            # ISO8601形式をパース（Zタイムゾーンを処理）
            if iso_datetime.endswith('Z'):
                iso_datetime = iso_datetime[:-1] + '+00:00'
            elif 'T' in iso_datetime and '+' not in iso_datetime and 'Z' not in iso_datetime:
                # タイムゾーン情報がない場合はローカル時刻として扱う
                pass
                
            dt = datetime.fromisoformat(iso_datetime)
            # Hinemos形式（yyyy-MM-dd HH:mm:ss.SSS）に変換
            return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # マイクロ秒を切り捨ててミリ秒まで
        except (ValueError, TypeError) as e:
            # 変換に失敗した場合は元の値をそのまま返す
            print(f"警告: 日時フォーマット変換に失敗しました: {iso_datetime}, エラー: {e}")
            return iso_datetime
                
    def get_calendar_list(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        カレンダー一覧取得API (/calendar/calendar)
        Args:
            owner_role_id: オーナーロールID (任意, クエリパラメータ)
        Returns:
            カレンダー情報配列
        レスポンス例:
            [
              {
                "calendarId": "CALENDAR_001",
                "calendarName": "営業日カレンダー",
                "description": "営業日の定義",
                "ownerRoleId": "ADMINISTRATORS",
                "validTimeFrom": "2024-01-01T00:00:00.000Z",
                "validTimeTo": "2024-12-31T23:59:59.999Z",
                "calendarDetailList": []
              }
            ]
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'CalendarRestEndpoints/calendar/calendar', params=params)

    def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """
        カレンダー情報取得API (/calendar/calendar/{calendarId})
        Args:
            calendar_id: カレンダーID (必須, パスパラメータ)
        Returns:
            カレンダー情報
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}"
        return self._make_request('GET', endpoint)

    def add_calendar(self, calendar_info: dict) -> Dict[str, Any]:
        """
        カレンダー追加API (/calendar/calendar)
        Args:
            calendar_info: カレンダー情報(dict)。例:
                {
                "calendarId": "CALENDAR_001",                # 必須, 1-64文字, 英数字/アンダースコア/ハイフン
                "calendarName": "営業日カレンダー",           # 必須, 最大256文字
                "description": "営業日の定義",                # 任意, 最大256文字
                "ownerRoleId": "ADMINISTRATORS",              # 必須, 最大64文字
                "validTimeFrom": "2024-01-01T00:00:00.000Z",  # 必須, ISO8601
                "validTimeTo": "2024-12-31T23:59:59.999Z",    # 必須, ISO8601
                "calendarDetailList": [                       # 任意, 詳細リスト
                    {
                    "orderNo": 1,
                    "year": 2024,
                    "month": 1,
                    "day": 1,
                    "dayType": "SPECIFIC_DAY",                # 例: "SPECIFIC_DAY"
                    "startTime": "09:00",                     # "HH:mm"
                    "endTime": "18:00",                       # "HH:mm"
                    "operateFlg": True,
                    "description": "元日"
                    }
                ]
                }
        Returns:
            作成されたカレンダー情報
        """
        
        # カレンダー情報をコピーして変換処理を適用
        converted_info = calendar_info.copy()
        
        # validTimeFrom と validTimeTo を変換
        if 'validTimeFrom' in converted_info:
            converted_info['validTimeFrom'] = self.format_hinemos_datetime(converted_info['validTimeFrom'])
        
        if 'validTimeTo' in converted_info:
            converted_info['validTimeTo'] = self.format_hinemos_datetime(converted_info['validTimeTo'])

        return self._make_request('POST', 'CalendarRestEndpoints/calendar/calendar', json=converted_info)


    def modify_calendar(self, calendar_id: str, calendar_info: dict) -> Dict[str, Any]:
        """
        カレンダー更新API (/calendar/calendar/{calendarId})
        Args:
            calendar_id: カレンダーID (必須, パスパラメータ)
            calendar_info: カレンダー情報(dict)。add_calendarと同じだがcalendarIdは除く
        Returns:
            更新されたカレンダー情報
        """
        # カレンダー情報をコピーして変換処理を適用
        converted_info = calendar_info.copy()
        
        # validTimeFrom と validTimeTo を変換
        if 'validTimeFrom' in converted_info:
            converted_info['validTimeFrom'] = self.format_hinemos_datetime(converted_info['validTimeFrom'])
        
        if 'validTimeTo' in converted_info:
            converted_info['validTimeTo'] = self.format_hinemos_datetime(converted_info['validTimeTo'])

        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}"
        return self._make_request('PUT', endpoint, json=calendar_info)

    def delete_calendar(self, calendar_ids: list) -> Dict[str, Any]:
        """
        カレンダー削除API (/calendar/calendar)
        Args:
            calendar_ids: 削除するカレンダーIDリスト (必須, クエリパラメータ, カンマ区切り)
                例: ["CALENDAR_001", "CALENDAR_002"]
        Returns:
            削除されたカレンダー情報配列
        """
        params = {"calendarIds": ",".join(calendar_ids)}
        return self._make_request('DELETE', 'CalendarRestEndpoints/calendar/calendar', params=params)

    def get_calendar_month(self, calendar_id: str, year: int, month: int) -> Dict[str, Any]:
        """
        カレンダー月別稼働状態取得API (/calendar/calendar/{calendarId}/calendarDetail_monthOperationState)
        Args:
            calendar_id: カレンダーID (必須, パスパラメータ)
            year: 年 (必須, クエリパラメータ)
            month: 月 (必須, クエリパラメータ)
        Returns:
            月別稼働状態リスト
        レスポンス例:
            [
              {"day": 1, "operationStatus": "ALL_OPERATION"},
              {"day": 2, "operationStatus": "PARTIAL_OPERATION"},
              {"day": 3, "operationStatus": "NOT_OPERATION"}
            ]
        operationStatus値:
            - "ALL_OPERATION": 稼働
            - "PARTIAL_OPERATION": 稼働/非稼働
            - "NOT_OPERATION": 非稼働
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}/calendarDetail_monthOperationState"
        params = {"year": str(year), "month": str(month)}
        return self._make_request('GET', endpoint, params=params)

    def get_calendar_week(self, calendar_id: str, year: int, month: int, day: int) -> Dict[str, Any]:
        """
        カレンダー週情報取得API (/calendar/calendar/{calendarId}/calendarDetail_week)
        Args:
            calendar_id: カレンダーID (必須, パスパラメータ)
            year: 年 (必須, クエリパラメータ)
            month: 月 (必須, クエリパラメータ)
            day: 日 (必須, クエリパラメータ)
        Returns:
            週情報リスト（カレンダー詳細情報配列）
        """
        endpoint = f"CalendarRestEndpoints/calendar/calendar/{calendar_id}/calendarDetail_week"
        params = {"year": str(year), "month": str(month), "day": str(day)}
        return self._make_request('GET', endpoint, params=params)

    def get_calendar_pattern_list(self, owner_role_id: Optional[str] = None) -> Dict[str, Any]:
        """
        カレンダパターン一覧取得API (/calendar/pattern)
        Args:
            owner_role_id: オーナーロールID (任意, クエリパラメータ)
        Returns:
            カレンダーパターン情報配列
        レスポンス例:
            [
              {
                "calPatternId": "PATTERN_001",
                "calPatternName": "週末パターン",
                "ownerRoleId": "ADMINISTRATORS",
                "description": "土日を非稼働とするパターン"
              }
            ]
        """
        params = {}
        if owner_role_id:
            params["ownerRoleId"] = owner_role_id
        return self._make_request('GET', 'CalendarRestEndpoints/calendar/pattern', params=params)

    def get_calendar_pattern(self, calendar_pattern_id: str) -> Dict[str, Any]:
        """
        カレンダパターン情報取得API (/calendar/pattern/{calendarPatternId})
        Args:
            calendar_pattern_id: カレンダパターンID (必須, パスパラメータ)
        Returns:
            カレンダーパターン情報
        """
        endpoint = f"CalendarRestEndpoints/calendar/pattern/{calendar_pattern_id}"
        return self._make_request('GET', endpoint)

    def add_calendar_pattern(self, pattern_info: dict) -> Dict[str, Any]:
        """
        カレンダパターン追加API (/calendar/pattern)
        Args:
            pattern_info: カレンダーパターン情報(dict)。例:
                {
                  "calPatternId": "PATTERN_001",           # 必須, 1-64文字, 英数字/アンダースコア/ハイフン
                  "calPatternName": "週末パターン",        # 必須, 最大256文字
                  "ownerRoleId": "ADMINISTRATORS",         # 必須, 最大64文字
                  "description": "土日を非稼働とするパターン" # 任意, 最大256文字
                }
        Returns:
            作成されたカレンダーパターン情報
        """
        return self._make_request('POST', 'CalendarRestEndpoints/calendar/pattern', json=pattern_info)

    def modify_calendar_pattern(self, calendar_pattern_id: str, pattern_info: dict) -> Dict[str, Any]:
        """
        カレンダパターン更新API (/calendar/pattern/{calendarPatternId})
        Args:
            calendar_pattern_id: カレンダパターンID (必須, パスパラメータ)
            pattern_info: カレンダーパターン情報(dict)。add_calendar_patternと同じだがcalPatternIdは除く
        Returns:
            更新されたカレンダーパターン情報
        """
        endpoint = f"CalendarRestEndpoints/calendar/pattern/{calendar_pattern_id}"
        return self._make_request('PUT', endpoint, json=pattern_info)

    def delete_calendar_pattern(self, calendar_pattern_ids: list) -> Dict[str, Any]:
        """
        カレンダパターン削除API (/calendar/pattern)
        Args:
            calendar_pattern_ids: 削除するカレンダーパターンIDリスト (必須, クエリパラメータ, カンマ区切り)
                例: ["PATTERN_001", "PATTERN_002"]
        Returns:
            削除されたカレンダーパターン情報配列
        """
        params = {"calendarPatternIds": ",".join(calendar_pattern_ids)}
        return self._make_request('DELETE', 'CalendarRestEndpoints/calendar/pattern', params=params)
