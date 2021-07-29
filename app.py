# Import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy.sql.expression import distinct

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Reflect on existing database
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Flask routes - list all available routes under home page
@app.route("/")
def welcome():    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the DB
    session = Session(engine)

    # Query dates and precipitation
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from row data and append to list
    prcp_list = []
    for date, prcp in prcp_query:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)

    # Query stations
    station_query = session.query(distinct(Station.name)).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_query))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    
    # Calculate date for last year of data
    # recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query data for most active location over the last year
    most_active = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_prior).filter(Measurement.station == 'USC00519281').all()
    session.close()

    # Convert list of tuples into normal list
    activity = list(np.ravel(most_active))
    
    return jsonify(activity)

    

if __name__ == '__main__':
    app.run(debug=True)







