# Qualities of Things Multi-User Dimension
## (qtmud)

qtmud is an early alpha multiplayer text-based real-time virtual world simulator.

You can view the main documentation either locally through [./docs/](./docs/index.html) 
or if you're online, the documentation is served through [Github Pages](https://emsenn.github.io/qtmud/).

If you are anxious to start using qtmud, edit [](__init__.py) and set the 
constants `NAME`, `HOST`, and `MUD_PORT` (comments in the file explain their use.)

Then, run [](run.py) with python3.5. You should see some information about a 
Manager() being instanced, and services starting up. Now you can connect to 
your MUD through telnet with `telnet HOST MUD_PORT`, for example 
`telnet localhost 5787`.
