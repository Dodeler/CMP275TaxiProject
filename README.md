CMPUT 275 Final Project
Delaney Lothian (1441546), Chris Dodic (1515299)

Currently application will open map in a new window. Once clicking two places,
All taxis in taxi directory will pop up. The closest taxi will be called to the pickup
and will be drawn out following a path until pickup. Once reached pickup, path will be drawn
from pickup to drop off until "customer" is drop off. If a request is made, path can be driverted.

April 9th - Files changed:
		UberInterface.py
		taxi.py
		(Technically) server.py

#TODO:
	-How many passengers (Delaney)
	-(Potentially) have taxis return "home"
			making "home" deciding which "box" it's in and then have in go to the
			most inner middle corner of that bpx
	-Alerts (Delaney)
	-More efficient least_cost_path (?)
	-Make cars go faster (Delaney?)
	-Ensure customers can't become eternally stuck in a taxi.

The toolkit called Qt (officially pronounced "cuteâ€) is needed to run program.Run
	pip3 install pyqt5
in a terminal. If pip3 couldn't be found, grab it:
	https://pip.pypa.io/en/stable/installing/

Many comments in UberInterface.py were taken
from http://pyqt.sourceforge.net/Docs/PyQt5/
