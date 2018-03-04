CMPUT 275 Final Project
Delaney Lothian (1441546), Chris Dodic (1515299)

# Taxi Project

Currently application will open map in a new window. Once clicking two places,
All taxis in taxi directory will pop up. The closest taxi will be called to the pickup
and will be drawn out following a path until pickup. Once reached pickup, path will be drawn
from pickup to drop off until "customer" is drop off. If a request is made, path can be diverted.

### Execution Steps

To use the program, run the following command

`python3 UberInterface.py` 

Program must use python3 or greater. If PyQT is not installed, it should be installed using the package management system "pip" and by running the following command:

`pip3 install pyqt5`

### Using the program:

Once the program is loaded, the user may select two points on the map as well as enter the number of passengers
for the given request.  If the request is invalid the request will be ignore with no warning to the user. If the request is valid, a taxi will be assigned to pick that customer up based on an efficiency algorithm.  The map displays the current taxi's, and their current pathways.  During every cycle, the taxi's are moved one step closer to their next vertex destination (steps are based on the weight of the edge, coming from its euclidean distance).

### Usability:

The program slows down due to the least cost path function.  To increase the scope of usability, the least cost path function should be made more time efficient (perhaps by means of memoization) at the cost of extra memory.  In addition, to improve the taxi decision algorithm, it depends on being able to call the least cost path algorithm multiple times; to improve the taxi decision algorithm further, it would also depend on the improvement of the least cost path function.


Many comments in UberInterface.py were taken
from http://pyqt.sourceforge.net/Docs/PyQt5/
