import numpy as np
import plotly.graph_objects as go

def generar_grafico(f_num, constraints, p_opt, z_opt, limite_x, limite_y, resolucion):
    x_v = np.linspace(0, limite_x, resolucion)
    y_v = np.linspace(0, limite_y, resolucion)
    X, Y = np.meshgrid(x_v, y_v)
    
    fig = go.Figure()

    # Dibujar restricciones
    for i, r in enumerate(constraints):
        if r['b'] != 0:
            y_plot = (r['c'] - r['a']*x_v) / r['b']
            mask = (y_plot >= 0) & (y_plot <= limite_y)
            fig.add_trace(go.Scatter(x=x_v[mask], y=y_plot[mask], name=f"R{i+1}", mode='lines'))
        elif r['a'] != 0:
            x_const = r['c'] / r['a']
            if 0 <= x_const <= limite_x:
                fig.add_vline(x=x_const, line_dash="dash", line_color="orange")

    # Dibujar contorno
    Z = f_num(X, Y)
    fig.add_trace(go.Contour(x=x_v, y=y_v, z=Z, contours_coloring='lines', opacity=0.4, 
                             showscale=True, colorbar=dict(title="Z", x=1.05)))

    # Dibujar el punto óptimo
    if p_opt is not None:
        fig.add_trace(go.Scatter(x=[p_opt[0]], y=[p_opt[1]], mode='markers+text',
                                 text=[f"ÓPTIMO: {z_opt:,.0f}"], textposition="top center",
                                 marker=dict(size=15, color='red', symbol='star'), name="Óptimo"))

    fig.update_layout(
        xaxis=dict(range=[0, limite_x], title="Eje X"),
        yaxis=dict(range=[0, limite_y], title="Eje Y"),
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        legend=dict(orientation="h", y=1.1)
    )
    
    return fig