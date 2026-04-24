#solver.py
import sympy as sp
def hallar_puntos_criticos(formula_texto):
    f = sp.sympify(formula_texto)
    variables = sorted(list(f.free_symbols), key=lambda s: s.name)
    n = len(variables)
    
    # 1. Gradiente
    gradiente = [sp.diff(f, var) for var in variables]
    grad_dict = {f"df/d{var}": g for var, g in zip(variables, gradiente)}
    puntos_crudos = sp.solve(gradiente, variables, dict=True)

    puntos_limpios = []
    puntos_reales_calc = []

    # 2. Segundas derivadas
    derivadas_segundas = {}
    for i in range(n):
        for j in range(n):
            deriv = sp.diff(f, variables[i], variables[j])
            nombre = f"d²f / d{variables[i]}d{variables[j]}"
            derivadas_segundas[nombre] = deriv

    # 3. Cálculo de puntos
    puntos_crudos = sp.solve(gradiente, variables, dict=True)
    puntos_limpios = []
    
    for p in puntos_crudos:
        
        if all(val.is_real for val in p.values()):
            punto_str = {str(k): float(v) if v.is_real else v for k, v in p.items()}
            
            # --- LÍNEA CLAVE: EVALUAR f(P) ---
            # Sustituimos el punto en la función original y redondeamos
            valor_f = float(f.subs(p))
            punto_str["f_objetivo"] = round(valor_f, 4)
            # ---------------------------------
            puntos_limpios.append(punto_str)
            puntos_reales_calc.append(p)
    
    hessiana_sym = sp.hessian(f, variables)
    
    return puntos_limpios, puntos_reales_calc, hessiana_sym, variables, grad_dict, derivadas_segundas