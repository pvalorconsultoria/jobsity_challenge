from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ReportWeeklyAverage(db.Model):
    __tablename__ = 'report_weekly_average'
    id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String(100))
    region = db.Column(db.String(100))
    route = db.Column(db.String(100))
    bounding_box_id = db.Column(db.Integer())
    weekly_average = db.Column(db.Float())

    def to_dict(self):
        return {
            'id': self.id,
            'report': self.report,
            'region': self.region,
            'route': self.route,
            'bounding_box_id': self.bounding_box_id,
            'weekly_average': self.weekly_average
        }
