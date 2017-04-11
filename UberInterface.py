from PyQt5.QtWidgets import (QMainWindow, QWidget, QToolTip,
							QPushButton, QGridLayout, QApplication, QLabel, QComboBox,
							QLineEdit, QTextEdit, QAction, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QMouseEvent, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
import ConversionFunctions
import server
from taxi import UberTaxi
from collections import defaultdict
import os


# from PyQt5.QtGui import QColor, QBrush
# then,
# green = QColor(0, 255, 0)
# red = QColor(255, 0, 0)
# greenPen = QPen(green)
# redBrush = QBrush(red)
# ellipse = self.mapScene.addEllipse(0,0,50,50, greenPen, redBrush)

window = None
__location__=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

g = server.read_city_graph('edmonton-roads-2.0.1.txt')
#cars = dict()

taxi_directory=defaultdict(UberTaxi.Taxi)
cust_directory=defaultdict(UberTaxi.Passenger)


taxi_directory[0]=UberTaxi.Taxi(1410080240,5)  #lets call this home
taxi_directory[1]=UberTaxi.Taxi(1402804968,5)
taxi_directory[2]=UberTaxi.Taxi(1402804895,5)
taxi_directory[3]=UberTaxi.Taxi(1402785059,5)
taxi_directory[4]=UberTaxi.Taxi(1410080240,5)


class GraphicsScene(QGraphicsScene):
	#Subclasses do not need init.
	#Checks to see if the mouse has been released
	def mouseReleaseEvent(self, event):
		#screenPos is the cursor's position on the window
		#Checks to see if the 'click' and 'release' are in the same place,
		#as to not include dragging events.
		if event.screenPos() == event.lastScreenPos():
			#scenePos is the cursor's position on the "scene" i.e.map image
			#Grad the x,y coords
			(x,y) = window.handleClick(event.scenePos())
			#Convert them into lat,lon

			lon  = ConversionFunctions.x_to_longitude(window.zoomlevel, x)
			lat = ConversionFunctions.y_to_latitude(window.zoomlevel, y)
			#Determine whether start location has already been decided
			if window.pressed == False:
				window.start = (lat, lon)
				#cars[window.howmanycars] = (lon, lat)
				window.pressed = True
			else:
				#Once dest has been decided, find shortest path and draw it
				window.dest = (lat, lon)
				window.pressed = False
				#carsdest[window.howmanycars] = (lon, lat)
				request = (window.start[0], window.start[1], 1, window.dest[0], window.dest[1])
				UberTaxi.handle_request(request,taxi_directory,cust_directory, window.customer_id, g)
				window.customer_id += 1
				timer.start()




class WindowTime(QMainWindow):
	'''This class handles the main window.'''

	def __init__(self):
		super().__init__()

		self.menubar = self.menuBar()

		self.status = self.statusBar()

		exitAction = QAction('Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.close)

		fileMenu = self.menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		self.zoomlevel = 2
		# self.pixmaps = {2: QPixmap('yeg-2.png'), 3: QPixmap('yeg-3.png'),
		# 				4: QPixmap('yeg-4.png'), 5: QPixmap('yeg-5.png'), 6: QPixmap('yeg-6.png')}
		#
		# self.sizes = {1: 512, 2: 1024, 3: 2048, 4: 4096, 5: 8192, 6: 16384}
		self.pixmaps = {2: QPixmap(os.path.join(__location__,'yeg-2.png')), 3: QPixmap(os.path.join(__location__,'yeg-3.png')),
						4: QPixmap(os.path.join(__location__,'yeg-4.png')), 5: QPixmap(os.path.join(__location__,'yeg-5.png'))}

		self.sizes = {1: 512, 2: 1024, 3: 2048, 4: 4096, 5: 8192}
		self.pressed = False
		self.start = 0
		self.dest = 0
		self.center = (0,0)
		self.howmanycars = 0
		self.customer_id = 0
		self.initUI()

		self.show()

	def initUI(self):
		#The QToolTip class provides tool tips (balloon help) for any widget.
		QToolTip.setFont(QFont('SansSerif', 10))

		w = QWidget()
		#The QGridLayout class lays out widgets in a grid.
		grid = QGridLayout()
		#setLayout(self, Qlayout) Sets the layout manager for this widget to layout.
		#The QLayout argument has it's ownership transferred to Qt.
		w.setLayout(grid)
		#The QLabel widget provides a text or image display.
		labelZoom = QLabel('Zoom here pls')

		#The QPushButton widget provides a command button. Takes in arguments
		#For text label
		btnZoomIn = QPushButton('+')
		btnZoomIn.setToolTip('Zoom In')
		btnZoomIn.clicked.connect(self.zoomIn)
		btnZoomOut = QPushButton('-')
		btnZoomOut.setToolTip('Zoom Out')
		btnZoomOut.clicked.connect(self.zoomOut)

		dropDownBox = QComboBox()

		self.mapScene = GraphicsScene()
		self.mapScene.setSceneRect(0,0,self.sizes[self.zoomlevel],self.sizes[self.zoomlevel])
		self.mapScene.addPixmap(self.pixmaps[self.zoomlevel])
		#ellipse = mapScene.addEllipse(50,100,50,50)
		self.mapView = QGraphicsView()
		self.mapView.setScene(self.mapScene)
		#Set it so user can drag map via cursor
		self.mapView.setDragMode(QGraphicsView.ScrollHandDrag)
		#Hide the scroll bar
		self.mapView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.mapView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)



		grid.addWidget(labelZoom, 0, 4)
		grid.addWidget(self.mapView, 0, 0, 4, 4)
		grid.addWidget(btnZoomIn, 1, 4)
		grid.addWidget(btnZoomOut, 2, 4)

		#How everything will look on the screen
		self.setGeometry(300, 300, 800, 600)
		self.setWindowTitle('Uber Pool')
		self.setCentralWidget(w)

		#CHANGED: This
	def setCenter(self):
		center = self.mapView.mapToScene(self.mapView.width()//2, self.mapView.height()//2)
		self.center = (ConversionFunctions.x_to_longitude(self.zoomlevel, center.x()),
						ConversionFunctions.y_to_latitude(self.zoomlevel, center.y()))

	def zoomIn(self):
		if self.zoomlevel < 5:
			self.pressed = False
			self.setCenter()
			self.zoomlevel += 1
			self.updateSceneZoom()
	def zoomOut(self):
		if self.zoomlevel > 2:
			self.pressed = False
			self.setCenter()
			self.zoomlevel -= 1
			self.updateSceneZoom()

	#updates the scence once the zoom button has been pressed. The scene is
	#updated on the center of the last scene
	def updateSceneZoom(self):
		self.mapScene.clear()
		self.mapScene.addPixmap(self.pixmaps[self.zoomlevel])
		self.mapScene.setSceneRect(0,0,self.sizes[self.zoomlevel],self.sizes[self.zoomlevel])
		(x,y) = (ConversionFunctions.longitude_to_x(self.zoomlevel, self.center[0]),
				ConversionFunctions.latitude_to_y(self.zoomlevel, self.center[1]))
		self.mapView.centerOn(x,y)



	#returns the x,y position of the cursor on the map
	def handleClick(self, pos):
		return(pos.x(), pos.y())
		# #Grab the x,y coords
		# (x, y) = (pos.x(), pos.y())
		# #Convert them into lat,lon
		# lon = x_to_longitude(self.zoomlevel, x)
		# lat = y_to_latitude(self.zoomlevel, y)
		#
		# #Determine whether start location has already been decided
		# if self.pressed == False:
		# 	self.start = Vertex(lat, lon)
		# 	self.pressed = True
		# 	self.drawBubble(self.start)
		# else:
		# 	#Once dest has been decided, find shortest path and draw it
		# 	self.dest = Vertex(lat, lon)
		# 	self.pressed = False
		# 	self.drawBubble(self.dest)
		# 	self.controller.passRequest(self.start, self.dest, 1)


	def drawCar(self):
		#Draws the map in place
		self.setCenter()
		self.mapScene.clear()
		self.mapScene.addPixmap(self.pixmaps[self.zoomlevel])
		self.mapScene.setSceneRect(0,0,self.sizes[self.zoomlevel],self.sizes[self.zoomlevel])
		(lat, lon) = self.center
		x = ConversionFunctions.longitude_to_x(self.zoomlevel, lon)
		y = ConversionFunctions.latitude_to_y(self.zoomlevel, lat)
		self.mapView.centerOn(x,y)
		#advance_taxi
		UberTaxi.advance_taxi(taxi_directory, cust_directory, g)
		for taxi in taxi_directory.values():
			#gets coords from vertex
			lon = server.coordinates[taxi.loc][1]
			lat = server.coordinates[taxi.loc][0]
			#stored in lat, lon, and then converted
			newx = ConversionFunctions.longitude_to_x(self.zoomlevel, lon)
			newy = ConversionFunctions.latitude_to_y(self.zoomlevel, lat)
			#draws path and car
			self.mapScene.addRect(newx, newy, 15, 10)
			self.mapScene.addEllipse(newx-2, newy+10, 6, 6)
			self.mapScene.addEllipse(newx+11, newy+10, 6, 6)
			self.drawPath(taxi.path)


	def drawPath(self, path):
		linePen = QPen()
		linePen.setWidth(3) #Set the width of the line to be noticeable
		for i in range(len(path)-1):
			lon1 = server.coordinates[path[i]][1]
			lat1 = server.coordinates[path[i]][0]
			lon2 = server.coordinates[path[i+1]][1]
			lat2 = server.coordinates[path[i+1]][0]

			self.mapScene.addLine(ConversionFunctions.longitude_to_x(self.zoomlevel, lon1),
			ConversionFunctions.latitude_to_y(self.zoomlevel, lat1),
			ConversionFunctions.longitude_to_x(self.zoomlevel, lon2),
			ConversionFunctions.latitude_to_y(self.zoomlevel, lat2), linePen)




if __name__ == '__main__':

	app = QApplication([])
	window = WindowTime()
	timer = QTimer()
	# in milliseconds
	timer.setInterval(0.1)
	#like with QPushButton, .connect calls something the timer parameters
	#have been met i.e. 1000ms have passed
	timer.timeout.connect(window.drawCar)
	exit(app.exec_())
