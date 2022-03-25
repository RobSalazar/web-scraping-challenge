#Import modules
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Set up flask
app = Flask(__name__)


client = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = client.db.mars_data.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = client.db.mars_data
    mars = scrape_mars.scrape()
    mars_data.update_one({}, {"$set": mars}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)