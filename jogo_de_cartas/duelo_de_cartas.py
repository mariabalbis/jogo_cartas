#!/usr/bin/env python3
"""Duelo de Cartas - Estruturas de Dados (versão terminal).
Rode no VS Code com:  python duelo_de_cartas.py
"""
import os, random, sys, time
from collections import deque

os.system("")  # habilita cores ANSI no Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VERDE, VERM, AZUL, CINZA, NEG, FIM = "\033[92m", "\033[91m", "\033[94m", "\033[90m", "\033[1m", "\033[0m"
RAW = [("Dragão", "🐉", 8, 4, 3), ("Fênix", "🔥", 7, 3, 6), ("Lobo", "🐺", 5, 3, 5),
       ("Golem", "🗿", 4, 6, 1), ("Ninja", "🥷", 6, 2, 6), ("Mago", "🧙", 7, 2, 4),
       ("Cavaleiro", "🏰", 5, 5, 3), ("Harpia", "🦅", 4, 2, 6), ("Troll", "👹", 6, 5, 2),
       ("Sereia", "🧜", 5, 3, 4), ("Arqueiro", "🏹", 6, 2, 5), ("Fantasma", "👻", 3, 4, 6)]
PV, LIMITE_CAMPO, LIMITE_DESCARTE = 30, 3, 3
FACES = "⚀⚁⚂⚃⚄⚅"


def pausa(s):
    if sys.stdout.isatty():
        time.sleep(s)


def log(tag, txt):
    print(f"  {AZUL}[{tag}]{FIM} {CINZA}{txt}{FIM}")


# Tópico 1: atributos das cartas lidos com laço
def ler_cartas():
    cartas = []
    for nome, emoji, atk, df, vel in RAW:
        cartas.append({"nome": nome, "emoji": emoji, "atk": atk, "def": df, "vel": vel, "dono": None})
    return cartas


def criar_baralho(dono):
    pilha = ler_cartas()
    for c in pilha:
        c["dono"] = dono
    random.shuffle(pilha)
    return pilha  # lista usada como PILHA: append / pop


# Tópico 2: comprar do baralho (pilha) com laço
def comprar(j, n):
    for _ in range(n):
        if not j["pilha"]:
            break
        c = j["pilha"].pop()
        j["mao"].append(c)
        log("PILHA", f"pop() -> {c['nome'] if j['humano'] else '(carta oculta)'}")


# Tópico 3: fila de prioridade (por velocidade). Posição achada por RECURSÃO
def posicao_rec(campo, vel, lo, hi, nivel=1):
    if lo >= hi:
        return lo
    m = (lo + hi) // 2
    log("RECURSÃO", f"nível {nivel}: meio={m} ({campo[m]['nome']}, vel {campo[m]['vel']})")
    if campo[m]["vel"] >= vel:
        return posicao_rec(campo, vel, m + 1, hi, nivel + 1)
    return posicao_rec(campo, vel, lo, m, nivel + 1)


def inserir(campo, c):
    i = posicao_rec(campo, c["vel"], 0, len(campo))
    campo.insert(i, c)
    log("FILA PRIORIDADE", f"{c['nome']} entra na posição {i + 1}")


# Tópicos 4 a 7: dados D6 com laço
def rolar_dados(n):
    dados = []
    for _ in range(n):
        dados.append(random.randint(1, 6))
    return dados


# Tópico 8: fila de descarte (FIFO)
def descartar(desc, c):
    desc.append(c)
    log("FILA FIFO", f"enqueue({c['nome']})")
    if len(desc) > LIMITE_DESCARTE:
        x = desc.popleft()
        log("FILA FIFO", f"dequeue() -> {x['nome']} sai do jogo")


def jogar_carta(e, j, c):
    j["mao"].remove(c)
    meus = [x for x in e["campo"] if x["dono"] == j["id"]]
    if len(meus) >= LIMITE_CAMPO:  # campo cheio: a mais lenta vai para o descarte
        lenta = meus[-1]
        e["campo"].remove(lenta)
        descartar(e["desc"], lenta)
    inserir(e["campo"], c)


# ---------- interface ----------
def linhas_carta(c, idx=None):
    w, cor = 12, (VERDE if c["dono"] == "J" else VERM)
    sob = (w - 2) // 2
    emo = " " * sob + c["emoji"] + " " * (w - 2 - sob)
    topo = f"[{idx}]".center(w + 2) if idx is not None else " " * (w + 2)
    corpo = ["┌" + "─" * w + "┐", "│" + emo + "│", "│" + c["nome"].center(w) + "│",
             "│" + f"ATQ {c['atk']}".center(w) + "│", "│" + f"DEF {c['def']}".center(w) + "│",
             "│" + f"VEL {c['vel']}".center(w) + "│", "└" + "─" * w + "┘"]
    return [topo] + [cor + l + FIM for l in corpo]


def mostrar(cartas, numerar=False):
    if not cartas:
        print("  (vazio)")
        return
    blocos = [linhas_carta(c, i + 1 if numerar else None) for i, c in enumerate(cartas)]
    for linha in zip(*blocos):  # laço de exibição
        print("  " + " ".join(linha))


def barra(pv):
    n = round(pv / PV * 20)
    return "█" * n + "░" * (20 - n)


def tela(e):
    J, C = e["J"], e["C"]
    print("\n" + "═" * 64)
    print(f"{VERM}CPU  {barra(C['pv'])} {C['pv']} PV{FIM}   pilha: {len(C['pilha'])}  mão: {len(C['mao'])}")
    print(f"\n{NEG}CAMPO (fila de prioridade, maior velocidade primeiro){FIM}")
    mostrar(e["campo"])
    print(f"\n{VERDE}VOCÊ {barra(J['pv'])} {J['pv']} PV{FIM}   pilha: {len(J['pilha'])}")
    print(f"{CINZA}Descarte (fila): " + (" -> ".join(c["emoji"] + c["nome"] for c in e["desc"]) or "vazio") + FIM)


def escolher(e):
    J, resgatou = e["J"], False
    while True:
        print(f"\n{NEG}Sua mão:{FIM}")
        mostrar(J["mao"], True)
        pode = bool(e["desc"]) and not resgatou
        op = input("> número da carta" + (" ou r para resgatar do descarte" if pode else "") + ": ").strip().lower()
        if op == "r" and pode:
            c = e["desc"].popleft()
            c["dono"] = "J"
            J["mao"].append(c)
            resgatou = True
            log("FILA FIFO", f"dequeue() -> {c['nome']} resgatado")
        elif op.isdigit() and 1 <= int(op) <= len(J["mao"]):
            return J["mao"][int(op) - 1]
        else:
            print("  opção inválida")


def atacar(e, at, df):
    for c in [x for x in e["campo"] if x["dono"] == at["id"]]:  # em ordem de velocidade
        esc = max([x["def"] for x in e["campo"] if x["dono"] == df["id"]], default=0)
        dados = rolar_dados(2)
        soma = sum(dados)
        dano = max(1, c["atk"] + soma - esc)
        df["pv"] = max(0, df["pv"] - dano)
        log("DADO", f"2d6 = {'+'.join(map(str, dados))}")
        print(f"  {' '.join(FACES[d - 1] for d in dados)}  {c['nome']}: ATQ {c['atk']} + dados {soma} - defesa {esc} = {NEG}{dano}{FIM} de dano")
        pausa(0.9)
        if df["pv"] <= 0:
            return


def partida():
    novo = lambda i, nome, h: {"id": i, "nome": nome, "humano": h, "pv": PV, "pilha": criar_baralho(i), "mao": []}
    e = {"J": novo("J", "Você", True), "C": novo("C", "CPU", False), "campo": [], "desc": deque()}
    log("REGISTRO", "12 cartas lidas por laço para cada baralho")
    comprar(e["J"], 3)
    comprar(e["C"], 3)
    atual, outro, turno = e["J"], e["C"], 0
    while True:  # Tópicos 9 e 10: while alterna os turnos (sem recursão, sem Stack Overflow)
        turno += 1
        print(f"\n{NEG}══ TURNO {turno} · {atual['nome']} ══{FIM}")
        if turno > 2:
            comprar(atual, 1)
        tela(e)
        carta = None
        if atual["humano"]:
            if atual["mao"]:
                carta = escolher(e)
            else:
                print("  sem cartas na mão")
        else:
            pausa(1)
            if atual["mao"]:
                carta = max(atual["mao"], key=lambda c: c["atk"] + c["vel"])
        if carta:
            jogar_carta(e, atual, carta)
            print(f"  {atual['nome']} jogou {carta['emoji']} {carta['nome']}")
            pausa(0.7)
        atacar(e, atual, outro)
        if outro["pv"] <= 0 or turno >= 40:
            break
        atual, outro = outro, atual
    venceu = atual if outro["pv"] <= 0 else (e["J"] if e["J"]["pv"] >= e["C"]["pv"] else e["C"])
    print(f"\n{NEG}{'🏆 Você venceu!' if venceu['humano'] else '🤖 A CPU venceu.'}{FIM}")


if __name__ == "__main__":
    try:
        while True:
            partida()
            if input("\nJogar de novo? (s/n): ").strip().lower() != "s":
                break
    except (EOFError, KeyboardInterrupt):
        print("\nAté a próxima!")
