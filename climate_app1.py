import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

## List all routes that are available.
@app.route("/")
def welcome():
    
    return (
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_D<br/>"
        f"/api/v1.0/startD/endD<br/>"
    )

## Convert the query results to a Dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitations():
    """Return a list of all precipitation date as key and prcp as value"""
    # Query all precipitations
    results_precipitations = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    
    for date, prcp in results_precipitations:
        precipitations_dict = {}
        precipitations_dict["date"] = date
        precipitations_dict["prcp"] = prcp
        all_prcp.append(precipitations_dict)

    return jsonify(all_prcp)

## Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    result_stations = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a dictionary
    stations = []
    
    # r.id , r.station, r.name, r.latitude, r.longitude, r.elevation
    for id, station, name, latitude, longitude, elevation in result_stations:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)

    return jsonify(stations)

## list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # Query all Measurement
    result_tobs = session.query(Measurement.date, Measurement.prcp, Measurement.tobs).all()

    # Create a dictionary from the row data and append to a list of stations
    all_tobs = []
    
    # r.id , r.station, r.name, r.latitude, r.longitude, r.elevation
    for date, prcp, tobs in result_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

## When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start_D>")
def start(start_D):
    result_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_D).all()
    
    temperatures_start = []
    for minimum, average, maximum in result_start:
        start_dict = {}
        start_dict["minimum"] = minimum
        start_dict["average"] = average
        start_dict["maximum"] = maximum
        temperatures_start.append(start_dict)

    return jsonify(temperatures_start)

## When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/<startD>/<endD>")
def end(startD, endD):
    result_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= startD).\
                filter(Measurement.date <= endD).all()
    
    # Convert list of tuples into normal list
    # temperatures_start_end = list(np.ravel(result_start_end))

    temperatures_start_end = []
    for minimum, average, maximum in result_start_end:
        start_dict = {}
        start_dict["minimum"] = minimum
        start_dict["average"] = average
        start_dict["maximum"] = maximum
        temperatures_start_end.append(start_dict)

    return jsonify(temperatures_start_end)
    

if __name__ == '__main__':
    app.run(debug=True)
