#################################################
# MongoDB and Flask Application
#################################################

from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
from pymongo import MongoClient
import time
import scrape_mars




client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Use flask_pymongo to set up mongo connection
#################################################

# mongo = pymongo(app, uri="mongodb://loalhost:27017/mars_app")
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = pymongo(app)




#################################################
# Flask Routes
#################################################
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route('/')
def index():
	mars = collection.find_one()
	return render_template('index.html', mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route('/scrape')

def scrape():
	scrape_mars.scrape()
	# mars.update({}, mars_data, upsert=True)
	return redirect('/', code = 302)

 

if __name__ == '__main__':
	
	app.run(debug=True)