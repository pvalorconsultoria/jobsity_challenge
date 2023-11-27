import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from src.models.trip import Trip
from src.models.reports import ReportWeeklyAverage

app = Flask(__name__)

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/api/trips", methods=["GET"])
def get_paginate_trips():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    records = Trip.query.paginate(page, per_page, error_out=False)
    data = [item.to_dict() for item in records.items]

    return jsonify(data)

@app.route("/api/report/weekly_average", methods=["GET"])
def get_report_weekly_average():
    report = request.args.get("report", "all", type=str)
    region = request.args.get("region", "all", type=str)
    route = request.args.get("route", "all", type=str)
    bbox_id = request.args.get("bbox_id", "all", type=str)

    query = ReportWeeklyAverage.query

    if report and report != 'all':
        query = query.filter(ReportWeeklyAverage.report == report)
    if region and region != 'all':
        query = query.filter(ReportWeeklyAverage.region == region)
    if route and route != 'all':
        query = query.filter(ReportWeeklyAverage.route == route)
    if bbox_id and bbox_id != 'all':
        query = query.filter(ReportWeeklyAverage.bounding_box_id == bbox_id)

    results = query.all()

    data = [result.to_dict() for result in results]

    return jsonify(data)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run()