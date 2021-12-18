
from typing import Optional

class MinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0
 
    def sift_up(self, i: int ):
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:
                self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
            i = i // 2
 
    def insert(self, k: int):
        self.heap_list.append(k)
        self.current_size += 1
        self.sift_up(self.current_size)
 
    def sift_down(self, i: int):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
            i = mc
 
    def min_child(self, i: int) -> int:
        if (i * 2)+1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i*2] < self.heap_list[(i*2)+1]:
                return i * 2
            else:
                return (i * 2) + 1
 
    def delete_min(self) -> Optional[int]:
        if len(self.heap_list) == 1:
            return None
        root = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        *self.heap_list, _ = self.heap_list
        self.current_size -= 1
        self.sift_down(1)
        return root

def init_heap(name: int) -> MinHeap:
    return name = MinHeap

def insert_from_list(list: list, name: MinHeap) -> None:
    for num in list:
        name.insert(num)


