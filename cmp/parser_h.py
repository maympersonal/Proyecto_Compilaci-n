from sly import Parser
from cmp.lexer_h import HulkLexer
from cmp.ast_h import *

# Definición de la clase Parser para el lenguaje Hulk
class HulkParser(Parser):
    # Archivo de depuración
    debugfile = 'debug.txt'
    parsertrack = []
    tokens = HulkLexer.tokens

    # Precedencia de operadores
    precedence = (('left', OR, AND), 
                  ('left', EQUAL, NOT_EQUAL),
                  ('left', LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL),
                  ('left', PLUS, MINUS, CONCAT, ESPACEDCONCAT),
                  ('left', MULTIPLY, DIVIDE, MODULE),
                  ('right', POWER, ASTERPOWER), 
                  ('right', NOT),
                  ('right', UNARY),
                 )

    # Regla inicial
    @_('program_decl_list')
    def program(self, p):
        self.parsertrack.append("program "+str([str(v) for v in p]))
        return Program(p.program_decl_list)

    
    @_('inst_list')
    def program_decl_list(self, p):
        self.parsertrack.append("program_decl_list "+str([v for v in p]))
        return p[0]

    @_('empty')
    def program_decl_list(self, p):
        self.parsertrack.append("program_decl_list "+str([v for v in p]))
        return []
        
    @_('program_level_decl program_decl_list')
    def program_decl_list(self, p):
       self.parsertrack.append("program_decl_list "+str([v for v in p]))
       return [y for x in [[p[0]], p[1]] for y in x] if len(p) == 2 else [p[0]]
        
    # Declaraciones a nivel de programa
    @_('type_declaration', 
       'function_declaration', 
       'protocol_declaration')
    def program_level_decl(self, p):
        self.parsertrack.append("program_level_decl "+str([v for v in p]))
        return p[0]

    @_( 'inst', #**************************************************
        'inst SEMICOLON', 
        'inst SEMICOLON inst_list')
    def inst_list(self, p):
        self.parsertrack.append("inst_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[2]] for y in x] if len(p) == 3 else [p[0]]

        
    # Instrucción
    @_('scope_list',
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def inst(self, p):
        self.parsertrack.append("inst "+str([v for v in p]))
        if len(p)==3:
            return p[1]
        else: 
            return p[0]

    # Declaración de variable
    @_('LET var_init_list IN var_decl_expr')
    def var_dec(self, p):
        self.parsertrack.append("var_dec "+str([v for v in p]))
        return VarDeclaration(p.var_init_list, p.var_decl_expr)

    # Expresión de declaración de variable
    @_('scope', 
       'flux_control', 
       'expression', 
       'LPAREN var_dec RPAREN')
    def var_decl_expr(self, p):
        self.parsertrack.append("var_decl_expr "+str([v for v in p]))
        if len(p)==3:
            return p[1]
        else: 
            return p[0]

    # Lista de inicializaciones de variables
    @_('var_init', 
       'var_init COMMA var_init_list')
    def var_init_list(self, p):
        self.parsertrack.append("var_init_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[2]] for y in x] if len(p) == 3 else [p[0]]

    # Inicialización de variable
    @_('identifier ASSIGN inst', 
       'identifier ASSIGN inst type_downcast')
    def var_init(self, p):
        self.parsertrack.append("var_init "+str([v for v in p]))
        if len(p) == 3:
            return VarInit(p.identifier, p.inst, p[1])
        else:
            return VarInit(p.identifier, p.inst, p[1],p.type_downcast)

    # Identificador o parámetro completamente tipado
    @_('atom', 
       'fully_typed_param')
    def identifier(self, p):
        self.parsertrack.append("identifier "+str([v for v in p]))
        return p[0]

    # Parámetro completamente tipado
    @_('IDENTIFIER type_anotation')
    def fully_typed_param(self, p):
        self.parsertrack.append("fully_typed_param "+str([v for v in p]))
        return VarUse(p.IDENTIFIER, p.type_anotation)

    # Anotación de tipo
    @_('COLON IDENTIFIER', 
       'COLON NUMBER_TYPE', 
       'COLON BOOLEAN_TYPE')
    def type_anotation(self, p):
        self.parsertrack.append("type_anotation "+str([v for v in p]))
        return p[1]
    
    @_( 'scope', #*******************************************************
        'scope scope_list')
    def scope_list(self, p):
        self.parsertrack.append("scope_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[1]] for y in x] if len(p) == 2 else [p[0]]
        
    # Alcance
    @_('LBRACE inst_list RBRACE', 
       'LBRACE RBRACE')
    def scope(self, p):
        self.parsertrack.append("scope "+str([v for v in p]))
        if len(p)==3:
            return Scope(p[1])

    # Expresión
    @_('aritmetic_operation')
    def expression(self, p):
        self.parsertrack.append("expression "+str([str(v) for v in p]))
        return p[0]

    @_('atom CONCAT expression', 
       'atom ESPACEDCONCAT expression')
    def expression(self, p):
        self.parsertrack.append("expression "+str([v for v in p]))
        return Concat(p[1], p[0], p[2])

    @_('var_asign',
       'LPAREN var_asign RPAREN')
    def expression(self, p):
        self.parsertrack.append("expression "+str([v for v in p]))
        if len(p)==3:
            return p[1]
        else:
            return p[0]

    @_('var_dec')
    def expression(self, p):
        self.parsertrack.append("expression "+str([v for v in p]))
        return p[0]

    # Operación aritmética
    @_('term PLUS aritmetic_operation', 
       'term MINUS aritmetic_operation', 
       'term')
    def aritmetic_operation(self, p):
        self.parsertrack.append("aritmetic_operation "+str([v for v in p]))
        if len(p)==1:
            return p[0]
        elif p[1]=='+':
            return Add(p[0],p[2])
        elif p[1]=='-':
            return Sub(p[0],p[2])
        

    # Término
    @_('factor MULTIPLY term', 
       'factor DIVIDE term', 
       'factor MODULE term', 
       'factor')
    def term(self, p):
        self.parsertrack.append("term "+str([v for v in p]))
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
       'factor ASTERPOWER base_exponent')
    def factor(self, p):
        self.parsertrack.append("factor "+str([v for v in p]))
        return Power(p[0],p[2])
        
    @_('base_exponent')
    def factor(self, p):
        self.parsertrack.append("factor1 "+str([v for v in p]))
        return p[0]
        
    @_('MINUS factor %prec UNARY',
       'PLUS factor %prec UNARY')
    def factor(self, p):
        self.parsertrack.append("factor "+str([v for v in p]))
        return Unary(p[0], p[1])
        
    # Base del exponente
    @_('identifier')
    def base_exponent(self, p):
        self.parsertrack.append("base_exponent "+str([v for v in p]))
        return p[0]

    @_('LPAREN aritmetic_operation RPAREN')
    def base_exponent(self, p):
        self.parsertrack.append("base_exponent "+str([v for v in p]))
        return p[1]

    # Átomo
    @_('function_call', 
       'var_use', 
       'vector', 
       'var_method',
       'type_instanciation', 
       'boolean_value', 
       'build_in_functions', 
       'build_in_consts')
    def atom(self, p):
        self.parsertrack.append("atom "+str([v for v in p]))
        return p[0]

    @_('STRING')
    def atom(self, p):
        self.parsertrack.append("String "+str([v for v in p]))
        return String(p[0])
        
    @_('NUMBER')
    def atom(self, p):
        self.parsertrack.append("Number "+str([v for v in p]))
        return Number(p[0])


    # Asignación de variable
    @_('var_use DEST_ASSIGN expression', 
       'var_use ASSIGN expression')
    def var_asign(self, p):
        self.parsertrack.append("var_asign "+str([v for v in p]))
        return VarInit(p.var_use, p.expression, p[1])

    # Declaración de función
    @_('FUNCTION IDENTIFIER parameters function_full_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN function_full_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration)
        
    @_('FUNCTION IDENTIFIER parameters function_full_declaration SEMICOLON')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN function_full_declaration SEMICOLON')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration)
        
    @_('FUNCTION IDENTIFIER parameters function_inline_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_inline_declaration, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN function_inline_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_inline_declaration)
    
    @_('FUNCTION IDENTIFIER parameters type_anotation function_full_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN type_anotation function_full_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation)
        
    @_('FUNCTION IDENTIFIER parameters type_anotation function_full_declaration SEMICOLON')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN type_anotation function_full_declaration SEMICOLON')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation)
        
    @_('FUNCTION IDENTIFIER parameters type_anotation function_inline_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_inline_declaration, type_anotation = p.type_anotation, parameters = p.parameters)
        
    @_('FUNCTION IDENTIFIER LPAREN RPAREN type_anotation function_inline_declaration')
    def function_declaration(self, p):
        self.parsertrack.append("function_declaration "+str([v for v in p]))
        return FunctionDeclaration(p.IDENTIFIER, p.function_inline_declaration, type_anotation = p.type_anotation )

    # Declaración completa de función
    @_('scope')
    def function_full_declaration(self, p):
        self.parsertrack.append("function_full_declaration "+str([v for v in p]))
        return p.scope

    # Declaración inline de función
    @_('RETURN inst SEMICOLON')
    def function_inline_declaration(self, p):
        self.parsertrack.append("function_inline_declaration "+str([v for v in p]))
        return p.inst
    
        
    # Condicional
    @_('IF inline_conditional', 
       'IF full_conditional')
    def conditional(self, p):
        self.parsertrack.append("conditional "+str([v for v in p]))
        return p[1]

    @_('LPAREN conditional_expression RPAREN expression else_elif_statement')
    def inline_conditional(self, p):
        self.parsertrack.append("inline_conditional "+str([v for v in p]))
        return InlineConditional(p.conditional_expression, p.expression, p.else_elif_statement)

    @_('LPAREN conditional_expression RPAREN scope_list else_elif_statement')
    def full_conditional(self, p):
        self.parsertrack.append("full_conditional "+str([v for v in p]))
        return FullConditional(p.conditional_expression, p.scope_list, p.else_elif_statement)

    # Sentencia else o elif
    @_('ELIF inline_conditional', 
       'ELIF full_conditional')
    def else_elif_statement(self, p):
        self.parsertrack.append("else_elif_statement "+str([v for v in p]))
        return p[1]

    @_('ELSE inline_else', 
       'ELSE full_else')
    def else_elif_statement(self, p):
        self.parsertrack.append("else_elif_statement "+str([v for v in p]))
        return p[1]

    # Else inline
    @_('expression')
    def inline_else(self, p):
        self.parsertrack.append("inline_else "+str([v for v in p]))
        return p[0]

    # Else completo
    @_('scope')
    def full_else(self, p):
        self.parsertrack.append("full_else "+str([v for v in p]))
        return p[0]

    # Bucle while
    @_('WHILE LPAREN conditional_expression RPAREN scope',
       'WHILE LPAREN conditional_expression RPAREN expression',
       'WHILE LPAREN expression RPAREN scope',
       'WHILE LPAREN expression RPAREN expression')
    def while_loop(self, p):
        self.parsertrack.append("while_loop "+str([v for v in p]))
        return WhileLoop(p[2], p[4])
    
    # Bucle for
    @_('FOR LPAREN identifier IN expression RPAREN scope',
       'FOR LPAREN identifier IN expression RPAREN expression')
    def for_loop(self, p):
        self.parsertrack.append("for_loop "+str([v for v in p]))
        return ForLoop(p[2], p[4] , p[6])

    # Expresión condicional
    @_('condition AND conditional_expression', 
       'condition OR conditional_expression', 
       'NOT condition', 
       'condition')
    def conditional_expression(self, p):
        self.parsertrack.append("conditional_expression "+str([v for v in p]))
        if len(p)==1:
            return p[0]
        elif p[1]=='&':
            return And(p[0],p[2])
        elif p[1]=='|':
            return Or(p[0],p[2])
        elif p[0]=='!':
            return Not(p[1])


    # Condición
    @_('comparation')
    def condition(self, p):
        self.parsertrack.append("condition "+str([v for v in p]))
        return p[0]
  


    @_('IDENTIFIER IS identifier')
    def condition(self, p):
        self.parsertrack.append("condition "+str([v for v in p]))
        return Is(p[0],p[2])

    @_('LPAREN conditional_expression RPAREN')
    def condition(self, p):
        self.parsertrack.append("condition "+str([v for v in p]))
        return p[1]

    # Comparación
    @_('expression GREATER_THAN expression', 
       'expression LESS_THAN expression',
       'expression GREATER_EQUAL expression', 
       'expression LESS_EQUAL expression',
       'expression EQUAL expression', 
       'expression NOT_EQUAL expression')
    def comparation(self, p):
        self.parsertrack.append("comparation "+str([v for v in p]))
        if p[1]=='>':
            return GreaterThan(p[0],p[2])
        elif p[1]=='<':
            return LessThan(p[0],p[2])
        elif p[1]=='>=':
            return GreaterEqual(p[0],p[2])  
        elif p[1]=='<=':
            return LessEqual(p[0],p[2])
        elif p[1]=='==':
            return Equal(p[0],p[2])
        elif p[1]=='!=':
            return NotEqual(p[0],p[2])

    # Valor booleano
    @_('TRUE', 
       'FALSE')
    def boolean_value(self, p):
        self.parsertrack.append("boolean_value "+str([v for v in p]))
        return Boolean(p[0])

    # Declaración de tipo
    @_( 'TYPE IDENTIFIER parameters decl_body',
        'TYPE IDENTIFIER parameters decl_body SEMICOLON')
    def type_declaration(self, p):
        self.parsertrack.append("type_declaration "+str([v for v in p]))
        return TypeDeclaration(p.IDENTIFIER, parameters = p.parameters,decl_body = p.decl_body)
        
    @_( 'TYPE IDENTIFIER parameters inherits_type decl_body',
        'TYPE IDENTIFIER parameters inherits_type decl_body SEMICOLON')
    def type_declaration(self, p):
        self.parsertrack.append("type_declaration "+str([v for v in p]))
        return TypeDeclaration(p.IDENTIFIER, parameters = p.parameters, inherits_type = p.inherits_type, decl_body = p.decl_body)
            
    @_('TYPE IDENTIFIER decl_body',
       'TYPE IDENTIFIER decl_body SEMICOLON')
    def type_declaration(self, p):
        self.parsertrack.append("type_declaration "+str([v for v in p]))
        return TypeDeclaration(p.IDENTIFIER, decl_body = p.decl_body)
        
    @_('TYPE IDENTIFIER inherits_type decl_body',
       'TYPE IDENTIFIER inherits_type decl_body SEMICOLON')
    def type_declaration(self, p):
        self.parsertrack.append("type_declaration "+str([v for v in p]))
        return TypeDeclaration(p.IDENTIFIER, inherits_type = p.inherits_type, decl_body = p.decl_body)
           
        
    

    # Parámetros
    @_('LPAREN arguments_list RPAREN')
    def parameters(self, p):
        self.parsertrack.append("parameters "+str([v for v in p]))
        return p[1]

    # Herencia de tipo
    @_('INHERITS IDENTIFIER', 
       'INHERITS IDENTIFIER parameters')
    def inherits_type(self, p):
        self.parsertrack.append("inherits_type "+str([v for v in p]))
        if len(p) == 3:
            return InheritsType(p.IDENTIFIER, p.parameters)
        else:
            return InheritsType(p.IDENTIFIER)

    # Cuerpo de la declaración
    @_('LBRACE RBRACE', 
       'LBRACE decl_list RBRACE')
    def decl_body(self, p):
        self.parsertrack.append("decl_body "+str([v for v in p]))
        if len(p)==3:
            return DeclarationScope(p[1])
        else:
            return DeclarationScope([])

    # Lista de declaraciones
    @_('decl SEMICOLON', 
       'decl SEMICOLON decl_list')
    def decl_list(self, p):
        self.parsertrack.append("decl_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[2]] for y in x] if len(p) == 3 else [p[0]]
        
    # Declaración
    @_('atribute_declaration', 
       'method_declaration')
    def decl(self, p):
        self.parsertrack.append("decl "+str([v for v in p]))
        return p[0]

    # Declaración de atributo
    @_('identifier ASSIGN expression', 
       'identifier ASSIGN expression type_downcast')
    def atribute_declaration(self, p):
        self.parsertrack.append("atribute_declaration "+str([v for v in p]))
        if len(p) == 3:
            return TypeVarInit(p.identifier, p.expression)
        else:
            return TypeVarInit(p.identifier, p.expression, p.type_downcast)

    
    @_('IDENTIFIER parameters RETURN expression')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.expression, parameters = p.parameters)
        
    @_('IDENTIFIER parameters function_full_declaration')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.function_full_declaration, parameters = p.parameters)
        
    @_('IDENTIFIER LPAREN RPAREN RETURN expression')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.expression)
        
    @_('IDENTIFIER LPAREN RPAREN function_full_declaration')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.function_full_declaration)
        
    @_('IDENTIFIER parameters type_anotation RETURN expression')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.expression, type_anotation = p.type_anotation, parameters = p.parameters)
        
    @_('IDENTIFIER parameters type_anotation function_full_declaration')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation, parameters = p.parameters)
        
    @_('IDENTIFIER LPAREN RPAREN type_anotation RETURN expression')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.expression, type_anotation = p.type_anotation)
        
    @_('IDENTIFIER LPAREN RPAREN type_anotation RETURN conditional_expression')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.conditional_expression, type_anotation = p.type_anotation)
        
    @_('IDENTIFIER LPAREN RPAREN type_anotation function_full_declaration')
    def method_declaration(self, p):
        self.parsertrack.append("method_declaration "+str([v for v in p]))
        return TypeMethodDeclaration(p.IDENTIFIER, p.function_full_declaration, type_anotation = p.type_anotation)
    
    
    # Llamada a función
    @_('IDENTIFIER LPAREN arguments_list RPAREN', 
       'IDENTIFIER LPAREN RPAREN')
    def function_call(self, p):
        self.parsertrack.append("function_call "+str([v for v in p]))
        if len(p) == 4:
            return FunctionCall(p[0], p[2])
        else:
            return FunctionCall(p[0])

        
    # Instanciación de tipo
    @_('NEW IDENTIFIER LPAREN arguments_list RPAREN', 
       'NEW IDENTIFIER LPAREN RPAREN')
    def type_instanciation(self, p):
        self.parsertrack.append("type_instanciation "+str([v for v in p]))
        if len(p) == 5:
            return TypeInstanciation(p.IDENTIFIER, p.arguments_list)
        else:
            return TypeInstanciation(p.IDENTIFIER)

    

    # Downcast de tipo
    @_('AS identifier')
    def type_downcast(self, p):
        self.parsertrack.append("type_downcast "+str([v for v in p]))
        return p[1]

    # Lista de argumentos
    @_('argument', 
       'argument COMMA arguments_list')
    def arguments_list(self, p):
        self.parsertrack.append("arguments_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[2]] for y in x] if len(p) == 3 else [p[0]]
    
    
        
    # Argumento
    @_('expression', 
       'conditional')
    def argument(self, p):
        self.parsertrack.append("argument "+str([v for v in p]))
        return p[0]

    # Uso de variable
    @_('IDENTIFIER',
       'var_attr')
    def var_use(self, p):
        self.parsertrack.append("var_use "+str([v for v in p]))
        return VarUse(p[0])
    
    @_('atom LBRACKET expression RBRACKET')
    def var_use(self, p):
        self.parsertrack.append("var_use "+str([v for v in p]))
        return VectorVarUse(p[0], p[2])
        
    # Atributo de variable
    @_('IDENTIFIER DOT IDENTIFIER', 
       'IDENTIFIER DOT var_attr')
    def var_attr(self, p):
        self.parsertrack.append("var_attr "+str([v for v in p]))
        return VarAttr(p[0], p[2])
    

    # Método de variable
    @_('IDENTIFIER DOT function_call')
    def var_method(self, p):
        self.parsertrack.append("var_method "+str([v for v in p]))
        return VarMethod(p.IDENTIFIER, p.function_call)

    # Control de flujo
    @_('while_loop', 
       'conditional', 
       'for_loop')
    def flux_control(self, p):
        self.parsertrack.append("flux_control "+str([v for v in p]))
        return p[0]

    # Declaración de protocolo
    @_('PROTOCOL IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER protocol_body SEMICOLON')
    def protocol_declaration(self, p):
       self.parsertrack.append("protocol_declaration "+str([v for v in p]))
       return ProtocolDeclaration(p[1], p[2])
        
    @_('PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body',
       'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body SEMICOLON')
    def protocol_declaration(self, p):
        self.parsertrack.append("protocol_declaration "+str([v for v in p]))
        return ProtocolDeclaration(p[1], p[4], p[3])
        
    
    # Cuerpo del protocolo
    @_('LBRACE virtual_method_list RBRACE')
    def protocol_body(self, p):
        self.parsertrack.append("protocol_body "+str([v for v in p]))
        return p[1]

    # Lista de métodos virtuales
    @_('virtual_method SEMICOLON', 
       'virtual_method SEMICOLON virtual_method_list')
    def virtual_method_list(self, p):
        self.parsertrack.append("virtual_method_list "+str([v for v in p]))
        return [y for x in [[p[0]], p[2]] for y in x] if len(p) == 3 else [p[0]]

    # Método virtual
    @_('IDENTIFIER LPAREN RPAREN type_anotation')
    def virtual_method(self, p):
        self.parsertrack.append("virtual_method "+str([v for v in p]))
        return ProtocolMethodDeclaration(p[0], p[3])
    
    @_('IDENTIFIER parameters type_anotation')
    def virtual_method(self, p):
        self.parsertrack.append("virtual_method "+str([v for v in p]))
        return ProtocolMethodDeclaration(p[0], p[2], p[1])
    
       
    # Vector
    @_('LBRACKET vector_decl RBRACKET')
    def vector(self, p):
        self.parsertrack.append("vector "+str([v for v in p]))
        return p[1]

    # Declaración de vector
    @_('arguments_list')
    def vector_decl(self, p):
        self.parsertrack.append("vector_decl "+str([v for v in p]))
        return VectorRangeDeclaration(p[0])
    
    @_('expression SINCETHAT identifier IN expression',
       'expression OR identifier IN expression')
    def vector_decl(self, p):
        self.parsertrack.append("vector_decl "+str([v for v in p]))
        return VectorExpressionDeclaration(p[0], p[2], p[4])

        
    # Rango
    @_('RANGE LPAREN argument COMMA argument RPAREN')
    def build_in_range(self, p):
        self.parsertrack.append("build_in_range "+str([v for v in p]))
        return BinaryBuildInFunction(p[0], p[2], p[4])

    # Imprimir
    @_('PRINT LPAREN argument RPAREN')
    def build_in_print(self, p):
        self.parsertrack.append("build_in_print "+str([v for v in p]))
        return UnaryBuildInFunction(p[0], p[2])

    # Funciones integradas
    @_('build_in_range', 
       'build_in_print')
    def build_in_functions(self, p):
        self.parsertrack.append("build_in_functions "+str([v for v in p]))
        return p[0]

    @_('SQRT LPAREN argument RPAREN', 
       'SIN LPAREN argument RPAREN',
       'COS LPAREN argument RPAREN', 
       'EXP LPAREN argument RPAREN')
    def build_in_functions(self, p):
        self.parsertrack.append("build_in_functions "+str([v for v in p]))
        return UnaryBuildInFunction(p[0], p[2])

    @_('LOG LPAREN argument COMMA argument RPAREN')
    def build_in_functions(self, p):
        self.parsertrack.append("build_in_functions "+str([v for v in p]))
        return BinaryBuildInFunction(p[0], p[2], p[4])

    @_('RAND LPAREN RPAREN')
    def build_in_functions(self, p):
        self.parsertrack.append("build_in_functions "+str([v for v in p]))
        return NoParamBuildInFunction(p[0])
                
    # Constantes integradas
    @_('PI_CONST', 
       'E_CONST')
    def build_in_consts(self, p):
        self.parsertrack.append("build_in_consts "+str([v for v in p]))
        return BuildInConst(p[0])

    # Regla vacía
    @_('')
    def empty(self, p):
        self.parsertrack.append("empty "+str([v for v in p]))
        pass

    # Manejo de errores
    def error(self, p):
        print(p)
        lineno = p.lineno if p else 'EOF'
        value = repr(p.value) if p else 'EOF'
        print(f'{lineno}: Syntax error at {value} {p}')

    def parse(self, tokens):
        self.parsertrack = []
        state = 1
        result = super().parse(tokens)
        if self.debugfile:
            with open(self.debugfile, 'a') as f:
                f.write(f'\nParser track:\n\n')
                for track in self.parsertrack:
                    f.write(f'({state}): {track}\n')
                    # state += 1
                # viever = HulkPrintVisitor()
                # ast = viever.visit(result)
                # f.write(f'\nAST:\n\n')
                # f.write(ast)
        '''for track in self.parsertrack:
            print(f'State {state}: {track}')
            state += 1'''
        return result