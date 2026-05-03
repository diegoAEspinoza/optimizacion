#solver.py
import re
import sympy as sp
import numpy as np
from itertools import combinations

def procesar_restricciones(restr_list, x_s, y_s):
    constraints = []
    errores = []

    for r_str in restr_list:
        if not r_str.strip():
            continue
            
        try:
            parts = re.split(r'(<=|>=|<|>|=)', r_str.replace(" ", ""))
            
            if len(parts) == 3:
                lhs_str, op, rhs_str = parts
                e = sp.sympify(lhs_str) - sp.sympify(rhs_str)
                
                a = float(e.coeff(x_s))
                b = float(e.coeff(y_s))
                c_val = float(-e.subs({x_s: 0, y_s: 0}))
                
                constraints.append({
                    'a': a, 'b': b, 'c': c_val, 'op': op, 'expr': r_str
                })
            else:
                errores.append(f"Formato inválido en: '{r_str}'. Falta el operador (=, <, >, etc.)")
                
        except Exception as e:
            errores.append(f"Error de sintaxis en: '{r_str}'")
            
    return constraints, errores



def calcular_optimo(f_str, restr_list, objetivo):
    x_s, y_s = sp.symbols('x y')
    f_sym = sp.sympify(f_str)
    f_num = sp.lambdify((x_s, y_s), f_sym, 'numpy')

    # Parsear restricciones
    constraints, lista_errores= procesar_restricciones(restr_list, x_s, y_s)

    # Calcular todos los vértices posibles
    vertices = []
    for r1, r2 in combinations(constraints, 2):
        A = np.array([[r1['a'], r1['b']], [r2['a'], r2['b']]], dtype=float)
        B = np.array([r1['c'], r2['c']], dtype=float)
        try:
            interseccion = np.linalg.solve(A, B)
            if interseccion[0] >= 0 and interseccion[1] >= 0:
                vertices.append(interseccion)
        except np.linalg.LinAlgError:
            continue 

    for r in constraints:
        if r['a'] != 0: vertices.append(np.array([r['c']/r['a'], 0]))
        if r['b'] != 0: vertices.append(np.array([0, r['c']/r['b']]))
    
    vertices.append(np.array([0, 0]))

    # Filtrar vértices factibles
    vertices_factibles = []
    for v in vertices:
        cumple = True
        for r in constraints:
            valor_izq = r['a'] * v[0] + r['b'] * v[1]
            c_val = r['c']
            op = r['op']
            tol = 1e-5

            if op == "<=":
                if not (valor_izq <= c_val + tol): cumple = False
            elif op == ">=":
                if not (valor_izq >= c_val - tol): cumple = False
            elif op == "=":
                if not np.isclose(valor_izq, c_val, atol=tol): cumple = False
            elif op == "<":
                if not (valor_izq < c_val): cumple = False
            elif op == ">":
                if not (valor_izq > c_val): cumple = False
            
            if not cumple: break
            
        if cumple:
            if not any(np.allclose(v, vf, atol=tol) for vf in vertices_factibles):
                vertices_factibles.append(v)

    # Hallar el óptimo
    p_opt, z_opt = None, None
    if vertices_factibles:
        puntos = np.array(vertices_factibles)
        valores_z = [float(f_sym.subs({x_s: p[0], y_s: p[1]})) for p in puntos]
        idx_opt = np.argmin(valores_z) if objetivo == "Minimizar" else np.argmax(valores_z)
        p_opt = puntos[idx_opt]
        z_opt = valores_z[idx_opt]

    if len(vertices_factibles) > 2:
        centro = np.mean(vertices_factibles, axis=0)
        vertices_factibles.sort(key=lambda p: np.arctan2(p[1] - centro[1], p[0] - centro[0]))

    puntos_tabla = []
    if vertices_factibles:
        puntos = np.array(vertices_factibles)
        # Calculamos todos los valores de Z para la tabla
        valores_z = [float(f_sym.subs({x_s: p[0], y_s: p[1]})) for p in puntos]
        
        # Creamos una lista de diccionarios para la tabla
        for i in range(len(puntos)):
            puntos_tabla.append({
                "Punto": f"Vértice {i+1}",
                "X": round(puntos[i][0], 4),
                "Y": round(puntos[i][1], 4),
                "Z (Valor Objetivo)": round(valores_z[i], 4),
                "Es Óptimo": "!!" if i == idx_opt else ""
            })
        
        # REORDENAR: Ponemos el óptimo al inicio
        puntos_tabla.insert(0, puntos_tabla.pop(idx_opt))

    return f_num, constraints, vertices_factibles, p_opt, z_opt, lista_errores, puntos_tabla