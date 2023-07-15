from flask import Flask, render_template, request
import requests, configparser

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def render_result():
    city_name = request.form['cityName']
    
    api_key = get_api_key()
    data = get_weather_result(city_name, api_key)
    temp = "{0:.0f}".format(data["main"]["temp"])
    feels_like = "{0:.0f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html', location=location, temp=temp, feels_like=feels_like, weather=weather)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_result(city_name, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
