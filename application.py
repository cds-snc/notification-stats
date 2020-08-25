import os
import sys
import datetime

from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

# DB conection string
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", 'postgresql://postgres@localhost/notification_api')

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
CORS(application)

db = SQLAlchemy(application)

NOTIFICATION_TYPE = ['email', 'sms']
notification_types = db.Enum(*NOTIFICATION_TYPE, name='notification_type')


class NotificationHistory(db.Model):
    __tablename__ = 'notifications' # history table empty locally

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('services.id'), index=True, unique=False)
    service = db.relationship('Service')
    notification_type = db.Column(notification_types, index=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, unique=False, nullable=False)
    sent_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def __repr__(self):
        return "<Not {}: {} {}>".format(self.created_at, self.service.name, self.notification_type )

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow)
    active = db.Column(db.Boolean, index=False, unique=False, nullable=False, default=True)
    restricted = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    volume_sms = db.Column(db.Integer(), nullable=True, unique=False)
    volume_email = db.Column(db.Integer(), nullable=True, unique=False)
    count_as_live = db.Column(db.Boolean, nullable=False, default=True)
    organisation_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organisation.id'), index=True, nullable=True)
    # organisation = db.relationship('Organisation', backref='services')

    def __repr__(self):
        return "<Service {} {}>".format(self.name, self.id)


@application.route('/')
def hello():
    services = Service.query.all()
    notifications = NotificationHistory.query.all()

    print(services[:2], file=sys.stdout)
    print(notifications[:5], file=sys.stdout)
    sys.stdout.flush()

    try:
        response = {
            'notifications': len(notifications),
            'services': len(services)
        }
        return(response)
    except:
        resp_error = {
            'error':"Had an error connecting to database"
        }
        return(resp_error)


@application.route('/live-services')
def get_live_services():
    live_services = Service.query.filter(Service.count_as_live == True).all()
    print(live_services)
    
    try:
        response = {
            'live_services': len(live_services)
        }
        return(response)
    except:
        resp_error = {
            'error':"Had an error connecting to database"
        }
        return(resp_error)


# unfinished
@application.route('/notifications-by-month')
def get_notifications_sent_by_month():
    month = func.date_trunc('month', NotificationHistory.sent_at)
    notifications = NotificationHistory.query(func.sum(NotificationHistory.sent_at),extract('month', Loan_Amendment.AmendDate)).first()

    notifications_by_month = {}

    print(notifications)
    
    return("success")

if __name__ == '__main__':
    application.run()
