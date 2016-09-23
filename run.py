#!/usr/bin/python3


import qtmud
from qtmud.services import mudsocket, noisemaker, mover


if __name__ == '__main__':
    qtmud.log.info('loading core services')
    qtmud.services.loaded.extend([mudsocket, noisemaker])
    qtmud.log.info('adding subscriptions')
    qtmud.subscribe(qtmud.services.send,
                    mover.move,
                    mudsocket.process_client_input)
    qtmud.log.info('binding mudsocket')
    qtmud.services.mudsocket.bind(('localhost', 5787))
    qtmud.log.info('running qtmud.services.tick() until interrupt')
    try:
        while True:
            qtmud.services.tick()
    except KeyboardInterrupt as err:
        qtmud.log.critical('keyboard interrupt received, shutting down')
        exit()
