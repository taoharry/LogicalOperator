#!/usr/bin/env python
# coding:utf8

import re
import json
from typing import List, Dict, Tuple

from . import configs
from .make_tree import MakeTree, TraversalTree



class TreeRelation(object):

    def iter_num(self, _id, _str):
        if _id - 1 > 0:
            _str = _str + f"{_id - 1}"
            return self.iter_num(_id - 1, _str)
        else:
            return _str

    # 规则优先级映射关系生成树
    def make_rule_tree(self, record: Dict[int, str]) -> dict:
        keys = []
        traversal_trees = []

        for k in record:
            keys.append(k)
        keys.sort()
        for k in keys:
            strK = str(k)
            lenK = len(strK)
            child_tree = TraversalTree()
            if lenK == 1:
                now_dept = strK
                father_dept = ""
                if k > 1:
                    now_dept = strK
                    father_dept = self.iter_num(k, "")
            else:
                orgDept = strK[:1]
                org_int = int(orgDept)
                if org_int == 1:
                    now_dept = strK
                    father_dept = strK[:lenK - 1]
                else:
                    if lenK > 2:
                        now_dept = strK
                        father_dept = strK[:lenK - 1] + orgDept + self.iter_num(org_int, "")
                    else:
                        now_dept = strK
                        father_dept = orgDept + self.iter_num(org_int, "")

            child_tree.NowId = now_dept
            child_tree.FatherId = father_dept.strip()
            child_tree.Rule = record[k]
            traversal_trees.append(child_tree)

        # print("result : ", traversal_trees)
        p_traversal_trees = []
        for i in range(len(traversal_trees)):
            a = traversal_trees[i]
            p_traversal_trees.append(a)

        node = traversal_trees[0]
        MakeTree().make(p_traversal_trees, node)

        data = json.dumps(node, default=lambda o: o.__dict__, indent=4)
        out_str = json.dumps(json.loads(data),  indent=4)
        print("Tree=", out_str)
        return data

    @staticmethod
    def remove_kong(strs: List[str]) -> List[str]:
        result = []
        for k in strs:
            if k != "" and k != configs.LuKong:
                result.append(k)
        return result

    # 规整化规则和操作符位置
    def format_rules(self, rule: str):
        key_rules = []
        for i in configs.LuSlice:
            rule = rule.replace(i, f" {i} ")

        rule2 = rule
        for i in configs.LuSlice:
            rule2 = rule2.replace(i, " ")

        rule_slice = rule2.split(configs.LuKong)
        key_rules_no_trims = self.remove_kong(rule_slice)
        for k in key_rules_no_trims:
            key_rules.append(k.replace(configs.LuKong, ""))
        return rule, key_rules

    # 传入规则, 返回优先级执行列表, 优先级映射关系和对应的所有规则名列表
    def relational_analysis(self, rule: str) -> Tuple[List[str], Dict[int, str], List[str]]:
        rule, key_rules = self.format_rules(rule)
        priority = []
        record = {}
        priority, record = self.parser_rule(rule, 1, priority, record)
        return priority, record, key_rules

    # 通过()发现优先级
    def parser_rule(self, rule: str, dept: int, priority: List[str], record: Dict[int, str]) -> Tuple[
        List[str], Dict[int, str]]:
        record[dept] = rule
        _complex = r'\([\u4e00-\u9fa5\&\|\!\=\+\*a-zA-Z0-9\ ]*?\)'
        find = re.compile(_complex)
        results = find.findall(rule)
        print("运行第", dept, "层 result = ", results)
        if len(results) > 0:
            for n, k in enumerate(results):
                new_dept = f"{dept}{n + 1}"
                trim_k = k.strip(configs.LuLeftParenthesis).strip(configs.LuRightParenthesis)
                new_dep_int = int(new_dept)
                priority, record = self.flag_parser(trim_k, new_dep_int, priority, record)
                rule = rule.replace(k, new_dept, 1)
            priority, record = self.parser_rule(rule, dept + 1, priority, record)
        else:
            print("迭代完成生成rule: ", rule)
            priority, record = self.flag_parser(rule, dept, priority, record)
            # print("优先级为: ", priority)
            # print(f"优先级映射关系 = {record}")
        return priority, record

    # 处理支持的操作符, 映射该层级优先符号对应数组
    def flag_parser(self, rule: str, dept: int, priority: List[str], record: Dict[int, str]) -> Tuple[
        List[str], Dict[int, str]]:
        find = re.compile(configs.FlagParserComplex)
        results = find.findall(rule)

        record[dept] = rule
        if len(results) == 0 and len(priority) == 0:
            priority.append(rule)
            return priority, record

        if len(results) == 1:
            priority.append(rule)
            return priority, record
        rule_slice = rule.split(configs.LuKong)
        rules = self.remove_kong(rule_slice)
        lu_flag = 0
        _next = 0
        perch_rule = ""
        for n, key in enumerate(rules):
            if key in configs.LuSlice:
                lu_flag += 1
                if lu_flag == 1:
                    continue
                if perch_rule == "":
                    splitRule = " ".join(rules[_next:n])
                else:
                    splitRule = perch_rule + " " + " ".join(rules[_next:n])
                perch_rule = f"{dept}{lu_flag - 1}"

                _next = n
                priority.append(splitRule)
                tmpCreateRuleInt = int(perch_rule)
                record[tmpCreateRuleInt] = splitRule
                rule = rule.replace(splitRule, perch_rule, 1)
                # print("rule解析后: ", rule)
                if n + 2 == len(rules):
                    rule = perch_rule + " " + " ".join(rules[n:])
                    priority.append(rule)
                    record[tmpCreateRuleInt + 1] = rule
        return priority, record
