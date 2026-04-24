import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from itertools import combinations

st.set_page_config(page_title="Solver Lineal Dinámico", layout="wide")

st.title("Optimización Lineal Multirestricción 🚀")
st.write("Calcula la región factible y el punto óptimo para cualquier número de restricciones lineales.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("1. Función Objetivo")
    # Definimos las variables fijas para el análisis
    var_x, var_y = "x", "y"
    f_str = st.text_input("Z = f(x, y):", "36000*x + 36000*y")
    objetivo = st.radio("Objetivo:", ["Minimizar", "Maximizar"])
    
    st.header("2. Restricciones")
    st.info("Escribe la parte izquierda de ax + by ≥ c")
    num_restr = st.number_input("¿Cuántas restricciones tienes?", min_value=1, max_value=20, value=3)
    
    restr_list = []
    for i in range(int(num_restr)):
        st.markdown(f"**Restricción {i+1}**")
        col_a, col_b = st.columns(2)
        with col_a:
            exp = st.text_input(f"g(x,y) {i+1}", "10*x + 20*y", key=f"exp_{i}")
        with col_b:
            val = st.number_input(f"Valor c {i+1}", value=800, key=f"val_{i}")
        restr_list.append({'expr': exp, 'c': val})

    st.header("3. Visualización")
    col_x, col_y = st.columns(2)
    with col_x:
        limite_x = st.slider("Límite eje X", 10, 2000, 200)
    with col_y:
        limite_y = st.slider("Límite eje Y", 10, 2000, 200)
    
    resolucion = st.select_slider("Resolución de gráfico", options=[50, 100, 200], value=100)

# --- PROCESAMIENTO MATEMÁTICO ---
x_s, y_s = sp.symbols('x y')
try:
    f_sym = sp.sympify(f_str)
    f_num = sp.lambdify((x_s, y_s), f_sym, 'numpy')

    constraints = []
    for r in restr_list:
        e = sp.sympify(r['expr'])
        a = float(e.coeff(x_s))
        b = float(e.coeff(y_s))
        constraints.append({'a': a, 'b': b, 'c': r['c']})

    # --- CÁLCULO DE VÉRTICES ---
    vertices = []
    # Intersecciones entre restricciones
    for r1, r2 in combinations(constraints, 2):
        A = np.array([[r1['a'], r1['b']], [r2['a'], r2['b']]], dtype=float)
        B = np.array([r1['c'], r2['c']], dtype=float)
        try:
            interseccion = np.linalg.solve(A, B)
            if interseccion[0] >= 0 and interseccion[1] >= 0:
                vertices.append(interseccion)
        except np.linalg.LinAlgError:
            continue 

    # Intersecciones con ejes (x=0 y y=0)
    for r in constraints:
        if r['a'] != 0: vertices.append(np.array([r['c']/r['a'], 0]))
        if r['b'] != 0: vertices.append(np.array([0, r['c']/r['b']]))
    
    # Origen (siempre es un vértice potencial en primer cuadrante)
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
            # Evitar duplicados
            if not any(np.allclose(v, vf) for vf in vertices_factibles):
                vertices_factibles.append(v)

    # --- GRÁFICO ---
    x_v = np.linspace(0, limite_x, resolucion)
    y_v = np.linspace(0, limite_y, resolucion)
    X, Y = np.meshgrid(x_v, y_v)
    
    fig = go.Figure()

    for i, r in enumerate(constraints):
        if r['b'] != 0:
            y_plot = (r['c'] - r['a']*x_v) / r['b']
            mask = (y_plot >= 0) & (y_plot <= limite_y)
            fig.add_trace(go.Scatter(x=x_v[mask], y=y_plot[mask], name=f"R{i+1}", mode='lines'))
        elif r['a'] != 0:
            x_const = r['c'] / r['a']
            if 0 <= x_const <= limite_x:
                fig.add_vline(x=x_const, line_dash="dash", line_color="orange")

    Z = f_num(X, Y)
    fig.add_trace(go.Contour(x=x_v, y=y_v, z=Z, contours_coloring='lines', opacity=0.4, 
                             showscale=True, colorbar=dict(title="Z", x=1.05)))

    # Punto óptimo
    if vertices_factibles:
        puntos = np.array(vertices_factibles)
        valores_z = [float(f_sym.subs({x_s: p[0], y_s: p[1]})) for p in puntos]
        
        idx_opt = np.argmin(valores_z) if objetivo == "Minimizar" else np.argmax(valores_z)
        p_opt = puntos[idx_opt]
        z_opt = valores_z[idx_opt]

        fig.add_trace(go.Scatter(x=[p_opt[0]], y=[p_opt[1]], mode='markers+text',
                                 text=[f"ÓPTIMO: {z_opt:,.0f}"], textposition="top center",
                                 marker=dict(size=15, color='red', symbol='star')))

    fig.update_layout(
        xaxis=dict(range=[0, limite_x], title="Eje X"),
        yaxis=dict(range=[0, limite_y], title="Eje Y"),
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        legend=dict(orientation="h", y=1.1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- RESULTADOS ---
    if vertices_factibles:
        st.success(f"### Resultado Final ({objetivo})")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Variable X", f"{p_opt[0]:.2f}")
        col_res2.metric("Variable Y", f"{p_opt[1]:.2f}")
        col_res3.metric("Valor Z", f"{z_opt:,.2f}")
    else:
        st.error("No se encontró una región factible. El polígono de soluciones está vacío.")

except Exception as e:
    st.error(f"Error en el procesamiento: {e}")