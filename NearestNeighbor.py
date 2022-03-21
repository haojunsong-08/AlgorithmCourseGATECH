import math
import copy
import time

# Function used to calculate distance
def find_distance(x, y):
    
    distance = math.sqrt((y["x"] - x["x"]) ** 2 + (y["y"] - x["y"]) ** 2)

    return round(distance)



def SeedApprox(array, start_time, time_limit, seed=None):
    
    
    visited = ""
    total_distance = 0


    origin = [x for x in array if x["id"] == seed][0]
    
    current = origin

    visited += str(current["id"]-1)

    # print("Origin is: ")
    # print(current)
    # print()

    # Find the origin and delete it from the list
    for i in range(len(array)):
        if array[i]['id'] == current["id"]:
            del array[i]
            break

    # print(array)
    # print()

    # Finding nearest neighbor until the list is empty
    while len(array)>0:
        
        # Update the distance from current node to each node
        mini = 9999999999
        for node in array:
            node["dist"] = find_distance(current, node)
            
            # Find the nearest neighbor
            if node["dist"] < mini:
                mini = node["dist"]
        # print(mini)

        # Find the nearest neighbor and delete it from the array
        for i in range(len(array)):
            if array[i]['dist'] == mini:
                current = array[i]
                visited += "," + str(current["id"]-1)
                # print(current)
                del array[i]
                break

            
        
        # Add the distance to the total_distance
        total_distance += mini
        
        # print(array)

        # print(time.time() - start_time)

        if time.time() - start_time > time_limit:
            break

    # print(origin)
    # print(current)
    total_distance += find_distance(current, origin)

    return total_distance, visited
    


def OptiApprox(num, array, start_time, time_limit):

    opti_visited = []
    opti_distance = 999999999

    # Iterate through all node as origin
    for i in range(1, num+1):

        array_temp = copy.deepcopy(array)
        # print(array_temp)
        visited = ""
        total_distance = 0

        seed = i
        
        # print(seed)
        origin = [x for x in array_temp if x["id"] == seed][0]
        # print(origin)

        current = origin

        visited += str(current["id"]-1)

        # print("Origin is: ")
        # print(current)
        # print()

        # Find the origin and delete it from the list
        for i in range(len(array_temp)):
            if array_temp[i]['id'] == current["id"]:
                del array_temp[i]
                break

        # print(array)
        # print()

        # Finding nearest neighbor until the list is empty
        while len(array_temp)>0:
            
            # Update the distance from current node to each node
            mini = 9999999999
            for node in array_temp:
                node["dist"] = find_distance(current, node)
                
                # Find the nearest neighbor
                if node["dist"] < mini:
                    mini = node["dist"]
            # print(mini)

            # Find the nearest neighbor and delete it from the array
            for i in range(len(array_temp)):
                if array_temp[i]['dist'] == mini:
                    current = array_temp[i]
                    visited += "," + str(current["id"]-1)
                    # print(current)
                    del array_temp[i]
                    break
            

            # Add the distance to the total_distance
            total_distance += mini
            
            # print(array)

            # print(time.time() - start_time)

            if time.time() - start_time > time_limit:
                break

        # print()

        # print(origin)
        # print(current)
        total_distance += find_distance(current, origin)

        # print(total_distance)

        if total_distance < opti_distance:
            opti_distance = total_distance
            opti_visited = visited

        # print(time.time() - start_time)

        if time.time() - start_time > time_limit:
            break

    return opti_distance, opti_visited