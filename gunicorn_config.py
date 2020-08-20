import os


bind = "0.0.0.0:{}".format(os.getenv("PORT"))
accesslog = '-'


def on_starting(server):
    server.log.info("Starting Notifications Stats")


def on_exit(server):
    server.log.info("Stopping Notifications Stats")
