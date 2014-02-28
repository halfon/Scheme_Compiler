# coding=utf8
import pc
import reader

class AbstractSexpr:

    @staticmethod
    def readFromString(string):
        return reader.pSexpr.match(string)

    def __init__(self):
        self.ref=0
    def __str__(self):
        return self.accept(AsStringVisitor)

class AbstractSexprVisitor:
    def visitBoolean(self):
        pass
    def visitInteger(self):
        pass


class AsStringVisitor(AbstractSexprVisitor):
    def visitAbstractBoolean(self):
        return self.string
    def visitInteger(self):
        return str(self.number)
    def visitFraction(self):
        return str(self.nume) + '/' + str(self.deno)
    def visitSymbol(self):
        return self.string
    def visitString(self):
        return '"'+self.string+'"'
    def visitChar(self):
        return '#\\'+self.char
    def visitNil(self):
        return "()"
    def visitVoid(self):
        return "#<void>"
    def visitPair(self):
        return '(' + str(self.first) + ' . ' + str(self.second) + ')'
    def visitVector(self):
        i = 0
        ans=  '#('
        while i<self.length :
            ans=ans+str(self.elements[i])
            if i<self.length-1:
                ans=ans+ " "
            i=i+1
        ans = ans + ')'
        return ans
    def visitQuote(self):
        return "'" + str(self.quoted)
    def visitQQuote(self):
        return "`" + str(self.qquoted)
    def visitUnquotedSpliced(self):
        return ",@" + str(self.spliced)
    def visitUnquoted(self):
        return "," + str(self.unquoted)

class AbstractBoolean(AbstractSexpr):
    pass

class true(AbstractBoolean):
    def __init__(self):
        super().__init__()
        self.string = '#t'
        self.value = True
    def accept(self, v):
        return v.visitAbstractBoolean(self)

class false(AbstractBoolean):
    def __init__(self):
        super().__init__()
        self.string = '#f'
        self.value = False
    def accept(self, v):
        return v.visitAbstractBoolean(self)
    
class AbstractNumber(AbstractSexpr):
    pass

class Integer(AbstractNumber):
    def __init__(self, number):
        super().__init__()
        self.number=number
    def accept(self, v):
        return v.visitInteger(self)
    
class Fraction(AbstractNumber):
    def __init__(self, nume, deno):
        super().__init__()
        self.nume=nume
        self.deno=deno
    def accept(self, v):
        return v.visitFraction(self)

class Symbol(AbstractSexpr):
    def __init__(self, string):
        super().__init__()
        self.string=string
        self.length=len(string)
    def accept(self, v):
        return v.visitSymbol(self)

class String(AbstractSexpr):
    def __init__(self, string):
        super().__init__()
        self.string=string
        self.length=len(string)
    def accept(self, v):
        return v.visitString(self)

class Char(AbstractSexpr):
    def __init__(self, char):
        super().__init__()
        self.char=char
    def accept(self, v):
        return v.visitChar(self)

class Nil(AbstractSexpr):
    def accept(self, v):
        return v.visitNil(self)

class Void(AbstractSexpr):
    def accept(self, v):
        return v.visitVoid(self)

class Pair(AbstractSexpr):
    def __init__(self, first, second):
        super().__init__()
        self.first = first
        self.second = second    
    def accept(self, v):
        return v.visitPair(self)

class Vector(AbstractSexpr):
    def __init__(self, elements):
        super().__init__()
        self.length = len(elements)
        self.elements = elements    
    def accept(self, v):
        return v.visitVector(self)
