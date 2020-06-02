class Node:
    def __init__(self, v):
        self.v = v
        self.next = None

class Queue:

    def __init__(self):
        self.head = None
        self.tail = None  # for enqueue (끝부분을 기억해 append)

    def is_empty(self):
        return False if self.head else True

    def enqueue(self, data):
        next_node = Node(data)
        if self.is_empty():
            self.head = next_node
            self.tail = next_node
        else:
            self.tail.next = next_node
            self.tail = next_node

    def dequeue(self):
        if self.is_empty(): return None

        result = self.head.data
        self.head = self.head.next
        return result