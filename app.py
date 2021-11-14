import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# .envファイルの内容を環境変数としてos.environ辞書に追加。
# ファイルが見つからないなら親へ親へと辿っていく
load_dotenv()

# ぼっとトークンとソケットモードハンドラーを使ってアプリを初期化
app = App(token=os.environ.get('SLACK_BOT_TOKEN'))


# 'hello' を含むメッセージをリッスン
# 指定可能なリスナーのメソッド引数の一蘭は以下のモジュールドキュメント参考
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message('hello')
def message_hello(message, say):
  # イベントがトリガーされたチャンネルへ say() でメッセージを送信
  say(
    blocks=[
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
        "accessory": {
          "type": "button",
          "text": {"type": "plain_text", "text": "Click Me"},
          "action_id": "button_click"
        }
      }
    ],
    text=f"Hey there <@{message['user']}>!"
  )

@app.action("button_click")
def action_button_click(body, ack, say):
  # アクションを確認したことを即時で応答します
  ack()
  # チャンネルにメッセージを投稿します
  say(f"<@{body['user']['id']}> にゃのだよ")


# アプリを起動
if __name__ == '__main__':
  SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()
