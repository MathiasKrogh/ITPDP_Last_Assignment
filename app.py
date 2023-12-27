"""Creates a web site summarising dice throws from a Core2"""
import os.path
from flask import Flask, render_template

from db.data_sqlite3 import SQLite3db

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

SQLITE3_DB = os.path.join(ROOT_DIR, "db/data_readings.db")

# Establish a DB depending on the existence of ../secrets/mysql.json
db = SQLite3db(SQLITE3_DB)

app = Flask(__name__)


@app.route('/main')
def homepage():
    """
    Returns html-template and makes a list using a method from data_sqlite3.py which
    returns all the data.
    """
    return render_template('main_page.html', list=db.all_data_readings())

@app.route('/minmax')
def minmax():
    """
    Returns html-template and makes a 5 lists using a methods from data_sqlite3.py which
    returns min and max for TVOC and eCO2 and the latest data.
    """
    return render_template('min_and_max.html',
    minTvoc=db.min_tvoc(),
    maxTvoc=db.max_tvoc(),
    minEco2=db.min_eco2(),
    maxEco2=db.max_eco2(),
    latestData=db.latest()
    )

if __name__ == "__main__":
    app.run(debug=True)
