import heapq
import random
from turtle import width
import pygame
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
file = "results.txt"
pygame.init()
class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def is_empty(self):
        return len(self.list) == 0

class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def is_empty(self):
        return len(self.list) == 0

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def lets_empty(self):
        while len(self.heap) != 0:
            (_, _, item) = heapq.heappop(self.heap)

    def update(self, item, priority):
        for index, (p, c, count) in enumerate(self.heap):
            if count == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class circle(object):
    r = 30
    width = 900

    def __init__(self, start, color=(50, 205, 50)):
        self.position = start
        self.direction_x = 1
        self.direction_y = 0
        self.color = color

    def draw(self, surface, snake_face=False):
        dis = self.width // self.r
        count = self.position[0]
        j = self.position[1]
        pygame.draw.circle(surface, self.color, (count * dis + dis // 2, j * dis + dis // 2), dis // 2)
        if snake_face:
            eye_radius = 2
            mouth_width = 8
            mouth_height = 4
            # Draw left eye
            pygame.draw.circle(surface, (0, 0, 0), (count * dis + dis // 2 - 5, j * dis + 8), eye_radius)
            # Draw right eye
            pygame.draw.circle(surface, (0, 0, 0), (count * dis + dis // 2 + 5, j * dis + 8), eye_radius)
            # Draw mouth
            pygame.draw.rect(surface, (0, 0, 0), (count * dis + dis // 2 - mouth_width // 2, j * dis + 16, mouth_width, mouth_height))

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, position):
        pygame.init()
        self.color = color
        self.head = circle(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1
        self.lines = [self.head]
        self.score = 0

    def movements(self, key):
        directions = {"LEFT": (-1, 0), "RIGHT": (1, 0), "UP": (0, -1), "DOWN": (0, 1)}
        if key in directions:
            self.direction_x, self.direction_y = directions[key]
            self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
        for count, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.direction_x, c.direction_y = turn[0], turn[1]
                c.position = (c.position[0] + c.direction_x, c.position[1] + c.direction_y)
                if count == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if any(
                    [
                        c.direction_x == -1 and c.position[0] <= 0,
                        c.direction_x == 1 and c.position[0] >= c.r - 1,
                        c.direction_y == 1 and c.position[1] >= c.r - 1,
                        c.direction_y == -1 and c.position[1] <= 0,
                    ]
                ):
                    self.end = True
                    self.resetToStart((10, 10))
                else:
                    c.position = (c.position[0] + c.direction_x, c.position[1] + c.direction_y)

    def resetToStart(self, position):
        self.head = circle(position)
        self.body = [self.head]
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1
        self.lines = self.body
        self.score = 0

    def increase_body(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y
        moves = [(1, 0, -1, 0), (-1, 0, 1, 0), (0, 1, 0, -1), (0, -1, 0, 1)]  # Adjusted moves list
        for move in moves:
            dx_move, dy_move, dx_new, dy_new = move
            if dx == dx_move and dy == dy_move:
                new_position = (tail.position[0] + dx_new, tail.position[1] + dy_new)
                self.body.append(circle(new_position))
                self.lines = self.body
                alllines = self.body
                self.body[-1].direction_x = dx
                self.body[-1].direction_y = dy
                break

    def draw(self, surface):
        for count, c in enumerate(self.body):
            c.draw(surface, True) if count == 0 else c.draw(surface)

    def check_goal_state(self, current_position):
        return current_position == storeFood.position

    def start_return(self):
        return self.head.position

    def acheive_goal(self, current_position):
        wall_positions = [wall.position for wall in self.lines]
        success = []
        x, y = current_position
        moves = [(1, 0, "RIGHT", 0.5), (-1, 0, "LEFT", 0.5), (0, 1, "DOWN", 1), (0, -1, "UP", 1)]
        for dx, dy, direction, cost in moves:
            nextX, nextY = x + dx, y + dy
            if not (0 <= nextX < 20 and 0 <= nextY < 20):
                continue
            nextState = nextX, nextY
            if nextState not in wall_positions and nextState != current_position:
                success.append((nextState, direction, euclidean(current_position, storeFood.position) * cost))
        return success

def euclidean(positionition, goal):
    xy1 = positionition
    xy2 = goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5

def draw_grid(width, r, surface):
    space = width // r  
    for x in range(0, width+1, space):
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, width), 2)
    for y in range(0, width+1, space):
        pygame.draw.line(surface, (0, 0, 0), (0, y), (width, y), 2)

def window_updating(surface, snake):
    pygame.init()
    global r, width, snack
    surface.fill((0, 0, 0))
    draw_grid(width, r, surface)
    snake.draw(surface)
    snack.draw(surface)

    # Print the score on the screen
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: {}".format(snake.score), True, (255, 255, 255))
    surface.blit(score_text, (10, 10))
    pygame.display.update()

class Snack:
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        x, y = self.position
        pygame.draw.circle(surface, (255, 0, 0), (x * r + r//2, y * r + r//2), r//2)

def place_snack(r, item):
    positionitions = item.body
    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        if len(list(filter(lambda z: z.position == (x, y), positionitions))) > 0:
            continue
        else:
            break
    return Snack((x, y))

storeFood = []
start_state = 0
start_position = (0, 0)
foodposition = []
def generateFoodposition():
    global foodposition
    foodposition = []
    for j in range(0, 399):
        foodX = random.randrange(19)
        foodY = random.randrange(19)
        food = foodX, foodY
        foodposition.append(food)

generateFoodposition()
action_list = [[], [], []]
score_list = [0, 0, 0]
costs_list = [[], [], []]
costs_avg = [[], [], []]

def common_lines(snake, count):
    global width, r, snack, storeFood, start_state, food
    width = 600
    r = 20
    window = pygame.display.set_mode((width, width))
    start_state = start_position
    snack = circle(foodposition[count], color=(255,0,0))
    storeFood = snack
    clock = pygame.time.Clock()
    return window, clock

def actions(snake, window, clock, directions, speed):
    for direction in directions:
        if speed:
            pygame.time.delay(5)
            clock.tick(30)
        snake.movements(direction)
        window_updating(window, snake)

def DFS(snake, count, speed):
    window, clock = common_lines(snake, count)
    dfs_stack = Stack()
    visited = set()
    dfs_stack.push((snake.start_return(), []))
    pygame.display.set_caption("DFS Algorithm")

    while not dfs_stack.is_empty():
        curr, dir = dfs_stack.pop()
        if curr not in visited:
            visited.add(curr)
            if snake.check_goal_state(curr):
                snake.score += 1
                snake.increase_body()
                actions(snake, window, clock, dir, speed)
                action_list[0].append(len(dir))
                score_list[0] = len(snake.body)
                score_list[0] = snake.score
            for node, direction, cost in snake.acheive_goal(curr):
                if node not in dfs_stack.list and node not in visited:
                    dfs_stack.push((node, dir + [direction]))
                    
def BFS(snake, count, speed):
    window, clock = common_lines(snake, count)
    bfsQ = Queue()
    visited = set()
    bfsQ.push((snake.start_return(), []))
    pygame.display.set_caption("BFS Algorithm")

    while not bfsQ.is_empty():
        curr, dir = bfsQ.pop()
        if curr not in visited:
            visited.add(curr)
            if snake.check_goal_state(curr):
                snake.score += 1
                snake.increase_body()
                actions(snake, window, clock, dir, speed)
                action_list[1].append(len(dir))
                score_list[1] = len(snake.body)
                score_list[1] = snake.score
            for node, direction, cost in snake.acheive_goal(curr):
                if node not in bfsQ.list and node not in visited:
                    bfsQ.push((node, dir + [direction]))

def A_star(snake, count, speed):
    def manhattan(positionition):
        xy1 = positionition
        xy2 = storeFood.position
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    window, clock = common_lines(snake, count)
    aStar_PQ = PriorityQueue()
    visited = set()
    aStar_PQ.push((snake.start_return(), [], 0), 0)
    pygame.display.set_caption("A* Algorithm")

    while not aStar_PQ.is_empty():
        curr, dir, costs = aStar_PQ.pop()
        if curr not in visited:
            visited.add(curr)
            if snake.check_goal_state(curr):
                snake.score += 1
                snake.increase_body()
                actions(snake, window, clock, dir, speed)
                action_list[2].append(len(dir))
                score_list[2] = len(snake.body)
                score_list[2] = snake.score
            for node, direction, cost in snake.acheive_goal(curr):
                if node not in aStar_PQ.heap and node not in visited:
                    hCost = costs + cost + manhattan(node)
                    aStar_PQ.push((node, dir + [direction], costs + cost), hCost)
#------------------ Running Algorihtm ----------------------------#
def run_algorithms(run):
    global action_list
    action_list = [[], [], []]
    mySnake = snake((255, 0, 0), start_position)
    slow_speed = False
    mySnake.resetToStart(start_position)

    print("DFS ", run)
    for count in range(0, len(foodposition)):
        DFS(mySnake, count, slow_speed)
    mySnake.resetToStart(start_position)
    print("BFS ", run)
    for count in range(0, len(foodposition)):
        BFS(mySnake, count, slow_speed)
    mySnake.resetToStart(start_position)
    print("RUNNING ASTAR#", run)
    for count in range(0, len(foodposition)):
        A_star(mySnake, count, slow_speed)
    mySnake.resetToStart(start_position)
    # --------- Calculate Scores

    DFS_actions = sum(action_list[0])
    BFS_actions = sum(action_list[1])
    AStar_actions = sum(action_list[2])
    print("Total DFS actions taken:", DFS_actions)
    print("Total BFS actions taken:", BFS_actions)
    print("Total A_Star actions taken:", AStar_actions)
    print("RAW SCORES [ DFS, BFS, ASTAR ]: ")
    print(score_list)
    calcScores = [0, 0, 0]
    calcScores[0] = (score_list[0] / DFS_actions) * 100
    calcScores[1] = (score_list[1] / BFS_actions) * 100
    calcScores[2] = (score_list[2] / AStar_actions) * 100

    print("DFS score:", calcScores[0])
    print("BFS score:", calcScores[1])
    print("A_Star score:", calcScores[2])

    costs_list[0].append(calcScores[0])
    costs_list[1].append(calcScores[1])
    costs_list[2].append(calcScores[2])

    # ---------------- Write to file

    file = "results.txt"  # File path for writing results
    my_file = open(file, "a")
    my_file.write(f"RUN NUMBER: {run} DATE: {datetime.now()}\n")
    my_file.write(f"BFS ACTIONS: {BFS_actions:>14}\n")
    my_file.write(f"DFS ACTIONS: {DFS_actions:>14}\n")
    my_file.write(f"RAW BFS SCORE: {score_list[0]:>14}\n")
    my_file.write(f"RAW DFS SCORE: {score_list[1]:>14}\n")
    my_file.write(f"CALC BFS SCORE: {calcScores[0]:>14}\n")
    my_file.write(f"CALC DFS SCORE: {calcScores[1]:>14}\n")
    my_file.write(f"CALC BFS SCORE: {calcScores[0]:>14}\n")
    my_file.write(f"CALC DFS SCORE: {calcScores[1]:>14}\n")
    my_file.write(f"CALC ASTAR SCORE:{calcScores[2]:>14}\n")
    my_file.close()

    # Pad action lists with zeros
    maxLen = max(len(action_list[0]), len(action_list[1]), len(action_list[2]))
    for i in range(3):
        action_list[i] += [0] * (maxLen - len(action_list[i]))

    data = {"Algorithm": ["DFS", "BFS", "ASTAR"],
            "Score": [round(x, 2) for x in calcScores]}
    dataFrame = pd.DataFrame(data=data)
    ax = dataFrame.plot(kind='bar', x="Algorithm", y="Score", color=["#007ACC"], rot=0,
                        title=f"Snake Game")
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show(block=True)

    print(len(action_list[0]))
    print(len(action_list[1]))
    print(len(action_list[2]))

    algorithms = ["DFS", "BFS", "ASTAR"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for i, algorithm in enumerate(algorithms):
        data = {"Score": range(maxLen), algorithm: action_list[i]}
        df = pd.DataFrame(data=data)
        df.plot(kind='line', x="Score", y=algorithm, rot=70,
                title="Actions of Snake Game Search Algorithms - " + algorithm,
                color=colors[i])
    plt.show()
    pygame.quit()

run_algorithms(400)