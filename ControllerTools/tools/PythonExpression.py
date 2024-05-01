 
def python_expression(expression):
    try:
        result = eval(expression)
        ret = expression + " = " + str(result)
        print(ret)
        return ret
    except Exception as e:
        print(str(e))
        return  str(e)



#Es el tipo de datos que lleva el parametro
def python_expression_call():
    return """Use it when you need execute a simple python expression, or if you need to do a aritmetic calculation or comparission between values
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

def python_expression_name():
    return "python_expression"