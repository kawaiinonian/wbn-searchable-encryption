class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def build_forest(edges):
    nodes = {}
    
    for a, b in edges:
        if a not in nodes:
            nodes[a] = TreeNode(a)
        if b not in nodes:
            nodes[b] = TreeNode(b)
        
        nodes[a].children.append(nodes[b])
    
    roots = [node for node in nodes.values() if not any(node in n.children for n in nodes.values())]
    return roots

def print_tree(node, depth=0, is_last=True):
    if depth == 0:
        print(str(node.value), end="")
    else:
        prefix = "    " * (depth - 1) + ("└── " if is_last else "├── ") + str(node.value)
        print("\n" + prefix, end="")
    
    for index, child in enumerate(node.children):
        is_last_child = index == len(node.children) - 1
        print_tree(child, depth + 1, is_last_child)

# # 示例输入：列表中的元组代表边的关系
# edge_list = [(1, 2), (1, 3), (2, 7), (4, 5), (6, 4)]

# forest = build_forest(edge_list)

# print("Forest Structure:")
# for tree in forest:
#     print_tree(tree)
#     print("\n" + "-" * 20)