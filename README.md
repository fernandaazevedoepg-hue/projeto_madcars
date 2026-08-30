# MADCARS - MVP de Avaliação Técnica: Plataforma de Análise de Oportunidades de Importação de Veículos

Projeto: MVP de Avaliação Técnica - Análise de Oportunidades de Importação de Veículos (Europa/EAU -> Espanha)
Stack Tecnológica: Python 3.13, Django 6.1, NumPy, HTML5, CSS3, Bootstrap 5, SQLite3


## 1. Resumo Executivo e Visão Geral da Arquitetura

Este MVP é uma ferramenta de inteligência de mercado e suporte à decisão desenvolvida para empresas de importação de veículos (com foco no corredor Europa/EAU -> Espanha). A plataforma permite aos analistas avaliar se a importação de um determinado veículo oferece uma oportunidade comercial real após contabilizar os custos de aquisição, taxas de leilão, transporte internacional, homologação/ITV, impostos de matriculação locais (IEDMT) e benchmarks do mercado espanhol.

### Justificação da Stack Tecnológica
- **Python / Django:** Escolhido por permitir um desenvolvimento ágil e seguro de uma aplicação web estruturada. A utilização do padrão MVT (Model-View-Template) facilitou o isolamento rigoroso das regras de negócio num módulo dedicado (`services.py`).
- **SQLite:** Adotado por ser uma solução leve, autónoma e perfeitamente adequada para o âmbito de um protótipo / MVP de avaliação técnica.
- **NumPy:** Utilizado na camada de serviços para apurar com rigor estatístico a média, mínimo, máximo e mediana dos preços de mercado.

### Arquitetura
O projeto segue rigorosamente uma arquitetura modular em 3 camadas:
1. **Camada de Dados (`models.py` e SQLite):** Gestão de listagens estruturadas de veículos (`Vehicle`) e parâmetros de custos de importação (`ImportCalculation`). A utilização de escolhas padronizadas (`choices`) garante a normalização dos dados entre os mercados de origem e destino.
2. **Camada de Lógica de Negócio (`services.py`):** Processamento de cálculos de domínio com precisão `Decimal`. Calcula escalões do imposto IEDMT com base nas emissões de CO2, apura o Landed Cost total e executa um algoritmo transparente de Opportunity Score (0-100).
3. **Camada de Apresentação e Controlo (`views.py` e `calculator.html`):** Renderização do painel interativo, seleção dinâmica do veículo ativo, edição e re-cálculo dinâmico de custos na própria interface, criação automática de registos de cálculo pendentes e apresentação do benchmark do mercado espanhol em tempo real.

---

## 2. Escopo Funcional e Funcionalidades Concluídas

- **Normalização de Dados de Veículos:** Estrutura de dados interna comum para especificações do veículo (incluindo URL original do anúncio, moeda, transmissão, combustível, motor e potência).
- **Calculadora de Custos Editável:** Estimativa dinâmica do Landed Cost total permitindo a simulação e edição direta no Dashboard de custos manuais, fixos e baseados em fórmulas (taxas de leilão, honorários, transporte, documentação, gestoria, homologação, ITV e imposto CO2).
- **Benchmark do Mercado Espanhol:** Consulta e filtragem automática de veículos comparáveis em Espanha com base na Marca, Modelo, Intervalo de Anos (+/- 3 anos), Combustível e Tipo de Transmissão.
- **Análise de Oportunidades e Modelo de Pontuação:**
  * Cálculo automático do Preço Médio, Mínimo, Máximo e Mediana do mercado espanhol.
  * Estimativa da margem comercial (EUR e %), preço final sugerido e poupança potencial do cliente.
  * Opportunity Score transparente (0-100) combinando a percentagem de margem e a confiança na amostra de comparáveis.
  * Emblemas de classificação de estado segundo as regras de negócio: Good Opportunity (>=80), Review Required (60-79) e Not Attractive (<60).
- **Integração no Django Admin:** Painel de administração customizado com editores inline (`ImportCalculationInline`), ações personalizadas de duplicação (`duplicar_veiculos`) e rótulos de campos alinhados com a interface pública.

---

## 3. Lógica de Negócio e Cálculos (services.py)

### Fórmula do Landed Cost
`Landed Cost = Preço de Aquisição + Taxa de Leilão + Honorários + Documentação + Transporte + Homologação + ITV + Gestoria + Imposto IEDMT`

### Escalões do Imposto de Matriculação (IEDMT) por Emissões de CO2
- <= 120 g/km: 0.00%
- 121 - 160 g/km: 4.75%
- 161 - 200 g/km: 9.75%
- > 200 g/km: 14.75%

### Algoritmo do Opportunity Score (0 a 100)
- **Pontos por Margem (Máximo 60 pts):**
  * Margem >= 20%: 60 pts
  * Margem 10% - 19.9%: 40 pts
  * Margem 0.1% - 9.9%: 20 pts
  * Margem <= 0%: 0 pts
- **Pontos por Confiança da Amostra (Máximo 40 pts):**
  * >= 5 comparáveis: 40 pts
  * 2 - 4 comparáveis: 25 pts
  * 1 comparável: 10 pts
  * 0 comparáveis: 0 pts

### Classificação do Resultado
- 80 a 100 pts: **Good Opportunity**
- 60 a 79 pts: **Review Required**
- 0 a 59 pts: **Not Attractive**

---

## 4. Estratégia de Dados Externos, Pressupostos e Limitações

### Estratégia de Captura de Dados
Para este MVP de avaliação técnica, são utilizados dados estruturados representativos (baseados nos valores de referência da especificação) e inserção direta de dados pelo utilizador via Dashboard ou Django Admin. A captura de dados em tempo real (web scraping) contra portais como Mobile.de ou AutoScout24 foi omitida nesta fase devido a mecanismos anti-bot (captchas Akamai/Cloudflare) e limites de pedidos por IP.

### Requisitos para Integração de Web Scraping em Produção
1. **Cluster de Browsers Headless:** Implementação de workers Playwright / Puppeteer em instâncias cloud isoladas.
2. **Rotação de Proxies:** Integração com redes de proxies residenciais para evitar bloqueios de IP.
3. **Pipeline de Correspondência de Dados:** Utilização de fuzzy matching (ex. distância Levenshtein) para tratar divergências de versões/acabamentos entre diferentes portais de origem.

### Limitações Conhecidas
- As fórmulas fiscais aplicam atualmente as tarifas nacionais espanholas padrão; regimes regionais especiais (ex. IGIC das Ilhas Canárias) não estão incluídos.
- As margens comerciais são calculadas com base no Landed Cost direto do veículo.

---

## 5. Como Executar o Projeto

### Pré-requisitos
- Python 3.11+
- Git

### Passos de Configuração
1. Clonar o projeto e aceder à pasta:
   `cd projeto_madcars`

2. Activar o Ambiente Virtual:
   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Instalar as Dependências:
   `pip install django numpy`

4. Aplicar as Migrações:
   `python manage.py migrate`

5. Iniciar o Servidor de Desenvolvimento:
   `python manage.py runserver`

6. Aceder à Aplicação:
   - Dashboard Principal: http://127.0.0.1:8000/
   - Django Admin: http://127.0.0.1:8000/admin/

---

## 6. Próximos Passos para a Versão de Produção

1. **Web Scraping Automático em Tempo Real:** Integração de workers em segundo plano com Playwright para extração automática de anúncios.
2. **Exportação de Orçamentos em PDF:** Geração com um clique de propostas comerciais em PDF para clientes finais.
3. **Motor Contabilístico Avançado:** Suporte para fiscalidade especial (IGIC Canárias), tarifa de importação de 5% dos EAU e regimes especiais de IVA (REBU).