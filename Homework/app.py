import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Hello and welcome to my Hawaiin Vacation Home Page!<br/>"
        f"Here you will be able to inspect the past the weather in <br/> "
        f"Honolulu, Hawaii and decide which days are best to visit<br/>"
        f"Safe Travels<br/>"
        f"<br/>"
        f"Use the following Routes to inspect weather measurements:<br/>"
        f"<br/>"                   
        f"/api/v1.0/precipitation <br/>"     
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def about():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and percipitation"""
    # Query 
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)


# @app.route("/contact")
# def contact():
#     email = "peleke@example.com"

#     return f"Questions? Comments? Complaints? Shoot an email to {email}."


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
