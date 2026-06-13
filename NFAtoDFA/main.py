# -*- coding: utf-8 -*-
"""Conversor de AFN-ε para AFD (construção de subconjuntos) com teste de palavras.

Formato do arquivo de entrada (NFA):
    linha 1: estados separados por espaço          ex.: A B C D
    linha 2: estado inicial                         ex.: A
    linha 3: estados finais separados por espaço    ex.: E
    demais : transições "origem símbolo destino"    ex.: A 1 B

O símbolo de transição-épsilon é "h" (configurável em EPSILON).

Uso:
    python main.py                                  # usa nfa.txt / words.txt
    python main.py --nfa outro.txt --words p.txt
"""
import argparse
from collections import defaultdict, deque

EPSILON = "h"


def read_nfa(path):
    """Lê o AFN do arquivo. Retorna (inicial, finais, transições, alfabeto)."""
    with open(path, encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    initial = lines[1]
    finals = set(lines[2].split())
    transitions = defaultdict(set)
    alphabet = set()
    for line in lines[3:]:
        origin, symbol, dest = line.split()
        transitions[(origin, symbol)].add(dest)
        if symbol != EPSILON:
            alphabet.add(symbol)
    return initial, finals, transitions, sorted(alphabet)


def epsilon_closure(transitions, states):
    """Conjunto de estados alcançáveis a partir de `states` só por transições-ε."""
    closure = set(states)
    stack = list(states)
    while stack:
        current = stack.pop()
        for nxt in transitions.get((current, EPSILON), ()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return frozenset(closure)


def move(transitions, states, symbol):
    """ε-fecho do conjunto alcançado a partir de `states` lendo `symbol`."""
    reached = set()
    for state in states:
        reached |= transitions.get((state, symbol), set())
    return epsilon_closure(transitions, reached)


def nfa_to_dfa(initial, finals, transitions, alphabet):
    """Construção de subconjuntos. Cada estado do AFD nomeia o subconjunto do AFN."""
    def name(states):
        return "{" + ",".join(sorted(states)) + "}" if states else "∅"

    start = epsilon_closure(transitions, {initial})
    dfa_transitions = {}
    dfa_finals = set()
    seen = {start}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current & finals:
            dfa_finals.add(name(current))
        for symbol in alphabet:
            target = move(transitions, current, symbol)
            if not target:
                continue
            dfa_transitions[(name(current), symbol)] = name(target)
            if target not in seen:
                seen.add(target)
                queue.append(target)

    states = sorted(name(s) for s in seen)
    return states, name(start), dfa_finals, dfa_transitions


def accepts(word, initial, finals, transitions):
    """True se o AFD aceita `word`."""
    state = initial
    for symbol in word:
        state = transitions.get((state, symbol))
        if state is None:
            return False
    return state in finals


def save_dfa(path, states, initial, finals, transitions):
    with open(path, "w", encoding="utf-8") as file:
        file.write(" ".join(states) + "\n")
        file.write(initial + "\n")
        file.write(" ".join(sorted(finals)) + "\n")
        for (state, symbol), dest in sorted(transitions.items()):
            file.write(f"{state} {symbol} {dest}\n")


def main():
    parser = argparse.ArgumentParser(description="Conversor AFN-ε → AFD")
    parser.add_argument("--nfa", default="nfa.txt")
    parser.add_argument("--words", default="words.txt")
    parser.add_argument("--out", default="output.txt")
    parser.add_argument("--results", default="results.txt")
    args = parser.parse_args()

    initial, finals, transitions, alphabet = read_nfa(args.nfa)
    states, dfa_initial, dfa_finals, dfa_transitions = nfa_to_dfa(
        initial, finals, transitions, alphabet)
    save_dfa(args.out, states, dfa_initial, dfa_finals, dfa_transitions)

    print(f"AFD: {len(states)} estados · alfabeto {alphabet}")
    print(f"Inicial: {dfa_initial}")
    print(f"Finais : {', '.join(sorted(dfa_finals)) or '(nenhum)'}\n")

    with open(args.words, encoding="utf-8") as file:
        words = [w.strip() for w in file if w.strip()]
    results = []
    for word in words:
        ok = accepts(word, dfa_initial, dfa_finals, dfa_transitions)
        results.append(f"{word}: {'aceita' if ok else 'rejeitada'}")

    with open(args.results, "w", encoding="utf-8") as file:
        file.write("\n".join(results) + "\n")
    print("\n".join(results))


if __name__ == "__main__":
    main()
