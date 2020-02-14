# Create Flask API for Climate Analysis

# Dependencies
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

# Flask setup 
app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect existing database into new model
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

# Save references to tables
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Welcome to the Hawaii Climate API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Specify a start date in the format yyyy-mm-dd in the URL below when executing to get min, avg, max temps.<br/>"
        f"/api/v1.0/start_date<br/>"
        f"<br/>"
        f"Specify a start and end date in the format yyyy-mm-dd in the URL below when executing to get min, avg, max temps.<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to database
    session = Session(engine)

    """Return list of all dates and precipitation amounts in the last year"""
    results = session.query(Measurement.date, func.sum(Measurement.prcp))\
                            .filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).all()

    session.close()

    # Create dictionary of raw data and append to list of precipitation_results
    precipitation_results = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date]= prcp
        precipitation_results.append(prcp_dict)

    return jsonify(precipitation_results)

@app.route("/api/v1.0/stations")
def station():
    # Create session link from Python to database
    session = Session(engine)

    """Return list of all distinct stations in database"""
    results = session.query(Measurement.station).distinct().all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return list of all temperatures for previous year in database"""
    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23' ).filter(Measurement.station == 'USC00519281').all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start_date>")
def calc_temp(start_date):
    session = Session(engine)

    """Return list of all min, avg, and max temperature after given start date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= start_date).all()

    session.close()

    return jsonify(results)                     

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    session = Session(engine)

    """Return list of all min, avg, and max temperature between given start and end date inclusive"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    return jsonify(results)
    
if __name__ == '__main__':
    app.run(debug=True)





