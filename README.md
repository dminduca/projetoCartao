# 📊 Projeto de Processamento e Categorização de Faturas (PDF)

Este projeto realiza a **extração, padronização, categorização automática e consolidação** de lançamentos financeiros a partir de **faturas em PDF** de diferentes bancos (ex: Nubank, PicPay).

O foco é automatizar um processo normalmente manual, tratando **layouts reais de faturas**, aplicando **categorização inteligente baseada em histórico e similaridade textual**, e permitindo **aprendizado incremental supervisionado** ao longo do uso.

---

## 🧠 Visão Geral do Fluxo

O pipeline do projeto funciona da seguinte forma:

1. 📄 Leitura dos PDFs de faturas  
2. 🧩 Identificação automática do banco emissor  
3. 🔍 Extração e parsing dos lançamentos  
4. 🧾 Padronização e enriquecimento dos dados  
5. 🏷️ Categorização automática (exata + fuzzy)  
6. 🚩 Geração de pendências (quando necessário)  
7. 📊 Consolidação em DataFrame  
8. 📤 Exportação para Excel  
9. 📂 Arquivamento dos PDFs processados  

---

## 📁 Estrutura do Projeto

```text
projetoCartao/
│
├── main.py
├── config.py
├── processador_faturas.py
├── categorizador.py
├── modelos.py
├── importar_pendencias.py
├── README.md
│
├── utils/
│   ├── __init__.py
│   ├── conversores.py
│   └── normalizacao.py
│
├── parsers/
│   ├── __init__.py
│   ├── parser_base.py
│   ├── nubank_parser.py
│   └── picpay_parser.py
│
├── data/
│   └── categorias/
│       ├── base_2025_normalizada.xlsx
│       └── categorias_2026.xlsx
│
├── input/
│   ├── faturas_pdf/
│   └── faturas_processadas/
│
├── output/
│   ├── lancamentos.xlsx
│   └── pendencias_categorizacao.xlsx
│
└── testes/
    └── teste_utils.py
```

---

## 🧰 Requisitos

* Python **3.10+**
* pandas
* pdfplumber
* rapidfuzz
* openpyxl

Recomendado criar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

---

## ⚙️ Configuração do Projeto (`config.py`)

O arquivo `config.py` centraliza todos os caminhos do projeto utilizando `pathlib`.

Responsabilidades:

* Definir pastas de **entrada**, **processados** e **saída**
* Definir caminhos das bases de categorização
* Criar automaticamente as pastas caso não existam

Principais diretórios:

* `input/faturas_pdf` → PDFs a serem processados
* `input/faturas_processadas` → PDFs já processados (organizados por banco)
* `output` → Arquivos finais gerados

---

## 🧾 Modelo de Dados (`modelos.py`)

O projeto utiliza o modelo `LancamentoCartao` para representar cada transação extraída da fatura.

Campos do modelo:

| Campo           | Descrição                     |
| --------------- | ----------------------------- |
| banco           | Banco emissor da fatura       |
| arquivo         | Nome do PDF de origem         |
| data            | Data da transação             |
| cartao          | Cartão utilizado              |
| descricao       | Descrição do lançamento       |
| valor           | Valor da transação            |
| data_vencimento | Data de vencimento da fatura  |
| categoria       | Categoria atribuída           |
| formPagto       | Forma de Pagamento (Crédito)  |
| operacao        | Operação (Despesa)            |
| status          | Status (Pendênte)             |
| desc_normalizada| Descrição Normalizada         |
| ind_categoria   | Índice da categoria           |
| tipo_match      | Tipo de match (EXATO / FUZZY) |
| score_match     | Score de similaridade (0–100) |

O modelo possui o método:

```python
to_dict()
```

Que permite a conversão direta para dicionário e posterior criação de `DataFrame`.

---

## 🧩 Parsers de Faturas (`parsers/`)

Cada banco possui um **parser específico**, responsável por interpretar o layout do PDF.

### Parsers disponíveis

* `NubankParser`
* `PicPayParser`

Todos herdam de `ParserBase`, garantindo:

* Interface comum (`parse()`)
* Reuso de lógica de leitura de PDF
* Padronização da saída

Responsabilidades dos parsers:

* Ler o PDF
* Identificar a seção correta de transações
* Ignorar resumos e totais
* Interpretar datas, descrições, valores e cartão
* Extrair a data de vencimento da fatura
* Retornar uma lista de `LancamentoCartao`

---

## 🔄 Processamento das Faturas (`processador_faturas.py`)

Este módulo atua como **orquestrador do pipeline**.

Responsabilidades:

* Identificar automaticamente o banco pelo nome do arquivo
* Instanciar o parser correto
* Injetar o serviço de categorização
* Consolidar todos os lançamentos
* Retornar os dados prontos para exportação

---

## 🏷️ Categorização Automática (`categorizador.py`)

A categorização é baseada em **histórico real de lançamentos** e **similaridade textual**.

### Arquivos de referência

Localizados em:

```text
data/categorias/
```

* **base_2025_normalizada.xlsx**

  * Histórico de descrições normalizadas
  * Relação descrição → índice de categoria

* **categorias_2026.xlsx**

  * Dicionário de categorias
  * Índice → nome da categoria

### Estratégia de categorização

* Normalização da descrição do lançamento
* Match exato com base histórica
* Match aproximado (*fuzzy matching*) utilizando **rapidfuzz**
* Avaliação de score de similaridade
* Retorno da melhor categoria encontrada
* Fallback para **NÃO CLASSIFICADO** quando não há match aceitável

---

## 🧠 Aprendizado Incremental por Pendências

Quando um lançamento não encontra categoria válida, o sistema gera automaticamente um arquivo de pendências:

``` text
output/pendencias_categorizacao.xlsx
```

Fluxo de aprendizado

  1. Execute `python main.py`

  2. Abra `pendencias_categorizacao.xlsx`

  3. Preencha a coluna **IndCategoria**

  4. Execute:

      ``` bash
      python importar_pendencias.py
      ```

  5. As descrições são incorporadas à base histórica

  6. O arquivo de pendências é removido

Na próxima execução, os lançamentos já serão classificados automaticamente.

## 🔤 Normalização e Conversões (`utils/`)

O módulo `utils` contém funções auxiliares reutilizáveis.

### `conversores.py`

Responsável por:

* Conversão de valores monetários para `float`
* Conversão de datas específicas por banco
* Conversão de datas parciais em datas completas

Essas funções garantem consistência entre diferentes layouts de fatura.

---

## ▶️ Como Executar o Projeto

### 1️⃣ Adicione os PDFs

Coloque as faturas em:

```text
input/faturas_pdf/
```

### 2️⃣ Execute o pipeline

```bash
python main.py
```

### 3️⃣ Resultado esperado

* PDFs movidos para `input/faturas_processadas/`
* Arquivo Excel gerado em:

```text
output/lancamentos.xlsx
```

---

## 📊 Estrutura do Arquivo de Saída

Colunas geradas:

```text
banco | arquivo | data | cartao | descricao | valor | data_vencimento | categoria | tipo_match | score_match
```

Datas são exportadas no formato **DD/MM/AAAA**.

---

## 🧪 Testes

Testes manuais podem ser executados com:

```bash
python -m testes.teste_utils
```

---

## 🚀 Próximas Evoluções Planejadas

* 🔎 Aprimorar regras de normalização
* 🧠 Ajuste fino de threshold de fuzzy matching
* 📈 Métricas de qualidade de categorização
* 🗄️ Persistência em banco de dados
* 🌐 API ou interface web

---

## ✅ Status do Projeto

``` text
✔ Pipeline funcional
✔ Parsers operacionais
✔ Categorização integrada (exata + fuzzy)
✔ Tratamento de layouts reais
✔ Exportação concluída
```

---

## 👤 Autor

Projeto desenvolvido para automação financeira, organização de gastos e evolução técnica em Python.
