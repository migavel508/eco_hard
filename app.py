from flask import Flask, jsonify, request
import gspread
import datetime
import json

app = Flask(__name__)

gc = gspread.service_account(filename='./service_account.json')

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/append_row', methods=['POST'])
def append_row():
    try:
        request_data = request.get_json()
        user_data = [get_current_date_time()] + (request_data.get("data", []) if "data" in request_data else [])

        sh = gc.open("sih_23")
        worksheet = sh.sheet1
        worksheet.append_row(user_data)

        return jsonify({"message": "Row appended successfully."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_data', methods=['GET'])
def get_data():
    sh = gc.open("sih_23")
    worksheet = sh.sheet1
    data = worksheet.get_all_values()

    if data and len(data) > 1:
        header, *rows = data
        result = [dict(zip(header, row)) for row in rows]
    else:
        result = []

    return jsonify({"data": result})

if __name__ == '__main__':
    app.run(debug=True)
