import contextlib
import io
import sys
import sys 

@contextlib.contextmanager

def python_code(code):
    try:
        # Step to capture the output
        output_capture = io.StringIO()
        original_stdout = sys.stdout  # Save the original stdout
        sys.stdout = output_capture  # Redirect stdout to the StringIO object

        # Code to execute
        exec(code)
        print(code)
        # Restore stdout
        sys.stdout = original_stdout

        # Get the captured output
        captured_output = output_capture.getvalue()
        output_capture.close()  # Don't forget to close the StringIO object

        print("Captured:", captured_output)
        return str(captured_output)
    except Exception as e:
        print(str(e))
        return  str(e)



#Es el tipo de datos que lleva el parametro
def python_code_call():
    return """Use it when you need execute a simple python code,
        Examples:     
        Cálculo de un porcentaje:
            Para calcular el 20% de un número almacenado en la variable total: (20 / 100) * total

        Expresiones con funciones matemáticas:
            Usando la librería math para calcular el seno de un ángulo: math.sin(math.radians(45))
            Esto calcula el seno de 45 grados, primero convirtiendo los grados a radianes.

        Funciones con condiciones complejas:
            Una función que devuelve el máximo de tres números usando una expresión con el operador ternario:
                 def max_of_three(a, b, c):
                    return a if a > b and a > c else (b if b > c else c)

        Expresiones que utilizan list comprehensions:
            Crear una lista de los cuadrados de los números pares de otra lista: [x**2 for x in original_list if x % 2 == 0]

        Uso de funciones con argumentos variables:
            Una función que calcula el promedio de una cantidad arbitraria de números:
                def average(*args):
                    return sum(args) / len(args) if args else 0

        Expresiones involucrando cadenas de caracteres y métodos de cadena:
            Combinar métodos de cadena para limpiar y capitalizar un nombre ingresado por el usuario:
               user_input.strip().capitalize()

        Uso de expresiones lambda para operaciones inmediatas:
            Multiplicar todos los elementos de una lista por un número usando map y una expresión lambda: list(map(lambda x: x * 2, numbers))
"""



def python_code_name():
    return "python_code"