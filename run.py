#!/usr/bin/python3
""" qtmud startup script

    .. versionadded:: 0.0.1
"""


import qtmud
from mudlib import starhopper

if __name__ == '__main__':
    if qtmud.active_services[qtmud.services.MUDSocket].bind(('localhost',
                                                             5787)):
        try:
            while True:
                qtmud.tick()
        except KeyboardInterrupt:
            qtmud.log.critical('keyboard interrupt, shutting down')
            exit()
    else:
        qtmud.log.critical('failed to bind, shutting down')
        exit()
