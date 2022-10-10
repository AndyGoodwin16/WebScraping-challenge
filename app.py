from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Created an instance of Flask.
app = Flask(__name__)

#Used PyMongo to establish Mongo connection.
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
#Ran data into index.html file.
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
#Used scrape_mars.py to get data and save into Mongo.
def scraper():
    #Created a mars database.
    mars = mongo.db.mars
    #Scrapped data.
    mars_data = scrape_mars.scrape()
    #Updated with newly scraped data.
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)