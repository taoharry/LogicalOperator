import unittest
import json
from .make_tree import TraversalTree, MakeTree
from .tree_relation import TreeRelation


class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_make_tree():
        traversal_trees = []
        a = TraversalTree()
        a.NowId = "1"
        a.FatherId = ""
        traversal_trees.append(a)
        a = TraversalTree()
        a.NowId = "3"
        a.FatherId = "1"
        traversal_trees.append(a)
        a = TraversalTree()
        a.NowId = "4"
        a.FatherId = "1"
        traversal_trees.append(a)
        a = TraversalTree()
        a.NowId = "5"
        a.FatherId = "31"
        traversal_trees.append(a)
        a = TraversalTree()
        a.NowId = "6"
        a.FatherId = "31"
        traversal_trees.append(a)

        p_traversal_trees = []
        for i in range(len(traversal_trees)):
            p_traversal_trees.append(traversal_trees[i])

        node = traversal_trees[0]
        MakeTree().make(p_traversal_trees, node)

        data = json.dumps(node, default=lambda o: o.__dict__, indent=4)
        print(data)

    @staticmethod
    def test_parser_rule():
        tr = TreeRelation()
        for rule in [
            "a && ((b || c) && d)",
            "rule1 && (rule2 && (rule3 || rule4) && (rule5 && rule6)) &&  (rule7 != (rule8 || rule9)) || rule10",
            "a!=b&&c"
        ]:
            print(f"------------开始解析------------")
            priority, record, keyRules = tr.relational_analysis(rule)
            print(f"执行顺序 = {priority}")
            print(f"测试映射结果 = {record}")
            print(f"生成key值 = {keyRules}" )
            print(f"------------解析结束------------")

    def test_tree_map(self):
        tr = TreeRelation()
        priority = []
        record = {}
        rule = "rule1 && (rule2 && (rule3 || rule4) && (rule5 && rule6)) &&  (rule7 != (rule8 || rule9)) || rule10"
        priority, record = tr.parser_rule(rule, 1, priority, record)
        print(f"执行顺序 = {priority}")
        print(f"测试映射结果 = {record}")
        tr.make_rule_tree(record)


if __name__ == '__main__':
    unittest.main()
