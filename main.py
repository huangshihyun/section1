import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 替換成你的 Channel Secret 和 Access Token
line_bot_api = LineBotApi('phINNsVm5oJ7jYVWTeIM2ah557Q8bo9C19n9i/z9wzQirxWbyVo4iM4/FKQAURL6btlstUdAgkC6oPaPsRuQj9CkN0QetBg7rxuwmq/lxYKyqy1zHa/brZbDrF/jRI/PHQt34sx0lNj0actWf2kjdAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8ff5fdedc984d306f913486b4768825')
NEWS_API_KEY = '1241266abd9e4c61bdf7a71a149615e0'  # 替換成你的 NewsAPI Key

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received_text = event.message.text
    news = get_news(received_text)
    if news:
        reply_text = '\n'.join([f"{i+1}. {article['title']}" for i, article in enumerate(news[:5])])
    else:
        reply_text = '抱歉，無法獲取新聞資訊。'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
