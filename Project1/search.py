import time
from resource import getrusage, RUSAGE_SELF
from utils import *

class Problem:
    """
    This is an abstract class that defines the required methods to apply
    search algorithms as seen in class
    """

    def getStartState(self):
        raise "Not implemented"

    def isGoalState(self):
        raise "Not Implemented"

    def getSuccessors(self):
        raise "Not Implemented"

    def getCostOfAction(self):
        raise "Not Implemented"

class Solver:
    """
    This class contains methods that use search algorithms seen in class, and computes
    some statistics about the methods given a problem.
    """
    def __init__(self):
        self.path = []
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 1
        self.max_fringe_size = 1
        self.search_depth = 0
        self.max_search_depth = 0
        self.running_time = 0
        self.max_ram_usage = 0

    def breadthFirstSearch(self, problem):
        """
        Implements Breadth First Search Strategy
        """
        start_time = time.time()
        frontier = Queue()
        frontier.enqueue(problem.getStartState())
        explored = set()
        while not frontier.isEmpty():
            state = frontier.dequeue()
            self.fringe_size -= 1
            explored.add(state)
            if problem.isGoalState(state):
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = state.depth
                self.running_time = time.time() - start_time
                return True
            
            neighbors = problem.getSuccessors(state)
            self.nodes_expanded += 1
            for neighbor in neighbors:
                neighbor.depth = state.depth + 1
                if neighbor not in explored:
                    frontier.enqueue(neighbor)
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.depth > self.max_search_depth:
                        self.max_search_depth = neighbor.depth
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1024
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

             
    def depthFirstSearch(self, problem):
        """
        Implements Depth First Search Strategy
        """
        start_time = time.time()
        frontier = Stack()
        frontier.push(problem.getStartState())
        explored = set()
        while not frontier.isEmpty():
            state = frontier.pop()
            self.fringe_size -= 1
            explored.add(state)
            if problem.isGoalState(state):
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = state.depth
                self.running_time = time.time() - start_time
                return True
            
            neighbors = problem.getSuccessors(state)
            self.nodes_expanded += 1
            neighbors.reverse()
            for neighbor in neighbors:
                neighbor.depth = state.depth + 1
                if neighbor not in explored:
                    frontier.push(neighbor)
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.depth > self.max_search_depth:
                        self.max_search_depth = neighbor.depth
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1024
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

    def depthLimitedSearch(self, problem, limit):
        """
        Implements Depth Limited Search Strategy
        """
        start_time = time.time()
        frontier = Stack()
        frontier.push(problem.getStartState())
        explored = set()
        while not frontier.isEmpty():
            state = frontier.pop()
            self.fringe_size -= 1
            explored.add(state)
            if problem.isGoalState(state):
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = state.depth
                self.running_time = time.time() - start_time
                return True

            if state.depth < limit:
                neighbors = problem.getSuccessors(state)
                self.nodes_expanded += 1
                neighbors.reverse()
                for neighbor in neighbors:
                    neighbor.depth = state.depth + 1
                    if neighbor not in explored:
                        frontier.push(neighbor)
                        explored.add(neighbor)
                        self.fringe_size += 1
                        if self.fringe_size > self.max_fringe_size:
                            self.max_fringe_size = self.fringe_size
                        if neighbor.depth > self.max_search_depth:
                            self.max_search_depth = neighbor.depth
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1024
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

    def iterativeDeepening(self, problem):
        """
        Search for a solution using IDS strategy
        """
        
        # Initial depth
        k = 0

        # Applies DLS using different depths
        while not self.depthLimitedSearch(problem, k):
            self.path = []
            self.cost_of_path = 0
            self.nodes_expanded = 0
            self.fringe_size = 1
            self.max_fringe_size = 1
            self.search_depth = 0
            self.max_search_depth = 0
            self.running_time = 0
            self.max_ram_usage = 0
            k += 1

    def uniformCostSearch(self, problem):
        """
        Implements Depth First Search Strategy
        """
        start_time = time.time()
        frontier = PriorityQueue()
        frontier.insert(problem.getStartState(), 0)
        explored = set()
        while not frontier.isEmpty():
            state = frontier.deleteMin()
            self.fringe_size -= 1
            explored.add(state)
            if problem.isGoalState(state):
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = state.depth
                self.running_time = time.time() - start_time
                return True
            
            neighbors = problem.getSuccessors(state)
            self.nodes_expanded += 1
            for neighbor in neighbors:
                neighbor.depth = state.depth + 1
                if neighbor not in explored:
                    frontier.insert(neighbor, problem.getCostOfAction(neighbor))
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.depth > self.max_search_depth:
                        self.max_search_depth = neighbor.depth
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1024
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

    def aStarSearch(self, problem, h = nullHeuristic):
        """
        Implements A-Star Search Strategy
        """
        start_time = time.time()
        frontier = PriorityQueue()
        frontier.insert(problem.getStartState(), 0)
        explored = set()
        while not frontier.isEmpty():
            state = frontier.deleteMin()
            self.fringe_size -= 1
            explored.add(state)
            if problem.isGoalState(state):
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = state.depth
                self.running_time = time.time() - start_time
                return True
            
            neighbors = problem.getSuccessors(state)
            self.nodes_expanded += 1
            for neighbor in neighbors:
                neighbor.depth = state.depth + 1
                if neighbor not in explored:
                    frontier.insert(neighbor, problem.getCostOfAction(neighbor) + h(neighbor))
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.depth > self.max_search_depth:
                        self.max_search_depth = neighbor.depth
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1024
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False
