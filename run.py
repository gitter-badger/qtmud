#!/usr/bin/python3.5

import sys
import os
import logging

sys.path.insert(0, os.path.abspath('../'))

import qtmud
from qtmud.services.mover import Mover
from qtmud.services.parser import Parser
from qtmud.services.mudsocket import MUDSocket
from qtmud.qualities import Client
from qtmud.qualities import Room

if __name__ == '__main__':
    # Main launch script
    try:
        # Create engine manager
        print('instancing Manager()')
        manager = qtmud.Manager()
        # set up an alias
        qtmud.manager = manager
        manager.log.info('Manager() instanced @ qtmud.manager')
        # instance arguments as tick()able services under qtmud.manager.services
        manager.log.info('instancing services')
        manager.add_services(MUDSocket, Parser, Mover)
        manager.log.info('instancing qtmud.manager.back_room')
        manager.back_room = manager.new_thing(Room)
        # ---
        # ---
        # testing goes here
        print('testing block\n\n'
            '{0} - manager.back_room.contents'
            ''.format(manager.back_room.contents))
        # ---
        # ---
        # Run engine manager
        manager.run()
    except KeyboardInterrupt as err:
        manager.log.info('{0} received, shutting down.'.format(err))
        exit()
