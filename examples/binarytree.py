class BinaryTree:
   def __init__(self, data) -> None:
      self.left = None
      self.right = None
      self.data = data

   def insert(self, data) -> None:
      if self.data:
        if data < self.data:
            if self.left is None:
               self.left = BinaryTree(data)
            else:
               self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right = BinaryTree(data)
            else:
                self.right.insert(data)
      else:
         self.data = data
   def PrintTree(self) -> None:
      if self.left:
         self.left.PrintTree()
      print( self.data),
      if self.right:
         self.right.PrintTree()


def tree(name: str) ->BinaryTree:
    name = BinaryTree(12)
    root.insert(6)
    root.insert(14)
    root.insert(3)
    root.PrintTree()

    return name
