import streamlit as st


st.sidebar.image('image/author.jpg', width=150, )
st.sidebar.write("""Guilherme Miranda Costa
                 guilherme.miranda.ltda@gmail.com
                 (99)9.8121-6058
                 """)
st.sidebar.markdown('<a href="https://www.linkedin.com/in/guilherme-miranda-6657666a/" target="_blank">Linkedin</a>', unsafe_allow_html=True)


st.title('Analisador de Aderência de Materiais')

st.write("""No cenário atual da construção rede Elétricas, a eficiência na gestão de  materiais é um fator crítico que impacta diretamente na viabilidade, custo e sucesso dos projetos. 

Frente a essa necessidade, desenvolvemos um sistema avançado para análise de cobertura de materiais, visando otimizar a distribuição e alocação de materiais para várias obras simultaneamente. 

O objetivo deste projeto é maximizar a utilização dos recursos disponíveis, minimizando desperdícios e garantindo que todas as obras tenham suas necessidades de material adequadamente atendidas.""")
st.image('image/cover.png')

st.write('Construído orgulhosamente por Guilherme Miranda!')

st.subheader('Desafio')
st.markdown("""
O principal desafio enfrentado pelas Distribuidora de Energia Elétrica é garantir que cada projeto tenha os materiais necessários disponíveis quando necessário, sem excesso de estoque. 
            
A complexidade da gestão de materiais se intensifica com o número crescente de projetos simultâneos, cada um com suas especificidades e cronogramas. """)