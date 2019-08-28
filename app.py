#Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import selenium

#Set connection
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/masr_db")
mongo.db.mars.drop()

#route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)
    

@app.route('/scrape')
def scrape():
   
    mongo.db.mars.drop()
    data = scrape_mars.scrape()
    mongo.db.mars.insert_one(
        data
    )
    #mars.insert_one(data)
    
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
