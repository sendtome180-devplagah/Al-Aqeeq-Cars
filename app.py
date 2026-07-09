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

# 1. البريد الذي سيقوم بـ (الإرسال) - ضع بريد جي ميل الخاص بك هنا
SENDER_EMAIL = "your_email@gmail.com"  

# 2. كلمة مرور التطبيقات (App Password) وليس كلمة مرور حسابك العادية
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  

# 3. البريد الذي سيقوم بـ (الاستقبال) - بريدك الحالي للمتابعة والطلب
RECEIVER_EMAIL = "almatrafi12@gmail.com"  
# ----------------------------------------------------------

def send_showroom_email(subject, body_text, files=None):
    """دالة برمجية احترافية لإرسال النصوص والملفات والصور عبر البريد"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        
        # ربط نص الرسالة بترميز العربي الصحيح
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
        
        # إذا كان هناك صور مرفوعة من الزبون، يتم إرفاقها بالبريد هنا
        if files:
            for file in files:
                if file.filename == '':
                    continue
                part = MIMEBase('application', "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={file.filename}')
                msg.attach(part)
                file.seek(0) # إعادة مؤشر الملف لأوله
        
        # الاتصال بخادم جوجل الآمن لشحن الرسالة
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"خطأ أثناء محاولة إرسال البريد: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')


# مسار استقبال طلبات شراء السيارات (عروض الأسعار)
@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    client_name = request.form.get('client_name')
    client_phone = request.form.get('client_phone')
    car_requested = request.form.get('car_requested')
    client_notes = request.form.get('client_notes')

    subject = f"🔔 طلب شراء جديد: {car_requested}"
    body = f"""
    مرحباً، وصلك طلب تسعيرة جديدة من واجهة المعرض:
    
    اسم العميل: {client_name}
    رقم الجوال: {client_phone}
    السيارة المطلوبة: {car_requested}
    تفاصيل إضافية: {client_notes}
    """
    
    if send_showroom_email(subject, body):
        return jsonify({"status": "success", "message": "تم إرسال الطلب لبريدك"})
    else:
        return jsonify({"status": "error", "message": "فشل إرسال البريد، تحقق من الإعدادات"})


# مسار استقبال طلبات بيع السيارات (مع رفع الصور المتعددة)
@app.route('/submit_sell_car', methods=['POST'])
def submit_sell_car():
    seller_name = request.form.get('seller_name')
    seller_phone = request.form.get('seller_phone')
    car_details = request.form.get('car_details')
    expected_price = request.form.get('expected_price')
    
    # جلب قائمة الصور التي رفعها المستخدم
    uploaded_files = request.files.getlist('car_images')

    subject = f"🚗 عرض سيارة للبيع: {car_details}"
    body = f"""
    مرحباً، قام أحد العملاء بعرض سيارته للبيع عبر الموقع:
    
    اسم المعلن: {seller_name}
    رقم جوال المعلن: {seller_phone}
    تفاصيل ومواصفات السيارة: {car_details}
    السعر المتوقع للبيع: {expected_price} ريال سعودي
    """
    
    if send_showroom_email(subject, body, files=uploaded_files):
        return jsonify({"status": "success", "message": "تم إرسال تفاصيل السيارة وصورها لبريدك"})
    else:
        return jsonify({"status": "error", "message": "فشل رفع وإرسال البريد"})

if __name__ == '__main__':
    app.run(debug=True)
