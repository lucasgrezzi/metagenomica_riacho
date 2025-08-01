# Análise Metagenômica do Riacho

Este repositório contém os dados e a documentação do pipeline de análise metagenômica de uma amostra de riacho.

## Estrutura do Projeto
metagenomica_riacho/
├── data/                            # Contém dados de entrada e resultados intermediários
│   ├── assembly_megahit/            # Resultados da montagem (MEGAHIT) e predição de genes (Prodigal)
│   │   ├── annotation_results.domtblout # Saída HMMER anotada
│   │   ├── final.contigs.fa         # Contigs montadas
│   │   └── proteins.faa             # Proteínas preditas
│   ├── databases/                   # Banco de dados HMM (Pfam) e índices
│   │   └── Pfam-A.hmm               # Arquivo principal do Pfam (e seus índices .h3*)
│   ├── raw/                         # Reads FastQ brutas
│   └── trimmed_final/               # Reads FastQ após o trimming
├── results/                         # Contém os resultados finais das análises
│   ├── annotation_analysis/         # Gráficos e sumarizações da anotação Pfam (treemap)
│   ├── fastqc/                      # Relatórios FastQC para reads brutas e/ou limpas
│   └── hmm_results/                 # Resultados brutos do hmmsearch (se salvos aqui, ou linkados)
├── scripts/                         # Scripts Python para as etapas de análise
│   └── analyze_annotations.py       # Script Python para analisar e visualizar anotações Pfam
├── pipeline_commands.sh             # Arquivo com os comandos de terminal executados em cada etapa
└── README.md                        # Este arquivo de documentação

## Ferramentas Utilizadas

As seguintes ferramentas de bioinformática foram utilizadas no pipeline e devem ser instaladas (preferencialmente via Conda) em um ambiente virtual:

* **FastQC**: Controle de qualidade das reads.
* **Trimmomatic**: Remoção de adaptadores e filtragem de qualidade.
* **MEGAHIT**: Montagem de genomas metagenômicos.
* **Prodigal**: Predição de genes em sequências nucleotídicas.
* **HMMER (hmmsearch)**: Busca de domínios de proteínas usando Modelos Ocultos de Markov (HMMs).
* **Python 3**: Para scripts de análise de dados (com bibliotecas como Pandas, Matplotlib, Seaborn e Squarify).

## Configuração do Ambiente (Conda)

Para configurar o ambiente Conda com as ferramentas e bibliotecas necessárias:

```bash
# Crie o ambiente (se ainda não o fez)
conda create -n metagenomics_env python=3.9 -y

# Ative o ambiente
conda activate metagenomics_env

# Instale as ferramentas de bioinformática via Bioconda
conda install -c bioconda fastqc trimmomatic megahit prodigal hmmer -y

# Instale as bibliotecas Python
pip install pandas matplotlib seaborn squarify

# Desative o ambiente ao terminar (opcional)
conda deactivate

Fluxo de Trabalho e Comandos Executados
Todas as etapas do pipeline foram executadas no terminal WSL. Os comandos detalhados para cada etapa estão documentados no arquivo pipeline_commands.sh localizado na raiz deste repositório.

Etapas Principais:
Download dos Dados Brutos (FastQ): Aquisição das reads FastQ de sequenciamento.

Controle de Qualidade e Trimming das Reads: Avaliação da qualidade e remoção de adaptadores/bases de baixa qualidade.

Montagem do Genoma Metagenômico: Reconstrução de contigs a partir das reads limpas.

Predição de Genes e Proteínas: Identificação de genes e extração de suas sequências de aminoácidos nas contigs.

Anotação Funcional (HMMER/Pfam): Atribuição de funções aos domínios proteicos através de busca em banco de dados Pfam.

Análise e Visualização das Anotações Pfam: Sumarização e representação gráfica das famílias Pfam mais abundantes.

Execução da Análise de Anotações (Script Python)
O script analyze_annotations.py é responsável por ler os resultados brutos da anotação do hmmsearch (annotation_results.domtblout), aplicar filtros e gerar um treemap das famílias Pfam mais frequentes.

Para executar a análise e gerar o gráfico:

Certifique-se de que você está no diretório raiz do projeto (metagenomica_riacho/).

Ative seu ambiente Conda: conda activate metagenomics_env

Execute o script Python:

Bash

python scripts/analyze_annotations.py
O gráfico (treemap) será salvo em results/annotation_analysis/pfam_families_treemap.png.

Análise de Resultados
O treemap gerado em results/annotation_analysis/pfam_families_treemap.png visualiza a proporção de cada família Pfam encontrada nas proteínas preditas, após a aplicação de um limiar de E-value. Cada retângulo representa uma família Pfam, e seu tamanho é proporcional à sua contagem (número de proteínas que contêm aquele domínio). Isso oferece um panorama funcional das entidades microbianas presentes na amostra do riacho.

Próximos Passos (Sugestões para Aprimoramento)
Análise Taxonômica: Identificar os organismos presentes na amostra.

Análise de Vias Metabólicas: Mapear as proteínas para vias bioquímicas conhecidas (ex: KEGG, GO).

Montagem de Genomas de Organismos Específicos (MAGs): Reconstruir genomas de espécies abundantes a partir das contigs.

Comparação entre Amostras: Se tiver mais amostras, comparar os perfis funcionais e/ou taxonômicos.


**Como usar este `README.md`:**

1.  **Crie (ou substitua) o arquivo `README.md`** na pasta raiz do seu projeto (`metagenomica_riacho/`).
2.  **Cole todo o conteúdo acima** nele.
3.  **Faça uma última revisão:** Verifique se os nomes das pastas, arquivos e as descrições correspondem exatamente ao que você tem e fez.

Com este `README.md` e o `pipeline_commands.sh`, seu projeto estará extremamente bem documentado e pronto para ser compartilhado ou servir de base para futuras análises mais aprofundadas!