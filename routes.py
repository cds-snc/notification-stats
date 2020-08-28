import sys
import datetime

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


@application.route('/live-services-by-month')
def get_live_services_by_month():
    services = get_data_by_month(get_live_services_by_go_live_date)

    return(services)


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


@application.route('/notifications-by-month')
def get_notifications_sent_by_month():
    notifications = get_data_by_month(get_notifications_for_month)
    
    return(notifications)


@application.route('/notifications-by-month-and-type')
def get_notifications_sent_by_month_and_type():
    notifications = {}
    notifications = get_data_by_month(get_notifications_by_type_and_month)

    return notifications

def get_data_by_month(which_data):
    # we know we are measuring since november 2019
    year = 2019
    month = 11

    today = datetime.date.today()

    data = {}

    while year <= today.year:
        data[year] = {}
        if year < today.year:
            while month <= 12:
                # print("Month: {}, Year: {}".format(month, year))
                data[year][month] = which_data(month, year)
                month = month + 1
        else:
            while month < today.month:
                # print("Month: {}, Year: {}".format(month, year))
                data[year][month] = which_data(month, year)
                month = month + 1
        
        year = year + 1
        month = 1
    
    return(data)


def get_notifications_for_month(month, year):
    notification_count = len(NotificationHistory.query.filter(func.extract('month', NotificationHistory.sent_at) == month).filter(func.extract('year', NotificationHistory.sent_at) == year).all())
    return notification_count


def get_notifications_by_type_and_month(month, year):
    data = {}

    data["email"] = len(NotificationHistory.query.filter(NotificationHistory.notification_type=="email").filter(func.extract('month', NotificationHistory.sent_at) == month).filter(func.extract('year', NotificationHistory.sent_at) == year).all())
    data["sms"] = len(NotificationHistory.query.filter(NotificationHistory.notification_type=="sms").filter(func.extract('month', NotificationHistory.sent_at) == month).filter(func.extract('year', NotificationHistory.sent_at) == year).all())
    return data


def get_live_services_by_go_live_date(month,year):
    services = len(Service.query.filter(func.extract('month', Service.go_live_at) == month).filter(func.extract('year', Service.go_live_at) == year).all())
    # note - this also counts archived services.. do we want to filter that out?
    return services


# Organisation
@application.route('/organisations')
def get_list_of_organisations():
    organisations = Organisation.query.all()
    try:
        response = {
            'organisations': [organisations.name for organisations in organisations],
        }
        return(response)
    except:
        resp_error = {
            'error':"Had an error connecting to database"
        }
        return(resp_error)
