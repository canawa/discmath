import matplotlib.pyplot as plt
import re
from operations import *

ops = {
    "inv": inv,
    "conj": conj,
    "disj": disj,
    "imp": imp,
    "xor": xor,
    "eq": eq,
    "pierce": pierce,
    "sheffer": sheffer
}

labels = {
    'xor': '⊕',
    'inv': '¬',
    'pierce': '↓',
    'sheffer': '|',
    'imp': '→',
    'eq': '∼',
    'conj': '⋀',
    'disj': '⋁',
}


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def split_args(s: str):
    args = []
    depth = 0
    cur = ""

    for ch in s:
        if ch == "," and depth == 0:
            args.append(cur)
            cur = ""
        else:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            cur += ch

    if cur:
        args.append(cur)

    return args


def parse(expr: str):
    expr = expr.replace(" ", "")

    if re.fullmatch(r"[a-z]", expr):
        return Node(expr)

    for name in ops.keys():
        if expr.startswith(name + "(") and expr.endswith(")"):
            inner = expr[len(name) + 1:-1]
            args = split_args(inner)
            children = [parse(a) for a in args]
            return Node(name, children)

    raise ValueError(f"Cannot parse: {expr}")


def collect_nodes(node, out):
    for c in node.children:
        collect_nodes(c, out)
    out.append(node)


def extract_vars(nodes):
    return sorted({
        n.value for n in nodes if re.fullmatch(r"[a-z]", n.value)
    })


def evaluate(node, env, cache):
    if node.value in env:
        return env[node.value]

    if node in cache:
        return cache[node]

    args = [evaluate(c, env, cache) for c in node.children]
    res = ops[node.value](*args)

    cache[node] = res
    return res


def to_infix(node):
    # переменная
    if node.value not in ops or not node.children:
        return node.value

    # отрицание
    if node.value == "inv":
        child = to_infix(node.children[0])

        # всегда показываем скобки, если это не переменная
        if len(node.children[0].children) > 0:
            return f"¬({child})"
        return f"¬{child}"

    # бинарные операции
    if len(node.children) == 2:
        left = to_infix(node.children[0])
        right = to_infix(node.children[1])

        return f"({left} {labels[node.value]} {right})"

    # на случай неожиданных форм
    return f"{labels.get(node.value, node.value)}({', '.join(to_infix(c) for c in node.children)})"


def draw_truth_table(img_name: str, function: str):
    root = parse(function)

    nodes = []
    collect_nodes(root, nodes)

    seen = set()
    unique_nodes = []
    for n in nodes:
        if id(n) not in seen:
            unique_nodes.append(n)
            seen.add(id(n))

    variables = extract_vars(unique_nodes)
    var_count = len(variables)

    expr_nodes = [n for n in unique_nodes if n.value not in variables]

    table_data = []

    for i in range(2 ** var_count):
        bits = list(map(int, format(i, f"0{var_count}b")))
        env = dict(zip(variables, bits))

        cache = {}
        row = []

        for v in variables:
            row.append(env[v])

        for node in expr_nodes:
            row.append(evaluate(node, env, cache))

        table_data.append(row)

    col_labels = variables + [to_infix(n) for n in expr_nodes]

    fig, ax = plt.subplots()
    ax.axis("off")

    ax.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="center"
    )

    plt.savefig(f"{img_name}.png", bbox_inches="tight")
    plt.close()