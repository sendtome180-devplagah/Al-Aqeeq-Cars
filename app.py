import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ----------------------------------------------------------
# إعدادات خادم البريد الإلكتروني (Gmail SMTP)
# ----------------------------------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# قراءة البيانات من متغيرات البيئة في Render
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")


def send_showroom_email(subject, body_text, files=None):
"""إرسال البريد الإلكتروني مع إمكانية إرفاق ملفات"""

try:
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = subject

msg.attach(MIMEText(body_text, "plain", "utf-8"))

if files:
for file in files:
if file.filename == "":
continue

part = MIMEBase("application", "octet-stream")
part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header(
"Content-Disposition",
f'attachment; filename="{file.filename}"'
)
msg.attach(part)
file.seek(0)

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)
server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
server.quit()

return True

except Exception as e:
print("خطأ أثناء إرسال البريد:", e)
return False


@app.route("/")
def index():
return render_template("index.html")


# استقبال طلب شراء سيارة
@app.route("/submit_quote", methods=["POST"])
def submit_quote():

client_name = request.form.get("client_name")
client_phone = request.form.get("client_phone")
car_requested = request.form.get("car_requested")
client_notes = request.form.get("client_notes")

subject = f"طلب شراء جديد: {car_requested}"

body = f"""
تم استلام طلب شراء سيارة جديد

اسم العميل:
{client_name}

رقم الجوال:
{client_phone}

السيارة المطلوبة:
{car_requested}

ملاحظات:
{client_notes}
"""

if send_showroom_email(subject, body):
return jsonify({
"status": "success",
"message": "تم إرسال الطلب بنجاح"
})

return jsonify({
"status": "error",
"message": "فشل إرسال البريد، تحقق من الإعدادات"
})


# استقبال طلب بيع سيارة
@app.route("/submit_sell_car", methods=["POST"])
def submit_sell_car():

seller_name = request.form.get("seller_name")
seller_phone = request.form.get("seller_phone")
car_details = request.form.get("car_details")
expected_price = request.form.get("expected_price")

uploaded_files = request.files.getlist("car_images")

subject = f"عرض سيارة للبيع: {car_details}"

body = f"""
تم استلام عرض سيارة للبيع

اسم البائع:
{seller_name}

رقم الجوال:
{seller_phone}

تفاصيل السيارة:
{car_details}

السعر المطلوب:
{expected_price} ريال سعودي
"""

if send_showroom_email(subject, body, uploaded_files):
return jsonify({
"status": "success",
"message": "تم إرسال البيانات والصور بنجاح"
})

return jsonify({
"status": "error",
"message": "فشل إرسال البريد"
})


if __name__ == "__main__":
app.run(debug=True)
