#-*- coding: utf-8 -*-

#Opisuja łączność argumentów - niektóre są prawo, niektóre lewostronnie łączne

leftAssociative = 0
rightAssociative = 1

#Słownik operatorów, zawierający ich priorytet, łączność i ich operacje.
OPERATORS = {
	'+' : (0, leftAssociative, lambda x,y: y+x),
	'-' : (0, leftAssociative, lambda x,y: y-x),
	'*' : (1, leftAssociative, lambda x,y: y*x),
	'/' : (1, leftAssociative, lambda x,y: x/y),
	'^' : (2, rightAssociative, lambda x,y: x**y)
}
#Zwraca true jeśli znak jest operatorem, false jeśli nie jest
def isOperator(token):
	return token in OPERATORS.keys()

#Zwraca true jeśli operator ma łączność podaną w wywołaniu funkcji
def cmpAssociative(token, associative):
	if not isOperator(token):
		raise VauleError("Bledny operator")
	return OPERATORS[token][1] == associative

#Zwraca licznbę >0 gdy operator 1 ma większy priorytet, 0 gdy są o takim samym priorytecie, 
#<0 gdy 1 operator jest o mniejszym priorytecie
def cmpPrecedence(token1, token2):
	# if not 
	return OPERATORS[token1][0] - OPERATORS[token2][0]

#funkcja zwracająca rownanie w ONP
def infixToRPN(tokens):

	stack=[]
	output=[]

	for token in tokens:
		if isOperator(token):
			while len(stack)!=0 and isOperator(stack[-1]):
				#Jesli na szczytu stosu jest operator (y), a nasz operator w zmiennej token (x) jest:
				#lewostronnie łączny i o priorytecie takim samym, lub mniejszym jak y, 
				#albo x jest prawostronnie łączne i ma priorytet mniejszy jak y
				#wtedy usuwamy y ze stosu i umieszczamy na wyjściu, a x umieszczamy na stosie
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

#funkcja zwracajaca wynik wyrazenia w ONP
def calcRPN(tokens):

	stack=[]

	for token in tokens:
		if token in OPERATORS:
			stack.append(OPERATORS[token][2](stack.pop(), stack.pop()))
		else:
			stack.append(float(token))
	return stack.pop()

#funkcja ktora rozpoznaje czy zostalo wpisane rownanie w 
#zapisie ONP, czy w zwyklym, ktore ma zostac zamienione na ONP
def makeCalculation(input):

	#tworzy liste taka jak input, tylko nie zawierajaca nawiasow
	temp=[y for y in input if (y != "(" and y != ")")]

	#sprawdza czy input jest rownaniem w ONP czy nie
	for i in range(0, len(temp)-1):
		if (not isOperator(temp[i])) and (not isOperator(temp[i+1])):
			return calcRPN(input)
		else:
			return infixToRPN(input)


input = raw_input().split(" ")
print makeCalculation(input)