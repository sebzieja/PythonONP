#-*- coding: utf-8 -*-

"""Opisuja łączność argumentów - niektóre są prawo, niektóre lewostronnie łączne"""

leftAssociative = 0
rightAssociative = 1

"""Słownik operatorów, zawierający ich priorytet, łączność i ich operacje."""
OPERATORS = {
	'+' : (0, leftAssociative, lambda x,y: y+x),
	'-' : (0, leftAssociative, lambda x,y: y-x),
	'*' : (1, leftAssociative, lambda x,y: y*x),
	'/' : (1, leftAssociative, lambda x,y: y/x),
	'^' : (2, rightAssociative, lambda x,y: y**x)
}
"""Zwraca true jeśli znak jest operatorem, false jeśli nie jest"""
def isOperator(token):
	return token in OPERATORS.keys()

"""Zwraca true jeśli operator ma łączność podaną w wywołaniu funkcji"""
def cmpAssociative(token, associative):
	if not isOperator(token):
		raise VauleError("Bledny operator: %s" % token)
	return OPERATORS[token][1] == associative

"""Zwraca liczbę >0 gdy operator 1 ma większy priorytet, 0 gdy są o takim samym priorytecie, 
<0 gdy 1 operator jest o mniejszym priorytecie"""
def cmpPrecedence(token1, token2):
	if not isOperator(token1) or not isOperator(token2):
		raise ValueError("Bledne operatory: %s %s" % (token1, token2))
	return OPERATORS[token1][0] - OPERATORS[token2][0]

"""funkcja zwracająca rownanie w ONP"""
def infixToRPN(tokens):

	stack=[]
	output=[]

	for token in tokens:
		if isOperator(token):
			while len(stack)!=0 and isOperator(stack[-1]):
				if (cmpAssociative(token, leftAssociative) and cmpPrecedence(token, stack[-1])<=0) or (cmpAssociative(token, rightAssociative) and cmpPrecedence(token, stack[-1])<0):
					output.append(stack.pop())
					continue
				break
			stack.append(token)
		elif token == "(":
			stack.append("(")
		elif token == ")":
			while len(stack)!=0 and stack[-1]!="(":
				output.append(stack.pop())
			stack.pop()
		else:
			output.append(token)

	#po skonczonej petli przenieś wszystko ze stosu do wyjścia
	while len(stack)!=0:
		output.append(stack.pop())

	#zwraca str z wynikiem
	return " ".join(output)

"""funkcja zwracajaca wynik wyrazenia ONP"""
def calcRPN(tokens):

	stack=[]

	for token in tokens:
		if token in OPERATORS:
			stack.append(OPERATORS[token][2](stack.pop(), stack.pop()))
		else:
			stack.append(float(token))
	return stack.pop()

"""funkcja ktora rozpoznaje czy zostalo wpisane rownanie w 
zapisie ONP, czy w zwyklym, ktore ma zostac zamienione na ONP
"""
def makeCalculation(tokens):

	#tworzy liste taka jak tokens, tylko nie zawierajaca nawiasow
	temp=[y for y in tokens if (y != "(" and y != ")")]

	#sprawdza czy tokens jest rownaniem w ONP czy nie
	for i in range(0, len(temp)-1):
		if (not isOperator(temp[i])) and (not isOperator(temp[i+1])):
			return calcRPN(tokens)
		else:
			return infixToRPN(tokens)


#tokens = raw_input.split(" ")
#makeCalculation(tokens)

import unittest

"""Klasa wykonujaca testy calego programu i poprawnosci algorytmu"""
class TestONP(unittest.TestCase):
	def setUp(self):
		self.r1 = "2 3 + 4 *".split(" ")
		self.r2 = "( 1 + 2 ) * ( 3 + 3 )".split(" ")
		self.r3 = "5 3 + 2 ^ 4 3 * -3 / +".split(" ")
		self.r4 = "( 5 + 3 ) ^ 2 + 4 * -3 / 3".split(" ")
		self.r5 = "1 4 3 * -3 / +".split(" ")
	def testCalcRpn(self):
		self.assertEqual(repr(makeCalculation(self.r1)), "20.0")
		self.assertEqual(repr(makeCalculation(self.r3)), "60.0")
		self.assertEqual(repr(makeCalculation(self.r5)), "-3.0")
	def testInfixToRPN(self):
		self.assertEqual(makeCalculation(self.r2), "1 2 + 3 3 + *")
		self.assertEqual(makeCalculation(self.r4), "5 3 + 2 ^ 4 -3 * 3 / +")


if __name__ == "__main__":
    unittest.main()  # wszystkie testy