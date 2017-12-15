from collections import defaultdict

class nodedict(defaultdict):
    def __missing__(self, key):
        ret = self[key] = set([key])
        return ret

def build_groups(connections):
    groups = nodedict()

    for node, *neighbours in connections:
        merged_group = set.union(groups[node], *(groups[neighbour] for neighbour in neighbours))

        for union_node in merged_group:
            groups[union_node] = merged_group

    return groups
