# Monitor de Crédito e Risco do Brasil

Este projeto reúne num painel só os principais indicadores de crédito que o Banco Central publica (inadimplência, endividamento das famílias, juros e spread bancário) e mostra o que eles dizem quando são lidos em conjunto: em que ponto do ciclo de crédito o Brasil está.

**Painel ao vivo:** _[publique no Streamlit Community Cloud e cole o link aqui]_

> Status: primeira versão completa. Ingestão, banco PostgreSQL, análise em SQL, testes e painel funcionando.

## O problema

Os dados de crédito no Brasil são públicos e atualizados pelo Banco Central. A dificuldade não é falta de dado, é que ele fica espalhado em muitas séries separadas, cada uma com seu código e até sua frequência. Para responder algo simples como "o crédito está piorando ou melhorando?", é preciso baixar várias séries, alinhar datas que não coincidem e cruzar tudo na mão.

Este projeto faz esse trabalho de forma automatizada e deixa os indicadores prontos para leitura, lado a lado. É voltado para quem quer essa visão sem precisar mexer na API do Banco Central: analistas, estudantes de economia e finanças, e pessoas curiosas sobre o tema.

## As perguntas que o projeto responde

O projeto foi organizado em torno de cinco perguntas. Cada dado e cada gráfico existe para responder uma delas.

1. A inadimplência está subindo ou caindo, e o movimento vem mais da pessoa física ou da jurídica?
2. As famílias estão mais endividadas, e comprometendo uma fatia maior da renda com dívida?
3. O spread bancário acompanha a taxa básica de juros, ou descola dela?
4. Quanto tempo a inadimplência leva para reagir a uma mudança nos juros?
5. Em que fase do ciclo de crédito o país se encontra hoje?

## O que os dados mostram

O painel detalha cada ponto, mas os principais resultados são estes.

A inadimplência da pessoa física fica acima da pessoa jurídica ao longo de toda a série, cerca de 1,7 ponto percentual a mais na média. Ela chegou ao menor nível no fim de 2020 e voltou a subir depois, e hoje está perto de 5,4%. A da pessoa jurídica é mais baixa e varia menos.

O endividamento das famílias subiu de cerca de 30% da renda de um ano em 2010 para perto de 50%, o maior nível da série. O comprometimento de renda, que é a parte do salário mensal que já vai para pagar dívida, foi de 22% para perto de 29%. Os dois têm correlação de 0,81, ou seja, andam praticamente juntos.

O spread e a Selic têm correlação de apenas 0,57. Em vários períodos o spread sobe mesmo com a Selic parada, o que sugere que boa parte do custo do crédito vem do risco que o banco precifica, e não só do juro básico.

Testando a inadimplência contra a Selic de vários meses atrás, a relação mais forte aparece por volta de 9 a 10 meses de defasagem, com correlação de 0,83. Na prática, o efeito de uma mudança nos juros aparece na inadimplência quase um ano depois, o que ajuda a antecipar o risco.

Somando os indicadores, o momento atual é de piora do crédito: a inadimplência voltou a subir nos últimos meses, no intervalo esperado depois do juro alto de 2024 e 2025.

## Os indicadores, em poucas palavras

Para quem não é da área financeira, o que cada número significa:

- **Inadimplência:** a parcela da carteira de crédito com pagamento em atraso.
- **Endividamento das famílias:** o quanto as famílias devem em relação à renda de um ano.
- **Comprometimento de renda:** a parte da renda mensal que já está reservada para pagar dívida.
- **Spread bancário:** a diferença entre o juro que o banco cobra do cliente e o custo que ele tem para captar o dinheiro.
- **Taxa básica de juros (Selic):** a referência de juros da economia, definida pelo Banco Central.

## De onde vêm os dados

Todos os dados vêm do Sistema Gerenciador de Séries Temporais (SGS), do Banco Central do Brasil, coletados pela API pública. A série começa em 2010 e cobre um período longo o bastante para ver mais de um ciclo econômico.

O dado bruto é guardado exatamente como chega da fonte, antes de qualquer limpeza. Toda transformação é refeita a partir dele, então qualquer número do painel pode ser rastreado de volta até a origem. A cada nova coleta, o painel reflete o dado mais recente disponível.

Esses números são agregados no nível do país e passam por revisões periódicas do Banco Central. A leitura leva isso em conta e evita conclusões apoiadas em um único mês.

## Como o projeto foi construído

O projeto é um pequeno pipeline de dados, com o dado passando por camadas até virar o painel:

```
API do Banco Central
        │  ingestão (Python + requests)
        ▼
   data/raw/*.csv          dado bruto, intocado, para auditoria
        │  carga (Python → PostgreSQL)
        ▼
   schema raw              tabela longa: uma linha por (série, data, valor)
        │  tratamento (SQL)
        ▼
   schema analytics        tabela mensal e pivotada, uma linha por mês
        │  análise (SQL: janelas, correlação, defasagem)
        ▼
   perguntas respondidas  →  painel Streamlit
```

O tratamento e a análise são feitos em SQL, dentro do PostgreSQL. Unir as séries, padronizar a frequência e calcular defasagens e correlações acontece no banco, com uma materialized view mensal e consultas que usam funções de janela. O Python cuida da coleta na API e da orquestração do fluxo.

O dado bruto entra num schema `raw` e não é alterado. A camada `analytics` é sempre reconstruída a partir dele, o que permite auditar qualquer número voltando à fonte.

As séries não têm todas a mesma frequência. Quase todas são mensais, mas a Selic é diária. A padronização para mensal é feita no SQL, na montagem da camada analítica. Sem esse passo, a Selic diária não casaria com o resto e a tabela final ficaria cheia de buracos.

A coleta também precisou contornar um limite da API: séries diárias não podem ser pedidas com mais de dez anos por vez. A ingestão baixa em janelas e junta os pedaços, repetindo a tentativa quando a API falha. Um comando, `python run_pipeline.py`, roda o fluxo inteiro. Dois testes com pytest cobrem os pontos mais sensíveis: que nenhuma janela de download passe do limite da API, e que a tabela final tenha um registro por mês.

Estrutura das pastas:

```
br-credit-risk-monitor/
├── data/
│   ├── raw/             dado bruto, como veio da fonte (não versionado)
│   └── processed/       tabela mensal exportada do banco (versionada)
├── sql/
│   ├── 01_schema.sql    cria os schemas raw e analytics
│   ├── 02_analytics.sql matview mensal e pivotada (o tratamento)
│   └── perguntas/       uma query SQL por pergunta da análise
├── src/
│   ├── config.py        série, caminhos e conexão (lê o .env)
│   ├── db.py            conexão com o PostgreSQL
│   ├── ingestion/       coleta dos dados na API
│   ├── loading/         carga do bruto no banco
│   └── processing/      construção da camada analytics
├── notebooks/           exploração e conclusões da análise
├── dashboard/           painel Streamlit
├── tests/               testes com pytest
├── docker-compose.yml   banco PostgreSQL em container
├── run_pipeline.py      roda o pipeline inteiro num comando
└── README.md            este arquivo
```

## Tecnologias

Python com pandas e requests para coletar os dados. PostgreSQL como banco, onde o tratamento e a análise acontecem em SQL, com uma materialized view mensal e consultas que usam funções de janela e correlação. O banco roda em container com Docker, o que deixa o ambiente reproduzível. A exploração é feita em Jupyter e o painel em Streamlit. Git para o versionamento e pytest para os testes.

## Como executar

O painel já vem com os dados processados versionados, então para só ver a visualização bastam três passos:

```bash
git clone https://github.com/SEU-USUARIO/br-credit-risk-monitor.git
cd br-credit-risk-monitor

python -m venv .venv
.venv\Scripts\activate            # Windows. No Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt

streamlit run dashboard/app.py
```

Para reprocessar os dados do zero, baixando da fonte e reconstruindo o banco, você precisa do Docker:

```bash
copy .env.example .env            # Windows. No Mac/Linux: cp .env.example .env
# abra o .env e ajuste a senha do banco

docker compose up -d              # sobe o PostgreSQL em container
python run_pipeline.py            # ingestão, carga, camada analytics e exportação do CSV
```

Para rodar os notebooks e os testes, instale também as ferramentas de desenvolvimento:

```bash
pip install -r requirements-dev.txt
pytest
```

## Escopo e próximos passos

Está dentro do escopo: indicadores agregados de crédito no nível Brasil, com recorte por tipo de cliente (pessoa física e jurídica), série histórica cobrindo mais de um ciclo, análise em SQL e um painel interativo publicado.

Fica de fora por enquanto, e são as evoluções mais naturais: dados por instituição financeira, um modelo de previsão de inadimplência que vá além da defasagem simples, e recorte por estado ou região. Ficam registradas no histórico de mudanças conforme forem entrando.

## Licença

MIT. Uso livre, com atribuição.

## Autor

João Pedro Vieira Brandão. Formado em Administração pela UFMG, com foco em análise de dados aplicada a finanças e risco.

---

## Histórico de mudanças

Toda mudança de escopo, fonte, ferramenta ou pergunta é registrada aqui e versionada com um commit começando por `Doc:`. Formato: data, o que mudou, motivo.

- 2026-06-28: criação do README e definição inicial do projeto.
- 2026-07-01: primeira versão completa. README atualizado com a arquitetura real (camadas raw e analytics no PostgreSQL, banco em Docker, análise em SQL, painel em Streamlit, testes com pytest), resultados da análise e instruções de execução.
