# MXA220164
# Mustafa Alawad
# CS 3345.009
# Project 1


class Node: # Consturtor for node class 
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree: # Constructor for Splay Tree
    def __init__(self):
        self.root = None

    # Right rotation around node x
    def _right_rotate(self, x):
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    # Left rotation around node x
    def _left_rotate(self, x):
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    # Splay node x to the root using bottom-up splaying
    def splay(self, x):
        if x is None:
            return
        while x.parent is not None:
            if x.parent.parent is None:
                # Zig step: x is child of root.
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left == x and g.left == p:
                    # Zig-zig: both are left children.
                    self._right_rotate(g)
                    self._right_rotate(p)
                elif p.right == x and g.right == p:
                    # Zig-zig: both are right children.
                    self._left_rotate(g)
                    self._left_rotate(p)
                elif p.left == x and g.right == p:
                    # Zig-zag: x is left child and p is right child.
                    self._right_rotate(p)
                    self._left_rotate(g)
                elif p.right == x and g.left == p:
                    # Zig-zag: x is right child and p is left child.
                    self._left_rotate(p)
                    self._right_rotate(g)

    # Insert key into the tree.
    def insert(self, key):
        node = Node(key)
        y = None
        x = self.root
        while x:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                # Key already exists; splay the found node.
                self.splay(x)
                return
        node.parent = y
        if y is None:
            self.root = node  # Tree was empty
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self.splay(node)

    # Search for key; if found, splay it to the root.
    # If not found, splay the last accessed node.
    def search(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self.splay(x)
                return x
        if last:
            self.splay(last)
        return None

    # Delete key from the tree.
    def delete(self, key):
        node = self.search(key)
        if node is None or node.key != key:
            print("Key not found in the tree.")
            return

        # At this point the node is at the root.
        if node.left:
            left_subtree = node.left
            left_subtree.parent = None
        else:
            left_subtree = None

        if node.right:
            right_subtree = node.right
            right_subtree.parent = None
        else:
            right_subtree = None

        if left_subtree:
            # Splay the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            self.splay(max_node)
            # Attach right subtree.
            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node
            self.root = max_node
        else:
            self.root = right_subtree

    # Helper function for preorder traversal.
    def _preorder_helper(self, node, result):
        if not node:
            return
        if node.parent is None:
            suffix = "RT"
        elif node.parent.left == node:
            suffix = "L"
        else:
            suffix = "R"
        result.append(f"{node.key}{suffix}")
        self._preorder_helper(node.left, result)
        self._preorder_helper(node.right, result)

    # Print the tree in preorder with formatting.
    def print_preorder(self):
        result = []
        self._preorder_helper(self.root, result)
        print(", ".join(result))

# baisc I/O to interact with the Splay Tree created.
def main():
    tree = SplayTree()
    
    # Initialize the tree with nodes 1 to N.
    n_input = input("Enter the initial number of nodes (N): ").strip()
    if n_input.isdigit():
        N = int(n_input)
        for i in range(1, N + 1):
            tree.insert(i)
        print("Initial tree (preorder):")
        tree.print_preorder()
    else:
        print("Invalid input for N.")
        return

    # Go thru I/O until the user exits. 
    print("\nEnter operations in the format 'insert k', 'delete k', or 'search k' (or type 'exit' to quit):")
    while True:
        line = input().strip()
        if line.lower() == "exit":
            break
        parts = line.split()
        if len(parts) != 2:
            print("Invalid operation format. Please use: operation key")
            continue
        op, key_str = parts
        try:
            key = int(key_str)
        except ValueError:
            print("The key must be an integer.")
            continue

        if op.lower() == "insert":
            tree.insert(key)
            print("After insert operation:")
            tree.print_preorder()
        elif op.lower() == "delete":
            tree.delete(key)
            print("After delete operation:")
            tree.print_preorder()
        elif op.lower() == "search":
            result = tree.search(key)
            if result and result.key == key:
                print(f"Key {key} found.")
            else:
                print(f"Key {key} not found.")
            print("After search operation:")
            tree.print_preorder()
        else:
            print("Unknown operation. Please use 'insert', 'delete', or 'search'.")

if __name__ == "__main__":
    main()