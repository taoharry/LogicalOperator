# LogicalOperator
    LogicalOperator是一个简单的优先级操作符解析程序, 目标是为了实现规则的逻辑运算

## 安装
### 方法1
```text
git clone https://github.com/taoharry/LogicalOperator.git
cd LogicalOperator
python setup.py install --user
```
### 方法2
```text
pip install git+https://github.com/taoharry/LogicalOperator.git

```

## 简介
    
    字符串传入规则逻辑操作, 解析为规则列表, 规则执行优先级列表, 规则对应映射表. 如果需要可以查看规则优先级树.

### 示例

#### 输入 
    rule1 && (rule2 && (rule3 || rule4) && (rule5 && rule6)) &&  (rule7 != (rule8 || rule9)) || rule10

#### 输出
```
    规则执行优先级列表: [' rule3  ||  rule4 ', ' rule5  &&  rule6 ', ' rule8  ||  rule9 ', 'rule2 && 11', '211 && 12', ' rule7  !=   13  ', 'rule1 && 21', '31 && 22', '32 || rule10']
    规则对应映射表:  {1: 'rule1  &&   ( rule2  &&   ( rule3  ||  rule4 )   &&   ( rule5  &&  rule6 )  )   &&    ( rule7  !=   ( rule8  ||  rule9 )  )   ||  rule10', 11: ' rule3  ||  rule4 ', 12: ' rule5  &&  rule6 ', 13: ' rule8  ||  rule9 ', 2: 'rule1  &&   ( rule2  &&   11   &&   12  )   &&    ( rule7  !=   13  )   ||  rule10', 21: ' rule2  &&   11   &&   12  ', 211: 'rule2 && 11', 212: '211 && 12', 22: ' rule7  !=   13  ', 3: 'rule1  &&   21   &&    22   ||  rule10', 31: 'rule1 && 21', 32: '31 && 22', 33: '32 || rule10'}
    规则列表:  ['rule1', 'rule2', 'rule3', 'rule4', 'rule5', 'rule6', 'rule7', 'rule8', 'rule9', 'rule10']
```

#### code
```text
from LogicalOperator.tree_relation import TreeRelation
tr = TreeRelation()
for rule in [
    "rule1 && (rule2 && (rule3 || rule4) && (rule5 && rule6)) &&  (rule7 != (rule8 || rule9)) || rule10"
]:
    print(f"------------开始解析------------")
    priority, record, keyRules = tr.relational_analysis(rule)
    print(f"执行顺序 = {priority}")
    print(f"测试映射结果 = {record}")
    print(f"生成key值 = {keyRules}" )
    print(f"------------解析结束------------")
```


### 映射树

#### 输入 
    规则对应映射表
#### 输出
```json
    {
        "NowId": "1",
        "FatherId": "",
        "Rule": "rule1 && (rule2 && (rule3 || rule4) && (rule5 && rule6)) &&  (rule7 != (rule8 || rule9)) || rule10",
        "Child": [
            {
                "NowId": "2",
                "FatherId": "1",
                "Rule": "rule1 && (rule2 && 11 && 12) &&  (rule7 != 13) || rule10",
                "Child": [
                    {
                        "NowId": "3",
                        "FatherId": "21",
                        "Rule": "rule1 && 21 &&  22 || rule10",
                        "Child": [
                            {
                                "NowId": "31",
                                "FatherId": "321",
                                "Rule": "rule1 && 21",
                                "Child": []
                            },
                            {
                                "NowId": "32",
                                "FatherId": "321",
                                "Rule": "31 && 22",
                                "Child": []
                            },
                            {
                                "NowId": "33",
                                "FatherId": "321",
                                "Rule": "32 || rule10",
                                "Child": []
                            }
                        ]
                    },
                    {
                        "NowId": "21",
                        "FatherId": "21",
                        "Rule": "rule2 && 11 && 12",
                        "Child": [
                            {
                                "NowId": "211",
                                "FatherId": "2121",
                                "Rule": "rule2 && 11",
                                "Child": []
                            },
                            {
                                "NowId": "212",
                                "FatherId": "2121",
                                "Rule": "211 && 12",
                                "Child": []
                            }
                        ]
                    },
                    {
                        "NowId": "22",
                        "FatherId": "21",
                        "Rule": "rule7 != 13",
                        "Child": []
                    }
                ]
            },
            {
                "NowId": "11",
                "FatherId": "1",
                "Rule": "rule3 || rule4",
                "Child": []
            },
            {
                "NowId": "12",
                "FatherId": "1",
                "Rule": "rule5 && rule6",
                "Child": []
            },
            {
                "NowId": "13",
                "FatherId": "1",
                "Rule": "rule8 || rule9",
                "Child": []
            }
        ]
    }
```

#### code
```text
tr = TreeRelation()
tr.make_rule_tree(record)
```