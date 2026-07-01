# Monitor de Crédito e Risco do Brasil

O crédito é o pulso silencioso de uma economia. Quando ele aperta, a conta chega para todo mundo: a família que começa a atrasar a fatura, a empresa que segura um investimento, o banco que fica mais desconfiado antes de emprestar. O problema é que os sinais desse aperto ficam espalhados em dezenas de séries soltas do Banco Central, cada uma contando só um pedaço da história. Este projeto junta esses pedaços num lugar só e transforma número solto em leitura clara: em que ponto do ciclo de crédito o Brasil está agora, e para onde ele parece caminhar.

**Painel ao vivo:** _[publique no Streamlit Community Cloud e cole o link aqui]_

> Status: primeira versão completa. Pipeline de ingestão, banco PostgreSQL, análise em SQL, testes e painel funcionando de ponta a ponta.

## O problema

Os dados sobre crédito no Brasil são públicos, gratuitos e atualizados de perto pelo Banco Central. Esse não é o problema. O problema é que eles vivem fragmentados. A inadimplência está numa série, o endividamento das famílias em outra, o spread em outra, a Selic em outra, cada uma com sua página, seu código numérico e até sua frequência de atualização. Para responder uma pergunta simples como "o crédito está piorando ou melhorando?", é preciso caçar cada série, baixar uma a uma, alinhar datas que não batem e cruzar tudo na mão. Na prática, quase ninguém faz esse trabalho, e a leitura acaba superficial ou refém da manchete do dia.

Este projeto faz o garimpo e a junção uma vez só, de forma automatizada e auditável, e entrega o que interessa: os indicadores lado a lado e, principalmente, o que eles dizem quando lidos em conjunto. Foi pensado para quem precisa dessa leitura sem virar especialista em API de banco central: analistas, estudantes de economia e finanças, jornalistas, e qualquer pessoa curiosa sobre a saúde do crédito no país.

## As perguntas que o projeto responde

Todo o projeto existe para responder cinco perguntas. Elas guiaram cada decisão: se um dado ou um gráfico não ajudava a responder uma delas, ele não entrava.

1. A inadimplência está subindo ou caindo, e o movimento vem mais da pessoa física ou da jurídica?
2. As famílias estão mais endividadas, e comprometendo uma fatia maior da renda com dívida?
3. O spread bancário acompanha a taxa básica de juros, ou descola dela?
4. Quanto tempo a inadimplência leva para reagir a uma mudança nos juros?
5. Em que fase do ciclo de crédito o país se encontra hoje?

## O que os dados revelaram

Cinco leituras se destacaram quando os indicadores foram cruzados. O painel mostra cada uma em detalhe, mas o resumo é este.

**Quem sente o aperto primeiro é a pessoa física.** A inadimplência da pessoa física é estruturalmente mais alta que a da jurídica, quase dois pontos percentuais acima na média histórica. Ela caiu ao menor nível da série no fim de 2020, no auge do auxílio emergencial e do crédito mais cauteloso, mas voltou a subir com força desde então e hoje ronda 5,4%. A pessoa jurídica é mais baixa e mais estável. Quando o crédito piora, é o bolso da pessoa física que estica primeiro.

**As famílias nunca deveram tanto.** O endividamento das famílias, que mede quanto elas devem em relação à renda de um ano inteiro, subiu de cerca de 30% em 2010 para perto de 50%, o maior patamar da série. E não é só dever mais. O comprometimento de renda, a fatia do salário que já sai todo mês só para pagar dívida, foi de 22% para perto de 29%. Os dois indicadores andam quase colados, com correlação de 0,81, o que mostra que o endividamento maior virou pressão real no orçamento mensal, e não apenas um número no papel.

**O spread não é a Selic com outro nome.** Existe uma intuição de que, quando o Banco Central sobe os juros, o custo do crédito para o cliente sobe na mesma medida. Os dados dizem que é mais complicado. A correlação entre spread e Selic é de apenas 0,57, e em vários períodos o spread sobe por conta própria, mesmo com a Selic parada. Esse é o prêmio de risco: quando os bancos ficam com mais medo de calote, cobram mais, independentemente do juro básico.

**A inadimplência reage aos juros com quase um ano de atraso.** Esta é a descoberta mais forte do projeto. Testando a relação entre a inadimplência e a Selic de vários meses atrás, a conexão mais forte aparece por volta de 9 a 10 meses de defasagem, e é uma relação robusta, com correlação de 0,83. Na prática, isso é um sinal antecipado: o juro alto de hoje já está, em boa parte, escrito na inadimplência do ano que vem. Para quem trabalha com risco de crédito, enxergar esse movimento com antecedência tem muito valor.

**Onde estamos agora: deterioração.** Juntando as peças, o país está hoje numa fase de deterioração do crédito. A inadimplência voltou a subir nos últimos meses, empurrada pela esteira de juros altos de 2024 e 2025, exatamente no prazo que a defasagem prevê. Olhando a série inteira, a deterioração é a fase mais frequente de todas, o que diz bastante sobre como o crédito brasileiro passa mais tempo sob tensão do que folgado.

## Os indicadores, em linguagem simples

Para quem não é da área financeira, um resumo rápido do que cada número significa:

- **Inadimplência:** a parcela da carteira de crédito com pagamento em atraso. É o termômetro mais direto de dificuldade das pessoas e empresas em honrar dívidas.
- **Endividamento das famílias:** o quanto as famílias devem em relação à renda que recebem ao longo de um ano inteiro. Um estoque de dívida.
- **Comprometimento de renda:** a parcela da renda mensal que já está reservada só para pagar dívida. É o peso da dívida no orçamento do mês.
- **Spread bancário:** a diferença entre o juro que o banco cobra do cliente e o custo que ele tem para captar o dinheiro. É onde entra o prêmio de risco.
- **Taxa básica de juros (Selic):** a referência de juros da economia, definida pelo Banco Central. Move todas as outras taxas.

## De onde vêm os dados

Todos os dados vêm do Sistema Gerenciador de Séries Temporais (SGS), do Banco Central do Brasil, coletados pela API pública. A série histórica começa em 2010 e cobre um período longo o bastante para enxergar mais de um ciclo econômico completo, de aperto e de folga.

Uma escolha importante do projeto é que o dado bruto é guardado exatamente como chega da fonte, antes de qualquer limpeza. Toda transformação é refeita a partir dele, o que significa que qualquer número do painel pode ser rastreado de volta até a fonte original. A cada nova coleta, o painel passa a refletir o dado mais recente disponível.

Vale lembrar que esses números são agregados no nível do país e passam por revisões periódicas do próprio Banco Central. A leitura leva isso em conta e evita conclusões apoiadas em um único mês.

## Como o projeto foi construído

Mais do que baixar dados e fazer gráficos, o projeto foi montado como um pequeno produto de dados, com uma arquitetura em camadas que separa o dado cru do dado tratado. O caminho que o dado percorre é sempre o mesmo:

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

Três decisões de arquitetura sustentam isso.

**O SQL é protagonista, não coadjuvante.** O tratamento (unir as séries e padronizar a frequência) e a análise (defasagens, correlações, classificação do ciclo) acontecem dentro do PostgreSQL, com uma materialized view mensal e consultas que usam funções de janela, correlação e `LAG`. A pergunta da defasagem, por exemplo, cruza a tabela com uma lista de atrasos e deixa os próprios dados escolherem qual é o mais forte, tudo em SQL. O Python cuida do que ele faz melhor, que é falar com a API e orquestrar o fluxo.

**O dado bruto nunca é alterado.** Ele entra num schema `raw` e permanece do jeito que veio. A camada `analytics` é sempre reconstruída a partir dele, num estilo parecido com o de uma arquitetura medalhão. Isso torna o pipeline auditável e reproduzível: se alguém questionar um número, dá para voltar ao bruto e refazer tudo.

**Frequências diferentes são um detalhe que quebra projetos, e aqui está resolvido.** Quase todas as séries são mensais, mas a Selic é diária. Juntar tudo pela data crua produziria uma tabela furada. A padronização para frequência mensal é feita no SQL, na hora de montar a camada analítica.

Coletar da fonte também teve seus percalços reais. A API do Banco Central recusa séries diárias com mais de dez anos por chamada, então a ingestão baixa em janelas e junta os pedaços, com tentativas automáticas quando a API engasga. Um comando único, `python run_pipeline.py`, roda o fluxo inteiro do começo ao fim. E dois testes automatizados travam justamente os dois erros mais perigosos do projeto: uma janela de download que passe do limite da API, e a mistura de frequências na tabela final.

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

Python com pandas e requests para coletar os dados. PostgreSQL como banco, onde o tratamento e a análise acontecem em SQL, com uma materialized view mensal e consultas que usam funções de janela e correlação. O banco roda em container com Docker, o que deixa o ambiente reproduzível em qualquer máquina. A exploração da análise é feita em Jupyter, e o painel em Streamlit. Git cuida do versionamento e o pytest dos testes automatizados.

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

Para rodar os testes:

```bash
pytest
```

## Escopo e próximos passos

O que está dentro: indicadores agregados de crédito no nível Brasil, com recorte por tipo de cliente (pessoa física e jurídica), série histórica cobrindo mais de um ciclo completo, análise em SQL e um painel interativo publicado.

O que fica de fora por enquanto, e são as ideias mais naturais de evolução: dados por instituição financeira, um modelo estatístico de previsão de inadimplência (indo além da defasagem simples), e recorte por estado ou região. São passos registrados no histórico de mudanças conforme forem entrando.

## Licença

MIT. Uso livre, com atribuição.

## Autor

João Pedro Vieira Brandão. Formado em Administração pela UFMG, com foco em análise de dados aplicada a finanças e risco.

---

## Histórico de mudanças

Toda mudança de escopo, fonte, ferramenta ou pergunta é registrada aqui e versionada com um commit começando por `Doc:`. Formato: data, o que mudou, motivo.

- 2026-06-28: criação do README e definição inicial do projeto.
- 2026-07-01: primeira versão completa. README reescrito com a arquitetura real (camadas raw e analytics no PostgreSQL, banco em Docker, análise em SQL, painel em Streamlit, testes com pytest), narrativa das descobertas e instruções de execução.
