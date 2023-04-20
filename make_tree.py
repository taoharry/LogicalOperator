#!/usr/bin/env python
# coding:utf8

# Tree obj
class TraversalTree:

    def __init__(self):
        self.NowId = ''
        self.FatherId = ''
        self.Rule = ''
        self.Child = []

# Many Tree Obj make a tree
class MakeTree(object):

    @staticmethod
    def has_child(v1, vs):
        has_value = False
        for v2 in vs:
            v3 = v2
            if v1.NowId + v1.FatherId == v3.FatherId:
                has_value = True
                break
        return has_value

    @staticmethod
    def find_child(v, vs):
        ret = []
        for v2 in vs:
            if v.NowId + v.FatherId == v2.FatherId:
                ret.append(v2)
            else:
                pass
        return ret

    def make(self, all_nodes, root_node):
        children = self.find_child(root_node, all_nodes)
        for child in children:
            root_node.Child.append(child)
            if self.has_child(child, all_nodes):
                self.make(all_nodes, child)
