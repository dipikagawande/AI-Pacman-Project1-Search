# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  
        The sequence must be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, strategy = "dfs", heuristic=nullHeuristic) 


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, strategy = "bfs", heuristic=nullHeuristic) 
   
    
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, strategy = "ucs", heuristic=nullHeuristic) 


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, strategy = "astar", heuristic=heuristic)  


def genericSearch(problem, strategy, heuristic):
    """
    A generic search algorithm that is called by DFS, BFS, UCS and A-star
    functions above. The strategy argument determines which of the 4 search
    algorithms will be carried out. The heuristic argument calls the 
    nullHeuristic for all strategies but A-star.

    Written according to the generic search algorithm pseudocode from PSET 1.

    We use dictionaries for the closed list and running versions of the open 
    list, so that nodes can be used as keys to retrieve their corresponding 
    action or parent. Earlier instances of nodes are automatically replaced with 
    later ones if the priority condition is met (since we don't want duplicate
    nodes in the open list in BFS or A-star search).
    """
    ####################
    ## Initialization ##
    ####################
    ## Initialize the open list as a stack (DFS) or a queue (BFS)
    if strategy == "dfs":
        open = util.Stack()
    if strategy == "bfs":
        open = util.Queue()
    if strategy in ["ucs", "astar"]:
        open = util.PriorityQueue()
        ## Initialize open cost list as dictionary with entries (n : cost)
        openCost = {}  
    ## Initialize running version of open list as dictionary with entries (n : parent)
    openRunning = {} 
    ## Initialize closed list as a dictionary with entries (n : action).
    closed = {}
    ## Initialize final solution path as an empty list.
    path = []

    ## Push the start node onto the open list
    startNode = problem.getStartState()
    if strategy in ["bfs", "dfs"]:
        open.push((startNode, '', 0))
    if strategy in ["ucs", "astar"]:
        open.push((startNode, '', 0), 0)

    #######################
    ## Search iterations ##
    #######################
    ## While open list is not empty:
    while not open.isEmpty():
        ## Pop next node n from the open list
        thisNode = open.pop()
        ## Add/replace n in the closed list
        closed[thisNode[0]] = thisNode[1]

        ## (Late goal-check) If n is the goal:
        if problem.isGoalState(thisNode[0]):
            ## If this node is the goal, need to backtrack for solution path.
            child = thisNode[0]

            ## Now backtrack through the closed list for solution path
            while(child in openRunning.keys()):
                print("Current child is", child)
                ## Set predecessor node from running open list as parent
                parent = openRunning[child]
                ## Add its child's ACTION to index 0 of path list
                path.insert(0, closed[child])
                ## Set predecessor parent as new child to continue backtrack
                child = parent
                
            return path

        #######################
        ## Manage the fringe ##
        #######################
        if strategy == "dfs":
            ## For each successor node n' of n
            for nPrime in problem.getSuccessors(thisNode[0]):
                ## If n' not in closed list:
                if nPrime[0] not in closed.keys():
                    ## Set n as parent of n' by adding (n' : n) to running open list
                    openRunning[nPrime[0]] = thisNode[0]
                    ## Push n' onto the open list
                    open.push(nPrime)

        if strategy == "bfs":
            ## For each successor node n' of n
            for nPrime in problem.getSuccessors(thisNode[0]):
                ## If n' neither in closed list NOR in open list:
                if nPrime[0] not in closed.keys() and nPrime[0] not in openRunning.keys():
                    ## Set n as parent of n' by adding (n' : n) to running open list
                    openRunning[nPrime[0]] = thisNode[0]
                    ## Push n' onto the open list
                    open.push(nPrime)

        if strategy in ["ucs", "astar"]:
            ## For each successor node n' of n
            for nPrime in problem.getSuccessors(thisNode[0]):
                ## Let c' be cumulative cost of moving from start to n’ via n
                g = thisNode[2] + nPrime[2]
                cPrime = g + heuristic(nPrime[0], problem)
                ## If n' not in closed list:
                if nPrime[0] not in closed.keys():
                    ## If n' not in running open list OR if n' exists with c > c':
                    if nPrime[0] not in openCost.keys() or openCost[nPrime[0]] > cPrime:
                        ## Set n parent of n', add/replace (n' : n) to running open list
                        openRunning[nPrime[0]] = thisNode[0]
                        ## Add/replace (n' : cost') to the open cost list
                        openCost[nPrime[0]] = cPrime
                        ## Push n' onto the open list
                        open.push(item = (nPrime[0], nPrime[1], g), priority = cPrime)

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

