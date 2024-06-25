from io import FileIO
from cmp.lexer_h import HulkLexer
from cmp.parser_h import HulkParser
from cmp.ast_h import HulkPrintVisitor
import os
# from cmp.sentactic_analyzer import TypeCollector
# from cmp.sentactic_analyzer import TypeBuilder
# from cmp.sentactic_analyzer import TypeChecker


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
        viever = HulkPrintVisitor()
        # Tokenizar el contenido del archi#o
        tokens = lexer.tokenize(contenido)
        # Imprimir los tokens
        #for token in tokens:
           #print(token)

        #input()
        print()
        result = parser.parse(lexer.tokenize(contenido))
        v = viever.visit(result)
        print()
        print("AST = " + v)
        print()
        print_visitor.visit(result)
        print(result)
        print(archivo)
        if stop:
            input()

        # collector = TypeCollector(errors)
        # collector.visit(ast)

        # builder = TypeBuilder(collector.context, errors)
        # builder.visit(ast)
            
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
#uno("programs/shorts/test7.hulk")
#uno("programs/test.1.hulk")
#creacodigos()

