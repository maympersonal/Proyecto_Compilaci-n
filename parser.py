from sly import Parser
from lexer import HulkLexer

# Definición de la clase Parser para el lenguaje Hulk
class HulkParser(Parser):
    # Archivo de depuración
    debugfile = 'debug.txt'
    tokens = HulkLexer.tokens

    # Precedencia de operadores
    precedence = (('left', OR, AND), 
                  ('left', EQUAL, NOT_EQUAL),
                  ('left', LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL),
                  ('left', PLUS, MINUS, CONCAT, ESPACEDCONCAT),
                  ('left', MULTIPLY, DIVIDE, MODULE),
                  ('right', POWER, ASTERPOWER), 
                  ('right', NOT))

    # Regla inicial
    @_('program_decl_list')
    def program(self, p):
        pass

    # Lista de declaraciones del programa
    @_('inst_wrapper', 
       'program_level_decl program_decl_list', 
       'empty')
    def program_decl_list(self, p):
        pass

    # Declaraciones a nivel de programa
    @_('type_declaration', 
       'function_declaration', 
       'protocol_declaration')
    def program_level_decl(self, p):
        pass

    # Lista de instrucciones
    @_('inst SEMICOLON', 
       'inst SEMICOLON inst_list')
    def inst_list(self, p):
        pass

    # Instrucción con o sin punto y coma
    @_('inst', 
       'inst SEMICOLON')
    def inst_wrapper(self, p):
        pass

    # Instrucción
    @_('scope', 
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def inst(self, p):
        pass

    # Declaración de variable
    @_('LET var_init_list IN var_decl_expr')
    def var_dec(self, p):
        pass

    # Expresión de declaración de variable
    @_('scope', 
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def var_decl_expr(self, p):
        pass

    # Lista de inicializaciones de variables
    @_('var_init', 
       'var_init COMMA var_init_list')
    def var_init_list(self, p):
        pass

    # Inicialización de variable
    @_('identifier ASSIGN inst', 
       'identifier ASSIGN inst type_downcast')
    def var_init(self, p):
        pass

    # Identificador o parámetro completamente tipado
    @_('atom', 
       'fully_typed_param')
    def identifier(self, p):
        pass

    # Parámetro completamente tipado
    @_('IDENTIFIER type_anotation')
    def fully_typed_param(self, p):
        pass

    # Anotación de tipo
    @_('COLON IDENTIFIER', 
       'COLON NUMBER_TYPE', 
       'COLON BOOLEAN_TYPE')
    def type_anotation(self, p):
        pass

    # Alcance
    @_('LBRACE inst_list RBRACE', 
       'LBRACE RBRACE')
    def scope(self, p):
        pass

    # Expresión
    @_('aritmetic_operation')
    def expression(self, p):
        pass

    @_('atom CONCAT expression', 
       'atom ESPACEDCONCAT expression')
    def expression(self, p):
        pass

    @_('var_asign')
    def expression(self, p):
        pass

    @_('var_dec')
    def expression(self, p):
        pass

    # Operación aritmética
    @_('term PLUS aritmetic_operation', 
       'term MINUS aritmetic_operation', 
       'term')
    def aritmetic_operation(self, p):
        pass

    # Término
    @_('factor MULTIPLY term', 
       'factor DIVIDE term', 
       'factor MODULE term', 'factor')
    def term(self, p):
        pass

    # Factor
    @_('factor POWER base_exponent', 
       'factor ASTERPOWER base_exponent', 
       'base_exponent')
    def factor(self, p):
        pass

    # Base del exponente
    @_('identifier')
    def base_exponent(self, p):
        pass

    @_('LPAREN aritmetic_operation RPAREN')
    def base_exponent(self, p):
        pass

    # Átomo
    @_('NUMBER', 
       'STRING', 
       'function_call', 
       'var_use', 
       'vector', 
       'var_method',
       'type_instanciation', 
       'boolean_value', 
       'build_in_functions', 
       'build_in_consts')
    def atom(self, p):
        pass

    # Asignación de variable
    @_('var_use DEST_ASSIGN expression', 
       'var_use ASSIGN expression')
    def var_asign(self, p):
        pass

    # Declaración de función
    @_('func_decl_id parameters function_full_declaration',
       'func_decl_id LPAREN RPAREN function_full_declaration',
       'func_decl_id parameters function_full_declaration SEMICOLON',
       'func_decl_id LPAREN RPAREN function_full_declaration SEMICOLON',
       'func_decl_id parameters function_inline_declaration',
       'func_decl_id LPAREN RPAREN function_inline_declaration')
    def function_declaration(self, p):
        pass

    # Identificador de declaración de función
    @_('FUNCTION IDENTIFIER')
    def func_decl_id(self, p):
        pass

    # Declaración completa de función
    @_('scope')
    def function_full_declaration(self, p):
        pass

    # Declaración inline de función
    @_('RETURN inst SEMICOLON', 
       'type_anotation RETURN inst SEMICOLON')
    def function_inline_declaration(self, p):
        pass

    # Condicional
    @_('IF inline_conditional', 
       'IF full_conditional')
    def conditional(self, p):
        pass

    @_('LPAREN conditional_expression RPAREN expression else_elif_statement')
    def inline_conditional(self, p):
        pass

    @_('LPAREN conditional_expression RPAREN scope else_elif_statement')
    def full_conditional(self, p):
        pass

    # Sentencia else o elif
    @_('ELIF inline_conditional', 
       'ELIF full_conditional')
    def else_elif_statement(self, p):
        pass

    @_('ELSE inline_else', 
       'ELSE full_else')
    def else_elif_statement(self, p):
        pass

    # Else inline
    @_('expression')
    def inline_else(self, p):
        pass

    # Else completo
    @_('scope')
    def full_else(self, p):
        pass

    # Bucle while
    @_('WHILE LPAREN conditional_expression RPAREN scope',
       'WHILE LPAREN conditional_expression RPAREN expression',
       'WHILE LPAREN expression RPAREN scope',
       'WHILE LPAREN expression RPAREN expression')
    def while_loop(self, p):
        pass

    # Bucle for
    @_('FOR LPAREN identifier IN expression RPAREN scope',
       'FOR LPAREN identifier IN expression RPAREN expression')
    def for_loop(self, p):
        pass

    # Expresión condicional
    @_('condition AND conditional_expression', 
       'condition OR conditional_expression', 
       'NOT condition', 
       'condition')
    def conditional_expression(self, p):
        pass

    # Condición
    @_('comparation', 
       'IDENTIFIER type_conforming', 
       'LPAREN conditional_expression RPAREN')
    def condition(self, p):
        pass

    # Comparación
    @_('expression GREATER_THAN expression', 
       'expression LESS_THAN expression',
       'expression GREATER_EQUAL expression', 
       'expression LESS_EQUAL expression',
       'expression EQUAL expression', 
       'expression NOT_EQUAL expression')
    def comparation(self, p):
        pass

    # Valor booleano
    @_('TRUE', 
       'FALSE')
    def boolean_value(self, p):
        pass

    # Declaración de tipo
    @_('TYPE IDENTIFIER parameters decl_body',
       'TYPE IDENTIFIER parameters inherits_type decl_body',
       'TYPE IDENTIFIER parameters decl_body SEMICOLON',
       'TYPE IDENTIFIER parameters inherits_type decl_body SEMICOLON',
       'TYPE IDENTIFIER decl_body', 'TYPE IDENTIFIER inherits_type decl_body',
       'TYPE IDENTIFIER decl_body SEMICOLON',
       'TYPE IDENTIFIER inherits_type decl_body SEMICOLON')
    def type_declaration(self, p):
        pass

    # Parámetros
    @_('LPAREN arguments_list RPAREN')
    def parameters(self, p):
        pass

    # Herencia de tipo
    @_('INHERITS IDENTIFIER', 
       'INHERITS IDENTIFIER parameters')
    def inherits_type(self, p):
        pass

    # Cuerpo de la declaración
    @_('LBRACE RBRACE', 
       'LBRACE decl_list RBRACE')
    def decl_body(self, p):
        pass

    # Lista de declaraciones
    @_('decl SEMICOLON', 'decl SEMICOLON decl_list')
    def decl_list(self, p):
        pass

    # Declaración
    @_('atribute_declaration', 
       'method_declaration')
    def decl(self, p):
        pass

    # Declaración de atributo
    @_('identifier ASSIGN expression', 
       'identifier ASSIGN expression type_downcast')
    def atribute_declaration(self, p):
        pass

    # Declaración de método
    @_( 'IDENTIFIER parameters RETURN expression',
        'IDENTIFIER parameters function_full_declaration',
        'IDENTIFIER LPAREN RPAREN RETURN expression',
        'IDENTIFIER LPAREN RPAREN function_full_declaration',
        'IDENTIFIER parameters type_anotation RETURN expression',
        'IDENTIFIER parameters type_anotation function_full_declaration',
        'IDENTIFIER LPAREN RPAREN type_anotation RETURN expression',
        'IDENTIFIER LPAREN RPAREN type_anotation RETURN conditional_expression',
        'IDENTIFIER LPAREN RPAREN type_anotation function_full_declaration')
    def method_declaration(self, p):
        pass

    # Llamada a función
    @_('IDENTIFIER LPAREN arguments_list RPAREN', 
       'IDENTIFIER LPAREN RPAREN')
    def function_call(self, p):
        pass

    # Instanciación de tipo
    @_('NEW IDENTIFIER LPAREN arguments_list RPAREN', 
       'NEW IDENTIFIER LPAREN RPAREN')
    def type_instanciation(self, p):
        pass

    # Conformidad de tipo
    @_('IS identifier')
    def type_conforming(self, p):
        pass

    # Downcast de tipo
    @_('AS identifier')
    def type_downcast(self, p):
        pass

    # Lista de argumentos
    @_('argument', 
       'argument COMMA arguments_list')
    def arguments_list(self, p):
        pass

    # Argumento
    @_('expression', 
       'conditional')
    def argument(self, p):
        pass

    # Uso de variable
    @_('IDENTIFIER', 
       'atom LBRACKET expression RBRACKET', 
       'var_attr')
    def var_use(self, p):
        pass

    # Atributo de variable
    @_('IDENTIFIER DOT IDENTIFIER', 
       'IDENTIFIER DOT var_attr')
    def var_attr(self, p):
        pass

    # Método de variable
    @_('IDENTIFIER DOT function_call')
    def var_method(self, p):
        pass

    # Control de flujo
    @_('while_loop', 
       'conditional', 
       'for_loop')
    def flux_control(self, p):
        pass

    # Declaración de protocolo
    @_('PROTOCOL IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER protocol_body SEMICOLON',
       'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body SEMICOLON')
    def protocol_declaration(self, p):
        pass

    # Cuerpo del protocolo
    @_('LBRACE virtual_method_list RBRACE')
    def protocol_body(self, p):
        pass

    # Lista de métodos virtuales
    @_('virtual_method SEMICOLON', 
       'virtual_method SEMICOLON virtual_method_list')
    def virtual_method_list(self, p):
        pass

    # Método virtual
    @_('IDENTIFIER parameters type_anotation', 
       'IDENTIFIER LPAREN RPAREN type_anotation')
    def virtual_method(self, p):
        pass

    # Vector
    @_('LBRACKET vector_decl RBRACKET')
    def vector(self, p):
        pass

    # Declaración de vector
    @_('arguments_list', 
       'expression SINCETHAT identifier IN expression',
       'expression OR identifier IN expression')
    def vector_decl(self, p):
        pass

    # Rango
    @_('RANGE LPAREN argument COMMA argument RPAREN')
    def build_in_range(self, p):
        pass

    # Imprimir
    @_('PRINT LPAREN argument RPAREN')
    def build_in_print(self, p):
        pass

    # Funciones integradas
    @_('build_in_range', 
       'build_in_print')
    def build_in_functions(self, p):
        pass

    @_('SQRT LPAREN argument RPAREN', 
       'SIN LPAREN argument RPAREN',
       'COS LPAREN argument RPAREN', 
       'EXP LPAREN argument RPAREN')
    def build_in_functions(self, p):
        pass

    @_('LOG LPAREN argument COMMA argument RPAREN')
    def build_in_functions(self, p):
        pass

    @_('RAND LPAREN RPAREN')
    def build_in_functions(self, p):
        pass

    # Constantes integradas
    @_('PI_CONST', 
       'E_CONST')
    def build_in_consts(self, p):
        pass

    # Regla vacía
    @_('')
    def empty(self, p):
        pass

    # Manejo de errores
    def error(self, p):
        print(p)
        lineno = p.lineno if p else 'EOF'
        value = repr(p.value) if p else 'EOF'
        print(f'{lineno}: Syntax error at {value} {p}')
