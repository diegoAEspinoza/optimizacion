import sympy as sp
import numpy as np
from itertools import combinations

import numpy as np
import sympy as sp
from itertools import combinations

def calcular_optimo(f_str, restr_list, objetivo):
    x_s, y_s = sp.symbols('x y')
    f_sym = sp.sympify(f_str)
    f_num = sp.lambdify((x_s, y_s), f_sym, 'numpy')

    # Parsear restricciones
    constraints = []
    for r in restr_list:
        e = sp.sympify(r['expr'])
        a = float(e.coeff(x_s))
        b = float(e.coeff(y_s))
        constraints.append({'a': a, 'b': b, 'c': r['c']})

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
            if not (r['a']*v[0] + r['b']*v[1] >= r['c'] - 1e-5):
                cumple = False
                break
        if cumple:
            if not any(np.allclose(v, vf) for vf in vertices_factibles):
                vertices_factibles.append(v)

    # Hallar el óptimo
    p_opt, z_opt = None, None
    if vertices_factibles:
        puntos = np.array(vertices_factibles)
        valores_z = [float(f_sym.subs({x_s: p[0], y_s: p[1]})) for p in puntos]
        idx_opt = np.argmin(valores_z) if objetivo == "Minimizar" else np.argmax(valores_z)
        p_opt = puntos[idx_opt]
        z_opt = valores_z[idx_opt]

    return f_num, constraints, vertices_factibles, p_opt, z_opt

class LinearOptimizer:
    def __init__(self, f_str, restr_list):
        self.x_s, self.y_s = sp.symbols('x y')
        self.f_sym = sp.sympify(f_str)
        self.constraints = self._parse_constraints(restr_list)

    def _parse_constraints(self, restr_list):
        parsed = []
        for r in restr_list:
            e = sp.sympify(r['expr'])
            parsed.append({
                'a': float(e.coeff(self.x_s)),
                'b': float(e.coeff(self.y_s)),
                'c': r['c']
            })
        return parsed

    def find_vertices(self):
        vertices = [np.array([0, 0])]
        # Intersecciones entre restricciones
        for r1, r2 in combinations(self.constraints, 2):
            A = np.array([[r1['a'], r1['b']], [r2['a'], r2['b']]], dtype=float)
            B = np.array([r1['c'], r2['c']], dtype=float)
            try:
                inter = np.linalg.solve(A, B)
                if inter[0] >= 0 and inter[1] >= 0: vertices.append(inter)
            except np.linalg.LinAlgError: continue
        
        # Intersecciones con ejes
        for r in self.constraints:
            if r['a'] != 0: vertices.append(np.array([r['c']/r['a'], 0]))
            if r['b'] != 0: vertices.append(np.array([0, r['c']/r['b']]))
            
        return self._filter_feasible(vertices)

    def _filter_feasible(self, vertices):
        factibles = []
        for v in vertices:
            if all(r['a']*v[0] + r['b']*v[1] >= r['c'] - 1e-5 for r in self.constraints):
                if not any(np.allclose(v, vf) for vf in factibles):
                    factibles.append(v)
        return factibles