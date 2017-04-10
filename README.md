CMPUT 275 Final Project
Delaney Lothian (1441546), Chris Dodic (1515299)

Currently application will open map in a new window. Once clicking two places,
All taxis in taxi directory will pop up. The closest taxi will be called to the pickup
and will be drawn out following a path until pickup. Once reached pickup, path will be drawn
from pickup to drop off until "customer" is drop off. If a request is made, path can be diverted.

Instructions:

To use the program, run the file "UberInterface.py" from the command line using python3 or greater.
If PyQT is not installed, it should be installed from the command line using pip ("pip3 install pyqt5").

Using the program:

Once the program is loaded, the user may select two points on the map as well as enter the number of passengers
for the given request.  If the request is invalid the request will be ignore with no warning to the user. If the request is valid, a taxi will be assigned to pick that customer up based on an efficiency algorithm.  The map displays the current taxi's, and their current pathways.  During every cycle, the taxi's are moved one step closer to their next vertex destination (steps are based on the weight of the edge, coming from its euclidean distance).

Usability:

The program slows down due to the least cost path function.  To increase the scope of usability, the least cost path function should be made more time efficient (perhaps by means of memoization) at the cost of extra memory.  In addition, to improve the taxi decision algorithm, it depends on being able to call the least cost path algorithm multiple times; to improve the taxi decision algorithm further, it would also depend on the improvement of the least cost path function.

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
