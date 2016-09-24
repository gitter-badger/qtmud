from mudlib import starhopper
from mudlib import yeolderpg


# change this to change which library clients get sent to
MUDLIB = starhopper


START_LOCATION = MUDLIB.START_LOCATION
startup_services = MUDLIB.startup_services

def add_client(client):
    return MUDLIB.add_client(client)

def remove_client(client):
    return MUDLIB.remove_client(client)