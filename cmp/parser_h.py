from sly import Parser
from cmp.lexer_h import HulkLexer
from cmp.ast_h import *

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
        print("program "+str([str(v) for v in p]))
        return Program(p.program_decl_list)

    # Lista de declaraciones del programa
    @_(#'inst_wrapper', 
       'inst_list',
       'program_level_decl program_decl_list', 
       'empty')
    def program_decl_list(self, p):
        print("program_decl_list "+str([v for v in p]))
        return p[0]

    # Declaraciones a nivel de programa
    @_('type_declaration', 
       'function_declaration', 
       'protocol_declaration')
    def program_level_decl(self, p):
        print("program_level_decl "+str([v for v in p]))
        return p[0]

    # Lista de instrucciones
    @_( 'inst', #**************************************************
        'inst SEMICOLON', 
        'inst SEMICOLON inst_list')
    def inst_list(self, p):
        print("inst_list "+str([v for v in p]))
        if len(p)==1 or len(p)==2:
            return p[0]
        else: return [p[0]]+p[2]
        
        

    # Instrucción con o sin punto y coma
    '''@_('inst', 
       'inst SEMICOLON')
    def inst_wrapper(self, p):
        print("inst_wrapper "+str([v for v in p]))
        pass'''

    # Instrucción
    @_(#'scope', 
       'scope_list',
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def inst(self, p):
        print("inst "+str([v for v in p]))
        if len(p)==3:
            return p[1]
        else: 
            return p[0]

    # Declaración de variable
    @_('LET var_init_list IN var_decl_expr')
    def var_dec(self, p):
        print("var_dec "+str([v for v in p]))
        pass

    # Expresión de declaración de variable
    @_('scope_list', 
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def var_decl_expr(self, p):
        print("var_decl_expr "+str([v for v in p]))
        pass

    # Lista de inicializaciones de variables
    @_('var_init', 
       'var_init COMMA var_init_list')
    def var_init_list(self, p):
        print("var_init_list "+str([v for v in p]))
        pass

    # Inicialización de variable
    @_('identifier ASSIGN inst', 
       'identifier ASSIGN inst type_downcast')
    def var_init(self, p):
        print("var_init "+str([v for v in p]))
        pass

    # Identificador o parámetro completamente tipado
    @_('atom', 
       'fully_typed_param')
    def identifier(self, p):
        print("identifier "+str([v for v in p]))
        return p[0]

    # Parámetro completamente tipado
    @_('IDENTIFIER type_anotation')
    def fully_typed_param(self, p):
        print("fully_typed_param "+str([v for v in p]))
        pass

    # Anotación de tipo
    @_('COLON IDENTIFIER', 
       'COLON NUMBER_TYPE', 
       'COLON BOOLEAN_TYPE')
    def type_anotation(self, p):
        print("type_anotation "+str([v for v in p]))
        pass
    
    @_( 'scope', #*******************************************************
        'scope scope_list')
    def scope_list(self, p):
        print("scope_list "+str([v for v in p]))
        pass
        
    # Alcance
    @_('LBRACE inst_list RBRACE', 
       'LBRACE RBRACE')
    def scope(self, p):
        print("scope "+str([v for v in p]))
        pass

    # Expresión
    @_('aritmetic_operation')
    def expression(self, p):
        print("expression "+str([str(v) for v in p]))
        return p[0]

    @_('atom CONCAT expression', 
       'atom ESPACEDCONCAT expression')
    def expression(self, p):
        print("expression "+str([v for v in p]))
        pass

    @_('var_asign')
    def expression(self, p):
        print("expression "+str([v for v in p]))
        pass

    @_('var_dec')
    def expression(self, p):
        print("expression "+str([v for v in p]))
        pass

    # Operación aritmética
    @_('term PLUS aritmetic_operation', 
       'term MINUS aritmetic_operation', 
       'term')
    def aritmetic_operation(self, p):
        print("aritmetic_operation "+str([v for v in p]))
        if len(p)==1:
            return p[0]
        elif p[1]=='+':
            return Add(p[0],p[2])
        elif p[1]=='-':
            return Sub(p[0],p[2])
        

    # Término
    @_('factor MULTIPLY term', 
       'factor DIVIDE term', 
       'factor MODULE term', 'factor')
    def term(self, p):
        print("term "+str([v for v in p]))
        if len(p)==1:
            return p[0]
        elif p[1]=='*':
            return Mult(p[0],p[2])
        elif p[1]=='/':
            return Div(p[0],p[2])
        elif p[1]=='%':
            return Mod(p[0],p[2])  

    # Factor
    @_('factor POWER base_exponent', 
       'factor ASTERPOWER base_exponent', 
       'base_exponent')
    def factor(self, p):
        print("factor "+str([v for v in p]))
        if len(p)==1:
            return p[0]
        else: 
            return Power(p[0],p[2])



    # Base del exponente
    @_('identifier')
    def base_exponent(self, p):
        print("base_exponent "+str([v for v in p]))
        return p[0]

    @_('LPAREN aritmetic_operation RPAREN')
    def base_exponent(self, p):
        print("base_exponent "+str([v for v in p]))
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
        print("atom "+str([v for v in p]))
        return p[0]

    # Asignación de variable
    @_('var_use DEST_ASSIGN expression', 
       'var_use ASSIGN expression')
    def var_asign(self, p):
        print("var_asign "+str([v for v in p]))
        pass

    # Declaración de función
    @_('func_decl_id parameters function_full_declaration',
       'func_decl_id LPAREN RPAREN function_full_declaration',
       'func_decl_id parameters function_full_declaration SEMICOLON',
       'func_decl_id LPAREN RPAREN function_full_declaration SEMICOLON',
       'func_decl_id parameters function_inline_declaration',
       'func_decl_id LPAREN RPAREN function_inline_declaration')
    def function_declaration(self, p):
        print("function_declaration "+str([v for v in p]))
        pass

    # Identificador de declaración de función
    @_('FUNCTION IDENTIFIER')
    def func_decl_id(self, p):
        print("func_decl_id "+str([v for v in p]))
        pass

    # Declaración completa de función
    @_('scope_list')
    def function_full_declaration(self, p):
        print("function_full_declaration "+str([v for v in p]))
        pass

    # Declaración inline de función
    @_('RETURN inst SEMICOLON', 
       'type_anotation RETURN inst SEMICOLON')
    def function_inline_declaration(self, p):
        print("function_inline_declaration "+str([v for v in p]))
        pass

    # Condicional
    @_('IF inline_conditional', 
       'IF full_conditional')
    def conditional(self, p):
        print("conditional "+str([v for v in p]))
        pass

    @_('LPAREN conditional_expression RPAREN expression else_elif_statement')
    def inline_conditional(self, p):
        print("inline_conditional "+str([v for v in p]))
        pass

    @_('LPAREN conditional_expression RPAREN scope else_elif_statement')
    def full_conditional(self, p):
        print("full_conditional "+str([v for v in p]))
        pass

    # Sentencia else o elif
    @_('ELIF inline_conditional', 
       'ELIF full_conditional')
    def else_elif_statement(self, p):
        print("else_elif_statement "+str([v for v in p]))
        pass

    @_('ELSE inline_else', 
       'ELSE full_else')
    def else_elif_statement(self, p):
        print("else_elif_statement "+str([v for v in p]))
        pass

    # Else inline
    @_('expression')
    def inline_else(self, p):
        print("inline_else "+str([v for v in p]))
        pass

    # Else completo
    @_('scope_list')
    def full_else(self, p):
        print("full_else "+str([v for v in p]))
        pass

    # Bucle while
    @_('WHILE LPAREN conditional_expression RPAREN scope',
       'WHILE LPAREN conditional_expression RPAREN expression',
       'WHILE LPAREN expression RPAREN scope',
       'WHILE LPAREN expression RPAREN expression')
    def while_loop(self, p):
        print("while_loop "+str([v for v in p]))
        pass

    # Bucle for
    @_('FOR LPAREN identifier IN expression RPAREN scope',
       'FOR LPAREN identifier IN expression RPAREN expression')
    def for_loop(self, p):
        print("for_loop "+str([v for v in p]))
        pass

    # Expresión condicional
    @_('condition AND conditional_expression', 
       'condition OR conditional_expression', 
       'NOT condition', 
       'condition')
    def conditional_expression(self, p):
        print("conditional_expression "+str([v for v in p]))
        pass

    # Condición
    @_('comparation', 
       'IDENTIFIER type_conforming', 
       'LPAREN conditional_expression RPAREN')
    def condition(self, p):
        print("condition "+str([v for v in p]))
        pass

    # Comparación
    @_('expression GREATER_THAN expression', 
       'expression LESS_THAN expression',
       'expression GREATER_EQUAL expression', 
       'expression LESS_EQUAL expression',
       'expression EQUAL expression', 
       'expression NOT_EQUAL expression')
    def comparation(self, p):
        print("comparation "+str([v for v in p]))
        pass

    # Valor booleano
    @_('TRUE', 
       'FALSE')
    def boolean_value(self, p):
        print("boolean_value "+str([v for v in p]))
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
        print("type_declaration "+str([v for v in p]))
        pass

    # Parámetros
    @_('LPAREN arguments_list RPAREN')
    def parameters(self, p):
        print("parameters "+str([v for v in p]))
        pass

    # Herencia de tipo
    @_('INHERITS IDENTIFIER', 
       'INHERITS IDENTIFIER parameters')
    def inherits_type(self, p):
        print("inherits_type "+str([v for v in p]))
        pass

    # Cuerpo de la declaración
    @_('LBRACE RBRACE', 
       'LBRACE decl_list RBRACE')
    def decl_body(self, p):
        print("decl_body "+str([v for v in p]))
        pass

    # Lista de declaraciones
    @_('decl SEMICOLON', 'decl SEMICOLON decl_list')
    def decl_list(self, p):
        print("decl_list "+str([v for v in p]))
        pass

    # Declaración
    @_('atribute_declaration', 
       'method_declaration')
    def decl(self, p):
        print("decl "+str([v for v in p]))
        pass

    # Declaración de atributo
    @_('identifier ASSIGN expression', 
       'identifier ASSIGN expression type_downcast')
    def atribute_declaration(self, p):
        print("atribute_declaration "+str([v for v in p]))
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
        print("method_declaration "+str([v for v in p]))
        pass

    # Llamada a función
    @_('IDENTIFIER LPAREN arguments_list RPAREN', 
       'IDENTIFIER LPAREN RPAREN')
    def function_call(self, p):
        print("function_call "+str([v for v in p]))
        pass

    # Instanciación de tipo
    @_('NEW IDENTIFIER LPAREN arguments_list RPAREN', 
       'NEW IDENTIFIER LPAREN RPAREN')
    def type_instanciation(self, p):
        print("type_instanciation "+str([v for v in p]))
        pass

    # Conformidad de tipo
    @_('IS identifier')
    def type_conforming(self, p):
        print("type_conforming "+str([v for v in p]))
        pass

    # Downcast de tipo
    @_('AS identifier')
    def type_downcast(self, p):
        print("type_downcast "+str([v for v in p]))
        pass

    # Lista de argumentos
    @_('argument', 
       'argument COMMA arguments_list')
    def arguments_list(self, p):
        print("arguments_list "+str([v for v in p]))
        pass

    # Argumento
    @_('expression', 
       'conditional')
    def argument(self, p):
        print("argument "+str([v for v in p]))
        pass

    # Uso de variable
    @_('IDENTIFIER', 
       'atom LBRACKET expression RBRACKET', 
       'var_attr')
    def var_use(self, p):
        print("var_use "+str([v for v in p]))
        pass

    # Atributo de variable
    @_('IDENTIFIER DOT IDENTIFIER', 
       'IDENTIFIER DOT var_attr')
    def var_attr(self, p):
        print("var_attr "+str([v for v in p]))
        pass

    # Método de variable
    @_('IDENTIFIER DOT function_call')
    def var_method(self, p):
        print("var_method "+str([v for v in p]))
        pass

    # Control de flujo
    @_('while_loop', 
       'conditional', 
       'for_loop')
    def flux_control(self, p):
        print("flux_control "+str([v for v in p]))
        pass

    # Declaración de protocolo
    @_('PROTOCOL IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER protocol_body SEMICOLON',
       'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body SEMICOLON')
    def protocol_declaration(self, p):
        print("protocol_declaration "+str([v for v in p]))
        pass

    # Cuerpo del protocolo
    @_('LBRACE virtual_method_list RBRACE')
    def protocol_body(self, p):
        print("protocol_body "+str([v for v in p]))
        pass

    # Lista de métodos virtuales
    @_('virtual_method SEMICOLON', 
       'virtual_method SEMICOLON virtual_method_list')
    def virtual_method_list(self, p):
        print("virtual_method_list "+str([v for v in p]))
        pass

    # Método virtual
    @_('IDENTIFIER parameters type_anotation', 
       'IDENTIFIER LPAREN RPAREN type_anotation')
    def virtual_method(self, p):
        print("virtual_method "+str([v for v in p]))
        pass

    # Vector
    @_('LBRACKET vector_decl RBRACKET')
    def vector(self, p):
        print("vector "+str([v for v in p]))
        pass

    # Declaración de vector
    @_('arguments_list', 
       'expression SINCETHAT identifier IN expression',
       'expression OR identifier IN expression')
    def vector_decl(self, p):
        print("vector_decl "+str([v for v in p]))
        pass

    # Rango
    @_('RANGE LPAREN argument COMMA argument RPAREN')
    def build_in_range(self, p):
        print("build_in_range "+str([v for v in p]))
        pass

    # Imprimir
    @_('PRINT LPAREN argument RPAREN')
    def build_in_print(self, p):
        print("build_in_print "+str([v for v in p]))
        pass

    # Funciones integradas
    @_('build_in_range', 
       'build_in_print')
    def build_in_functions(self, p):
        print("build_in_functions "+str([v for v in p]))
        pass

    @_('SQRT LPAREN argument RPAREN', 
       'SIN LPAREN argument RPAREN',
       'COS LPAREN argument RPAREN', 
       'EXP LPAREN argument RPAREN')
    def build_in_functions(self, p):
        print("build_in_functions "+str([v for v in p]))
        pass

    @_('LOG LPAREN argument COMMA argument RPAREN')
    def build_in_functions(self, p):
        print("build_in_functions "+str([v for v in p]))
        pass

    @_('RAND LPAREN RPAREN')
    def build_in_functions(self, p):
        print("build_in_functions "+str([v for v in p]))
        pass

    # Constantes integradas
    @_('PI_CONST', 
       'E_CONST')
    def build_in_consts(self, p):
        print("build_in_consts "+str([v for v in p]))
        pass

    # Regla vacía
    @_('')
    def empty(self, p):
        print("empty "+str([v for v in p]))
        pass

    # Manejo de errores
    def error(self, p):
        print(p)
        lineno = p.lineno if p else 'EOF'
        value = repr(p.value) if p else 'EOF'
        print(f'{lineno}: Syntax error at {value} {p}')