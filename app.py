from flask import Flask, request, abort

app = Flask(__name__)

# สร้าง Webhook endpoint สำหรับ Line Messaging API
@app.route("/webhook", methods=["POST"])
def webhook():
    # ตรวจสอบความถูกต้องของ signature
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handle_webhook(body, signature)
    return "OK"

def handle_webhook(body, signature):
    # ตรวจสอบความถูกต้องของ signature และ body
    # โดยใช้ Channel Secret ของคุณ
    # ถ้าไม่ถูกต้องให้ raise Exception("Invalid signature")
    
    # ดึงข้อมูลจาก webhook
    events = request.json["events"]
    for event in events:
        if event["type"] == "message":
            handle_message_event(event)

def handle_message_event(event):
    # ดึงข้อความจาก event
    message_text = event["message"]["text"]
    
    # ประมวลผลข้อความ
    # อาจเรียกใช้โมเดลที่คุณได้สร้างขึ้นหรือทำสิ่งอื่นๆ เพื่อตอบกลับผู้ใช้
    response_text = "คุณพูดว่า: " + message_text
    
    # ส่งข้อความกลับไปยังผู้ใช้
    reply_token = event["replyToken"]
    send_message(reply_token, response_text)

def send_message(reply_token, message_text):
    # ส่งข้อความกลับไปยังผู้ใช้โดยใช้ Line Messaging API
    # โดยใช้ Channel Access Token ของคุณ
    # ตัวอย่างนี้ใช้สำหรับข้อความปกติ สามารถปรับปรุงเพื่อใช้กับประเภทข้อความอื่นๆ ได้
    reply_url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "9mfCCWlnBGRerI71QYVkPimqooylc5T0MolaRYLbKJZZxuopqsp7BWH4YzDGgDkBGjISZnjhdZhcbRYDV77mmnZvpxkX/mZ7dn66V5+JQJF9EGA455n5gQyZBhuhs9DK3in8bmE+gszGubEJu5F+BwdB04t89/1O/w1cDnyilFU="
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message_text}]
    }
    response = requests.post(reply_url, headers=headers, json=data)
    response.raise_for_status()

if __name__ == "__main__":
    app.run()
