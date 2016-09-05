add defaults to logging system if error comes from exception
    syntaxes:   except Exception: manager.warning('something broke')
                except Exception as err: manager.warning(err)

render description like render.style('{name}\n\n{visual_desc}'.format(**locals()))

implement __slots__

holly's holistic healing hut


class MUDSocket(object):
    def __init__(self, manager):
        self.manager = manager
        if type(MUD_ADDR) == tuple:
            self.address = MUD_ADDR
        elif type(MUD_ADDR) == int:
            self.address = ('0.0.0.0', MUD_ADDR)
        else:
            self.manager.log.warning('qtmud.MUD_ADDR needs to be string '
                'or tuple, got {0}'.format(type(MUD_ADDR)))
            return
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind(self.address)
        except Exception as err:
            self.manager.log.warning('failed to bind on '
                '{0} - {1}'.format(self.address, err))
            return
        self.socket.listen(5)
        self.connections = [self.socket]
        self.clients = {}
        return
