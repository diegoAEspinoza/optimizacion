#plots.py
import numpy as np
import plotly.graph_objects as go
import sympy as sp

def generar_grafica_completa(f_sym, vars_sym, puntos_criticos):
    n = len(vars_sym)
    
    # CASO 1: Una sola variable (Grafica 2D)
    if n == 1:
        x_sym = vars_sym[0]
        f_num = sp.lambdify(x_sym, f_sym, 'numpy')
        
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f_num(x_vals)
        
        fig = go.Figure()
        # Curva de la función
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='royalblue', width=3)))
        
        # Puntos críticos
        for p in puntos_criticos:
            px = float(p.get(str(x_sym), 0))
            py = float(f_num(px))
            fig.add_trace(go.Scatter(x=[px], y=[py], mode='markers', 
                                   marker=dict(size=12, color='red', symbol='diamond'),
                                   name=f"Crítico x={px:.2f}"))
        
        fig.update_layout(title="Visualización 2D", xaxis_title=str(x_sym), yaxis_title="f(x)")
        return fig

    # CASO 2: Dos variables (Grafica 3D)
    elif n == 2:
        x_sym, y_sym = vars_sym
        f_num = sp.lambdify((x_sym, y_sym), f_sym, 'numpy')
        
        x_vals = np.linspace(-5, 5, 100)
        y_vals = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f_num(X, Y)
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)])
        
        for p in puntos_criticos:
            px = float(p.get(str(x_sym), 0))
            py = float(p.get(str(y_sym), 0))
            pz = float(f_num(px, py))
            fig.add_trace(go.Scatter3d(x=[px], y=[py], z=[pz], mode='markers',
                                     marker=dict(size=8, color='red')))
        
        fig.update_layout(title="Visualización 3D", scene=dict(xaxis_title=str(x_sym), yaxis_title=str(y_sym)))
        return fig

    return None