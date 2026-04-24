#logic.pý
import numpy as np

def calcular_clasificacion(H, tol=1e-8):
    """Lógica central para determinar el tipo de punto crítico."""
    autovalores = np.linalg.eigvals(H)
    n = len(autovalores)
    
    positivos = sum(autovalores > tol)
    negativos = sum(autovalores < -tol)
    ceros = sum(np.abs(autovalores) <= tol)

    if ceros > 0:
        return "Inconcluyente", "Matriz semidefinida.", autovalores
    elif positivos == n:
        return "Mínimo", "Definida Positiva.", autovalores
    elif negativos == n:
        return "Máximo", "Definida Negativa.", autovalores
    elif positivos > 0 and negativos > 0:
        return "Silla", "Indefinida.", autovalores
    return "Error", "Error de cálculo.", autovalores

def clasificar_autovalores(H_num):
    autovalores = np.linalg.eigvals(H_num)
    # Filtramos ceros por precisión numérica
    pos = sum(autovalores > 1e-9)
    neg = sum(autovalores < -1e-9)
    n = len(autovalores)

    if pos == n: return "Mínimo Local", autovalores
    if neg == n: return "Máximo Local", autovalores
    if pos > 0 and neg > 0: return "Punto de Silla", autovalores
    return "Inconcluyente (Semidefinida)", autovalores

def clasificar_sylvester(H_num):
    n = H_num.shape[0]
    # Calculamos los determinantes de las submatrices (Menores principales)
    menores = [np.linalg.det(H_num[:i, :i]) for i in range(1, n + 1)]
    
    # Redondeamos para evitar problemas de precisión decimal en la vista
    menores = [round(float(m), 4) for m in menores]
    
    pos_todos = all(m > 1e-9 for m in menores)
    # Patrón: Delta1 < 0, Delta2 > 0, Delta3 < 0...
    alterna = all(menores[i] * ((-1)**(i+1)) < -1e-9 for i in range(n))
    
    if pos_todos:
        res = "Mínimo Local"
    elif alterna:
        res = "Máximo Local"
    else:
        res = "Indefinida (Punto de Silla)"
        
    return res, menores

def obtener_menores_sylvester(H):
    """Calcula los menores principales para el criterio de Sylvester."""
    return [np.linalg.det(H[:k, :k]) for k in range(1, H.shape[0] + 1)]