from io import FileIO
from lexer import HulkLexer
from parser import HulkParser
import os



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
        # Tokenizar el contenido del archivo
        tokens = lexer.tokenize(contenido)
        # Imprimir los tokens
        #for token in tokens:
           #print(token)

        #input()
        print()
        result = parser.parse(lexer.tokenize(contenido))
        print(result)
        print(archivo)
        if stop:
            input()
            
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
#uno("programs//shorts//test35.hulk")
uno("programs//test.1.hulk")
#creacodigos()

