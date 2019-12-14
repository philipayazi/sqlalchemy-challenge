import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import json
from decimal import Decimal

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
        f'Welcome to Hawaii Climate App<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/2016-8-23/2017-8-23<br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    
    session = Session(engine)

    duration = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    twelve_mo_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= duration).all()

    session.close()

    return jsonify(twelve_mo_precipitation)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    stations = session.query(Station.name).all()

    session.close()

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    duration = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    one_year_temp_readings = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= duration).all()

    session.close()

    return jsonify(one_year_temp_readings)


@app.route('/api/v1.0/2016-8-23/2017-8-23')
def trip():

    session = Session(engine)

    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.
        
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
            
        Returns:
            TMIN, TAVE, and TMAX
        """
        
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # function usage example
    temp_results = calc_temps('2016-8-23', '2017-8-23')

    session.close()

    return jsonify(temp_results)




if __name__ == "__main__":
    app.run(debug=True)