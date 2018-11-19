from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.mars_collection


@app.route("/")
def index():
    mars_facts = db.mars_collection.find_one()
    return render_template("index.html", listings=mars_facts)


@app.route("/scrape")
def scraper():
    listings_data = scrape_mars.scrape()
    print(listings_data)
    print("Scraping complete")
    collection.insert(listings_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
