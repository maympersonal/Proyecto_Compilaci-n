from Lexer.Cmp_lex.utils import Grammar

G = Grammar()
INIT = G.NonTerminal("INIT", startSymbol=True)
PROGRAM = G.NonTerminal("PROGRAM")
NUMBER, STRING, IDENTIFIER = G.Terminals("NUMBER STRING IDENTIFIER")
LET, IN, FUNCTION, IF, ELSE, ELIF, FOR, WHILE, NEW, INHERITS, TYPE, PROTOCOL, EXTENDS = G.Terminals("LET IN FUNCTION IF ELSE ELIF FOR WHILE NEW INHERITS TYPE PROTOCOL EXTENDS")
PLUS, MINUS, MULTIPLY, DIVIDE, ASTERPOWER, POWER, MODULE = G.Terminals("PLUS MINUS MULTIPLY DIVIDE ASTERPOWER POWER MODULE")
RETURN, LESS_EQUAL, LESS_THAN, GREATER_EQUAL, GREATER_THAN, EQUAL, NOT_EQUAL = G.Terminals("RETURN LESS_EQUAL LESS_THAN GREATER_EQUAL GREATER_THAN EQUAL NOT_EQUAL")
DEST_ASSIGN, ASSIGN, LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE = G.Terminals("DEST_ASSIGN ASSIGN LPAREN RPAREN LBRACKET RBRACKET LBRACE RBRACE")
SEMICOLON, COLON, COMMA, DOT, SINCETHAT = G.Terminals("SEMICOLON COLON COMMA DOT SINCETHAT")
AND, OR, NOT, ESPACEDCONCAT, CONCAT = G.Terminals("AND OR NOT ESPACEDCONCAT CONCAT")
TRUE, FALSE, IS, AS, PI_CONST, E_CONST, RANGE = G.Terminals("TRUE FALSE IS AS PI_CONST E_CONST RANGE")
PRINT, SQRT, SIN, COS, EXP, LOG, RAND = G.Terminals("PRINT SQRT SIN COS EXP LOG RAND")
BOOLEAN_TYPE, NUMBER_TYPE = G.Terminals("BOOLEAN_TYPE NUMBER_TYPE")
    
keywords = [NUMBER, STRING, IDENTIFIER,LET, IN, FUNCTION, IF, ELSE, ELIF, FOR, WHILE, NEW, INHERITS, TYPE, PROTOCOL, EXTENDS,PLUS, MINUS, MULTIPLY, DIVIDE, ASTERPOWER, POWER, MODULE,RETURN, LESS_EQUAL, LESS_THAN, GREATER_EQUAL, GREATER_THAN, EQUAL, NOT_EQUAL,
DEST_ASSIGN, ASSIGN, LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE, SEMICOLON, COLON, COMMA, DOT, SINCETHAT,AND, OR, NOT, ESPACEDCONCAT, CONCAT,TRUE, FALSE, IS, AS, PI_CONST, E_CONST, RANGE,
PRINT, SQRT, SIN, COS, EXP, LOG, RAND, BOOLEAN_TYPE, NUMBER_TYPE]
    
table_symbols = [
        (LET, "let"),
        (IN, "in"),
        (FUNCTION, "function"),
        (IF, "if"),
        (ELSE, "else"),
        (ELIF, "elif"),
        (FOR, "for"),
        (WHILE, "while"),
        (NEW, "new"),
        (INHERITS, "inherits"),
        (TYPE, "type"),
        (PROTOCOL, "protocol"),
        (EXTENDS, "extends"),
        (PLUS, "\+"),
        (MINUS, "-"),
        (MULTIPLY, "\*"),
        (DIVIDE, "/"),
        (ASTERPOWER, "\*\*"),
        (POWER, "^"),
        (MODULE, "%"),
        (RETURN, "=>"),
        (LESS_EQUAL, "<="),
        (LESS_THAN, "<"),
        (GREATER_EQUAL, ">="),
        (GREATER_THAN, ">"),
        (EQUAL, "=="),
        (NOT_EQUAL, "\!="),
        (DEST_ASSIGN, ":="),
        (ASSIGN, "="),
        (LPAREN, "\("),
        (RPAREN, "\)"),
        (LBRACKET, "\["),
        (RBRACKET, "\]"),
        (LBRACE, "{"),
        (RBRACE, "}"),
        (SEMICOLON, ";"),
        (COLON, ":"),
        (COMMA, ","),
        (DOT, "\."),
        (SINCETHAT, "\|\|"),
        (AND, "&"),
        (OR, "\|"),
        (NOT, "\!"),
        (ESPACEDCONCAT, "@@"),
        (CONCAT, "@"),
        (NUMBER_TYPE, "Number"),
        (TRUE, "true"),
        (FALSE, "false"),
        (IS, "is"),
        (AS, "as"),
        (PI_CONST, "PI"),
        (E_CONST, "E"),
        (RANGE, "range"),
        (PRINT, "print"),
        (SQRT, "sqrt"),
        (SIN, "sin"),
        (COS, "cos"),
        (EXP, "exp"),
        (LOG, "log"),
        (RAND, "rand"),
        (BOOLEAN_TYPE, "Boolean"),
        (STRING, "\"((\\\\\")|(\\A))*\""),
        (NUMBER, "([0..9]+\.)?[0..9]+"),
        (IDENTIFIER, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*")
] 
 
""" 
ESTA FUE PARA TEST


# No Terminals
init_ = G.NonTerminal("<init>", startSymbol=True)
program = G.NonTerminal("<program>")

# Terminals
string, identifier, number = G.Terminals("<string> <id> <number>")
plus, minus, times, divide, int_divide = G.Terminals("+ - * / //")
equal, dequal, lesst, greatt, lequal, gequal, notequal = G.Terminals("= == < > <= >= !=")
lparen, rparen, lbrack, rbrack, lbrace, rbrace = G.Terminals("( ) [ ] { }")
comma, period, colon, semicolon = G.Terminals(", . : ;")
arrow, darrow = G.Terminals("-> =>")
and_, or_, not_ = G.Terminals("& | !")

modulus, power, power_asterisk = G.Terminals("% ^ **")
destruct, concat = G.Terminals(":= @")
list_comprehension = G.Terminal("||")

for_, let, if_, else_, elif_ = G.Terminals("for let if else elif")
while_, function, pi, e, print_ = G.Terminals("while function pi e print")
new, inherits, protocol, type_, in_, range_, extends = G.Terminals("new inherits protocol type in range extends")
true, false = G.Terminals("true false")

rand = G.Terminal("rand")
sin, cos, sqrt, exp, log, tan, base = G.Terminals("sin cos sqrt exp log tan base")
as_, is_ = G.Terminals("as is")


keywords= [for_, let, if_, else_, elif_, while_, function, pi, e, print_,
            new, inherits, protocol, type_, in_, range_, true, false, extends, as_,
            rand, sin, cos, sqrt, exp, log, is_, tan, base]

tokens =  [
    (for_, "for"),
    (let, "let"),
    (if_, "if"),
    (else_, "else"),
    (elif_, "elif"),
    (while_, "while"),
    (function, "function"),
    (print_, "print"),
    (pi, "pi"),
    (e, "e"),
    (new, "new"),
    (inherits, "inherits"),
    (protocol, "protocol"),
    (type_, "type"),
    (in_, "in"),
    (range_, "range"),
    (true, "true"),
    (false, "false"),
    (extends, "extends"),
    (sin, "sin"),
    (cos, "cos"),
    (tan, "tan"),
    (sqrt, "sqrt"),
    (exp, "exp"),
    (log, "log"),
    (rand, "rand"),
    (base, "base"),
    (plus, "\+"),
    (times, "\*"),
    (minus, "-"),
    (divide, "/"),
    (equal, "="),
    (dequal, "=="),
    (notequal, "\!="),
    (lesst, "<"),
    (greatt, ">"),
    (lequal, "<="),
    (gequal, ">="),
    (lparen, "\("),
    (rparen, "\)"),
    (lbrack, "\["),
    (rbrack, "\]"),
    (lbrace, "{"),
    (rbrace, "}"),
    (comma, ","),
    (period, "\."),
    (colon, ":"),
    (semicolon, ";"),
    (arrow, "->"),
    (darrow, "=>"),
    (and_, "&"),
    (or_, "\|"),
    (list_comprehension, "\|\|"),
    (not_, "\!"),
    (modulus, "%"),
    (power, "^"),
    (destruct, ":="),
    (concat, "@"),
    (is_, "is"),
    (as_, "as"),
    (identifier, "([a..z]|[A..Z]|_)([a..z]|[A..Z]|_|[0..9])*"),
    (number, "([0..9]+\.)?[0..9]+"),
    (string, "\"((\\\\\")|(\\A))*\"")
] """