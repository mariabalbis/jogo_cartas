# 🃏 Duelo de Cartas

Jogo de cartas para o terminal, feito em Python, para demonstrar o uso de **estruturas de dados** (pilha, fila de prioridade e fila FIFO) e a escolha entre **laço** e **recursão** em cada parte do problema.

Trabalho de Estrutura de Dados.

## ▶️ Como rodar

Requisitos: Python 3.8 ou superior. Não há dependências externas.

```bash
python duelo_de_cartas.py
```

No Mac/Linux, se `python` não funcionar, use `python3 duelo_de_cartas.py`.

> Dica: use o terminal do VS Code ou o Terminal do Windows. O antigo Prompt de Comando (cmd) pode quebrar os emojis.

## 🎮 Como jogar

Você enfrenta a CPU. Cada jogador começa com **30 pontos de vida** e **3 cartas na mão**.

A cada turno:

1. Compra 1 carta do baralho (a partir do 3º turno).
2. Escolhe uma carta da mão para colocar no **campo de batalha**.
3. Suas cartas no campo atacam, da mais rápida para a mais lenta.

Quem zerar a vida do adversário vence.

**Comandos:**

| Tecla | Ação |
|-------|------|
| `1`, `2`, `3`... | Joga a carta correspondente |
| `r` | Resgata a primeira carta da fila de descarte |
| `Ctrl + C` | Sai do jogo |

### Regras

- Cada carta tem três atributos: **Ataque (ATQ)**, **Defesa (DEF)** e **Velocidade (VEL)**.
- O campo é compartilhado, com no máximo **3 cartas por jogador**. Se o seu limite estourar, a carta mais lenta vai para o descarte.
- Dano de um ataque: `ATQ + soma de 2 dados D6 − maior DEF do adversário no campo` (mínimo de 1).
- O descarte guarda no máximo 3 cartas. Ao entrar a 4ª, a mais antiga sai do jogo.

## 🧠 Estruturas de dados e decisões

| Tópico | Parte do jogo | Estrutura | Técnica | Por quê |
|--------|---------------|-----------|---------|---------|
| 1 | Atributos das cartas | Registro | **Laço** | A carta é só uma ficha de dados. Um laço lê os atributos de cada uma. |
| 2 | Comprar cartas | **Pilha** (LIFO) | **Laço** | Puxar 3 cartas do topo é repetir o `pop()` 3 vezes. Recursão complicaria algo simples. |
| 3 | Campo de batalha | **Fila de prioridade** | **Recursão** (inserção) e **laço** (exibição) | A posição pela velocidade é achada dividindo a lista ao meio e descendo pelos galhos. Exibir o campo ordenado é só varrer a lista. |
| 4 a 7 | Ataque e dado D6 | Lista de dados | **Laço** | Rolar 2 ou 3 dados e somar cabe em poucas linhas. |
| 8 | Descarte | **Fila** (FIFO) | **Laço** | Funciona como fila de banco: quem chega primeiro sai primeiro. |
| 9 e 10 | Alternar turnos | Controle do jogo | **Laço `while`** | O jogo roda até alguém vencer. Com recursão, cada turno acumularia memória até estourar a pilha (Stack Overflow). |

### Onde ver no código

| Função | O que faz |
|--------|-----------|
| `ler_cartas()` | Lê o registro de cada carta (laço) |
| `comprar()` | Retira cartas da pilha (laço) |
| `posicao_rec()` / `inserir()` | Fila de prioridade com busca recursiva pela posição |
| `rolar_dados()` | Rola os dados D6 (laço) |
| `descartar()` | Fila de descarte FIFO |
| `partida()` | Laço `while` que alterna os turnos |

## 🔎 Console de estruturas

Durante o jogo, cada operação aparece no terminal com uma etiqueta, para acompanhar o que acontece por trás:

```
[PILHA] pop() -> Dragão
[RECURSÃO] nível 1: meio=1 (Dragão, vel 3)
[FILA PRIORIDADE] Mago entra na posição 2
[DADO] 2d6 = 4+6
[FILA FIFO] enqueue(Lobo)
```

## 📁 Estrutura do projeto

```
.
├── duelo_de_cartas.py
└── README.md
```

## 👤 Autor

Maria Balbis, Luis Fernando, Nicolas Urban e Ryan Rodrigues · Ciência de dados e IA UniSenai
