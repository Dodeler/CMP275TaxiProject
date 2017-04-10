# CHANGES
from taxi import *
import select

g=read_city_graph('edmonton-roads-2.0.1.txt')

ServerRunning = True

# TAXI/CUSTOMER dictionaries
taxi_directory=defaultdict(UberTaxi.Taxi)
cust_directory=defaultdict(UberTaxi.Passenger)
customer_id=0

# TEST TAXIS

taxi_directory[0]=UberTaxi.Taxi(1410080240,5)  #lets call this home
taxi_directory[1]=UberTaxi.Taxi(1402804968,5)
taxi_directory[2]=UberTaxi.Taxi(1402804895,5)
taxi_directory[3]=UberTaxi.Taxi(1402785059,5)
taxi_directory[4]=UberTaxi.Taxi(1410080240,5)  #also at Home






import time #for testing

while ServerRunning:

    if select.select([sys.stdin,],[],[],0.0)[0]:
        request = sys.stdin.readline().strip().split()
        if len(request) != 5:
            pass #invalid request
        else:
            UberTaxi.handle_request(request,taxi_directory,cust_directory,customer_id,g)
            customer_id+=1
    UberTaxi.advance_taxi(taxi_directory,cust_directory,g)


    for taxi in taxi_directory:
        print("tx id: {}, tx loc: {}, cur psngrs: {}, EDL: {}, Pathlen: {}".format(taxi,taxi_directory[taxi].loc,taxi_directory[taxi].plist,taxi_directory[taxi].edge_distance_left,len(taxi_directory[taxi].path)))


    time.sleep(1)
