#!/usr/bin/python3
""" qtmud startup script
"""


import qtmud
from mudlib import starhopper

if __name__ == '__main__':
    qtmud.start()
    if qtmud.active_services[qtmud.services.MUDSocket].bind(('localhost',
                                                             5787)):
        qtmud.log.info('bound mudsocket')
        starhopper.start()
        try:
            while True:
                qtmud.tick()
        except KeyboardInterrupt:
            qtmud.log.critical('keyboard interrupt, shutting down')
            exit()
    else:
        qtmud.log.critical('failed to bind, shutting down')
        exit()
