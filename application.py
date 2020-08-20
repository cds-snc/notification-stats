import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

# DB conection string
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", 'postgresql://postgres@localhost/notification_api')

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(application)

NOTIFICATION_TYPE = ['email', 'sms']
notification_types = db.Enum(*NOTIFICATION_TYPE, name='notification_type')


class NotificationHistory(db.Model):
    __tablename__ = 'notifications' # history table empty locally

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('services.id'), index=True, unique=False)
    # service = db.relationship('Service')
    notification_type = db.Column(notification_types, index=True, nullable=False)
    created_at = db.Column(db.DateTime, index=True, unique=False, nullable=False)
    sent_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def __repr__(self):
        return '<Notification %r>' % self.id


@application.route('/')
def hello():
    try:
        return("len: {}".format(len(NotificationHistory.query.all())))
    except:
        return("Had an error connecting to database")


if __name__ == '__main__':
    application.run()
