import sympy as sp
import numpy as np
from itertools import combinations

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