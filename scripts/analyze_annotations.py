import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import squarify # Importe a biblioteca squarify

def analyze_pfam_annotations(hmmsearch_file, output_dir, evalue_threshold=1e-5):
    """
    Analisa os resultados do hmmsearch para anotações Pfam, 
    imprimindo todos os hits para análise detalhada e gerando gráfico (treemap).

    Args:
        hmmsearch_file (str): Caminho para o arquivo de saída hmmsearch (.domtblout).
        output_dir (str): Diretório para salvar os resultados da análise (gráficos).
        evalue_threshold (float): Limite de E-value para considerar uma anotação confiável.
    """
    print(f"\n--- Lendo e analisando o arquivo: {hmmsearch_file} ---")

    os.makedirs(output_dir, exist_ok=True)

    data_raw = [] # Para armazenar todos os hits, brutos
    data_filtered = [] # Para armazenar apenas os hits filtrados

    try:
        with open(hmmsearch_file, 'r') as f:
            lines = f.readlines()

        # Filtrar linhas de cabeçalho e linhas em branco
        parsed_lines = [line.strip() for line in lines if not line.startswith('#') and line.strip()]

        print("\n--- Processando Hits Brutos ---")
        for line_num, line in enumerate(parsed_lines, 1):
            parts = line.split(maxsplit=22) 

            if len(parts) < 22: 
                # print(f"ATENÇÃO: Linha {line_num} mal formatada (menos de 22 campos fixos), pulando: {line}")
                continue

            query_id = parts[0]
            pfam_family_name = parts[3] 
            pfam_accession = parts[4]
            
            try:
                e_value = float(parts[11])
            except ValueError:
                # print(f"ATENÇÃO: Linha {line_num} com E-value inválido '{parts[11]}', pulando: {line}")
                continue
            
            try:
                score = float(parts[12])
            except ValueError:
                # print(f"ATENÇÃO: Linha {line_num} com Score inválido '{parts[12]}', pulando: {line}")
                continue

            full_line_description = parts[22] if len(parts) > 22 else ""

            hit_info = [query_id, pfam_family_name, pfam_accession, e_value, score, full_line_description]
            data_raw.append(hit_info)
            
            # Imprime cada hit bruto lido para depuração
            # print(f"Raw Hit {line_num}: Proteína={query_id}, Família={pfam_family_name}, E-value={e_value:.2e}, Score={score:.1f}")

            # Aplica o filtro de E-value
            if e_value < evalue_threshold:
                data_filtered.append(hit_info)

    except FileNotFoundError:
        print(f"Erro: O arquivo {hmmsearch_file} não foi encontrado. Verifique o caminho.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler ou processar o arquivo: {e}")
        print("Verifique se o arquivo .domtblout está no formato esperado ou se a pasta de entrada existe.")
        return

    df_raw = pd.DataFrame(data_raw, columns=[
        'query_id', 'pfam_family_name', 'pfam_accession',
        'e_value', 'score', 'full_line_description'
    ])
    print(f"\nTotal de hits brutos lidos: {len(df_raw)}")

    df_filtered = pd.DataFrame(data_filtered, columns=df_raw.columns)
    print(f"Total de hits após filtro (E-value < {evalue_threshold}): {len(df_filtered)}")

    if df_filtered.empty:
        print("Nenhuma anotação confiável encontrada após o filtro de E-value. Tente relaxar o 'evalue_threshold'.")
        return

    df_unique_annotations = df_filtered.drop_duplicates(subset=['query_id', 'pfam_family_name'])
    pfam_counts = df_unique_annotations['pfam_family_name'].value_counts()
    
    print(f"\n--- Anotações Únicas e Confiáveis (que passaram pelo filtro) ---")
    print(f"Total de proteínas com anotações únicas e confiáveis: {len(df_unique_annotations)}")
    print("\nDetalhes das Anotações Únicas e Confiáveis:")
    for index, row in df_unique_annotations.iterrows():
        print(f"  Proteína: {row['query_id']}, Família Pfam: {row['pfam_family_name']}, E-value: {row['e_value']:.2e}")

    if pfam_counts.empty:
        print("Nenhuma família Pfam única e confiável para plotar.")
        return

    print("\n--- Frequência de Famílias Pfam (Todas as encontradas após filtro) ---")
    print(pfam_counts.to_string()) 

    # --- Gerar Treemap ---
    print(f"\n--- Gerando Treemap de Famílias Pfam ---")
    
    # As contagens serão os tamanhos dos retângulos
    sizes = pfam_counts.values 
    # Os labels serão os nomes das famílias Pfam
    labels = [f'{name}\n({count})' for name, count in pfam_counts.items()]

    plt.figure(figsize=(14, 10)) # Aumentar o tamanho para o treemap
    squarify.plot(sizes=sizes, label=labels, alpha=.8,
                  text_kwargs={'fontsize': 10, 'wrap': True, 'color': 'white'},
                  bar_kwargs={'edgecolor': 'white', 'linewidth': 1.5}) # Bordas brancas para clareza
    plt.title(f'Treemap das Famílias Pfam Anotadas (E-value < {evalue_threshold})', fontsize=16)
    plt.axis('off') # Remover eixos para um visual mais limpo
    
    output_plot_path = os.path.join(output_dir, 'pfam_families_treemap.png')
    plt.savefig(output_plot_path)
    print(f"Treemap salvo em: {output_plot_path}")
    plt.show()

if __name__ == "__main__":
    # --- Configurações de Caminhos ---
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Caminho de entrada para o arquivo domtblout
    hmmsearch_input_file = os.path.join(project_root, 'data', 'assembly_megahit', 'annotation_results.domtblout')
    
    # Caminho de saída para os gráficos de análise
    output_results_dir = os.path.join(project_root, 'results', 'annotation_analysis')
    
    # Definir o limite de E-value para a anotação
    # Use 0.3 para o seu exemplo original, ou 1e-5 para uma anotação mais rigorosa
    evalue_threshold_to_use = 0.3 

    # --- Execução da Análise ---
    analyze_pfam_annotations(hmmsearch_input_file, output_results_dir, evalue_threshold=evalue_threshold_to_use)