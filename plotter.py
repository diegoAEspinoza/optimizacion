# plotter.py
import numpy as np
import plotly.graph_objects as go

def generar_grafico(f_num, constraints, p_opt, z_opt, limite_x, limite_y, resolucion, vertices_factibles):
    x_v = np.linspace(0, limite_x, resolucion)
    y_v = np.linspace(0, limite_y, resolucion)
    X, Y = np.meshgrid(x_v, y_v)
    
    fig = go.Figure()

    # 1. Dibujar Región Factible (Sombreado)
    if vertices_factibles and len(vertices_factibles) > 2:
        v_x = [v[0] for v in vertices_factibles]
        v_y = [v[1] for v in vertices_factibles]
        v_x.append(v_x[0])
        v_y.append(v_y[0])
        
        fig.add_trace(go.Scatter(
            x=v_x, y=v_y, 
            fill="toself", 
            fillcolor='rgba(0, 255, 0, 0.2)', 
            line=dict(color='rgba(255,255,255,0)'),
            name="Región Factible",
            hoverinfo='skip' # Para que no interfiera con los puntos
        ))

    # 2. Dibujar restricciones (Líneas)
    for i, r in enumerate(constraints):
        if r['b'] != 0:
            y_plot = (r['c'] - r['a']*x_v) / r['b']
            mask = (y_plot >= 0) & (y_plot <= limite_y)
            fig.add_trace(go.Scatter(x=x_v[mask], y=y_plot[mask], name=f"R{i+1}", mode='lines'))
        elif r['a'] != 0:
            x_const = r['c'] / r['a']
            if 0 <= x_const <= limite_x:
                fig.add_vline(x=x_const, line_dash="dash", line_color="orange")

    # 3. Dibujar contorno de la función objetivo
    Z = f_num(X, Y)
    fig.add_trace(go.Contour(x=x_v, y=y_v, z=Z, contours_coloring='lines', opacity=0.4, 
                             showscale=True, colorbar=dict(title="Z", x=1.05)))
    
    v_otros_x = [v[0] for v in vertices_factibles]
    v_otros_y = [v[1] for v in vertices_factibles]

    fig.add_trace(go.Scatter(
        x=v_otros_x, y=v_otros_y,
        mode='markers',
        marker=dict(size=13, color='orange', opacity=0.6),
        name="Vértices",
        hovertemplate="X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>"
    ))

    # 4. Dibujar el punto óptimo (Estrella Roja)
    if p_opt is not None:
        fig.add_trace(go.Scatter(
            x=[p_opt[0]], y=[p_opt[1]], 
            mode='markers+text',
            text=["ÓPTIMO"], 
            textposition="top center",
            marker=dict(size=18, color='red', symbol='star', line=dict(width=2, color='black')), 
            name="Punto Óptimo"
        ))


    fig.update_layout(
        xaxis=dict(range=[0, limite_x], title="Eje X"),
        yaxis=dict(range=[0, limite_y], title="Eje Y"),
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        legend=dict(orientation="h", y=1.1)
    )
    
    return fig