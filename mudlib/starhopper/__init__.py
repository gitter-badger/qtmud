import pickle
from inspect import getmembers, isfunction


import qtmud
from mudlib.starhopper import builders, subscriptions, txt


NAME = "STARHOPPER"
START_SYSTEM = None
END_SYSTEM = None
accounts = {}
players = []




def load():
    global accounts
    global START_SYSTEM
    global END_SYSTEM
    qtmud.subscribers.update({s[1].__name__: [s[1]] for s
                              in getmembers(subscriptions) if isfunction(s[1])})
    try:
        accounts = pickle.load(open("./data/starhopper_accounts.p", 'rb'))
    except FileNotFoundError:
        qtmud.log.debug('no save file found')
        qtmud.schedule('save')
    qtmud.log.info('starhopper start()ed')
    START_SYSTEM = builders.build_system()
    qtmud.log.info('starhopper.START_SYSTEM is %s', START_SYSTEM.name)
    END_SYSTEM = builders.generate_system_name()
    qtmud.log.info('starhopper.END_SYSTEM is going to be %s', END_SYSTEM)