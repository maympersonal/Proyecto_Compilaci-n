from io import FileIO
from cmp.lexer_h import HulkLexer
from cmp.parser_h import HulkParser
from cmp.ast_h import HulkPrintVisitor
import os
from cmp.sentactic_analyzer import TypeCollector
from cmp.sentactic_analyzer import TypeBuilder
from cmp.sentactic_analyzer import TypeChecker
from cmp.HulkToCil import HulkToCilVisitor
from cmp.cil_h import get_formatter
from cmp.code_gen import HulkMIPSGenerator


def leer_archivos_hulk(ruta_carpeta):
    # Lista para almacenar los nombres de los archivos HULK encontrados
    archivos_hulk = []

    # Recorrer todos los archivos en la carpeta
    for nombre_archivo in os.listdir(ruta_carpeta):
        # Verificar si el archivo tiene la extensión .hulk
        if nombre_archivo.endswith('.hulk'):
            # Agregar el nombre del archivo a la lista
            archivos_hulk.append(nombre_archivo)

    return archivos_hulk

def hacer_lex(archivo, stop = False):
    # Abrir el archivo en modo lectura    
    with open(archivo, 'r') as f:
        # Leer el contenido del archivo
        
        contenido = f.read()
        print(contenido)
        print()
        # Crear un objeto Lexer
        lexer = HulkLexer(None)
        parser = HulkParser()
        viewer = HulkPrintVisitor()
        # Tokenizar el contenido del archi#o
        tokens = lexer.tokenize(contenido)
        # Imprimir los tokens
        # for token in tokens:
        #    print(token)

        #input()
        print()
        result = parser.parse(tokens)
        
        v = viewer.visit(result)
        print()
        print("AST = " + v)
        print()
        print(result)
        print(archivo)
        if stop:
            input()

        collector = TypeCollector()
        collector.visit(result)
        print(collector.context.types)
        print(collector.errors)

        builder = TypeBuilder(collector.context, collector.errors)
        builder.visit(result)
        print(builder)
        print(builder.errors)   


        checker = TypeChecker(builder.context,builder.errors)
        scope = checker.visit(result)
        print("SCOPE ")
        print(str(scope))#.locals))
        print("SCOPE PARENT ?")
        print(str(scope.parent))
        print("SCOPE CHILDREN")
        print(str(scope.children))
        
        hulk_to_cil = HulkToCilVisitor(builder.context)
        cil_ast = hulk_to_cil.visit(result, scope)

        formatter = get_formatter()
        print("CCCCCIIILLLLLLL")
        print("-------------------")
        print(formatter(cil_ast))
        
        code_gen = HulkMIPSGenerator()

        code_gen.visit(cil_ast)

        # v = viewer.visit(result)
        # print()
        # print("AST = " + v)
        # print()
        # print(result)
        # print(archivo)
        # if stop:
        #     input()
         
def todos():
    # Obtener la ruta de la carpeta actual
    ruta = os.getcwd() + "/programs/shorts/"
    
    # Obtener la lista de archivos HULK en la carpeta actual
    archivos_hulk = leer_archivos_hulk(ruta)
    
    # Imprimir los nombres de los archivos encontrados
    for nombre_archivo in archivos_hulk:
        print(ruta+nombre_archivo)
        hacer_lex(ruta+nombre_archivo)#, True)

def uno(archivo):
    hacer_lex(archivo)

    
#todos()
uno("programs/shorts/Debug.hulk")
# uno("programs/shorts/test2.hulk")
#uno("programs/shorts/test55.hulk")
#uno("programs/test.1.hulk")
#creacodigos()

