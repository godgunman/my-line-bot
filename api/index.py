from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('WnOAh83Ss4qSMw/6INKsbJnAdHS7Xe8T7qMRJ4bPwrzIEzkRezQDM2ow3KFjsQYqp2YHyvqOAaGdhFllhKLqjkEcRK8Kl/SBjqBGM+9SwDbaeQNahdjrp0TpsK6S3U32kwsr/4YVxTnH9O4nAUFySwdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('4a02436c986b12d55a812b590e515f96')

@app.route("/")
def home():
    return "LINE BOT API Server is running."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()