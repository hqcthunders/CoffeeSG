#!/usr/bin/env python3
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


def get_api_key():
    try:
        return os.environ['api_key_google']
    except KeyError:
        raise "Error environ"


def get_coffee(radius=1000, types="cafe"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    location = "?location=10.779614,106.699256"
    radius = "&radius={}".format(radius)
    types = "&types={}".format(types)
    key = "&key={}".format(get_api_key())
    url = url + location + radius + types + key
    r = requests.get(url)
    result = []
    datas = r.json()
    for data in datas["results"]:
        try:
            result.append({"name": data["name"], "rating": data["rating"],
                           "place_id": data["place_id"],
                           "vicinity": data["vicinity"]})
        except KeyError:
            result.append({"name": data["name"], "rating": " ",
                           "place_id": data["place_id"],
                           "vicinity": data["vicinity"]})
    return result


@app.route("/", methods=("GET", "POST"))
def index():
    data = get_coffee()
    if request.method == "POST":
        radius = request.form["radius"]
        types = request.form.get("types")
        data = get_coffee(radius, types)
        return render_template("index.html", coffee=data)
    else:
        return render_template("index.html", coffee=data)


@app.route("/coffee/<id>", methods=("GET", "POST"))
def coffee(id):
    return render_template("coffee.html", ids=[id])


if __name__ == "__main__":
    app.run()
