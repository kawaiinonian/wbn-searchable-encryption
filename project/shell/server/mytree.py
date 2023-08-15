class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def build_forest(edges):
    trees = {}
    nodes = {}
    
    for a, b, tree_id in edges:
        if a not in nodes:
            nodes[a] = TreeNode(a)
        if b not in nodes:
            nodes[b] = TreeNode(b)
        
        if tree_id not in trees:
            trees[tree_id] = []
        trees[tree_id].append((a, b))
    
    forest_roots = []
    for tree_id, tree_edges in trees.items():
        tree_nodes = set()
        for a, b in tree_edges:
            tree_nodes.add(a)
            tree_nodes.add(b)
        root_candidates = set(tree_nodes)
        for a, b in tree_edges:
            if b in root_candidates:
                root_candidates.remove(b)
        root = root_candidates.pop()
        forest_roots.append((tree_id, root, tree_edges))
    
    return forest_roots

def print_tree(tree_id, node, edges, depth=0, is_last=True):
    if depth == 0:
        print(tree_id)
        print(str(node.value), end="")
    else:
        prefix = "    " * (depth - 1) + ("└── " if is_last else "├── ") + str(node.value)
        print("\n" + prefix, end="")
    
    children = [b for a, b in edges if a == node.value]
    for index, child_value in enumerate(children):
        is_last_child = index == len(children) - 1
        child_edges = [(a, b) for a, b in edges if a == node.value and b == child_value]
        child_node = TreeNode(child_value)
        print_tree(tree_id, child_node, child_edges, depth + 1, is_last_child)

# # 示例输入：列表中的元组代表边的关系，以及边所属的树的标识
# edge_list = [(1, 2, 'A'), (1, 3, 'A'), (2, 7, 'B'), (4, 5, 'C'), (6, 4, 'D')]

# forest = build_forest(edge_list)

# print("Forest Structure:")
# for tree_id, root, edges in forest:
#     root_node = TreeNode(root)
#     print_tree(tree_id, root_node, edges)
#     print("\n" + "-" * 20)