
import re
from collections import defaultdict

wat_path = "functions.wat"


class Lexer:
    def __init__(self):
        self.globals = {}
        self.stack = []
        self.functions = {}
        self.output = []
        self.memory = defaultdict(int)
        self.locals = {}

        self.tokens = []
        self.ast = []
        
    def tokenize(self, wat):
        
        # Remove two types of comments
        wat = re.sub(r"\(\;.*?\;\)", "", wat, flags=re.DOTALL)

        wat = re.sub(r";;.*", "", wat)

        # Add spaces around parentheses
        wat = wat.replace("(", " ( ").replace(")", " ) ")

        tokens = wat.split()

        return tokens
        


