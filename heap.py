class myheap(object):
    def __init__(self):
        self.heap = []
        self.d = {}
    def push(self, tp):
        peso = tp[1]
        if tp[0] in self.d:
            for i in self.heap:
                if tp[0] == i[0]:
                    peso = tp[1] + i[1]
                    self.heap.remove((i[0],i[1]))
                    del(self.d[tp[0]])
                    break
                    
        for i in range(len(self.heap)):
            if tp[1] > self.heap[i][1]:
                self.d[tp[0]] = peso
                if (tp[0],peso) not in self.heap:
                    self.heap.insert(i,(tp[0],peso))
                break
        if self.len() < 64 and not tp[0] in self.d and (tp[0],peso) not in self.heap:
            self.heap.append((tp[0],peso))
        if self.len() > 64:
            self.heap = self.heap[:65:]

    def tp_b(self, tp):
        if tp[0] in self.d:
            return self.d[tp[0]]

    def len(self):
        return len(self.heap)

    def pop(self):
        return self.heap.pop(0)

    def tail(self):
        if self.len() >= 20:
            return self.heap[19]
        else:
            return self.heap[-1]
