from sqlalchemy.ext.declarative import declarative_base
from models.trip import Trip
from utils.functions import parse_point

import numpy as np
import pandas as pd

def run_migration(session):
    df = pd.read_csv("../data/trips.csv")
    
    df[["datetime"]] = df[["datetime"]].apply(pd.to_datetime)

    df[["origin_x", "origin_y"]] = df["origin_coord"].apply(lambda x: pd.Series(parse_point(x)))
    df[["destination_x", "destination_y"]] = df["destination_coord"].apply(lambda x: pd.Series(parse_point(x)))

    trips = [
        Trip(
            region=row["region"],
            origin_x=row["origin_x"],
            origin_y=row["origin_y"],
            destination_x=row["destination_x"],
            destination_y=row["destination_y"],
            datasource=row["datasource"]
        )
        for index, row in df.iterrows()
    ]

    session.add_all(trips)

    return session

