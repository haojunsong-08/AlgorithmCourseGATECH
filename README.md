# AlgorithmCourseGATECH
This is the project for Graduate level Alogrithm course using bnb, nearestNeighbors, SA and Twoopt.

Please make sure the following dependencies are enabled on your machine:
	time
	argparse
	sys
	math
	copy
	Path
	networkx
	numpy
	random
	csv

Please run your command as the following format on terminal to execute the program:
python tsp_main.py -inst 'DATA/DATA/Atlanta.tsp' -alg Approx -time 600 -seed 4

(Required)
-inst is followed by the filepath
-alg is followed by the algorithm, with the options of:
	1. BnB
	2. Approx
	3. LS1
	4. LS2
-time is followed by the cutoff time
(Optional)
-seed is followed by the randomly generated seed as origin(Not applicable for Branch-and-Bound, but applies to Approximation and Local Search)
