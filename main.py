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

# functions to generate the game tree
'''The creation of the list 'nodes' is only meant for helping debugging and we could consider to delete it later.'''
nodes = [] # for display
def game_tree (node, depth, maxdepth=5):
    if depth >= maxdepth:
        return
    divisors = check_possible_divisors(node.num)
    for d in divisors:
        newnum = node.num // d
        newpts, newbankpts = update_points(newnum, node.pts, node.bankpts)

        child_node = Node(newnum, newpts, newbankpts, depth + 1)
        child_node.divisor = d
        node.add_child(child_node)
        nodes.append(child_node) # for display

        game_tree(child_node, depth + 1, maxdepth)
    return nodes # for display


def hef(node):
    final_pts = node.pts + node.bankpts if node.pts % 2 == 0 else node.pts - node.bankpts
    final_score_parity = final_pts % 2  
    node.value = 0
    num_divisors = len(check_possible_divisors(node.num))

    if final_score_parity == 1:
        node.value += -999 
    else: 
        node.value += 999   
        
    node.value += num_divisors
    # node.value += node.depth

    return node.value


def minimax(node, is_max_turn):
    if not node.children:  # If leaf node, return its heuristic value
        node.value = hef(node)
        return node.value

    if is_max_turn:
        # Maximizing player (human): looking for a high heuristic value
        max_eval = float('-inf')
        for child in node.children:
            eval = minimax(child, False)
            max_eval = max(max_eval, eval)
        node.value = max_eval
        return node.value
    else:
        # Minimizing player (computer): looking for a low heuristic value
        min_eval = float('inf')
        for child in node.children:
            eval = minimax(child, True)
            min_eval = min(min_eval, eval)
        node.value = min_eval
        return node.value


def print_tree(node, level=0):
    # Print the current node's details
    print('  ' * level + f'Num: {node.num}, Pts: {node.pts}, BankPts: {node.bankpts}, Depth: {node.depth}, Value: {node.value}, Divisor: {getattr(node, "divisor", "N/A")}')
    
    # Recursively print each child
    for child in node.children:
        print_tree(child, level + 1)

def choose_next_node(num, pts, bankpts, depth=0):
    root = Node(num, pts, bankpts, depth)
    nodes = game_tree(root, depth)

    # Start minimax from the root node, assuming human starts the game
    minimax(root, True)
    print_tree(root)

    # Choose the child of the root with the minimum value (computer's best move)
    best_move = min(root.children, key=lambda x: x.value)
    print(best_move.divisor)
    return best_move.divisor


choose_next_node(300, -1, 1)




