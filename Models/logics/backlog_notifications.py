import string
import urllib.parse
import requests

def notify_backlog_issue(api_key: string, issue_id: string):
    try:
        url = 'https://opst.backlog.jp/api/v2/issues/{issue_id}/comments'.format(issue_id=issue_id)
        url = url + '?' + urllib.parse.urlencode({'apiKey':api_key})

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded '
        }

        params = {
            'content': '【Backlog通知用】レシートの画像認識完了しました。'
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code != 201:
            raise Exception
    except Exception as e:
        print(e)
