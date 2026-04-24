#parser_math.py
import sympy as sp
import numpy as np

def analizar_funcion(formula_texto):
    """
    Convierte texto en una matriz Hessiana simbólica y una función numérica.
    """
    x, y = sp.symbols('x y')
    # Convertimos el texto a una expresión de SymPy
    f = sp.sympify(formula_texto)
    
    # Calculamos las derivadas parciales (Matriz Hessiana)
    f_xx = sp.diff(f, x, x)
    f_yy = sp.diff(f, y, y)
    f_xy = sp.diff(f, x, y)
    
    hessiana_simbolica = sp.Matrix([[f_xx, f_xy], [f_xy, f_yy]])
    
    return f, hessiana_simbolica, (x, y)

def evaluar_hessiana(hessiana_simbolica, simbolos, punto_x, punto_y):
    """Evalúa la matriz simbólica en un punto específico."""
    x_sym, y_sym = simbolos
    # Sustituimos x e y por los valores numéricos
    H_num = hessiana_simbolica.subs({x_sym: punto_x, y_sym: punto_y})
    # Convertimos de SymPy Matrix a NumPy array de tipo float
    return np.array(H_num.tolist(), dtype=float)