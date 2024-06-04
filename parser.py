from sly import Parser
from lexer import HulkLexer

class HulkParser(Parser):
    debugfile = 'debug.txt'
    tokens = HulkLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQUAL, NOT_EQUAL),
        ('left', LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL),
        ('left', PLUS, MINUS, CONCAT, ESPACEDCONCAT),
        ('left', MULTIPLY, DIVIDE, MODULE),
        ('right', POWER, ASTERPOWER),
        ('right', NOT)
    )

    @_('program_decl_list')
    def program(self, p):
        pass

    @_( 'inst_wrapper',
        'program_level_decl program_decl_list',
        'empty')
    def program_decl_list(self, p):
        pass

    @_( 'type_declaration',
        'function_declaration',
        'protocol_declaration')
    def program_level_decl(self, p):
        pass

    @_( 'inst SEMICOLON',
        'inst SEMICOLON inst_list')
    def inst_list(self, p):
        pass

    @_( 'inst',
        'inst SEMICOLON')
    def inst_wrapper(self, p):
        pass

    @_( 'scope',
        'flux_control',
        'expression',
        'LPAREN var_dec RPAREN')
    def inst(self, p):
        pass

    @_('LET var_init_list IN var_decl_expr')
    def var_dec(self, p):
        pass

    @_( 'scope',
        'flux_control',
        'expression',
        'LPAREN var_dec RPAREN')
    def var_decl_expr(self, p):
        pass

    @_( 'var_init',
        'var_init COMMA var_init_list')
    def var_init_list(self, p):
        pass

    @_( 'identifier ASSIGN inst',
        'identifier ASSIGN inst type_downcast')
    def var_init(self, p):
        pass

    @_( 'identifier',
        'identifier COMMA id_list')
    def id_list(self, p):
        pass

    @_( 'atom',
        'fully_typed_param')
    def identifier(self, p):
        pass


    @_('IDENTIFIER type_anotation')
    def fully_typed_param(self, p):
        pass

    @_( 'COLON IDENTIFIER',
        'COLON NUMBER_TYPE',
        'COLON BOOLEAN_TYPE')
    def type_anotation(self, p):
        pass

    @_( 'LBRACE inst_list RBRACE',
        'LBRACE RBRACE')
    def scope(self, p):
        pass

    @_('aritmetic_operation')
    def expression(self, p):
        pass

    @_( 'atom CONCAT expression',
        'atom ESPACEDCONCAT expression')
    def expression(self, p):
        pass

    @_('var_asign')
    def expression(self, p):
        pass

    @_('var_dec')
    def expression(self, p):
        pass

    @_( 'term PLUS aritmetic_operation',
        'term MINUS aritmetic_operation',
        'term')
    def aritmetic_operation(self, p):
        pass

    @_( 'factor MULTIPLY term',
        'factor DIVIDE term',
        'factor MODULE term',
        'factor')
    def term(self, p):
        pass

    @_( 'factor POWER base_exponent',
        'factor ASTERPOWER base_exponent',
        'base_exponent')
    def factor(self, p):
        pass

    @_('atom')
    def base_exponent(self, p):
        pass

    @_('LPAREN aritmetic_operation RPAREN')
    def base_exponent(self, p):
        pass


    @_( 'NUMBER',
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

    @_( 'var_use DEST_ASSIGN expression',
        'var_use ASSIGN expression')
    def var_asign(self, p):
        pass

    @_( 'func_decl_id LPAREN id_list RPAREN function_full_declaration',
        'func_decl_id LPAREN RPAREN function_full_declaration',
        'func_decl_id LPAREN id_list RPAREN function_full_declaration SEMICOLON',
        'func_decl_id LPAREN RPAREN function_full_declaration SEMICOLON',
        'func_decl_id LPAREN id_list RPAREN function_inline_declaration',
        'func_decl_id LPAREN RPAREN function_inline_declaration')
    def function_declaration(self, p):
        pass

    @_('FUNCTION IDENTIFIER')
    def func_decl_id(self, p):
        pass

    @_('scope')
    def function_full_declaration(self, p):
        pass



    @_( 'RETURN inst SEMICOLON',
        'type_anotation RETURN inst SEMICOLON')
    def function_inline_declaration(self, p):
        pass

    @_( 'IF inline_conditional',
        'IF full_conditional')
    def conditional(self, p):
        pass

    @_('LPAREN conditional_expression RPAREN expression else_elif_statement')
    def inline_conditional(self, p):
        pass

    @_('LPAREN conditional_expression RPAREN scope else_elif_statement')
    def full_conditional(self, p):
        pass

    @_( 'ELIF inline_conditional',
        'ELIF full_conditional')
    def else_elif_statement(self, p):
        pass

    @_( 'ELSE inline_else',
        'ELSE full_else')
    def else_elif_statement(self, p):
        pass

    @_('expression')
    def inline_else(self, p):
        pass

    @_('scope')
    def full_else(self, p):
        pass

    @_( 'WHILE LPAREN conditional_expression RPAREN scope',
        'WHILE LPAREN conditional_expression RPAREN expression',
        'WHILE LPAREN expression RPAREN scope',
        'WHILE LPAREN expression RPAREN expression')
    def while_loop(self, p):
        pass

    @_( 'FOR LPAREN identifier IN expression RPAREN scope',
        'FOR LPAREN identifier IN expression RPAREN expression')
    def for_loop(self, p):
        pass

    @_( 'condition AND conditional_expression',
        'condition OR conditional_expression',
        'NOT condition',
        'condition')
    def conditional_expression(self, p):
        pass

    @_( 'comparation',  
        'IDENTIFIER type_conforming',
        'LPAREN conditional_expression RPAREN')
    def condition(self, p):
        pass

    @_( 'expression GREATER_THAN expression',
        'expression LESS_THAN expression',
        'expression GREATER_EQUAL expression',
        'expression LESS_EQUAL expression',
        'expression EQUAL expression',
        'expression NOT_EQUAL expression')
    def comparation(self, p):
        pass

    @_( 'TRUE',
        'FALSE')
    def boolean_value(self, p):
        pass

    @_( 'TYPE IDENTIFIER constructor decl_body',
        'TYPE IDENTIFIER constructor inherits_type decl_body',
        'TYPE IDENTIFIER constructor decl_body SEMICOLON',
        'TYPE IDENTIFIER constructor inherits_type decl_body SEMICOLON')
    def type_declaration(self, p):
        pass

    @_( 'LPAREN id_list RPAREN',
        'LPAREN param_list RPAREN',
        'LPAREN RPAREN',
        'empty')
    def constructor(self, p):
        pass

    @_('INHERITS IDENTIFIER constructor')
    def inherits_type(self, p):
        pass

    @_( 'LBRACE RBRACE',
        'LBRACE decl_list RBRACE')
    def decl_body(self, p):
        pass

    @_( 'decl SEMICOLON',
        'decl SEMICOLON decl_list')
    def decl_list(self, p):
        pass

    @_( 'atribute_declaration',
        'method_declaration')
    def decl(self, p):
        pass

    @_( 'identifier ASSIGN expression',
        'identifier ASSIGN expression type_downcast')
    def atribute_declaration(self, p):
        pass

    @_( 'IDENTIFIER LPAREN id_list RPAREN RETURN expression',
        'IDENTIFIER LPAREN id_list RPAREN function_full_declaration',
        'IDENTIFIER LPAREN RPAREN RETURN expression',
        'IDENTIFIER LPAREN RPAREN function_full_declaration',
        'IDENTIFIER LPAREN id_list RPAREN type_anotation RETURN expression',
        'IDENTIFIER LPAREN id_list RPAREN type_anotation function_full_declaration',
        'IDENTIFIER LPAREN RPAREN type_anotation RETURN expression',
        'IDENTIFIER LPAREN RPAREN type_anotation RETURN conditional_expression',
        'IDENTIFIER LPAREN RPAREN type_anotation function_full_declaration')
    def method_declaration(self, p):
        pass

    @_( 'IDENTIFIER LPAREN param_list RPAREN',
        'IDENTIFIER LPAREN RPAREN')
    def function_call(self, p):
        pass

    @_( 'NEW IDENTIFIER LPAREN param_list RPAREN',
        'NEW IDENTIFIER LPAREN RPAREN')
    def type_instanciation(self, p):
        pass

    @_( 'IS identifier')
    def type_conforming(self, p):
        pass

    @_( 'AS identifier')
    def type_downcast(self, p):
        pass

    @_( 'param',
        'param COMMA param_list')
    def param_list(self, p):
        pass

    @_( 'expression',
        'conditional')
    def param(self, p):
        pass

    @_( 'IDENTIFIER',
        'atom LBRACKET expression RBRACKET',
        'var_attr')
    def var_use(self, p):
        pass

    @_( 'IDENTIFIER DOT IDENTIFIER',
        'IDENTIFIER DOT var_attr')
    def var_attr(self, p):
        pass

    @_('IDENTIFIER DOT function_call')
    def var_method(self, p):
        pass

    @_( 'while_loop',
        'conditional',
        'for_loop')
    def flux_control(self, p):
        pass

    @_( 'PROTOCOL IDENTIFIER protocol_body',
        'PROTOCOL IDENTIFIER protocol_body SEMICOLON',
        'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body',
        'PROTOCOL IDENTIFIER EXTENDS IDENTIFIER protocol_body SEMICOLON')
    def protocol_declaration(self, p):
        pass

    @_('LBRACE virtual_method_list RBRACE')
    def protocol_body(self, p):
        pass

    @_( 'virtual_method SEMICOLON',
        'virtual_method SEMICOLON virtual_method_list')
    def virtual_method_list(self, p):
        pass


    @_( 'IDENTIFIER LPAREN RPAREN type_anotation',
        'IDENTIFIER LPAREN fully_typed_params RPAREN type_anotation')
    def virtual_method(self, p):
        pass

    @_( 'fully_typed_param',
        'fully_typed_param COMMA fully_typed_params')
    def fully_typed_params(self, p):
        pass

    @_('LBRACKET vector_decl RBRACKET')
    def vector(self, p):
        pass

    @_( 'param_list',
        'expression SINCETHAT identifier IN expression',
        'expression OR identifier IN expression')
    def vector_decl(self, p):
        pass

    @_( 'RANGE LPAREN param COMMA param RPAREN' )
    def build_in_range(self, p):
        pass

    @_( 'PRINT LPAREN param RPAREN' )
    def build_in_print(self, p):
        pass

    @_( 'build_in_range',
        'build_in_print')
    def build_in_functions(self, p):
        pass

    @_( 'SQRT LPAREN param RPAREN',
        'SIN LPAREN param RPAREN',
        'COS LPAREN param RPAREN',
        'EXP LPAREN param RPAREN')
    def build_in_functions(self, p):
        pass

    @_( 'LOG LPAREN param COMMA param RPAREN')
    def build_in_functions(self, p):
        pass

    @_( 'RAND LPAREN RPAREN')
    def build_in_functions(self, p):
        pass

    @_( 'PI_CONST',
        'E_CONST')
    def build_in_consts(self, p):
        pass

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        print(p)
        lineno = p.lineno if p else 'EOF'
        value = repr(p.value) if p else 'EOF'
        print(f'{lineno}: Syntax error at {value} {p}')

# To use the parser
if __name__ == '__main__':
    lexer = HulkLexer(None)
    parser = HulkParser()
    data = '''


function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}


    '''

    result = parser.parse(lexer.tokenize(data))
    print(result)