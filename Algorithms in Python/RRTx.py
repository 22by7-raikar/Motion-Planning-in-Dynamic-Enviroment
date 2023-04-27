class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0

class RRTx:
    def __init__(self, start, goal, obstacles):
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        self.obstacles = obstacles
        self.nodes = []
        self.nodes.append(self.start)
        self.max_iter = 1000
        self.max_dist = 50
        self.path = []
        self.reached_goal = False

    def distance(self, node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def cost(self, node):
        return node.cost

    def nearest_node(self, node):
        min_dist = float('inf')
        nearest_node = None
        for n in self.nodes:
            d = self.distance(node, n)
            if d < min_dist:
                min_dist = d
                nearest_node = n
        return nearest_node

    def steer(self, node1, node2):
        d = self.distance(node1, node2)
        if d <= self.max_dist:
            return node2
        else:
            theta = math.atan2(node2.y - node1.y, node2.x - node1.x)
            new_x = node1.x + self.max_dist * math.cos(theta)
            new_y = node1.y + self.max_dist * math.sin(theta)
            return Node(new_x, new_y)

    def check_collision(self, node1, node2):
        for obstacle in self.obstacles:
            if pygame.sprite.collide_rect(obstacle, Player(node1.x, node1.y)):
                return True
        return False

    def is_goal_reached(self, node):
        return self.distance(node, self.goal) <= 30

    def generate_path(self):
        for i in range(self.max_iter):
            rand_x = random.randint(0, WIDTH)
            rand_y = random.randint(0, HEIGHT)
            rand_node = Node(rand_x, rand_y)
            nearest_node = self.nearest_node(rand_node)
            new_node = self.steer(nearest_node, rand_node)
            if not self.check_collision(nearest_node, new_node):
                new_node.parent = nearest_node
                new_node.cost = nearest_node.cost + self.distance(nearest_node, new_node)
                self.nodes.append(new_node)
                for node in self.nodes:
                    if self.distance(node, new_node) <= self.max_dist and node.cost + self.distance(node, new_node) < new_node.cost:
                        if not self.check_collision(node, new_node):
                            new_node.parent = node
                            new_node.cost = node.cost + self.distance(node, new_node)
                # RRTx specific step
                for node in self.nodes:
                    if self.distance(node, new_node) <= self.max_dist and new_node.cost + self.distance(node, new_node) < node.cost:
                        if not self.check_collision(node, new_node):
                            node.parent = new_node
                            node.cost = new_node.cost + self.distance(node, new_node)
                if self.is_goal_reached(new_node):
                    self.reached_goal = True
                    break
        if self.reached_goal:
            node = self.nodes[-1]
            while node.parent is not None:
                self.path
