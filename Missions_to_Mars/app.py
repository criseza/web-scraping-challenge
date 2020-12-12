# Dependencies
import pymongo
from flask import Flask, Markup, redirect, render_template, url_for

import scrape_mars

# Connect to Flask
app = Flask(__name__)

# Connect to database
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    mars_dict = {}
    mars_dict = db.mars.find_one()
    is_empty=False

    # Check if it is the first time so the dictionary doesn't have any information
    if not bool(mars_dict):
        is_empty = True
        print("Dictionary is empty.")

    return render_template("index.html", mars=mars_dict, is_empty=is_empty)

@app.route("/scrape")
def scrape():
    # Call the function on the scrape_mars.py
    mars_dict = scrape_mars.scrape()
    # Clean the collection
    db.mars.drop()
    # Save in MongoDB
    db.mars.insert(mars_dict)

    return render_template("index.html", mars=mars_dict)

if __name__ == "__main__":
    app.run(debug=True)
