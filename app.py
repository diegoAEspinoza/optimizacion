#app.py
import streamlit as st
from ui import configurar_interfaz, mostrar_resultados
from solver import calcular_optimo
from plotter import generar_grafico

def main():
    f_str, objetivo, restr_list, limite_x, limite_y, resolucion = configurar_interfaz()

    try:
        f_num, constraints, vertices_factibles, p_opt, z_opt, lista_errores, puntos_tabla = calcular_optimo(f_str, restr_list, objetivo)

        if lista_errores:
            for err in lista_errores:
                st.warning(err)

        fig = generar_grafico(f_num, constraints, p_opt, z_opt, limite_x, limite_y, resolucion, vertices_factibles)
        st.plotly_chart(fig, width='stretch')

        mostrar_resultados(objetivo, p_opt, z_opt, vertices_factibles, puntos_tabla)

    except Exception as e:
        st.error(f"Error en el procesamiento de los datos: Verifique sus ecuaciones. Detalle técnico: {e}")

if __name__ == "__main__":
    main()