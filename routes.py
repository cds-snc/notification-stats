import sys

from flask_setup import application
from models import NotificationHistory, Organisation, Service

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


# Notifications related routes
@application.route('/notifications-by-type')
def get_notifications_by_type():
    notifications_email = NotificationHistory.query.filter(NotificationHistory.notification_type=="email").all()
    notifications_sms = NotificationHistory.query.filter(NotificationHistory.notification_type=="sms").all()

    try:
        response = {
            'email': len(notifications_email),
            'sms': len(notifications_sms)
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


# Organisation
@application.route('/organisations')
def get_list_of_organisations():
    return("unfinished")
