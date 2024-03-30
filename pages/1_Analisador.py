# pages/1_Analisador.py
import streamlit as st 
import pandas as pd
from controllers.rules_handler import RulesHandler

st.set_page_config(layout="wide")

# Título do aplicativo
st.title('Analisador de Aderência de Materiais para Obras')


# Upload dos arquivos Excel
uploaded_file_deposito = st.sidebar.file_uploader("Escolha o arquivo Excel do Depósito", type=['xlsx'])
uploaded_file_obras = st.sidebar.file_uploader("Escolha o arquivo Excel das Obras", type=['xlsx'])


# Verificação e leitura dos arquivos
if uploaded_file_deposito is not None and uploaded_file_obras is not None:
    # Leitura dos arquivos Excel
    try:
        df_storage = pd.read_excel(uploaded_file_deposito)
        df_construction  = pd.read_excel(uploaded_file_obras)
        

        analy1 = st.sidebar.checkbox('Análise da Cobertura', value=False)
        if analy1:
            handler = RulesHandler(df_storage, df_construction)
            

            handler = RulesHandler(df_storage, df_construction)
            coverage_df = handler.assess_material_coverage()
            st.write("COBERTURA 100% DOS MATERIAIS")
            coverage_df
            st.download_button(label='Obras Total',
                   data=coverage_df,
                   file_name='Obras_Total.xlsx',
                   mime='application/vnd.ms-excel')

            # Agora, calcular a cobertura parcial para as obras não totalmente cobertas e atualizar o estoque
            partial_coverage_df = handler.calculate_partial_coverage()
            st.write(" COBERTURA PARCIAL DOS MATERIAIS")
            partial_coverage_df
            st.download_button(label='Obras Parcial',
                   data=partial_coverage_df,
                   file_name='Obras_Parcial.xlsx',
                   mime='application/vnd.ms-excel')

            # st.write("Material Atendido:")
            handler.assess_material_coverage()
            st.write("MATERIAL ATENDIDO")
            st.dataframe(handler.df_coverage_analysis)
            st.download_button(label='Material',
                   data=handler.df_coverage_analysis,
                   file_name='Material.xlsx',
                   mime='application/vnd.ms-excel')

     


        
        # Aqui você pode adicionar a lógica para análise dos dados
        
    except Exception as e:
        st.error(f"Erro ao ler os arquivos: {e}")
else:
    st.info('Por favor, faça upload dos arquivos Excel do Depósito e das Obras para continuar.')


