# solver.py
import re
import sympy as sp
import numpy as np
from itertools import combinations

def procesar_restricciones(restr_list, x_s, y_s):
    """Convierte texto de usuario en datos numéricos y operadores."""
    constraints = []
    errores = []

    for r_str in restr_list:
        if not r_str.strip(): continue
        try:
            # Separar por operadores relacionales
            parts = re.split(r'(<=|>=|<|>|=)', r_str.replace(" ", ""))
            if len(parts) == 3:
                lhs_str, op, rhs_str = parts
                # Normalizar a la forma ax + by - c = 0
                e = sp.sympify(lhs_str) - sp.sympify(rhs_str)
                
                constraints.append({
                    'a': float(e.coeff(x_s)),
                    'b': float(e.coeff(y_s)),
                    'c': float(-e.subs({x_s: 0, y_s: 0})),
                    'op': op,
                    'expr': r_str
                })
            else:
                errores.append(f"Formato inválido: '{r_str}'")
        except Exception:
            errores.append(f"Error de sintaxis: '{r_str}'")
            
    return constraints, errores

def calcular_optimo(f_str, restr_list, objetivo):
    """Calcula vértices, región factible y el punto óptimo."""
    x_s, y_s = sp.symbols('x y')
    f_sym = sp.sympify(f_str)
    f_num = sp.lambdify((x_s, y_s), f_sym, 'numpy')

    constraints, lista_errores = procesar_restricciones(restr_list, x_s, y_s)

    vertices = [np.array([0.0, 0.0])] 
    
    for r1, r2 in combinations(constraints, 2):
        A = np.array([[r1['a'], r1['b']], [r2['a'], r2['b']]], dtype=float)
        B = np.array([r1['c'], r2['c']], dtype=float)
        try:
            inter = np.linalg.solve(A, B)
            if inter[0] >= -1e-9 and inter[1] >= -1e-9: vertices.append(inter)
        except np.linalg.LinAlgError: continue 

    for r in constraints:
        if r['a'] != 0: 
            p = r['c']/r['a']
            if p >= 0: vertices.append(np.array([p, 0.0]))
        if r['b'] != 0: 
            p = r['c']/r['b']
            if p >= 0: vertices.append(np.array([0.0, p]))

    vertices_factibles = []
    tol = 1e-5
    for v in vertices:
        cumple = True
        for r in constraints:
            val = r['a']*v[0] + r['b']*v[1]
            op = r['op']
            if op == "<=" and not (val <= r['c'] + tol): cumple = False
            elif op == ">=" and not (val >= r['c'] - tol): cumple = False
            elif op == "=" and not np.isclose(val, r['c'], atol=tol): cumple = False
            elif op == "<" and not (val < r['c']): cumple = False
            elif op == ">" and not (val > r['c']): cumple = False
            if not cumple: break
        
        if cumple and not any(np.allclose(v, vf, atol=tol) for vf in vertices_factibles):
            vertices_factibles.append(v)

    p_opt, z_opt, puntos_tabla = None, None, []
    
    if vertices_factibles:
        evaluaciones = []
        for p in vertices_factibles:
            z_val = float(f_sym.subs({x_s: p[0], y_s: p[1]}))
            evaluaciones.append((p, z_val))
        
        # Seleccionar el mejor
        best = min(evaluaciones, key=lambda x: x[1]) if objetivo == "Minimizar" else max(evaluaciones, key=lambda x: x[1])
        p_opt, z_opt = best[0], best[1]

        # Ordenar vértices para el gráfico 
        if len(vertices_factibles) > 2:
            centro = np.mean(vertices_factibles, axis=0)
            vertices_factibles.sort(key=lambda p: np.arctan2(p[1]-centro[1], p[0]-centro[0]))

        # Construir tabla con el óptimo al inicio
        for i, (p, z) in enumerate(evaluaciones):
            puntos_tabla.append({
                "Punto": f"Vértice {i+1}",
                "X": round(p[0], 2), "Y": round(p[1], 2),
                "Z (Valor Objetivo)": round(z, 2),
                "Status": "ÓPTIMO!!" if np.allclose(p, p_opt) else ""
            })
        puntos_tabla.sort(key=lambda x: x["Status"] == "", reverse=False)

    return f_num, constraints, vertices_factibles, p_opt, z_opt, lista_errores, puntos_tabla