import qtmud
from mudlib.starhopper import ship, starsystem


START_LOCATION = starsystem.apply(qtmud.new_thing())
startup_services = None

STARHOPPER_SPLASH = """
  *S * T * A * R *     * H * O * P * P * E * R\n\n\n

Welcome to STARHOPPER, one of qtmud's testing libraries.\n
To get started, "scan" your local system.
"""

def handle_client(client):
    player = client
    player = ship.apply(player)
    qtmud.schedule('send',
                   recipient=player,
                   text=STARHOPPER_SPLASH)
    qtmud.schedule('warp',
                   ship=player,
                   destination=START_LOCATION)
    return player