# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/first-50-year')
def firstyear(): 
    return render_template('first-fifty-year.html')

@app.route('/last-50-year')
def lastyear(): 
    return render_template('last-fifty-year.html')

@app.route('/year-mag')
def yearmag(): 
    return render_template('year-mag.html')

@app.route('/activemap')
def activemap(): 
    return render_template('activemap.html')

if __name__ == "__main__":
    app.run(debug=True)