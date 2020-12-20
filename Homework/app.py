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
# #################################################


#   * Home page.

#   * List all routes that are available.
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Hello and welcome to my Hawaiin Vacation Home Page!<br/>"
        f"Here you will be able to inspect the past weather in <br/> "
        f"Honolulu, Hawaii and decide which days are best to visit.<br/>"
        f"Safe Travels.<br/>"
        f"<br/>"
        f"Use the following Routes to inspect weather measurements:<br/>"
        f"<br/>"                   
        f"/api/v1.0/precipitation <br/>"     
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start_date/<start_date> <br/>"
        f"/api/v1.0/start_date/end_date/<start_date> <end_date><br/>"
    )
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def about():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and percipitation"""
    # Query 
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into dict
    dates_precipitation_all = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict['date'] = date
        rain_dict['prcp'] = prcp
        dates_precipitation_all.append(rain_dict)


    return jsonify(dates_precipitation_all)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def capture():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query 
    results = session.query(measurement.station).group_by(measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the most active station temperatures for last year of data"""
    # Query 
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date > '2016-08-22').order_by(measurement.date).all()

    session.close()
    # Convert list of tuples into normal list
     # Convert list of tuples into dict
    dates_temps_all = []
    for date, tobs in results:
        temps_dict = {}
        temps_dict['date'] = date
        temps_dict['tobs'] = tobs
        dates_temps_all.append(temps_dict)
    return jsonify(dates_temps_all)

# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


import datetime
@app.route("/api/v1.0/start_date/<start_date>")
def start_calc_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d    
    Returns:
        TMIN, TAVE, and TMAX
    """

    """ End point is YYYY-mm-dd = search_term = convert to string with datetime.datetime = start_date """
    t = datetime.datetime(start_date)
    start_date = t.strftime('%Y-%m-%d')
    
    session = Session(engine)
    session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    '''return jsonify({"error": f"The Date entered for /api/v1.0/<start> {start_date} not found."}), 404'''

    return jsonify(start_calc_temps(start_date))
                # f'The minimum temperature from {start_date} you choose is {start_calc_temps(start_date)[0]}.<br/>'
                # f'The average temperature is {start_calc_temps(start_date)[1]}.<br/>'
                # f'The maximum temperature is {start_calc_temps(start_date)[2]}.'
                # )

    

# @app.route("/api/v1.0/<start>/<end>")
# def calc_temps(start_date, end_date):

#     """TMIN, TAVG, and TMAX for a list of dates.
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
#     return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

#     return jsonify({"error": f"The Date entered for /api/v1.0/<start>/<end> {<start>/<end>} not found."}), 404


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
