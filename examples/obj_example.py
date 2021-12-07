from __future__ import annotations


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next = None

    def get_value(self) -> int:
        return self.value

    def set_next(self, node: Node) -> None:
        self.next = node


class LinkedList:
    def __init__(self, node: Node) -> None:
        self.head = node

    def get_length(self) -> int:
        current = self.head
        count = 0
        while current is not None:
            count += 1
            current = current.next
        return count


def is_next(node1: Node, node2: Node) -> bool:
    return node1.next == node2


def is_equal(node1: Node, node2: Node) -> bool:
    return node1.value == node2.value
