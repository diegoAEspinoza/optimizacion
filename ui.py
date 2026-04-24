import streamlit as st

def configurar_interfaz():
    st.set_page_config(page_title="Solver Lineal Dinámico", layout="wide")
    st.title("Optimización Lineal Multirestricción 🚀")
    st.write("Calcula la región factible y el punto óptimo para cualquier número de restricciones lineales.")

    with st.sidebar:
        st.header("1. Función Objetivo")
        f_str = st.text_input("Z = f(x, y):", "36000*x + 36000*y")
        objetivo = st.radio("Objetivo:", ["Minimizar", "Maximizar"])
        
        st.header("2. Restricciones")
        st.info("Escribe la parte izquierda de ax + by ≥ c")
        num_restr = st.number_input("¿Cuántas restricciones tienes?", min_value=1, max_value=20, value=1)
        
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

    return f_str, objetivo, restr_list, limite_x, limite_y, resolucion

def mostrar_resultados(objetivo, p_opt, z_opt, vertices_factibles):
    if vertices_factibles and p_opt is not None:
        st.success(f"### Resultado Final ({objetivo})")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Variable X", f"{p_opt[0]:.2f}")
        col_res2.metric("Variable Y", f"{p_opt[1]:.2f}")
        col_res3.metric("Valor Z", f"{z_opt:,.2f}")
    else:
        st.error("No se encontró una región factible. El polígono de soluciones está vacío.")