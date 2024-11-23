from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

# 定義函式來抓取氣象資料
def fetch_weather_data():
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-B0D1A24B-49E4-4FEA-ABA3-D7E7C8E8B1B1&locationName=&elementName='
    response = requests.get(url)
    if response.status_code == 200:
        data_json = response.json()
        location = data_json.get('records', {}).get('location', [])
        return [
            {
                "city": i['locationName'],
                "weather": i['weatherElement'][0]['time'][0]['parameter']['parameterName'],
                "max_temp": i['weatherElement'][1]['time'][0]['parameter']['parameterName'],
                "min_temp": i['weatherElement'][2]['time'][0]['parameter']['parameterName'],
                "comfort": i['weatherElement'][3]['time'][0]['parameter']['parameterName'],
                "rain_probability": i['weatherElement'][4]['time'][0]['parameter']['parameterName'],
            }
            for i in location
        ]
    else:
        return []

# 路由
@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = fetch_weather_data()
    result = None
    if request.method == "POST":
        city = request.form.get("city")  # 從表單獲取輸入的城市名稱
        if city:
            result = next((item for item in weather_data if city in item["city"]), None)
            if not result:
                result = {"error": f"No data found for city: {city}"}
    return render_template("weatherrepo.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.getenv('PORT', 5000))  # 預設埠號為 5000
    app.run(host='0.0.0.0', port=port)  # 確保綁定到 0.0.0.0
    