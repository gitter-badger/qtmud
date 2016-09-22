#!/usr/bin/python3
""" qtmud's start & run script
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/parser
        changed :class:`qtmud.Manager.back_room` to be :class:`Village 
        <qtmud.lib.Village>`
    .. versionchanged:: 0.0.2-feature/renderer
        added :class:`Renderer <qtmud.services.renderer.Renderer` to 
        startup services.
    .. versionchanged:: 0.0.3-feature/noise
        added Noise to startup qtmud services.
    .. versionchanged:: 0.0.3-feature/diceroller
        added Fighter to startup library services.
    
    Instances manager, loads services, subscribes them to events
"""

#!/usr/bin/python3.5

import sys
import os

sys.path.insert(0, os.path.abspath('../'))

#pylint: disable=wrong-import-position
import qtmud
from qtmud.services.mover import Mover
from qtmud.services.parser import Parser
from qtmud.services.mudsocket import MUDSocket
from qtmud.services import Renderer
from qtmud.services.sender import Sender
from qtmud.services.noisemaker import Noisemaker


from qtmud.lib import BackRoom


#plylint: enable=wrong-import position



if __name__ == '__main__':
    # Main launch script
    try:
        # Create engine manager
        print('instancing Manager()')
        # pylint says manager here is a constant... is it?
        manager = qtmud.Manager()
        # set up an alias
        qtmud.manager = manager
        manager.log.info('Manager() instanced @ qtmud.manager')
        # instance arguments as tick()able services under qtmud.manager.services
        manager.log.info('instancing qtmud services')
        manager.add_services(MUDSocket, Parser, Mover, Renderer, Sender,
                             Noisemaker)
        manager.log.info('instancing library services')
        manager.log.info('instancing qtmud.manager.back_room')
        manager.back_room= manager.new_thing(BackRoom)
        # ---
        # ---
        # testing goes here)
        # ---
        # ---
        # Run engine manager
        manager.run()
    except KeyboardInterrupt as err:
        manager.log.info('{0} received, shutting down.'.format(err))
        exit()
