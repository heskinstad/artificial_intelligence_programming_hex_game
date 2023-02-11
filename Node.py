class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []

    def replace_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def remove_child_at_index(self, index):
        self.children.remove(index)