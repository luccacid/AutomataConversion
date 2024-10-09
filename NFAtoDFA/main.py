from collections import defaultdict, deque

def read_nfa_file(file_path):
    """Lê a definição de um NFA a partir de um arquivo de texto especificado."""
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Lê todas as linhas do arquivo
    
    # Extrai estados, estado inicial e estados finais do arquivo
    states = lines[0].strip().split()  # Primeiro linha contém os estados
    initial_state = lines[1].strip()    # Segunda linha contém o estado inicial
    final_states = lines[2].strip().split()  # Terceira linha contém os estados finais
    
    # Cria um dicionário para armazenar as transições
    transitions = defaultdict(list)
    # Lê as transições do arquivo e popula o dicionário de transições
    for line in lines[3:]:  # As linhas restantes contêm as transições
        state, symbol, next_state = line.strip().split()
        transitions[(state, symbol)].append(next_state)
    
    return states, initial_state, final_states, transitions  # Retorna estados, estado inicial, estados finais e transições

def epsilon_closure(transitions, state):
    """Calcula o fechamento épsilon para um estado dado."""
    closure = {state}  # Inicializa o conjunto de fechamento com o estado dado
    stack = [state]    # Pilha para a travessia em profundidade (DFS)

    # Realiza DFS para encontrar todos os estados acessíveis via transições épsilon
    while stack:
        current = stack.pop()  # Obtém o estado atual da pilha
        if (current, 'h') in transitions:  # 'h' representa transições épsilon
            for next_state in transitions[(current, 'h')]:
                if next_state not in closure:
                    closure.add(next_state)  # Adiciona ao fechamento se não estiver presente
                    stack.append(next_state)   # Continua explorando esse estado
    
    return closure  # Retorna o conjunto de fechamento épsilon

def convert_to_dfa(nfa_states, initial_state, final_states, transitions):
    """Converte o NFA dado em um DFA."""
    # Calcula o fechamento épsilon inicial
    initial_closure = epsilon_closure(transitions, initial_state)
    # Mapeia estados do DFA; usa frozenset para garantir unicidade
    dfa_states = {frozenset(initial_closure): ''.join(sorted(initial_closure))}
    dfa_transitions = {}
    dfa_final_states = set()  # Conjunto para os estados finais do DFA
    
    # Fila para estados não marcados (abordagem BFS)
    unmarked_states = deque([frozenset(initial_closure)])
    
    while unmarked_states:
        current_set = unmarked_states.popleft()  # Obtém o próximo estado não marcado
        dfa_current_state = dfa_states[current_set]  # Obtém o estado correspondente no DFA

        # Itera sobre os símbolos do alfabeto do DFA
        for symbol in ['0', '1']:  
            next_states = set()  # Conjunto para armazenar os próximos estados alcançados
            for state in current_set:
                # Verifica transições para o estado atual e símbolo
                if (state, symbol) in transitions:
                    for next_state in transitions[(state, symbol)]:
                        # Atualiza os próximos estados com seus fechamentos épsilon
                        next_states.update(epsilon_closure(transitions, next_state))
            
            if next_states:
                next_states_frozenset = frozenset(next_states)  # Cria um conjunto único para os próximos estados
                # Se esse novo estado ainda não foi encontrado
                if next_states_frozenset not in dfa_states:
                    dfa_states[next_states_frozenset] = ''.join(sorted(next_states)) 
                    unmarked_states.append(next_states_frozenset)  # Adiciona aos estados não marcados
                
                # Registra a transição no DFA
                dfa_transitions[(dfa_current_state, symbol)] = dfa_states[next_states_frozenset]
    
    # Identifica os estados finais no DFA
    for state_set, dfa_state in dfa_states.items():
        if any(state in final_states for state in state_set):
            dfa_final_states.add(dfa_state)  # Adiciona o estado ao conjunto de estados finais

    return list(dfa_states.values()), dfa_states[frozenset(initial_closure)], list(dfa_final_states), dfa_transitions  # Retorna estados do DFA, estado inicial, estados finais e transições

def save_dfa(file_path, dfa_states, initial_state, dfa_final_states, dfa_transitions):
    """Salva a definição do DFA em um arquivo de texto especificado."""
    with open(file_path, 'w') as file:
        file.write(' '.join(dfa_states) + '\n')  # Escreve todos os estados do DFA
        file.write(initial_state + '\n')         # Escreve o estado inicial
        file.write(' '.join(dfa_final_states) + '\n')  # Escreve todos os estados finais
        
        # Escreve as transições
        for (state, symbol), next_state in dfa_transitions.items():
            file.write(f"{state} {symbol} {next_state}\n")  # Formato: estado símbolo próximo_estado

def test_words(dfa_states, dfa_transitions, initial_state, dfa_final_states, words_file):
    """Testa uma lista de palavras contra o DFA e retorna os resultados."""
    with open(words_file, 'r') as file:
        words = file.readlines()  # Lê as palavras do arquivo

    results = []
    for word in words:
        word = word.strip()  # Remove caracteres de espaço e nova linha
        current_state = initial_state  # Começa no estado inicial
        
        # Processa cada símbolo na palavra
        for symbol in word:
            if (current_state, symbol) in dfa_transitions:
                current_state = dfa_transitions[(current_state, symbol)]  # Move para o próximo estado
            else:
                current_state = None  # Sem transição válida, marca como rejeitado
                break
        
        # Determina se o estado atual é um estado final
        if current_state and current_state in dfa_final_states:
            results.append(f"{word} accepted")  # Palavra aceita
        else:
            results.append(f"{word} **rejected**")  # Palavra rejeitada
    
    return results  # Retorna os resultados das palavras testadas

def save_results(results, output_file):
    """Salva os resultados de aceitação em um arquivo de saída especificado."""
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')  # Escreve cada resultado em uma nova linha

def display_dfa(dfa_states, dfa_final_states, dfa_transitions):
    """Exibe os estados do DFA, estados finais e transições."""
    print("DFA States:")
    print(", ".join(dfa_states))  # Imprime todos os estados do DFA
    
    print("\nDFA Final States:")
    print(", ".join(dfa_final_states))  # Imprime todos os estados finais do DFA
    
    print("\nDFA Transitions:")
    for (state, symbol), next_state in dfa_transitions.items():
        print(f"  {state} --{symbol}--> {next_state}")  # Imprime cada transição

def main():
    """Função principal para executar a conversão de NFA para DFA e testar palavras."""
    nfa_file = "nfa.txt"  # Caminho do arquivo de entrada para o NFA
    dfa_file = "output.txt"  # Caminho do arquivo de saída para o DFA
    words_file = "words.txt"  # Caminho do arquivo que contém as palavras a serem testadas
    results_file = "results.txt"  # Caminho do arquivo para salvar os resultados  
    
    # Lê o NFA do arquivo de entrada
    nfa_states, initial_state, final_states, transitions = read_nfa_file(nfa_file)
    
    # Converte o NFA para DFA
    dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions = convert_to_dfa(nfa_states, initial_state, final_states, transitions)
    
    # Salva o DFA no arquivo de saída
    save_dfa(dfa_file, dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions)

    # Exibe os detalhes do DFA no console
    display_dfa(dfa_states, dfa_final_states, dfa_transitions)

    # Testa palavras contra o DFA e obtém resultados
    results = test_words(dfa_states, dfa_transitions, dfa_initial_state, dfa_final_states, words_file)
    
    # Salva os resultados em um arquivo de resultados
    save_results(results, results_file)

    # Imprime os resultados dos testes das palavras
    print("\nResultados das palavras:")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()  # Executa a função principal
