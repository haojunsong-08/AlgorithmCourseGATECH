
import time
import argparse
import sys
from NearestNeighbor import SeedApprox, OptiApprox
import TwoOpt as TO
import SA as SA
import bnb




def read_file(filename, array):
    
    with open(filename) as f:
        
        for i in range(5):
            title = f.readline()
            
            # print(title)
                
            if i == 1:
                num = int(title.split(" ")[1])
                # print(num)
                
        for j in range(num):
            vertex = f.readline().strip().split(" ")
            dict = {
                "id": int(vertex[0]),
                "x": float(vertex[1]),
                "y": float(vertex[2]),
                "dist": 0
            }
            array.append(dict)
        
        f.close()
    
    return num



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="sample command: python tsp_main.py -inst 'DATA/DATA/Atlanta.tsp' -alg Approx -time 600 -seed 4")
    parser.add_argument("-inst", dest="filepath", required= True, help="path of the input tsp file")
    parser.add_argument("-alg", dest="algorithm", required= True, help="specify the algorithm used to solve TSP")
    parser.add_argument("-time", dest="time", required= True, help="specify the cutoff time.", type=int)
    parser.add_argument("-seed", dest="seed", required= False, help="specify the random seed. Default: None",
                        default=None, type=int)

    args = parser.parse_args()

    # print(args)

    start_time = time.time()

    try:
        cutoff_time = int(args.time)
    except:
        sys.exit("Please input cutoff time.\n")

    city = args.filepath.split(".")[0].split("/")[2]
    # print(city)
    if args.seed == None:
        output1 = f"{city}_{args.algorithm}_{args.time}.sol"
        output2 = f"{city}_{args.algorithm}_{args.time}.trace"
    else:
        output1 = f"{city}_{args.algorithm}_{args.time}_{args.seed}.sol"
        output2 = f"{city}_{args.algorithm}_{args.time}_{args.seed}.trace"

    if args.algorithm == "Approx":
        array = []

        # print(args.seed)
        try:
            num = read_file(args.filepath, array)
        except:
            sys.exit("Incorrect filepath.\n")

        if args.seed != None:
            total_distance, visited = SeedApprox(array, start_time, cutoff_time, args.seed)
        else:
            total_distance, visited = OptiApprox(num, array, start_time, cutoff_time)
        # print(f"The distance travelled within {city} is {total_distance}")
        # print(f"Visited sequence: {visited}")

        f1 = open(output1, "w")
        print(total_distance, file=f1)
        print(visited, file=f1)
        
        f1.close()

        end_time = time.time()

        f2 = open(output2, "w")
        print(f"{round(end_time - start_time, 2)}, {total_distance}", file=f2)



    elif args.algorithm == "BnB":
        filename = args.filepath
        cutout_time = args.time
        bnb.main(filename, cutout_time, city)



    elif args.algorithm == "LS1":
        dim, adj_mat = TO.create_adj_mat(args.filepath)
        if args.seed:
            twoopt = TO.TwoOpt(adj_mat, dim, args.time, args.seed)
        else:
            twoopt = TO.TwoOpt(adj_mat, dim, args.time)
        visited, total_distance, trace = twoopt.two_opt()
        
        twoopt.output_sol(total_distance, visited, output1)
        twoopt.output_trace(trace, output2)



    elif args.algorithm == "LS2":
        dim, adj_mat = SA.create_adj_mat(args.filepath)
        if args.seed:
            s = SA.SA(adj_mat, dim, args.seed)
        else:
            s = SA.SA(adj_mat, dim)
        s.simulated_annealing(args.time)
        total_distance = s.best_distance
        visited = s.best_solution
        trace = s.trace

        s.output_sol(s.best_distance, s.best_solution, output1)
        s.output_trace(s.trace, output2)
        


    else:
        sys.exit("Incorrect algorithm input.\n")

    # print(end_time - start_time)