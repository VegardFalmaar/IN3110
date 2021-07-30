import math
import sys

class Calculator:
    def __init__(self):
        self.l = []
        self.operations = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            'p': self.print_last,
            'v': self.sqrt,
            'sin': self.sin,
            'cos': self.cos
        }

    
    def __call__(self, cmd):
        cmd = cmd.split()
        for sign in cmd:
            try:
                if '.' in sign:
                    num = float(sign)
                else:
                    num = int(sign)
                self.l.append(num)
            except ValueError:
                if sign in self.operations.keys():
                    self.operations[sign]()
                else:
                    print(f'Unknown command "{sign}"')

    def take_input(self):
        while True:
            sign = input(': ')
            if sign == 'x':
                break
            self(sign)

    def print_last(self):
        print(self.l[-1])

    def add(self):
        a = self.l.pop()
        b = self.l.pop()
        self.l.append(a + b)

    def sub(self):
        a = self.l.pop()
        b = self.l.pop()
        self.l.append(b - a)

    def mul(self):
        a = self.l.pop()
        b = self.l.pop()
        self.l.append(a * b)

    def div(self):
        a = self.l.pop()
        b = self.l.pop()
        self.l.append(b / a)

    def sqrt(self):
        a = self.l.pop()
        self.l.append(math.sqrt(a))

    def sin(self):
        a = self.l.pop()
        a *= math.pi/180
        self.l.append(math.sin(a))

    def cos(self):
        a = self.l.pop()
        a *= math.pi/180
        self.l.append(math.cos(a))

calc = Calculator()

if len(sys.argv) > 1:
    for sign in sys.argv[1:]:
        calc(sign)
    calc('p')

print('Welcome to RPN Calculator!\
\nEnter a command below\
\nTo exit, enter "x"')
calc.take_input()
