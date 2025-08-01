# Projeto de Análise Metagenômica de Riacho

---

Este repositório contém o pipeline completo para a **análise metagenômica de uma amostra de riacho**, abrangendo desde o controle de qualidade das reads brutas até a anotação funcional e visualização dos resultados Pfam. O projeto foi desenvolvido para demonstrar um fluxo de trabalho padrão em metagenômica, utilizando ferramentas de bioinformática populares e scripts Python para análise e visualização de dados.

---

## Configuração do Ambiente Conda

Para reproduzir este projeto, é **essencial configurar o ambiente Conda** com todas as ferramentas e bibliotecas necessárias. Siga os passos abaixo:

1.  **Crie o ambiente Conda** (se ainda não o fez):
    ```bash
    conda create -n metagenomics_env python=3.9 -y
    ```

2.  **Ative o ambiente recém-criado**:
    ```bash
    conda activate metagenomics_env
    ```

3.  **Instale as ferramentas de bioinformática via Bioconda**:
    ```bash
    conda install -c bioconda fastqc trimmomatic megahit prodigal hmmer -y
    ```

4.  **Instale as bibliotecas Python** para análise e visualização:
    ```bash
    pip install pandas matplotlib seaborn squarify
    ```

5.  **Desative o ambiente** ao terminar (opcional):
    ```bash
    conda deactivate
    ```

---

## Fluxo de Trabalho e Comandos Executados

Todas as etapas do pipeline foram executadas no terminal WSL. Os **comandos detalhados para cada etapa** estão documentados no arquivo `pipeline_commands.sh`, localizado na raiz deste repositório.

### Etapas Principais do Pipeline:

* **Download dos Dados Brutos (FastQ)**: Aquisição das reads FastQ de sequenciamento.
* **Controle de Qualidade e Trimming das Reads**: Avaliação da qualidade e remoção de adaptadores/bases de baixa qualidade.
* **Montagem do Genoma Metagenômico**: Reconstrução de contigs a partir das reads limpas.
* **Predição de Genes e Proteínas**: Identificação de genes e extração de suas sequências de aminoácidos nas contigs.
* **Anotação Funcional (HMMER/Pfam)**: Atribuição de funções aos domínios proteicos através de busca em banco de dados Pfam.
* **Análise e Visualização das Anotações Pfam**: Sumarização e representação gráfica das famílias Pfam mais abundantes.

---

## Execução da Análise de Anotações (Script Python)

O script `analyze_annotations.py` é responsável por ler os resultados brutos da anotação do `hmmsearch` (`annotation_results.domtblout`), aplicar filtros e gerar um treemap das famílias Pfam mais frequentes.

Para **executar a análise e gerar o gráfico**:

1.  Certifique-se de que você está no diretório raiz do projeto (`metagenomica_riacho/`).
2.  Ative seu ambiente Conda:
    ```bash
    conda activate metagenomics_env
    ```
3.  Execute o script Python:
    ```bash
    python scripts/analyze_annotations.py
    ```
    O gráfico (treemap) será salvo em `results/annotation_analysis/pfam_families_treemap.png`.

---

## Análise de Resultados

O **treemap** gerado em `results/annotation_analysis/pfam_families_treemap.png` visualiza a proporção de cada família Pfam encontrada nas proteínas preditas, após a aplicação de um limiar de E-value. Cada retângulo representa uma família Pfam, e seu tamanho é proporcional à sua contagem (número de proteínas que contêm aquele domínio). Isso oferece um **panorama funcional das entidades microbianas** presentes na amostra do riacho.

---

## Próximos Passos (Sugestões para Aprimoramento)

Este projeto pode ser expandido com as seguintes análises adicionais:

* **Análise Taxonômica**: Identificar os organismos presentes na amostra.
* **Análise de Vias Metabólicas**: Mapear as proteínas para vias bioquímicas conhecidas (ex: KEGG, GO).
* **Montagem de Genomas de Organismos Específicos (MAGs)**: Reconstruir genomas de espécies abundantes a partir das contigs.
* **Comparação entre Amostras**: Se houver mais amostras, comparar os perfis funcionais e/ou taxonômicos.
