class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []

    def ReplaceParent(self, parent):
        self.parent = parent

    def AddChild(self, child):
        self.children.append(child)

    def RemoveChildAtIndex(self, index):
        self.children.remove(index)