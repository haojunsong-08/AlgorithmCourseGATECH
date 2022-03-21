import math

import numpy as np
import networkx
import time
class branchnbound:
    '''
    THis is the Branch and bound method, the detail is in the project
    '''
    def __init__(self, file_path,start_time, cutout_time=600):
        self.file_path = file_path
        self.matrix = []
        self.num = 0
        self.best_path = None
        self.city_visited = 0
        self.start_time = start_time
        self.cutout_time =cutout_time



    def Sort_tree(self, graph):
        '''sort tree based and get the edgelist based on weight
        '''
        sorted_tree = sorted(graph.edges(data=True), key=lambda t: t[2].get('weight', 1))

        return sorted_tree
        #self.cutoff_time = cutoff_time


    def find_distance(self, vertice1, vertice2):
        '''find the istance between each cities'''
        distance = np.sqrt((vertice2[0] - vertice1[0]) ** 2 + (vertice2[1] - vertice1[1]) ** 2)

        return round(distance)

    def read_file(self):
        with open(self.file_path) as f:
            for i in range(5):
                title = f.readline()
                if i == 0:
                    city = title.split(" ")[1]
                    #(city)

                elif i == 1:
                    self.num = int(title.split(" ")[1])
                    self.matrix = np.zeros((self.num,2), dtype=float)

            for j in range(self.num):
                vertex = f.readline().strip().split(" ")
                self.matrix[j][0] = vertex[1]
                self.matrix[j][1] = vertex[2]
        f.close()
        ''' return the adjacent matrix'''
        return self.matrix

    def graph(self,path):
        '''
        #coordinates acquired
        #getting graph'''
        G = networkx.Graph()
        num = len(path)
        #print(path)
        if len(path[0]) == 2:
            weightmatrix = np.zeros((num, num), dtype=float)
            for m in range(num):
                for n in range(num):
                    '''# make the weight infinity if equal'''
                    distance = math.inf
                    if m == n:
                        continue
                    distance =self.find_distance(path[m], path[n])
                    weightmatrix[m][n] = weightmatrix[n][m] = distance
                    G.add_edge(m, n, weight=distance)
            #A = networkx.adjacency_matrix(self.G).
        return G

    def upper_bound(self, graph):
        '''
        #compute the current graph upper bound to prune the node if exceedded
        #use the gready method to find the smallest neighbor'''
        try:
            upper_bound = 0
            current_node = list(graph.nodes())[0]
            last_edges = list(graph.edges(current_node, data=True))
            tree = []
            while len(graph.nodes()) > 1:
                tree.append(current_node)
                next_node = sorted(graph.edges(current_node, data=True), key=lambda t: t[2]['weight'])[0]
                graph.remove_node(current_node)
                upper_bound += next_node[2]["weight"]
                current_node = next_node[1]
            last_one = list(filter(lambda t: t[1] == current_node, last_edges))[0][2]["weight"]
            #print(last_one)
            upper_bound += last_one
            tree.append(current_node)
        except:
            upper_bound = math.inf
        return upper_bound, tree

    def find_cycle(self, graph):
        try:
            return len(networkx.find_cycle(graph)) == len(graph.nodes())
        except:
            return False


    def get_lowest_cost_nodes(self, tree, node):
        lowest_cost = 0
        #lowest_cost_node = None
        count = 0
        # get the lowest cost node with vertice that from the previous node
        edges = []
        for edge in tree:
            # print(edge)
            if edge[0] == node or edge[1] == node:
                lowest_cost += edge[2].get('weight')
                edges.append(edge)
                #lowest_cost_node = edge
                count += 1
            if count == 2:
                break
        # print(tree, node)
        return lowest_cost, edges[0], edges[1]

    def lower_bound(self, graph):

        #iterating all the nodes and find the smallest mst
        distance_sum = math.inf
        sorted_tree = self.Sort_tree(graph)
        tree = None

        new_graph = graph.copy()
        new_graph.remove_node(0)
        #find MST
        MST = networkx.minimum_spanning_tree(new_graph, weight='weight')
        two_edge_sum, edge1, edge2 = self.get_lowest_cost_nodes(sorted_tree, 0)
        current = MST.size(weight="weight") + two_edge_sum

        if current < distance_sum:
            distance_sum = current
            tree = MST
            # print(tree.edges)
            #add edges to make a 1-tree
            tree.add_edge(edge1[0], edge1[1], weight=edge1[2]["weight"])
            tree.add_edge(edge2[0], edge2[1], weight=edge2[2]["weight"])
            # print(tree.edges)

        return round(distance_sum), tree

    @staticmethod
    def find_branching(path):
        #find branches that has more than 2 2 edges, for pruning the tree
        for node in path.nodes():
            if path.degree(node) > 2:
                for edge in networkx.edges(path, node):
                    yield edge
                return None

    def dfs(self, root):
        time_record = []
        lower_bound_list = []
        upper_bound, best_path = self.upper_bound(root.copy())
        upper_bound_time = time.time()
        time_record.append(upper_bound_time)
        lower_bound_list.append(upper_bound)
        #print(upper_bound, best_path)
        lower_bound, tree = self.lower_bound(root.copy())
        #generate node and its child node
        queue = [(root, upper_bound, lower_bound, tree)]
        overall_lower_bound = [math.inf]
        while queue:
            if (time.time()-self.start_time) > self.cutout_time:
                break
            root, upper_bound, lower_bound, tree = queue.pop()
            edges_to_remove = list(self.find_branching(tree))
            child_nodes = []
            for edge in edges_to_remove:
                graph = root.copy()
                graph.remove_edge(*edge)
                '''
                #see if the graph is still a full graph after remove the edges
                '''
                if networkx.is_connected(graph):
                    local_ub,_ = self.upper_bound(graph.copy())
                    upper_bound = min(upper_bound, local_ub)

                    lower_bound, tree = self.lower_bound(graph.copy())
                    '''
                    #find the smallest lowerbound
                    '''
                    if self.find_cycle(tree) and lower_bound <= upper_bound and lower_bound < sorted(overall_lower_bound)[0]:
                        upper_bound = lower_bound
                        best_path = tree.nodes
                        record = time.time()
                        time_record.append(record)
                        lower_bound_list.append(lower_bound)
                        overall_lower_bound.append(lower_bound)

                        #print(best_path, upper_bound, record, time_record, lower_bound_list)
                        '''
                        #enter to next level
                        '''
                    child_nodes.append((graph, upper_bound, lower_bound, tree))



            child_nodes = list(filter(lambda x: x[2] < upper_bound, child_nodes))
            child_nodes.sort(key=lambda x: x[2])


            queue += child_nodes
            #print(len(queue))
            #print(tree.edges)

        lower_bound = sorted(lower_bound_list)[0]

        return best_path, lower_bound, time_record, lower_bound_list


def main(filename,cutout_time, city):
    start_time = time.time()
    bnb = branchnbound(filename,start_time, cutout_time)
    matrix = bnb.read_file()
    g = bnb.graph(matrix)
    #print(bnb.upper_bound(g))
    best_path, lower_bound, time_record, lower_bound_list = bnb.dfs(g)
    with open(f'./{city}_BnB_{cutout_time}.sol', 'w') as f1:
        f1.write(str(lower_bound)+ '\n')
        f1.write(','.join(map(str,best_path)))

    with open(f'./{city}_BnB_{cutout_time}.trace', 'w') as f2:
        n = None
        for i in range(len(time_record)):
            if n != lower_bound_list[i]:
                n = lower_bound_list[i]
                # print(time_record)
                f2.write(f"{round(time_record[i] - start_time, 2)}, {n}\n")

        #print("The upperbound for "+ city +" is "+ str(upper_bound))






