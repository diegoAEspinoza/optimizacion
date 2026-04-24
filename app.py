#app.py
import streamlit as st
import sympy as sp
import numpy as np
from solver import hallar_puntos_criticos
from logic import clasificar_autovalores, clasificar_sylvester
from plots import generar_grafica_completa

# Configuración visual de la página
st.set_page_config(page_title="Hessian Master", layout="wide", page_icon="🧮")

# CSS personalizado para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("Analizador de Superficies y Puntos Críticos")
st.divider()


with st.sidebar:
    st.header("Configuración")
    formula_input = st.text_input("Función f(x, y, ...):", "x**3 + y**3 - 3*x*y")
    st.caption("Ejemplo: x**3 + y**3 - 3*x*y")


try:
    puntos_vis, puntos_calc, H_sym, vars_list, grad_dict, segundas_dict = hallar_puntos_criticos(formula_input)
    f_sym = sp.sympify(formula_input)

    col_left, col_right = st.columns([1, 1.5])

    with col_left:
        st.subheader("Análisis Simbólico")
        st.latex(f"f = {sp.latex(f_sym)}")
        
        # --- SECCIÓN DE DERIVADAS POR ESCRITO ---
        with st.expander("Ver derivadas paso a paso", expanded=False):
            st.write("**1. Primeras derivadas (Gradiente):**")
            for nombre, deriv in grad_dict.items():
                st.latex(f"{nombre} = {sp.latex(deriv)}")
            
            st.write("**2. Segundas derivadas (Hessiana):**")
            for nombre, deriv in segundas_dict.items():
                st.latex(f"{nombre} = {sp.latex(deriv)}")
        
        st.write("**Matriz Hessiana Final:**")
        st.latex(sp.latex(H_sym))
        st.divider()
        st.subheader("Resumen de Puntos Críticos")
        for i, p in enumerate(puntos_vis):
            valor_f = p.get("f_objetivo", "N/A")
            coords = {k: round(v, 4) if isinstance(v, (float, int)) else v 
                      for k, v in p.items() if k != "f_objetivo"}
            
            info_punto = f"Punto {i+1}: {coords}\nValor f(P): {valor_f}"
            
            with st.container():
                st.code(info_punto, language="python")

    with col_right:
        # Pestañas de resultados
        tab_graf, tab_eig, tab_syl = st.tabs(["Gráfica", "Autovalores", "Sylvester"])

        with tab_graf:
            if len(vars_list) <= 2:
                fig = generar_grafica_completa(f_sym, vars_list, puntos_vis)
                if fig:
                    st.plotly_chart(fig, width='stretch')
            else:
                st.warning("La visualización solo está disponible para 1 o 2 variables.")

        with tab_eig:
            for i, p in enumerate(puntos_calc):
                H_eval = np.array(H_sym.subs(p)).astype(np.float64)
                res, vals = clasificar_autovalores(H_eval)
                with st.expander(f"Punto {i+1}: {puntos_vis[i]}", expanded=True):
                    st.markdown(f"**Resultado:** `{res}`")
                    st.write(fr"$\lambda = {vals}$")

        with tab_syl:
            for i, p in enumerate(puntos_calc):
                H_eval = np.array(H_sym.subs(p)).astype(np.float64)
                res, mens = clasificar_sylvester(H_eval)
                with st.expander(f"Punto {i+1}: {puntos_vis[i]}", expanded=True):
                    st.markdown(f"**Resultado:** `{res}`")
                    deltas_latex = ", ".join([f"\\Delta_{{{j+1}}} = {v}" for j, v in enumerate(mens)])
                    st.latex(deltas_latex)

except Exception as e:
    st.error(f"Ocurrió un error: {e}")