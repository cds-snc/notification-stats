import os
import datetime

from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from flask_setup import application

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", 'postgresql://postgres@localhost/notification_api')

application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

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
