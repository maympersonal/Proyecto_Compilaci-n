from os import close
from sly import Lexer

# Definición de la clase Lexer para el lenguaje Hulk
class HulkLexer(Lexer):
    # Definición de los tokens
    tokens = {
        LET, IN, FUNCTION, IF, ELSE, ELIF, FOR, WHILE, NEW, INHERITS, TYPE,
        PROTOCOL, EXTENDS, IDENTIFIER, PLUS, MINUS, MULTIPLY, DIVIDE,
        ASTERPOWER, POWER, MODULE, RETURN, LESS_EQUAL, LESS_THAN,
        GREATER_EQUAL, GREATER_THAN, EQUAL, NOT_EQUAL, DEST_ASSIGN, ASSIGN,
        LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE, SEMICOLON, COLON,
        COMMA, DOT, SINCETHAT, AND, OR, NOT, ESPACEDCONCAT, CONCAT, STRING,
        NUMBER, NUMBER_TYPE, TRUE, FALSE, IS, AS, PI_CONST, E_CONST, RANGE,
        PRINT, SQRT, SIN, COS, EXP, LOG, RAND, BOOLEAN_TYPE
    }

    # Ignorar espacios en blanco y tabulaciones
    ignore = ' \t'

    # Ignorar saltos de línea, incrementando el contador de líneas
    @_(r'\n')
    def ignore_newline(self, t):
        self.lineno += 1

    # Ignorar comentarios de una línea, incrementando el contador de líneas
    @_(r'//.*\n')
    def ignore_comment(self, t):
        self.lineno += 1

    # Definición de operadores aritméticos
    PLUS = r'\+'
    MINUS = r'-'
    ASTERPOWER = r'\*\*'
    MULTIPLY = r'\*'
    DIVIDE = r'/'
    POWER = r'\^'
    MODULE = r'%'

    # Definición de función inline
    RETURN = r'=>'

    # Definición de operadores comparativos
    LESS_EQUAL = r'<='
    LESS_THAN = r'<'
    GREATER_EQUAL = r'>='
    GREATER_THAN = r'>'
    EQUAL = r'=='
    NOT_EQUAL = r'!='

    # Definición de operadores de asignación
    DEST_ASSIGN = r':='
    ASSIGN = r'='

    # Definición de otros tokens
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

    # Definición de operadores lógicos
    AND = r'&'
    OR = r'\|'
    NOT = r'!'

    # Definición de concatenación de espacios
    ESPACEDCONCAT = r'@@'
    CONCAT = r'@'

    # Definición de números, convirtiendo a float
    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    # Definición de cadenas, eliminando comillas y contando saltos de línea
    @_(r'"([^"\n\\]|\\.)*"')
    def STRING(self, t):
        self.lineno += t.value.count('\n')
        t.value = t.value[1:-1]
        return t

    # Definición de valores booleanos
    @_(r'true|false')
    def BOOLEAN(self, t):
        t.value = True if t.value == 'true' else False
        return t

    # Definición de identificadores y palabras clave
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

    # Manejo de errores léxicos
    def error(self, t):
        if self.context:
            self.context.error(self.lineno,
                               f'Illegal character {t.value[0]!r}')
        else:
            print(f'{self.lineno}: Illegal character {t.value[0]!r}')
        self.index += 1

    # Inicialización del lexer con un contexto dado
    def __init__(self, context):
        self.context = context

