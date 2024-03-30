import streamlit as st
import pandas as pd
from io import BytesIO

# Função para converter um DataFrame para Excel na memória
def to_excel(df):
    output = BytesIO()
    # Usar 'with' garante que o writer seja fechado corretamente após seu uso
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        # Não é necessário chamar writer.save() quando se usa 'with'
    output.seek(0)  # Importante: move o cursor para o início do stream
    return output.getvalue()

# Criar DataFrames de exemplo
df1 = pd.DataFrame({
    'CODIGO':['1010','2020','3030',],
    'TEXTO': ['POSTE','TRAFO','CABO',], 
    'UN':['UN','UN','M',], 
    'QUANTIDADE':[10,7,1500,]})
df2 = pd.DataFrame({
    'IDENTIFICADOR': ['OBRA 01','OBRA 01','OBRA 01','OBRA 02','OBRA 02','OBRA 02','OBRA 03','OBRA 03','OBRA 04','OBRA 05','OBRA 05','OBRA 05','OBRA 06','OBRA 06','OBRA 06','OBRA 07','OBRA 07','OBRA 07','OBRA 08','OBRA 08','OBRA 08','OBRA 09','OBRA 09','OBRA 10','OBRA 10','OBRA 10',], 
    'CODIGO':['1010','2020','3030','1010','2020','3030','1010','3030','3030','1010','2020','3030','1010','2020','3030','1010','2020','3030','1010','2020','3030','1010','2020','1010','2020','3030'],
    'DESCRICAO': ['POSTE','TRAFO','CABO','POSTE','TRAFO','CABO','POSTE','CABO','CABO','POSTE','TRAFO','CABO','POSTE','TRAFO','CABO','POSTE','TRAFO','CABO','POSTE','TRAFO','CABO','POSTE','TRAFO','POSTE','TRAFO','CABO',], 
    'UN':['UN','UN','M','UN','UN','M','UN','M','M','UN','UN','M','UN','UN','M','UN','UN','M','UN','UN','M','UN','UN','UN','UN','M',], 
    'QUANTIDADE':[3,1,150,5,4,300,1,50,100,7,3,400,8,4,500,4,2,100,2,1,50,1,1,1,1,50,]})

# Converter DataFrames para Excel
excel_file1 = to_excel(df1)
excel_file2 = to_excel(df2)

# Criar botões de download
st.download_button(label='Planilha Modelo Depósito',
                   data=excel_file1,
                   file_name='Deposito.xlsx',
                   mime='application/vnd.ms-excel')

st.download_button(label='Planilha Modelo Obras',
                   data=excel_file2,
                   file_name='Obras.xlsx',
                   mime='application/vnd.ms-excel')