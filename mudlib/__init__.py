from mudlib import starhopper
from mudlib import yeolderpg

MUDLIB = starhopper

START_LOCATION = MUDLIB.START_LOCATION
startup_services = MUDLIB.startup_services


def handle_client(client):
    return MUDLIB.handle_client(client)