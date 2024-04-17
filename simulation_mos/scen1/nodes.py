from random import random

class Node(object):
	# likelihood of a node to accept misinformation from incident node
	persuasion_probability = 0.4

	def __init__(self, belief=0):
		self.belief = belief

	def collect_beliefs(self):
		# if node has neighbor with misinformation and random event occurs,
		if -1 in [n.belief for n in self.neighbors] and random() <= Node.persuasion_probability:
			return -1
		elif 1 in [n.belief for n in self.neighbors]:
			return 1
		return self.belief

	def update_belief(self, belief):
		self.belief = belief
		return self.belief

class Instructor(Node):
	def __init__(self, name=None):
		self.name = name if name is not None else "Johnson"
		super().__init__(1)

	def update_belief(self, belief):
		# instructors know correct information
		pass

	def __repr__(self):
		return "Instructor " + str(self.name)

class Student(Node):
    # likelihood of a Student generating misinformation in a given timestep
    corruption_probability = 0.01

    def __init__(self, name=None):
        self.name = name if name is not None else "Johnson"
        self.neighbors = []
        self.belief = 0

    def collect_beliefs(self):
        # If the node has no neighbors, maintain neutral belief
        if not self.neighbors:
            return self.belief

        # If the node has neighbors, decide whether to generate misinformation
        if random() <= Student.corruption_probability:
            return -1  # Misinformation generated
	
        else:
            return super().collect_beliefs()  # Maintain current belief if no misinformation generated

    def add_neighbor(self, neighbor):
        if neighbor is not None:
            self.neighbors.append(neighbor)

    def __repr__(self):
        return "Student " + str(self.name)
