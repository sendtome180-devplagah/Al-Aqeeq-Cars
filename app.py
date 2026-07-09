import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 1. استقبال مسار طلب السعر (الشراء)
@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    # جلب البيانات بالأسماء الجديدة المفعّلة في الـ HTML
    client_name = request.form.get('client_name')
    client_phone = request.form.get('client_phone')
    car_requested = request.form.get('car_requested')
    client_notes = request.form.get('client_notes')

    # طباعة في الـ Logs للتأكد بنسبة 100% أن البيانات وصلت السيرفر بنجاح
    print("\n================ طلب شراء جديد ================")
    print(f"الاسم: {client_name}")
    print(f"الجوال: {client_phone}")
    print(f"السيارة: {car_requested}")
    print(f"ملاحظات: {client_notes}")
    print("===============================================\n")

    # هنا مستقبلاً يمكنك إضافة كود التليجرام أو الإيميل لإعادة التوجيه تلقائياً
    return jsonify({"status": "success", "message": "Received successfully"})

# 2. استقبال مسار عرض سيارة للبيع (مع الصور المتعددة)
@app.route('/submit_sell_car', methods=['POST'])
def submit_sell_car():
    seller_name = request.form.get('seller_name')
    seller_phone = request.form.get('seller_phone')
    car_details = request.form.get('car_details')
    expected_price = request.form.get('expected_price')
    
    # جلب قائمة الصور المرفوعة
    uploaded_files = request.files.getlist('car_images')

    print("\n================ طلب بيع سيارة ================")
    print(f"المعلن: {seller_name}")
    print(f"الجوال: {seller_phone}")
    print(f"المواصفات: {car_details}")
    print(f"السعر المتوقع: {expected_price} ريال")
    print(f"عدد الصور المرفوعة: {len(uploaded_files)}")
    print("===============================================\n")

    return jsonify({"status": "success", "message": "Received successfully"})

if __name__ == '__main__':
    app.run(debug=True)
