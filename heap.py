class MaxHeap:
    """
    """

    def __init__(self):
        self.maxsize = 10
        self.size = 0
        self.heap = [None] * self.maxsize + 1
    
    def parent(self, i):
        return self.heap[i // 2]
    
    def left_child(self, i):
        return self.heap[2 * i + 1]
    
    def right_child(self, i):
        return self.heap[2 * i + 2]

    