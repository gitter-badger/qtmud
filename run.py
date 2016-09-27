#!/usr/bin/python3
""" qtmud startup script
"""


import qtmud

if __name__ == '__main__':
    if qtmud.load():
        qtmud.log.info('qtmud load()ed successfully')
        qtmud.run()
    else:
        qtmud.log.warning('qtmud failed to load()')
        qtmud.log.critical('exit()ing')
        exit()
