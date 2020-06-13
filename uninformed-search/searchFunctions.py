import util
import time
import sys

from game import Directions

UNREACHABLE_GOAL_STATE = [Directions.STOP]

def tinyMazeSearch(problem): #Best answer for tiny maze

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


#Hamfekri ba sepehr babapour 96481073 va mobin dariush kheili komak kard :)))
def bfs(problem): #Q3
    visited = []
    result = []
    parent = {}
    queue = util.Queue()
    queue.push(problem.getStartState())
    while not queue.isEmpty():
        s = queue.pop()
        visited.append(s)
        if problem.isGoalState(s):
            temp = s
            while True:
                if (temp == problem.getStartState()):
                    break
                result.insert(0, temp[2])
                temp = parent[temp]

            return result
        for element in problem.getNextStates(s):
            if element not in visited and element not in (state for state in queue.list):
                parent[element] = s
                queue.push(element)


#Hamfekri ba sepehr babapour 96481073
def iddfs(problem): #Q1
    
    temp = []
    ans = []
    count = 0
    visitedLen = []
    
    # max = problem.walls.height * problem.walls.width
    # print max
    # blah = bounded_dfs(problem, max)
    # print "Done"
    # if len(blah) == 0:
    #     return [Directions.STOP]
    
    while (1):
        temp = bounded_dfs(problem, count)
        if len(temp[0]) != 0:
            break
        if temp[1] == visitedLen:
            return [Directions.STOP]
        count += 1
        visitedLen = temp[1]

    for element in temp[0]:
        ans.append(element[1])

    ans.pop(0)
    return ans

def bounded_dfs(problem, depth): #Function for Q1
    visited = []
    result = []
    history = []
    stack = util.Stack()
    
    stack.push((problem.getStartState(), Directions.STOP, 0))
    while not stack.isEmpty():
        s = stack.pop()
        visited.append(s[0])
        history.append(len(result))
        result.append(s)
        if problem.isGoalState(s[0]):
            return (result, visited)
        for element in problem.getNextStates(s[0]):
            # print element
            if len(result) == depth + 1:
                visited.append(element[0])
                history.append(len(result))           
            elif (element[0] not in visited) or (element[0] in visited and len(result) < history[visited.index(element[0])]):
                stack.push(element)
        i = len(result) - 1
        while isLeaf(problem, visited, result[i], history, result):
            result.pop()
            if len(result) == 0:
                break
            i = i - 1
    return ([], visited)
    
def isLeaf(problem, visited, item, history, result): #Function for Q1
    flag = True
    for element in problem.getNextStates(item[0]):
        if (element[0] not in visited) or (element[0] in visited and len(result) < conditionHelper(visited, element[0], history)):
            flag = False
    return flag

def conditionHelper(visited, element, history): #Function for Q1
    result = float('inf')
    for i in range(0, len(visited)):
        if visited[i] == element and history[i] < result:
            result = history[i]
    return result
    

def hide_and_seek(problem): #Q2
    
    visitedCorners = []
    if (isCorner(problem, problem.getStartState())):
        visitedCorners.append(problem.getStartState())
    result = []
    root = problem.getStartState()

    while(True):
        temp = bfs_for_Q2(problem, visitedCorners, root)
        if len(temp) == 0:
            break
        visitedCorners.append(temp[len(temp)-1])
        for item in temp:
            result.append(item)
        root = temp[len(temp)-1]

    lastCorner = result[len(result) -1]
    temp = bfs_for_goal(problem, lastCorner)
    for item in temp:
        result.append(item)

    ans = []
    for i in range(0, len(result) - 1):
        current = result[i]
        next = result[i+1]
        if current[0] - next[0] == 1:
            ans.append(Directions.WEST)
        if next[0] - current[0] == 1:
            ans.append(Directions.EAST)
        if current[1] - next[1] == 1:
            ans.append(Directions.SOUTH)
        if next[1] - current[1] == 1:
            ans.append(Directions.NORTH)
    return ans

def bfs_for_Q2(problem, visitedCorners, root): #Function for Q2
    
    visited = []
    queue = util.Queue()
    queue.push((root, []))

    while(True):
        if queue.isEmpty():
            return []

        current,path = queue.pop()
        visited.append(current)

        for child in problem.getNextStates(current):
            if child[0] not in visited and child[0] and child[0] not in (state[0] for state in queue.list):
                newPath = path + [current]
                if isCorner(problem, child[0]) and child[0] not in visitedCorners:
                    return  newPath + [child[0]]
                queue.push((child[0],newPath))


def isCorner(problem, state): #Function for Q2
    next = problem.getNextStates(state)
    if (len(next) == 2 and abs(next[0][0][0] - next[1][0][0]) == 1 and abs(next[0][0][1] - next[1][0][1]) == 1):
        return True
    return False
        
def bfs_for_goal(problem, start): #Function for Q2
    visited = []
    queue = util.Queue()
    queue.push((start, []))

    while(True):
        if queue.isEmpty():
            return []

        current,path = queue.pop()
        visited.append(current)

        for child in problem.getNextStates(current):
            if child[0] not in visited and child[0] not in (state[0] for state in queue.list):
                newPath = path + [current]
                if problem.isGoalState(child[0]):
                    return  newPath + [child[0]]
                queue.push((child[0],newPath))

def ucs(problem): #Q4
   
    pq = util.PriorityQueue()
    startNode = (problem.getStartState(), [], 0)
    pq.push(startNode, 0)
    visited = []

    while not pq.isEmpty():
        current = pq.pop()
        if problem.isGoalState(current[0]):
            return current[1]
        if current[0] not in visited:
            visited.append(current[0])
            for child in problem.getNextStates(current[0]):
                if child[0] not in visited:
                    cost = current[2] + child[2]
                    pq.push((child[0], current[1] + [child[1]], cost), cost)

