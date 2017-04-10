from server import *
from collections import defaultdict
from operator import itemgetter



# initialize the map


class UberTaxi:
	# defines a taxi object
	class Taxi:
		def __init__(self, init_vertex, max_num_passengers):
			self.loc = init_vertex
			self.num_pas = 0
			self.dest = (0,0)
			self.plist = []
			self.max = max_num_passengers
			self.path = []
			self.edge_distance_left=0

		def add_passenger(self, pasngr):
			self.plist.append(passenger_id)

		# def set_route(self, )

	# defines a passenger (could be multiple people: signfies number of riders and start/end points)
	class Passenger:
		def __init__(self, initial_loc, num_riders, dest):

			self.start_loc = initial_loc #closest_vertex(initial_loc[0],initial_loc[1])
			self.num_riders = int(num_riders)
			self.dest = dest #closest_vertex(dest_lat_lon[0],dest_lat_lon[1])

	def taxi_time(path):
		cost = 0
		for v_index in range(len(path)-2):
			cost+=edge_weights[(path[v_index],path[v_index+1])]
		return cost
	# determines which taxi to assign to the pickup
	def which_taxi(num_passengers, cust_loc, cust_dest, taxi_directory,cust_directory,g,taxi_time):
		# dictionary that keeps track of the time associated with each taxi
		# 	to pick up a given customer following a request
		time_dict=defaultdict(list)
		for taxi in taxi_directory:

			# too many passengers (skip this taxi)
			if (num_passengers+(taxi_directory[taxi].num_pas)) > taxi_directory[taxi].max:
				if taxi not in time_dict:
					time_dict[taxi]=[0,"",[]]
				time_dict[taxi][0]=float('inf')
			# taxi has no passengers
			elif not taxi_directory[taxi].plist:
				# cost to customer
				if taxi not in time_dict:
					time_dict[taxi]=[0,"",[]]
				path = least_cost_path(g, taxi_directory[taxi].loc, cust_loc,cost_distance)
				for v_index in range(len(path)-2):
					time_dict[taxi][0]+=edge_weights[(path[v_index],path[v_index+1])] #NOTE: edge_weights is a dictionary that was added to the server.py file
				time_dict[taxi][2]=path
				if not path:
					time_dict[taxi][0]=float('inf')


			# minimally optimal time cost for taxis that already have passengers
			else:

				print("taxi id: ",taxi)
				if taxi not in time_dict:
					time_dict[taxi]=[0,"",[]]
				path_to_cust = least_cost_path(g, taxi_directory[taxi].loc, cust_loc,cost_distance)
				time_dict[taxi][2]=[]
				# time directly to customer
				if not path_to_cust:
					time_to_cust=float('inf')
				else:
					time_to_cust = taxi_time(path_to_cust)
				print("TIME TO CUST: ",time_to_cust)

				# time to customer from current customers drop off point (only accounts for 1 passenger at the moment)
				current_cust_loc_dest = (cust_directory[taxi_directory[taxi].plist[0]].start_loc,cust_directory[taxi_directory[taxi].plist[0]].dest)
				path_to_cust_from_current_cust = least_cost_path(g, current_cust_loc_dest[1],cust_loc,cost_distance)
				if not path_to_cust_from_current_cust:
					time_to_cust_from_current_cust=float('inf')
				else:
					time_to_cust_from_current_cust = taxi_time(path_to_cust_from_current_cust)
				print("PATH to cust from cur cust: ",path_to_cust_from_current_cust)

				print("TIME TO CUST FROM CUR CUST: ",time_to_cust_from_current_cust)
				# time_dict[taxi][3]=path_to_cust_from_current_cust
				# for v_index in range(len(path)-2):
				# 	time_to_cust_from_current_cust+=edge_weight[(path_to_cust_from_current_cust[v_index],path_to_cust_from_current_cust[v_index+1])]

				#go pickup first
				if time_to_cust < time_to_cust_from_current_cust:
					time_dict[taxi][0]=time_to_cust
					time_dict[taxi][2]=path_to_cust
				#drop off first
				else:
					time_dict[taxi][0]=time_to_cust_from_current_cust
					time_dict[taxi][1]="drop first"
					# time_dict[taxi][2]=path_to_cust_from_current_cust



		# returns the id of the "quickest taxi"
		time_list_sorted = sorted(time_dict.items(), key=itemgetter(1))
		quickest_taxi=time_list_sorted[0][0]
		print("FASTEST TAXI! ",quickest_taxi)
		print("Time dict")
		for key in time_dict:
			print(key," ",time_dict[key][0])
		# print(time_dict.values()[0])
		return(quickest_taxi,time_dict[quickest_taxi][1],time_dict[quickest_taxi][2])




	def handle_request(request,taxi_directory,cust_directory,customer_id,g):
		#Don't think adding float*1000 is necessary
		start_loc = closest_vertex(request[0],request[1])
		num_passengers = int(request[2])
		dest_loc = closest_vertex(request[3],request[4])
		cust_directory[customer_id]=UberTaxi.Passenger(start_loc,num_passengers,dest_loc)


		taxi_to_use = UberTaxi.which_taxi(num_passengers,start_loc,dest_loc,taxi_directory,cust_directory,g,UberTaxi.taxi_time)
		tx_id = taxi_to_use[0]
		if taxi_to_use[1] == "":
			taxi_directory[tx_id].plist.append(customer_id)
			taxi_directory[tx_id].path=taxi_to_use[2]
			if taxi_to_use[2]:
				taxi_directory[tx_id].edge_distance_left=int(cost_distance(taxi_directory[tx_id].path[0],taxi_directory[tx_id].path[1]))
		else:
			taxi_directory[tx_id]
		# customer_id+=1

	def advance_taxi(taxi_directory,cust_directory,g):
		"""
		moves the location of the taxi up by 1 on its edge weight analysis
		"""
		for taxi in taxi_directory.values():
			if taxi.path: #taxi is enroute somewhere
				taxi.edge_distance_left-=1
				# if a vertex is reached
				if taxi.edge_distance_left == 0:
					# get rid of the vertex
					vertex_reached=taxi.path.pop(0)
					# if there is still a path to follow
					# 	set new destination and weight to that location
					if len(taxi.path) > 1:
						taxi.loc=vertex_reached
						taxi.edge_distance_left=int(edge_weights[(taxi.path[0],taxi.path[1])]) # sets new path 'time'


					else:
						# taxi has dropped off a passenger, what do now?
						taxi.loc=taxi.path.pop()
						#remove customer from the list if this is their destination
						for psngr in taxi.plist:
							if cust_directory[psngr].dest == taxi.loc:
								taxi.plist.remove(psngr) #remove customer from the list
						#if there are still customers in the taxi, set up next path
						if taxi.plist:
							taxi.path=least_cost_path(g, taxi.loc, cust_directory[taxi.plist[0]].dest,cost_distance)
							taxi.edge_distance_left=int(edge_weights[(taxi.path[0],taxi.path[1])]) # sets new path 'time'
						else:
							pass
			else:
				if taxi.plist:
					print(cust_directory[taxi.plist[0]].start_loc)
					print((cust_directory[taxi.plist[0]].dest))
					print(least_cost_path(g,cust_directory[taxi.plist[0]].start_loc, cust_directory[taxi.plist[0]].dest,cost_distance))
					taxi.path=least_cost_path(g,cust_directory[taxi.plist[0]].start_loc, cust_directory[taxi.plist[0]].dest,cost_distance)
					print(taxi.path)
					taxi.edge_distance_left=int(edge_weights[(taxi.path[0],taxi.path[1])])
