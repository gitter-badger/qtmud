add defaults to logging system if error comes from exception
    syntaxes:   except Exception: manager.warning('something broke')
                except Exception as err: manager.warning(err)

render description like render.style('{name}\n\n{visual_desc}'.format(**locals()))

implement __slots__

add syntax exception? (rewrite whole command thing)


