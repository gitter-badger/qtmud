#!/usr/bin/python3
""" qtmud startup script

    .. versionadded:: 0.0.1
"""


import qtmud
from qtmud.services import mudsocket
import mudlib


if __name__ == '__main__':
    qtmud.log.info('loading core services')
    qtmud.services.loaded.extend([mudsocket])
    if mudlib.startup_services:
        qtmud.log.info('loading mudlib services')
        for service in mudlib.startup_services:
            qtmud.services.loaded.extend([service])
    qtmud.log.info('adding subscriptions')
    for sub in qtmud.subscriptions:
        qtmud.subscribe(sub)
    qtmud.log.info('binding mudsocket')
    if qtmud.services.mudsocket.bind(('localhost', 5787)):
        qtmud.log.info('running qtmud.services.tick() until interrupt')
        try:
            while True:
                qtmud.services.tick()
        except KeyboardInterrupt as err:
            qtmud.log.critical('keyboard interrupt received, shutting down')
            exit()
    else:
        qtmud.log.error('failed to bind')
        qtmud.log.critical('fatal, shutting down')
        exit()
