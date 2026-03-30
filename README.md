# docker
docker repo for tchaikbachx

# updates 3/30:

### *notes*
> functional `add`, `delete`, and `edit` for instruments in the database!

> UI is not finished; you will see some parts are uglier than others, and some i haven't started working on yet

> still need to add `filter` before it is "MVP" worthy and the actual checkout functionality at minimum

> it is unclear what will happen on a blank database so at least keep a copy of the current database if you plan to test undefined behavior

> untested (as is) on a completely empty database, but theoretically should work & has when i last tested it (different set-up though)

> untested for completely blank new entries, (i.e., when adding a new instrument leave all fields blank)

### *how to run it (more or less)*

**requires python to be installed*

**the ONLY checkout staff username and password accepted are "t" for both fields, yes it is case sensitive*

1) in your terminal, paste `run pip install flask flask-cors`
2) still through terminal, navigate to the top level directory, `image`, where `server.py` is
3) on the command-line, enter `python server.py`; there should now be a locally hosted server (on port 5000)
4) click the link (ctrl+click?) in the terminal and it should open up the page automatically in your browser, go wild

### *extra info/changes*

* here is the [python http server handling](https://docs.python.org/3/library/http.server.html) if you're interested; it is not implemented particularly well
* will add more descriptive comments later but most of it is pretty sparse rn