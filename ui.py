#ui.py
import streamlit as st

def configurar_interfaz():
    st.set_page_config(page_title="Solver Lineal Dinámico", layout="wide")
    st.title("Optimización Lineal Multirestricción")
    st.write("Calcula la región factible y el punto óptimo para cualquier número de restricciones lineales.")

    with st.sidebar:
        st.header("1. Función Objetivo")
        f_str = st.text_input("Z = f(x, y):", "36000*x + 36000*y")
        objetivo = st.radio("Objetivo:", ["Minimizar", "Maximizar"])
        
        st.header("2. Restricciones")
        st.info("Escribe la restricción completa (ej. 10*x + 20*y <= 40, x + y = 10)")
        num_restr = st.number_input("¿Cuántas restricciones tienes?", min_value=0, max_value=20, value=3)
        defaults = [
            "10*x + 20*y >= 800",
            "30*x + 20*y >= 1600",
            "15*x + 70*y >= 1800"
        ]
        restr_list = []
        for i in range(int(num_restr)):
            default_val = defaults[i] if i < len(defaults) else ""
    
            val = st.text_input(
                f"Restricción {i+1}:", 
                value=default_val,  
                key=f"r_{i}"
            )
           
            if val:
                restr_list.append(val)
            else:
                val = []

        st.header("3. Visualización")
        col_x, col_y = st.columns(2)
        with col_x:
            limite_x = st.number_input("Límite eje X", min_value=1, max_value=10000, value=125, step=10)
        with col_y:
            limite_y = st.number_input("Límite eje Y", min_value=1, max_value=10000, value=90, step=10)
        
        resolucion = st.select_slider("Resolución de gráfico", options=[50, 100, 200], value=100)

    return f_str, objetivo, restr_list, limite_x, limite_y, resolucion

def mostrar_resultados(objetivo, p_opt, z_opt, vertices_factibles, puntos_tabla):
    if vertices_factibles and p_opt is not None:
        st.success(f"### Resultado Final ({objetivo})")
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Variable X", f"{p_opt[0]:.2f}")
        col_res2.metric("Variable Y", f"{p_opt[1]:.2f}")
        col_res3.metric("Valor Z", f"{z_opt:,.2f}")

        st.write("---")
        st.subheader("Análisis de Vértices de la Región Factible")
        st.markdown(f"La siguiente tabla muestra todos los puntos esquina evaluados. El **{objetivo}** se encuentra resaltado en la primera fila.")
        
        # Mostramos la tabla
        st.dataframe(
            puntos_tabla, 
            width='stretch', 
            hide_index=True
        )
        
    else:
        st.error("No se encontró una región factible. El polígono de soluciones está vacío.")