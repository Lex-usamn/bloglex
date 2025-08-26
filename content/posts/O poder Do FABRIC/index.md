---
title: Fabric (AI) — Automatize análises e prompts no seu fluxo
date: 2025-08-21T13:00:00Z
draft: false
author: "Lex Usamn"
tags: ["IA", "Automação"]
categories: ["Aplicativos", "IA"]
summary: "Como usar o Fabric para padronizar prompts, automatizar análises e integrar IA ao seu fluxo (ex.: Lex Flow/Obsidian/n8n)."
---

# Fabric (AI) — Automatize análises e prompts no seu fluxo

> ✍️ Transforme tarefas repetitivas de IA em **pipelines previsíveis e reprodutíveis** com padrões (patterns) reutilizáveis.

## 🔹 Contexto
**Fabric** é um conjunto de *patterns* (modelos de prompt + instruções) e um **CLI** que facilita rodar análises com IA sempre do mesmo jeito. Em vez de “inventar” o prompt toda vez, você chama um *pattern* (ex.: `summarize`, `explain`, `compare`, `classify`) e alimenta com seus arquivos, textos ou links.  
Para quem usa **Obsidian, Hugo, n8n, Dify** ou rotinas em script, o Fabric ajuda a padronizar resultados e acelerar o fluxo.

## 🔹 Conteúdo Principal
- **Padrões reutilizáveis**: coleções de prompts versionadas (ex.: resumo, explicação, checklist, análise TELOS).
- **CLI simples**: rode um pattern em qualquer fonte (`stdin`, arquivos, pastas) e salve a saída.
- **Integração fácil**: encaixa em scripts `.bat/.sh`, automações no **n8n**, tarefas do **VS Code** e rotinas de build do **Hugo**.
- **Resultados consistentes**: mesma entrada ⇒ mesma estrutura de saída, ideal para posts, relatórios e notas.
- **Extensível**: crie seus próprios patterns para o seu estilo, linguagem e formatação.

### 📌 Exemplo
```bash
# Executa um pattern de resumo sobre um arquivo e grava a saída
fabric -p summarize -i docs/artigo.md -o out/artigo-resumo.md

# Usa um pattern de "insights" lendo do stdin e devolvendo no terminal
cat notas/reuniao.txt | fabric -p insights

# Aplica um pattern customizado (local) para revisão TELOS diária
fabric -p patterns/telos_daily.yaml -i journals/2025-08-21.md -o journals/2025-08-21.review.md
```



### ✨ Exemplo de Pattern Personalizado (YAML)

# patterns/telos_daily.yaml
name: telos_daily_review
description: "Revisão diária TELOS com tarefas, aprendizados e próximos passos."
inputs:
  - name: entry
    type: file
    required: true
system: |
  Você é um facilitador objetivo. Estruture a resposta em seções fixas.
prompt: |
  A seguir está a entrada do diário:
  ---
  {{entry}}
  ---
  Gere:
  1) Tarefas (checkbox), 2) Insights (bullets), 3) Próximos passos (numérico),
  2) Obstáculos e como mitigar, 5) Resumo TELOS (1 parágrafo).
output_format: markdown

### 🔗 Onde o Fabric brilha no dia a dia

- **Hugo/Obsidian**: gerar _resumos prontos para post_ a partir de READMEs, vídeos transcritos ou notas.
    
- **n8n / Dify**: criar rotas automáticas (ex.: ao salvar novo `.md`, rodar `fabric -p summarize` e enviar para publicação).
    
- **Pipelines de conteúdo**: padronizar _callouts_, headings, tags e _front matter_ para seus posts.
    
- **Revisões semanais/TELOS**: transformar diários em relatórios objetivos com um clique.
    

## 🔹 Conclusão

O **Fabric** coloca a IA no piloto automático: você define os _patterns_, integra no seu fluxo e passa a produzir **mais rápido**, com **qualidade consistente** e **menos retrabalho**. Se você já usa Obsidian/Hugo e automações (n8n/Dify), adicionar o Fabric é o próximo passo natural. 🚀

{{< alert icon="fire" cardColor="#e63946" iconColor="#1d3557" textColor="#f1faee" >}}
Lembrando que estou Desenvolvendo uma plataforma pessoal, onde ira trabalar o Fabric com o TELOS que em breve explicarei mais
{{< /alert >}}

!![Image Description](Pasted%20image%2020250822113919.png)


✅ Obrigado por ler!  
📩 Quer trocar ideia? Deixe um comentário ou entre em contato.