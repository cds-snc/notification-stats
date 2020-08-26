import sys

from flask_setup import application
from models import Service, NotificationHistory


@application.route('/')
def hello():
    services = Service.query.all()
    notifications = NotificationHistory.query.all()

    print(services[:2], file=sys.stdout)
    print(notifications[:5], file=sys.stdout)
    sys.stdout.flush()

    try:
        return("Notifications: {} Services: {}".format(len(notifications), len(services)))
    except:
        return("Had an error connecting to database")

