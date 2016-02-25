from flask import Flask, render_template, json, request
import requests
import urllib, json

_name = ""
_email = ""
_city = ""
_animal = ""
_weather = ""
_giphy = ""

app = Flask(__name__)

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signUp():

    global _name
    global _email
    global _city
    global _animal
    global _weather
    global _giphy

    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _city = request.form['inputCity']
    _animal = request.form['inputAnimal']

    # Weather info
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    payload = {"q": str(_city), "units":"metric", "appid": "44db6a862fba0b067b1930da0d769e98"}
    response = requests.get(endpoint, params=payload)
    data = response.json()
    temperature = data["main"]["temp"]
    name = data["name"]
    weather = data["weather"][0]["main"]
    _weather = u"It's {}C in {}, and the sky is {}".format(temperature, name, weather)

    # Giphy https://github.com/Giphy/GiphyAPI
    data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/search?q=ryan+gosling&api_key=dc6zaTOxFJmzC&limit=5").read())
    _giphy = "http://api.giphy.com/v1/gifs/random?fmt=html&tag={}&api_key=dc6zaTOxFJmzC".format(_animal)

    # validate the received values
    if _name and _email and _city and _animal:
        return render_template('user.html', _name=_name, _email=_email, _city=_city, _animal=_animal, _weather=_weather, _giphy=_giphy)
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/thankyou', methods=['POST'])
def thankYou():

    global _name
    global _email
    global _city
    global _animal
    global _weather
    global _giphy

    _sendTo = request.form['inputEmail']

    requests.post(
        "https://api.mailgun.net/v3/sandbox4b9b1d94381b48b4b05732cffa0da0ac.mailgun.org/messages",
        auth=("api", "key-6c19c1c364273bc85bb70777ef854618"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox4b9b1d94381b48b4b05732cffa0da0ac.mailgun.org>",
              "to": "User <"+_sendTo+">",
              "subject": "User details",
              "html": "<iframe src="+_giphy+" width='150px' height='150px' allowFullScreen></iframe>" +
                      "This is a message from "+_name+" from "+_city+", " +
                      "where it looks like: "+_weather

    })

    return render_template('thankyou.html', _name=_name, _email=_sendTo, _city=_city, _animal=_animal, _weather=_weather)

if __name__ == "__main__":
    app.run()
