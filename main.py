from random import randint

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

def choose_next_node(num, pts, bankpts):
    divisors = check_possible_divisors(num)
    nodes = []
    for d in divisors:
        newnum = num / d
        newpts, newbankpts = update_points(newnum, pts, bankpts)
        nodes.append(Node(newnum, newpts, newbankpts))
    if not nodes:
        return 0
    else:
        picked_node = hef(nodes)
    return picked_node


def hef(nodes):
    # insert heuristic evaluation function here
    # for now first node is returned
    return nodes[0]


class Node():
    def __init__(self, num, pts, bankpts, value=0):
        self.num = num
        self.pts = pts
        self.bankpts = bankpts
        self.value = value

choose_next_node(60,0,0)


