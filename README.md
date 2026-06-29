# Monitor de Crédito e Risco do Brasil

Painel que acompanha a evolução do crédito no Brasil: inadimplência, endividamento das famílias, taxa de juros e spread bancário. A ideia é pegar séries econômicas que ficam espalhadas e transformar em uma leitura clara sobre em que ponto do ciclo de crédito o país está.

> Status: em construção. O link do painel publicado entra aqui assim que a primeira versão estiver no ar.

## O problema

Os dados sobre crédito brasileiro são públicos e atualizados pelo Banco Central, mas vivem separados em dezenas de séries soltas. Quem quer saber se a inadimplência está piorando, se as famílias estão mais endividadas ou se o spread está acompanhando os juros precisa juntar tudo na mão e interpretar por conta própria. Este projeto reúne esses indicadores em um lugar só e mostra o que eles dizem quando lidos em conjunto.

Pensado para quem precisa dessa leitura de forma rápida, como analistas, estudantes de economia e finanças, e qualquer pessoa curiosa sobre a saúde do crédito no país.

## O que o painel responde

- Se a inadimplência está subindo ou caindo, e se o movimento vem mais da pessoa física ou da pessoa jurídica.
- Como o endividamento e o comprometimento de renda das famílias se comportaram ao longo do tempo.
- Se o spread bancário acompanha a taxa básica de juros ou se está descolando dela.
- Quanto tempo a inadimplência leva para reagir a uma mudança nos juros.
- Em que fase do ciclo de crédito o país se encontra hoje.

## Indicadores usados

Para quem não é da área financeira, um resumo rápido do que cada número significa:

- Inadimplência: parcela da carteira de crédito com pagamento em atraso. Indica dificuldade das pessoas e empresas em honrar dívidas.
- Endividamento das famílias: quanto do que as famílias devem pesa em relação à renda que recebem ao longo de um ano.
- Comprometimento de renda: parcela da renda mensal que já está reservada só para pagar dívidas.
- Spread bancário: diferença entre o juro que o banco cobra do cliente e o custo que ele tem para captar o dinheiro.
- Taxa básica de juros: referência de juros da economia, definida pelo Banco Central.

## Fonte dos dados

Todos os dados vêm do Sistema Gerenciador de Séries Temporais (SGS), do Banco Central do Brasil, acessado pela API pública. A série histórica cobre um período longo o bastante para enxergar mais de um ciclo econômico. O dado bruto é guardado exatamente como chega da fonte, antes de qualquer limpeza, para que a análise possa ser auditada depois. A cada nova coleta, o painel passa a refletir o dado mais recente disponível.

Vale lembrar que esses números são agregados no nível do país e passam por revisões periódicas do próprio Banco Central. A análise leva isso em conta.

## Escopo

O que está dentro: indicadores agregados de crédito no nível Brasil, com recorte por tipo de cliente (pessoa física e jurídica), série histórica cobrindo ao menos um ciclo completo, e um painel interativo publicado.

O que fica de fora por enquanto: dados por instituição financeira, modelo de previsão de inadimplência e recorte por estado ou região. São ideias para uma evolução futura, registradas no histórico de mudanças.

## Como o projeto está organizado

O fluxo segue quatro camadas independentes, do dado cru até a leitura final:

1. Ingestão: coleta e guarda o dado bruto.
2. Tratamento: limpa, padroniza e une as séries.
3. Análise: calcula os indicadores e cruza as relações entre eles.
4. Visualização: entrega o painel.

Estrutura das pastas:

```
br-credit-risk-monitor/
├── data/
│   ├── raw/            dado bruto, como veio da fonte
│   └── processed/      dado tratado, pronto para análise
├── notebooks/          exploração e raciocínio da análise
├── src/
│   ├── ingestion/      coleta dos dados
│   ├── processing/     limpeza e tratamento
│   └── analysis/       cálculos e indicadores
├── dashboard/          aplicação do painel
├── docs/               imagens e material de apoio
└── README.md           este arquivo
```

## Tecnologias

Python com pandas para coletar e tratar os dados, SQL (PostgreSQL) para organizar as séries, e Git para o versionamento. A ferramenta do painel está em definição.

## Roteiro

O projeto avança por fases. Cada fase só é considerada concluída quando entrega um resultado que funciona, e vira um conjunto de commits.

- Fase 1, Ingestão: trazer as séries da fonte e guardar o bruto.
- Fase 2, Tratamento: limpar, padronizar e unir as séries numa tabela única.
- Fase 3, Análise: responder às cinco perguntas da seção acima.
- Fase 4, Painel: construir e publicar a visualização.
- Fase 5, Comunicação: escrever as conclusões e divulgar.

## Principais conclusões

A ser preenchido conforme a análise avança. Aqui vão as três a cinco leituras mais relevantes que o painel revelar, escritas em linguagem de negócio.

## Como executar

As instruções de instalação e execução serão adicionadas quando a primeira versão do painel estiver pronta.

## Licença

MIT. Uso livre, com atribuição.

## Autor

João Pedro Vieira Brandão. Formado em Administração pela UFMG, com foco em análise de dados aplicada a finanças e risco.

---

## Histórico de mudanças

Toda mudança de escopo, fonte, ferramenta ou pergunta é registrada aqui e versionada com um commit começando por `Doc:`. Formato: data, o que mudou, motivo.

- 2026-06-28: criação do README e definição inicial do projeto.
