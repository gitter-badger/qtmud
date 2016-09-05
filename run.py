#!/usr/bin/python3.5

import sys
import os
import logging

sys.path.insert(0, os.path.abspath('../'))

import qtmud
from qtmud.services.parser import Parser
from qtmud.services.mudsocket import MUDSocket
from qtmud.qualities import Client

if __name__ == '__main__':
    # Main launch script
    try:
        # Create engine manager
        print('instancing Manager()')
        manager = qtmud.Manager()
        qtmud.manager = manager
        manager.log.info('Manager() instanced @ qtmud.manager')
        # tell qtmud.manager to add servicese (instance & if applicable start)
        manager.add_services(MUDSocket, Parser)
        # ---
        # ---
        # testing goes here
        # ---
        # ---
        # Run engine manager
        manager.run()
    except KeyboardInterrupt as err:
        manager.log.info('{0} received, shutting down.'.format(err))
        for service in manager.services:
            try:
                service.shutdown()
                manager.log.info('{0} succesfully shutdown()'.format(service))
            except Exception:
                manager.log.info('no shutdown() function for '
                    '{0}'.format(service))
        exit()
