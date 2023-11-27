from sqlalchemy.ext.declarative import declarative_base

import numpy as np
import pandas as pd

def run_migration():
    from models.bounding_box import BoundingBox

    Base = declarative_base()
    Base.metadata.create_all(engine)

    df = pd.read_csv("../../data/trips.csv")

    df["x_min"] = df["x_min"].astype(float)
    df["y_min"] = df["y_min"].astype(float)
    df["x_max"] = df["x_max"].astype(float)
    df["y_max"] = df["y_max"].astype(float)

    bounding_boxes = [
        BoundingBox(
            x_min=row["x_min"],
            y_min=row["y_min"],
            x_max=row["x_max"],
            y_max=row["y_max"]
        )
        for index, row in df.iterrows()
    ]

    session = Session()
    session.add_all(bounding_boxes)
    session.commit()
    session.close()

if __name__ == "__main__":
    run_migration()