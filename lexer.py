from os import close
from sly import Lexer


class HulkLexer(Lexer):
    tokens = { LET, IN, FUNCTION, IF, ELSE, ELIF, FOR, WHILE, 
               NEW, INHERITS, TYPE, PROTOCOL, EXTENDS, IDENTIFIER, PLUS, MINUS, 
               MULTIPLY, DIVIDE, ASTERPOWER, POWER, MODULE, RETURN, LESS_EQUAL, 
               LESS_THAN, GREATER_EQUAL, GREATER_THAN, EQUAL, NOT_EQUAL, 
               DEST_ASSIGN, ASSIGN, LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE, 
               SEMICOLON, COLON, COMMA, DOT, SINCETHAT, AND, OR, NOT, ESPACEDCONCAT, 
               CONCAT, STRING, NUMBER, NUMBER_TYPE, TRUE, FALSE, IS, AS, PI_CONST, E_CONST, 
               RANGE, PRINT, SQRT, SIN, COS, EXP, LOG, RAND, BOOLEAN_TYPE } 

    ignore = ' \t'

    @_(r'\n')
    def ignore_newline(self, t):
        self.lineno += 1

    @_(r'//.*\n')
    def ignore_comment(self, t):
        self.lineno += 1

    
    
    # Operadores aritméticos
    PLUS = r'\+'
    MINUS = r'-'
    ASTERPOWER = r'\*\*'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    POWER = r'\^'
    MODULE = r'%'

    # Definición de funcion inline
    RETURN = r'=>'

    # Operadores comparativos
    LESS_EQUAL = r'<='
    LESS_THAN = r'<'
    GREATER_EQUAL = r'>='
    GREATER_THAN = r'>'
    EQUAL = r'=='
    NOT_EQUAL = r'!='

    # Operadores asignacion
    DEST_ASSIGN = r':='
    ASSIGN = r'='

    # Otros
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'{'
    RBRACE = r'}'
    SEMICOLON = r';'
    COLON = r':'
    COMMA = r','
    DOT = r'\.'
    SINCETHAT = r'\|\|'
    
    # Operadores lógicos
    AND = r'&'
    OR = r'\|'
    NOT = r'!'

    #JOIN whitespace
    ESPACEDCONCAT = r'@@'
    CONCAT = r'@'

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'"([^"\n\\]|\\.)*"')
    def STRING(self, t):
        self.lineno += t.value.count('\n')
        t.value = t.value[1:-1]
        return t

    @_(r'true|false')
    def BOOLEAN(self, t):
        t.value = True if t.value == 'true' else False
        return t

    
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['PI'] = PI_CONST
    IDENTIFIER['E'] = E_CONST
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['elif'] = ELIF
    IDENTIFIER['for'] = FOR 
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['let'] = LET
    IDENTIFIER['in'] = IN
    IDENTIFIER['function'] = FUNCTION
    IDENTIFIER['new'] = NEW
    IDENTIFIER['inherits'] = INHERITS
    IDENTIFIER['type'] = TYPE
    IDENTIFIER['protocol'] = PROTOCOL
    IDENTIFIER['extends'] = EXTENDS
    IDENTIFIER['true'] = TRUE
    IDENTIFIER['false'] = FALSE
    IDENTIFIER['Number'] = NUMBER_TYPE
    IDENTIFIER['Boolean'] = BOOLEAN_TYPE
    IDENTIFIER['is'] = IS
    IDENTIFIER['as'] = AS
    IDENTIFIER['range'] = RANGE
    IDENTIFIER['print'] = PRINT
    IDENTIFIER['sqrt'] = SQRT
    IDENTIFIER['sin'] = SIN
    IDENTIFIER['cos'] = COS
    IDENTIFIER['exp'] = EXP
    IDENTIFIER['log'] = LOG
    IDENTIFIER['rand'] = RAND
    
    def error(self, t):
        if self.context:
            self.context.error(self.lineno, f'Illegal character {t.value[0]!r}')
        else:
            print(f'{self.lineno}: Illegal character {t.value[0]!r}')
        self.index += 1

    def __init__(self, context):
        self.context = context

        
def test_lexer():
    lexer = HulkLexer(None)
    tokens = lexer.tokenize("""( ) { } [ ] , . - + * / ^ % => = 
                                // esto es un comentario 
                                := ; : , . || <= < >= > == != & | ! @@ @""")
    toktypes = [t.type for t in tokens]
    assert toktypes == [ 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 
                         'COMMA', 'DOT', 'MINUS', 'PLUS', 'MULTIPLY', 'DIVIDE', 'POWER', 
                         'MODULE', 'RETURN', 'ASSIGN', 'DEST_ASSIGN', 'SEMICOLON', 'COLON', 
                         'COMMA', 'DOT', 'SINCETHAT', 'LESS_EQUAL', 'LESS_THAN', 'GREATER_EQUAL', 
                         'GREATER_THAN', 'EQUAL', 'NOT_EQUAL', 'AND', 'OR', 'NOT', 
                         'ESPACEDCONCAT', 'CONCAT']
                    
    
    tokens = lexer.tokenize("let is as in function if else elif for while new inherits type protocol extends")
    toktypes = [t.type for t in tokens]
    assert toktypes == [ 'LET', 'IS', 'AS', 'IN', 'FUNCTION', 'IF', 'ELSE',
                         'ELIF', 'FOR', 'WHILE', 'NEW', 'INHERITS', 'TYPE',
                         'PROTOCOL', 'EXTENDS' ]

    tokens = lexer.tokenize('123 123.0 "hello" "hello\nworld" true false')
    tokvals = [(t.type, t.value) for t in tokens ]
    assert tokvals == [ ('NUMBER', 123), ('NUMBER', 123.0),
                        ('STRING', 'hello'), ('STRING', 'hello\nworld'), ('BOOLEAN', True), ('BOOLEAN', False)]

    tokens = lexer.tokenize('abc abc123 _abc_123')
    tokvals = [(t.type, t.value) for t in tokens ]
    assert tokvals == [ ('IDENTIFIER', 'abc'), ('IDENTIFIER', 'abc123'), ('IDENTIFIER', '_abc_123')]
    
if __name__ == '__main__':
    test_lexer()
    
        
