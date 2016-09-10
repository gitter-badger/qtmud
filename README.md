# Qualities of Things Multi-User Dimension
## (qtmud)

qtmud is an early alpha multiplayer text-based real-time virtual world simulator.

The main documentation is located at [docs/index.html](docs/index.html), but 
is intended to be built with Sphinx. You can view the latest Sphinx-built 
documentation in this repository's gh-pages branch, or build an up-to-date 
version with [](docs/build_docs.sh).

If you are anxious to start using qtmud, edit [](__init__.py) and set the 
constants `NAME`, `HOST`, and `MUD_PORT` (comments in the file explain their use.)

Then, run [](run.py) with python3.5. You should see some information about a 
Manager() being instanced, and services starting up. Now you can connect to 
your MUD through telnet with `telnet HOST MUD_PORT`, for example 
`telnet localhost 5787`.
