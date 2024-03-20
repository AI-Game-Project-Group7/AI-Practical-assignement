from random import randint

class Node():
    def __init__(self, num, pts, bankpts, depth, value=0):
        self.num = num
        self.pts = pts
        self.bankpts = bankpts
        self.value = value
        self.depth = depth
        self.parents = []
        self.children = []

    # function which adds parent to already generated node
    def add_parent(self, parent):
        self.parents.append(parent)

    # function which adds child to already generated node
    def add_child(self, child):
        self.children.append(child)

# function to generate 5 numbers in a range from 30000 to 50000
def generate_randoms(low=30000, high=50000, quantity=5):
    startnums = []
    for i in range(quantity):
        startnums.append(randint(low, high))
    return startnums

# function which returns all possible divisors of a number
def check_possible_divisors(num):
    divisors = []
    if num % 2 == 0:
        divisors.append(2)
        if num % 4 == 0:
            divisors.append(4)
    if num % 3 == 0:
        divisors.append(3)
    if num % 5 == 0:
        divisors.append(5)
    return sorted(divisors)

# function which updates total points and bank points
def update_points(num, pts, bankpts):
    if num % 2 == 1:
        pts += 1
    else:
        pts -= 1
    if num % 10 in (0, 5):
        bankpts += 1
    return pts, bankpts

#crea
nodes = []
def game_tree (node, depth, maxdepth=5):
    if depth >= maxdepth:
        return
    divisors = check_possible_divisors(node.num)
    for d in divisors:
        newnum = node.num // d
        newpts, newbankpts = update_points(newnum, node.pts, node.bankpts)
        child_node = Node(newnum, newpts, newbankpts, depth)
        node.add_child(child_node)
        nodes.append(child_node)
        print(nodes)
        game_tree(child_node, depth + 3, maxdepth)
    return nodes


def choose_next_node(num, pts, bankpts, depth=0):
    root = Node(num, pts, bankpts, depth)
    nodes = game_tree (root, 0)
    for node in nodes:
        print(node.num, node.pts, node.bankpts, node.depth)
    # Justin and Anastasia task
    # call this block recursively to generate game tree nodes till depth level 5
    #divisors = check_possible_divisors(num)
    #for d in divisors:
        #newnum = num // d
        #newpts, newbankpts = update_points(newnum, pts, bankpts)
        #nodes.append(Node(newnum, newpts, newbankpts))

    #if not nodes:
        #return 0
    #else:
        #picked_node = hef(nodes)
    return root

choose_next_node(12, -1, 1)

def hef(nodes):
    # abs(pts) + abs(bankpts) + numberofdivisors = odd - first players wins
    # abs(pts) + abs(bankpts) + numberofdivisors  = even - second player wins
    # insert heuristic evaluation function here
    # for now first node is returned
    return nodes[0]


# Hasan, you need to complete this algorithm
# As input, only bottom level nodes have heuristic values,
# For other nodes initial value is 0
def minimax(nodes):
    # the goal is to fill self.value parameter
    # for the potential nodes which computer may choose
    pass






