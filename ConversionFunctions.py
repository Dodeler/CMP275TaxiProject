#Delaney Lothian (1441546)

#map_limit is the the max amount of x and y pixels
map_limit = {1: 511, 2: 1023, 3: 2047, 4: 4095, 5: 8191, 6: 16383}
#map_box is the limits of the lat and lon of each map image
map_box = {1: (5364463,  -11373047, 5343572, -11337891), #N,W,S,E
            2: (5364464, -11373047, 5343572, -11337891),
            3: (5361858, -11368652, 5340953, -11333496),
            4: (5360554, -11368652, 5339643, -11333496),
            5: (5360554, -11367554, 5339643, -11332397),
            6: (5360228, -11367554, 5339316, -11332397)}

def map_adjuster(pos, in_min, in_max, out_min, out_max):
    #Does the same thing as Arduino map() does
    #Scales the position from between two points to two different points
    return int(((pos - in_min) * (out_max - out_min)) // (in_max - in_min) + out_min)

def x_to_longitude(map_num, map_x):
    return map_adjuster(map_x, 0, map_limit[map_num],
    map_box[map_num][1], map_box[map_num][3])

def y_to_latitude(map_num, map_y):
    return map_adjuster(map_y, 0, map_limit[map_num],
     map_box[map_num][0], map_box[map_num][2])


def longitude_to_x( map_num, map_longitude):
    return map_adjuster(map_longitude, map_box[map_num][1],
    map_box[map_num][3], 0,  map_limit[map_num])


def latitude_to_y( map_num, map_latitude):
    return map_adjuster(map_latitude,  map_box[map_num][0],
    map_box[map_num][2], 0,  map_limit[map_num])
