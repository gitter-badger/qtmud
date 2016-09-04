#!/usr/bin/python3.5

import sys
import os
import logging

sys.path.insert(0, os.path.abspath('../'))

import qtmud
from qtmud.services import Service

if __name__ == '__main__':
    # Main launch script
    try:
        # Create engine manager
        print('instancing Manager()')
        manager = qtmud.Manager()
        qtmud.manager = manager
        manager.log.info('Manager() instanced @ qtmud.manager')
        # loading of services goes here
        manager.add_services(Service)
        # ---
        # ---
        #
        # Run engine manager
        manager.run()
    except KeyboardInterrupt as err:
        manager.log.info('{0} received, shutting down.'.format(err))
        exit()
