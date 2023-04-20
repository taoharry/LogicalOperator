#!/usr/bin/env python
# coding:utf8

LuKong = " "
LuZhanWei = "LNF"
LuAnd = "&&"
LuOr = "||"
LuNon = "!="
LuLeftParenthesis = "("
LuRightParenthesis = ")"
CeAndAdd = "&+"
CeAndProduct = "&*"
CeLuNonANotB = "!&"
CeLuNonAAddB = "!+"
FlagParserComplex = r'\&\&|\|\||\!\=|\&\+|\&\*|\!\&|\!\+'
AND = "AND"
OR = "OR"
NOT = "AND NOT"
LuSlice = [LuAnd, LuOr, LuNon, LuLeftParenthesis, LuRightParenthesis, CeAndAdd, CeAndProduct, CeLuNonAAddB, CeLuNonANotB]
LuFMap = {LuAnd: AND, LuOr: OR, LuNon: NOT}