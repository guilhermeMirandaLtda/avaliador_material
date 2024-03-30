#controllers/rules_handler.py
import pandas as pd

class RulesHandler:
    def __init__(self, df_storage, df_construction):
        # Assegurando os tipos corretos no DataFrame df_storage
        self.df_storage = df_storage.astype({
            'CODIGO': 'string',
            'TEXTO': 'string',
            'UN': 'string',
            'QUANTIDADE': 'float'
        })
        
        # Assegurando os tipos corretos no DataFrame df_construction
        self.df_construction = df_construction.astype({
            'IDENTIFICADOR': 'string',
            'CODIGO': 'string',
            'DESCRICAO': 'string',
            'UN': 'string',
            'QUANTIDADE': 'float'
        })

        # Criar cópias do df_construction para análise de cobertura e atendimento
        self.df_coverage_analysis = self.df_construction.copy()
        self.df_coverage_analysis['QUANTIDADE_ATENDIDA'] = 0.0
        self.df_coverage_analysis['PORCENTAGEM_ATENDIDA'] = 0.0

    def assess_material_coverage(self):
        """" Primeiro, agrupamos os dados em df_construction por 'IDENTIFICADOR' e 'CODIGO'
        e somamos as quantidades necessárias para cada grupo. Isso nos dá a quantidade total
        necessária de cada material por obra."""
        self.aggregated_construction = self.df_construction.groupby(['IDENTIFICADOR', 'CODIGO'], as_index=False)['QUANTIDADE'].sum()
        
        # Similarmente, agrupamos os dados em df_storage por 'CODIGO' e somamos as quantidades.
        # Isso nos dá a quantidade total disponível de cada material no estoque.
        self.aggregated_storage = self.df_storage.groupby('CODIGO', as_index=False)['QUANTIDADE'].sum()

        construction_coverage = {}

        # Iteramos sobre cada grupo de materiais necessários por obra.
        for identifier, group in self.aggregated_construction.groupby('IDENTIFICADOR'):
            all_materials_covered = True
            storage_updates = {}  # Use um dicionário para atualizações pendentes

            # Iteramos sobre cada material necessário para a obra atual.
            for _, row in group.iterrows():
                # Copiamos a linha correspondente do df_storage para verificar a quantidade disponível.
                material_in_storage = self.aggregated_storage[self.aggregated_storage['CODIGO'] == row['CODIGO']].copy()

                # Se a quantidade disponível for menor que a necessária, marcar como não totalmente coberto.
                if material_in_storage.empty or material_in_storage['QUANTIDADE'].values[0] < row['QUANTIDADE']:
                    all_materials_covered = False
                    break
                else:
                    # Se o material puder ser totalmente coberto, armazenamos a quantidade que será usada.
                    storage_updates[row['CODIGO']] = row['QUANTIDADE']

            # Se todos os materiais para a obra foram cobertos, marcamos como '100%' e atualizamos o estoque.
            if all_materials_covered:
                construction_coverage[identifier] = '100%'
                # Atualize o estoque somente se todos os materiais para a obra estão cobertos
                for code, quantity in storage_updates.items():
                    self.aggregated_storage.loc[self.aggregated_storage['CODIGO'] == code, 'QUANTIDADE'] -= quantity

                    # Atualiza df_coverage_analysis com a quantidade atendida e a porcentagem para obras 100% cobertas
                    self.df_coverage_analysis.loc[(self.df_coverage_analysis['IDENTIFICADOR'] == identifier) & (self.df_coverage_analysis['CODIGO'] == code), 'QUANTIDADE_ATENDIDA'] = quantity
                    self.df_coverage_analysis.loc[(self.df_coverage_analysis['IDENTIFICADOR'] == identifier) & (self.df_coverage_analysis['CODIGO'] == code), 'PORCENTAGEM_ATENDIDA'] = 100
                
            else:
                # Se algum material não puder ser totalmente coberto, marcamos a obra como '-'.
                construction_coverage[identifier] = '-'

        self.construction_coverage = construction_coverage
        
        # Finalmente, atualizamos df_storage com as quantidades restantes após tentar alocar para as obras.
        # Isso é feito para refletir as mudanças no estoque após as tentativas de cobertura.
        for code, quantity in self.aggregated_storage.iterrows():
            self.df_storage.loc[self.df_storage['CODIGO'] == quantity['CODIGO'], 'QUANTIDADE'] = quantity['QUANTIDADE']

        # Retornamos um DataFrame que mapeia cada identificador de obra para sua respectiva cobertura.
        return pd.DataFrame(list(construction_coverage.items()), columns=['IDENTIFICADOR', 'COBERTURA_MATERIAL'])
    
    def calculate_partial_coverage(self):
        # Identifica os identificadores de obras que não foram totalmente cobertos na avaliação inicial de cobertura.
        identifiers_less_than_100 = [identifier for identifier, coverage in self.construction_coverage.items() if coverage == '-']
        
        # Armazenar informações temporárias de cobertura
        temp_coverage_info = []
        
        # Primeira passagem: Calcula a cobertura potencial baseada na quantidade disponível no estoque,
        # sem ainda fazer alterações no estoque.
        for identifier in identifiers_less_than_100:
            construction_rows = self.df_construction[self.df_construction['IDENTIFICADOR'] == identifier]
            
            # Inicializa as somas de quantidades necessárias e quantidades que podem ser cobertas.
            total_needed, total_covered = 0, 0
            for index, row in construction_rows.iterrows():
                needed_quantity = row['QUANTIDADE']
                available_quantity = self.df_storage[self.df_storage['CODIGO'] == row['CODIGO']]['QUANTIDADE'].values[0]
                
                # A quantidade que pode ser coberta é o mínimo entre o necessário e o disponível.
                coverable_quantity = min(needed_quantity, available_quantity)
                total_needed += needed_quantity
                total_covered += coverable_quantity
            
            # Calcula a porcentagem de cobertura para cada obra baseada nas quantidades que podem ser cobertas.
            coverage_percent = (total_covered / total_needed) * 100 if total_needed > 0 else 0
            temp_coverage_info.append((identifier, coverage_percent))

        # Segunda passagem: Classifica as obras pela porcentagem de cobertura potencial,
        # do maior para o menor, para priorizar a alocação de recursos.
        temp_coverage_info.sort(key=lambda x: x[1], reverse=True) 
        
        # Prepara a lista final de resultados de cobertura.
        final_coverage_results = []
        for identifier, _ in temp_coverage_info:
            construction_rows = self.df_construction[self.df_construction['IDENTIFICADOR'] == identifier]
            
            total_needed, total_covered = 0, 0
            for _, row in construction_rows.iterrows():
                needed_quantity = row['QUANTIDADE']
                available_quantity = self.df_storage[self.df_storage['CODIGO'] == row['CODIGO']]['QUANTIDADE'].values[0]
                
                coverable_quantity = min(needed_quantity, available_quantity)
                if coverable_quantity > 0:
                    self.df_storage.loc[self.df_storage['CODIGO'] == row['CODIGO'], 'QUANTIDADE'] -= coverable_quantity
                    total_covered += coverable_quantity

                    # Atualiza self.df_coverage_analysis diretamente com a quantidade atendida e a porcentagem.
                # Usando .loc ao invés de .at para lidar com múltiplos índices, se necessário.
                self.df_coverage_analysis.loc[
                    (self.df_coverage_analysis['IDENTIFICADOR'] == identifier) & 
                    (self.df_coverage_analysis['CODIGO'] == row['CODIGO']), 
                    ['QUANTIDADE_ATENDIDA', 'PORCENTAGEM_ATENDIDA']
                ] = [coverable_quantity, (coverable_quantity / needed_quantity) * 100]

                
                total_needed += needed_quantity
            
            # Calcula a porcentagem real de cobertura para cada obra após a alocação de recursos,
            # com base na quantidade efetivamente coberta.
            final_coverage_percent = (total_covered / total_needed) * 100 if total_needed > 0 else 0
            final_coverage_results.append((identifier, final_coverage_percent))
        
        # Retorna um DataFrame com os identificadores das obras e suas respectivas porcentagens de cobertura real,
        # após a alocação de recursos.
        return pd.DataFrame(final_coverage_results, columns=['IDENTIFICADOR', 'COBERTURA_MATERIAL_REAL'])
   

    def normalize_and_order(self):
        # Normalizar as quantidades necessárias por obra e código
        max_qty = self.df_construction['QUANTIDADE'].max()
        min_qty = self.df_construction['QUANTIDADE'].min()
        
        # Evitar divisão por zero se todos os valores são iguais
        if max_qty == min_qty:
            self.df_construction['QUANTIDADE_NORMALIZADA'] = 1.0
        else:
            self.df_construction['QUANTIDADE_NORMALIZADA'] = (self.df_construction['QUANTIDADE'] - min_qty) / (max_qty - min_qty)

        # Filtrar obras com cobertura '-'
        identifiers_less_than_100 = self.df_construction[self.df_construction['STATUS'] == '-']['IDENTIFICADOR'].unique()
        
        # Calcular a porcentagem de atendimento com o estoque restante
        obras_atendimento = []
        for identifier in identifiers_less_than_100:
            obras = self.df_construction[self.df_construction['IDENTIFICADOR'] == identifier]
            atendimento = self._calculate_atendimento(obras)
            obras_atendimento.append((identifier, atendimento))
        
        # Ordenar as obras pela porcentagem de atendimento
        obras_atendimento.sort(key=lambda x: x[1], reverse=True)

        # Atualiza df_construction com as obras ordenadas
        sorted_identifiers = [identifier for identifier, _ in obras_atendimento]
        self.df_construction['ORDEM_ATENDIMENTO'] = self.df_construction['IDENTIFICADOR'].apply(lambda x: sorted_identifiers.index(x) if x in sorted_identifiers else -1)

        return self.df_construction

    def update_quantities_atended(self):
        # Atualiza 'QUANTIDADE_ATENDIDA' para todos os itens em df_construction baseado no estoque atual
        for idx, row in self.df_construction.iterrows():
            # Encontrar a quantidade disponível no estoque para este código específico
            available_quantity = self.df_storage[self.df_storage['CODIGO'] == row['CODIGO']]['QUANTIDADE'].values[0] if not self.df_storage[self.df_storage['CODIGO'] == row['CODIGO']]['QUANTIDADE'].empty else 0
            
            # A quantidade atendida é o mínimo entre a quantidade necessária e a quantidade disponível
            atendida = min(row['QUANTIDADE'], available_quantity)
            
            # Atualizar o DataFrame de construção com a quantidade atendida
            self.df_construction.at[idx, 'QUANTIDADE_ATENDIDA'] = atendida

        # Após atualizar 'QUANTIDADE_ATENDIDA', podemos querer ajustar 'STATUS' e outras operações conforme necessário
        # Por exemplo, ajustar o estoque em df_storage após o cálculo
        # Isso é deixado como um exercício adicional conforme suas necessidades específicas

        return self.df_construction








