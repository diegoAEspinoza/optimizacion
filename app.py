import streamlit as st

# Importamos las funciones desde nuestros otros archivos
from ui import configurar_interfaz, mostrar_resultados
from solver import calcular_optimo
from plotter import generar_grafico

def main():
    f_str, objetivo, restr_list, limite_x, limite_y, resolucion = configurar_interfaz()

    try:
        f_num, constraints, vertices_factibles, p_opt, z_opt = calcular_optimo(f_str, restr_list, objetivo)

        fig = generar_grafico(f_num, constraints, p_opt, z_opt, limite_x, limite_y, resolucion)
        st.plotly_chart(fig, width='stretch')

        mostrar_resultados(objetivo, p_opt, z_opt, vertices_factibles)

    except Exception as e:
        st.error(f"Error en el procesamiento de los datos: Verifique sus ecuaciones. Detalle técnico: {e}")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()