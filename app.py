from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request-quote', methods=['POST'])
def request_quote():
    data = request.json
    print(f"New Quote Request: {data}")
    return jsonify({"status": "success", "message": "تم إرسال طلبك بنجاح! سنتواصل معك قريباً."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)