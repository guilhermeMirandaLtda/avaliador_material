import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """Carrega os dados do arquivo Excel."""
    data = pd.read_excel(file_path)
    return data

def perform_descriptive_analysis(data):
    """Realiza análise descritiva básica dos dados."""
    # Contagem de itens únicos
    unique_items_count = data['TEXTO'].nunique()
    
    # Soma de quantidades por item
    sum_quantities_by_item = data.groupby('TEXTO')['QUANTIDADE'].sum().sort_values(ascending=False)
    
    # Estatísticas descritivas das quantidades
    quantity_descriptive_stats = data['QUANTIDADE'].describe()
    
    return unique_items_count, sum_quantities_by_item, quantity_descriptive_stats

def plot_data(data):
    # Preparando os dados para os gráficos
    sum_quantities_by_item = data.groupby('TEXTO')['QUANTIDADE'].sum().reset_index()
    
    # Configurações básicas dos gráficos
    sns.set(style="whitegrid")
    
    # Criando o histograma de Quantidades
    plt.figure(figsize=(12, 6))
    sns.histplot(data['QUANTIDADE'], kde=False, bins=10, color='skyblue')
    plt.title('Distribuição de Quantidades')
    plt.xlabel('Quantidade')
    plt.ylabel('Frequência')
    plt.show()

    # Criando o gráfico de barras das quantidades por item
    plt.figure(figsize=(12, 6))
    sns.barplot(x='QUANTIDADE', y='TEXTO', data=sum_quantities_by_item, palette='viridis')
    plt.title('Quantidade por Item')
    plt.xlabel('Quantidade')
    plt.ylabel('Item')
    plt.show()

