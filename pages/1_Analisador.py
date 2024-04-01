# pages/1_Analisador.py
import streamlit as st 
import pandas as pd
from controllers.rules_handler import RulesHandler
from io import BytesIO

st.set_page_config(layout="wide")

def to_excel(df):
    """
    Função para converter um DataFrame para um arquivo Excel na memória,
    retornando o conteúdo binário sem chamar .save() explicitamente.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.getvalue()

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
        check_storage = st.sidebar.checkbox('Depósito', value=False)
        if check_storage:
            df_storage.dtype()
            df_storage
            
            
        df_construction  = pd.read_excel(uploaded_file_obras)
        check_construction  = st.sidebar.checkbox('Obras', value=False)
        if check_storage:
            df_construction.dtype()
            df_construction
        
        analy1 = st.sidebar.checkbox('Análise da Cobertura', value=False)
        if analy1:
            handler = RulesHandler(df_storage, df_construction)
            

            handler = RulesHandler(df_storage, df_construction)
            coverage_df = handler.assess_material_coverage()
            st.subheader("1. COBERTURA 100% DOS MATERIAIS")
            st.write(''' 
Esta seção identifica obras com todas as necessidades de materiais completamente atendidas pelo estoque atual. 
A análise visa otimizar o uso de materiais e suportar uma gestão de projeto eficiente.
''')
            coverage_df
            excel_data = to_excel(coverage_df)
            st.download_button(label='Obras Total',
                   data=excel_data,
                   file_name='Obras_Total.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            st.divider()
            # Agora, calcular a cobertura parcial para as obras não totalmente cobertas e atualizar o estoque
            partial_coverage_df = handler.calculate_partial_coverage()
            st.subheader("2. COBERTURA PARCIAL DOS MATERIAIS")
            st.write(''' 
Esta parte aborda as obras que não podem ser totalmente supridas com o inventário existente. 
''')
            partial_coverage_df
            excel_data = to_excel(partial_coverage_df)

            st.download_button(label='Obras Parcial',
                   data=excel_data,
                   file_name='Obras_Parcial.xlsx',
                   mime='application/vnd.ms-excel')

            st.divider()
            # st.write("Material Atendido:")
            handler.assess_material_coverage()
            st.subheader("3. MATERIAL ATENDIDO")
            st.write(''' 
Este tópico detalha a quantidade e porcentagem de materiais que foram efetivamente alocados para cada obra, refletindo o sucesso na cobertura das necessidades de construção com o estoque disponível. 
''')
            st.dataframe(handler.df_coverage_analysis)
            excel_data = to_excel(handler.df_coverage_analysis)
            st.download_button(label='Material',
                   data=excel_data,
                   file_name='Material.xlsx',
                   mime='application/vnd.ms-excel')

     


        
        # Aqui você pode adicionar a lógica para análise dos dados
        
    except Exception as e:
        st.error(f"Erro ao ler os arquivos: {e}")
else:
    st.info('Por favor, faça upload dos arquivos Excel do Depósito e das Obras para continuar.')


