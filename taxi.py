import server
from collections import defaultdict
from operator import itemgetter

class Taxi:
	"""

	The Taxi class is used to represent taxis on the map, and specifies a taxi's:
	-location
	-current number of passengers
	-destination
	-list of passengers
	-maximum number of passengers
	-pathway to current destination
	-edge distance left (used to simulate motion along the path)

	"""
    def __init__(self, init_vertex, max_num_passengers):
        self.loc = init_vertex
        self.num_pas = 0
        self.dest = (0,0)
        self.plist = []
        self.max = max_num_passengers
        self.path = []
        self.edge_distance_left = 0

    def add_passenger(self, pasngr):
        self.plist.append(passenger_id)

# defines a passenger (could be multiple people: signfies number of riders and start/end points)
class Passenger:
	"""
	The Passenger class is used to represent customers who make valid requests to
	the taxi service. They are specified by their:
	-start location
	-number of riders
	-destination
	"""
    def __init__(self, initial_loc, num_riders, dest):
        self.start_loc = initial_loc #closest_vertex(initial_loc[0],initial_loc[1])
        self.num_riders = int(num_riders)
        self.dest = dest #closest_vertex(dest_lat_lon[0],dest_lat_lon[1])

class UberTaxi:
    def __init__(self):
        self.taxi_directory = dict()
        self.cust_directory = dict()
        self.initialize_taxis()
        self.psngr_Q = list()
    #def initialize_taxis: gives the starting location of 5354017, -11355469, finds closest_vertex
    #and then set's that as initial point, with 5 passenger availability
    def initialize_taxis(self):
        starting_locations = [1410080240, 1402804968, 1402804895, 1402785059, 1410080240]
        for i in range(len(starting_locations)):
            lon = server.coordinates[starting_locations[i]][1]
            lat = server.coordinates[starting_locations[i]][0]
            self.taxi_directory[i] = Taxi(server.closest_vertex(lat, lon), 5)



	def taxi_time(path):
		"""
		Taxi time determines the 'time' it takes to get to a location based on the given path.

		Input:  A path (list)

		Output: Total edge weight sum of the edges in the path.
		"""
		cost = 0
		for v_index in range(len(path)-2):
			cost+=edge_weights[(path[v_index],path[v_index+1])]
		return cost
	# determines which taxi to assign to the pickup
	def which_taxi(self, customer_id, g):
		"""
		Determines which taxi should handle a customer request
		Inputs:		
				-customer id
				-the map's graph
			

		Output: (Fastest taxi,
			 string stating whether to drop current customer first or blank indicating adding to the list,
			 the path to the customer)
		"""
		# dictionary that keeps track of the time associated with each taxi
		# 	to pick up a given customer following a request
		time_dict=defaultdict(list)
		for taxi in self.taxi_directory:
			if taxi not in time_dict:
					time_dict[taxi]=[0,"",[]]
			# too many passengers (skip this taxi)
			if (self.cust_directory[customer_id].num_riders + (self.taxi_directory[taxi].num_pas)) > self.taxi_directory[taxi].max:
				time_dict[taxi][0]=float('inf')
			# taxi has no passengers
			elif not self.taxi_directory[taxi].plist:
				# cost to customer
				path = server.least_cost_path(g, self.taxi_directory[taxi].loc, self.cust_directory[customer_id].start_loc, server.cost_distance)
				time_dict[taxi][0]=self.taxi_time(path)
				time_dict[taxi][2]=path
				if not path:
					time_dict[taxi][0]=float('inf')


			# minimally optimal time cost for taxis that already have passengers
			else:
				path_to_cust = server.least_cost_path(g, self.taxi_directory[taxi].loc, self.cust_directory[customer_id].start_loc,cost_distance)
				time_dict[taxi][2]=[]
				# time directly to customer
				if not path_to_cust:
					time_to_cust=float('inf')
				else:
					time_to_cust = self.taxi_time(path_to_cust)

				# time to customer from current customers drop off point (only accounts for 1 passenger at the moment)
				current_cust_loc_dest = (self.cust_directory[self.taxi_directory[taxi].plist[0]].start_loc,self.cust_directory[self.taxi_directory[taxi].plist[0]].dest)
				path_to_cust_from_current_cust = least_cost_path(g, current_cust_loc_dest[1],self.cust_directory[customer_id].start_loc,cost_distance)
				if not path_to_cust_from_current_cust:
					time_to_cust_from_current_cust=float('inf')
				else:
					time_to_cust_from_current_cust = self.taxi_time(path_to_cust_from_current_cust)

				#go pickup first
				if time_to_cust < time_to_cust_from_current_cust:
					time_dict[taxi][0]=time_to_cust
					time_dict[taxi][2]=path_to_cust

				#drop off first
				else:
					time_dict[taxi][0]=time_to_cust_from_current_cust
					time_dict[taxi][1]="drop first"

		# returns the id of the "quickest taxi"
		time_list_sorted = sorted(time_dict.items(), key=itemgetter(1))
		quickest_taxi=time_list_sorted[0][0]

		return(quickest_taxi,time_dict[quickest_taxi][1],time_dict[quickest_taxi][2])




	def handle_request(request, customer_id, g):
		"""
		Takes a customer's request and uses the which_taxi function to determine which taxi to be assigned
		and updates the taxi's information.

		Input:  -customer request
			-taxi dictionary
			-customer dictionary
			-customer id number (order number)
			-the map's graph

		Output: none ==> updates a taxi following a request.
		"""
		# customer's initial location
		start_loc = closest_vertex(request[0],request[1])
		# number of passengers for the request
		num_passengers = int(request[2])
		# customer's destination
		dest_loc = closest_vertex(request[3],request[4])
		# creates an instance of the Passenger class for the customer based on the order number
		self.cust_directory[customer_id] = Passenger(start_loc,num_passengers,dest_loc)

		#determines the taxi to use
		taxi_to_use = self.which_taxi(customer_id, g)
		tx_id = taxi_to_use[0]

		# add customer to list

		# checks to see if the request has the "drop first" clause
		if taxi_to_use[1] == "":
			if self.taxi_directory[tx_id].plist:
				cur_cust_path=server.least_cost_path(g, self.cust_directory[customer_id].start_loc,self.cust_directory[self.taxi_directory[tx_id].plist[0]].dest,server.cost_distance)
				new_cust_path=server.least_cost_path(g, self.cust_directory[customer_id].start_loc,self.cust_directory[customer_id].dest,cost_distance)

				if self.taxi_time(cur_cust_path) < self.taxi_time(new_cust_path):
					self.taxi_directory[tx_id].plist.append(customer_id)
				else:
					self.taxi_directory[tx_id].plist=[customer_id]+self.taxi_directory[tx_id].plist
			else:
				self.taxi_directory[tx_id].plist.append(customer_id)
			self.taxi_directory[tx_id].path=taxi_to_use[2]
			self.taxi_directory[tx_id].num_pas+=self.cust_directory[customer_id].num_riders
			if taxi_to_use[2]:
				self.taxi_directory[tx_id].edge_distance_left=int(server.cost_distance(self.taxi_directory[tx_id].path[0],server.taxi_directory[tx_id].path[1]))
		# customer should be dropped off first before picking up the customer
		else:
			self.taxi_directory[tx_id].plist=[customer_id]+self.taxi_directory[tx_id].plist

			self.taxi_directory[tx_id].num_pas+=self.cust_directory[customer_id].num_riders
			if taxi_to_use[2]:
				self.taxi_directory[tx_id].edge_distance_left=int(server.cost_distance(self.taxi_directory[tx_id].path[0],self.taxi_directory[tx_id].path[1]))

	def advance_taxi(g):
		"""
		moves the location of the taxi up by 1 on its edge weight analysis
		Input:  
			-the map's graph
		Output: none ==> updates location of all taxi's
		"""
		for taxi in self.taxi_directory.values():
			#taxi is enroute somewhere
			if taxi.path:
				# decrement path time counter
				taxi.edge_distance_left-=1
				# if a vertex is reached
				if taxi.edge_distance_left == 0:
					# get rid of the vertex
					vertex_reached=taxi.path.pop(0)
					# if there is still a path to follow
					# 	set new destination and weight to that location
					if len(taxi.path):
						# updates taxi location
						taxi.loc=vertex_reached
						# sets new path 'time'
						taxi.edge_distance_left=int(edge_weights[(taxi.loc,taxi.path[0])])
					# Destination reached
					else:
						taxi.loc=vertex_reached
						#remove customer from the list if this is their destination
						for psngr in taxi.plist:
							if self.cust_directory[psngr].dest==taxi.loc:
								taxi.num_pas-=self.cust_directory[psngr].num_riders
								taxi.plist.remove(psngr)
						# if there are are still customers in the taxi, set up the next path
						if taxi.plist:
							# sets new pathway
							taxi.path=server.least_cost_path(g, taxi.loc, self.cust_directory[taxi.plist[0]].dest,server.cost_distance)
							# sets new path 'time'
							if taxi.path:
								taxi.edge_distance_left=int(server.edge_weights[(taxi.path[0],taxi.path[1])])
							# cautionary condtion that removes a passenger if there is no path to their destination
							else:
								pas_to_remove=taxi.plist.pop(0)
								taxi.num_pas-=self.cust_directory[pas_to_remove].num_riders

						# otherwise just wait
						else:
							pass

			# if taxi does not have a path currently
			else:
				# if there are still customers in the taxi
				if taxi.plist:
					# sets new taxi path based on current customer
					taxi.path=server.least_cost_path(g,self.cust_directory[taxi.plist[0]].start_loc, self.cust_directory[taxi.plist[0]].dest,server.cost_distance)
					# sets new path time
					if taxi.path:
						taxi.edge_distance_left=int(server.edge_weights[(taxi.path[0],taxi.path[1])])
					# cautionary condtion that removes a passenger if there is no path to their destination
					else:
						pas_to_remove=taxi.plist.pop(0)
						taxi.num_pas-=self.cust_directory[pas_to_remove].num_riders
