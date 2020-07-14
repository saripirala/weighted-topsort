"""
It is an implementation of Topological sort using Depth First Search.
The implementation provides a way to sort the nodes of the graph based on
the weights assigned to each node. When a node is dependent on two other nodes
the node with lowest weight is resolved first.

The input graph is a json structure with dependecies for the node are
indicated as a list. The weights for the nodes are provided as a set of
tag-value pairs.

"""

import heapq
from collections import deque


class CyclicGraphError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.errors = message


class TopSort(list):
    """
    Topological sort with weighted nodes

    :param graph: Directed graph to be sorted in json format with
                  dependencies as values to nodes
    :type  graph: json
    :param weights: The weights of nodes as json key value pairs
    :type weights: json

    :rtype: list

    """
    def __init__(self, graph, weights):
        self.data = graph
        self.weights = weights.copy()
        self.visit_stack = deque()
        self.sort_stack = deque()
        self.__process_nodes(self.data)

    def __iter__(self):
        return iter(self.sort_stack)

    def __process_nodes(self, jsondata):
        keys_heap = [(self.weights.get(k, 1), k) for k in jsondata.keys()]
        heapq.heapify(keys_heap)

        while keys_heap:
            _, key = heapq.heappop(keys_heap)
            if not (key in self.visit_stack):
                self.visit_stack.append(key)
                if jsondata.get(key):
                    ch_keys_heap = [
                        (self.weights.get(k, 1), k) for k in jsondata.get(key)
                    ]
                    heapq.heapify(ch_keys_heap)

                    while ch_keys_heap:
                        _, ch_val = heapq.heappop(ch_keys_heap)
                        if not (ch_val in self.visit_stack):
                            if str(ch_val) in self.data.keys():
                                self.__process_nodes(
                                    {ch_val: self.data.get(str(ch_val))})
                            else:
                                self.visit_stack.append(ch_val)
                                self.sort_stack.append(str(ch_val))
                        elif not (ch_val in self.sort_stack):
                            raise CyclicGraphError(
                                'Cycle detected in path {} -> {}'
                                .format(str(self.visit_stack), str(ch_val)))
                self.sort_stack.append(str(key))
        return self.sort_stack
