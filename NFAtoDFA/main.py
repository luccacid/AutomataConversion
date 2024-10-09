from collections import defaultdict, deque

def read_nfa_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    states = lines[0].strip().split()
    initial_state = lines[1].strip()
    final_states = lines[2].strip().split()
    
    transitions = defaultdict(list)
    for line in lines[3:]:
        state, symbol, next_state = line.strip().split()
        transitions[(state, symbol)].append(next_state)
    
    return states, initial_state, final_states, transitions

def epsilon_closure(transitions, state):
    closure = {state}
    stack = [state]

    while stack:
        current = stack.pop()
        if (current, 'h') in transitions:  
            for next_state in transitions[(current, 'h')]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    
    return closure

def convert_to_dfa(nfa_states, initial_state, final_states, transitions):
    initial_closure = epsilon_closure(transitions, initial_state)
    dfa_states = {frozenset(initial_closure): ''.join(sorted(initial_closure))}  
    state_count = 1
    dfa_transitions = {}
    dfa_final_states = set()
    
    unmarked_states = deque([frozenset(initial_closure)])
    
    while unmarked_states:
        current_set = unmarked_states.popleft()
        dfa_current_state = dfa_states[current_set]

        for symbol in ['0', '1']:  
            next_states = set()
            for state in current_set:
                if (state, symbol) in transitions:
                    for next_state in transitions[(state, symbol)]:
                        next_states.update(epsilon_closure(transitions, next_state))
            
            if next_states:
                next_states_frozenset = frozenset(next_states)
                if next_states_frozenset not in dfa_states:
                    dfa_states[next_states_frozenset] = ''.join(sorted(next_states)) 
                    unmarked_states.append(next_states_frozenset)
                
                dfa_transitions[(dfa_current_state, symbol)] = dfa_states[next_states_frozenset]
    
    for state_set, dfa_state in dfa_states.items():
        if any(state in final_states for state in state_set):
            dfa_final_states.add(dfa_state)

    return list(dfa_states.values()), dfa_states[frozenset(initial_closure)], list(dfa_final_states), dfa_transitions

def save_dfa(file_path, dfa_states, initial_state, dfa_final_states, dfa_transitions):
    with open(file_path, 'w') as file:
        file.write(' '.join(dfa_states) + '\n')  
        file.write(initial_state + '\n')         
        file.write(' '.join(dfa_final_states) + '\n') 
        
        for (state, symbol), next_state in dfa_transitions.items():
            file.write(f"{state} {symbol} {next_state}\n")  

def test_words(dfa_states, dfa_transitions, initial_state, dfa_final_states, words_file):
    with open(words_file, 'r') as file:
        words = file.readlines()

    results = []
    for word in words:
        word = word.strip()
        current_state = initial_state
        
        for symbol in word:
            if (current_state, symbol) in dfa_transitions:
                current_state = dfa_transitions[(current_state, symbol)]
            else:
                current_state = None
                break
        
        if current_state and current_state in dfa_final_states:
            results.append(f"{word} accepted")
        else:
            results.append(f"{word} **rejected**")
    
    return results

def save_results(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')

def display_dfa(dfa_states, dfa_final_states, dfa_transitions):
    print("DFA States:")
    print(", ".join(dfa_states))
    
    print("\nDFA Final States:")
    print(", ".join(dfa_final_states))
    
    print("\nDFA Transitions:")
    for (state, symbol), next_state in dfa_transitions.items():
        print(f"  {state} --{symbol}--> {next_state}")


def main():
    nfa_file = "nfa.txt"
    dfa_file = "output.txt"
    words_file = "words.txt"
    results_file = "results.txt"  
    
   
    nfa_states, initial_state, final_states, transitions = read_nfa_file(nfa_file)
    
    
    dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions = convert_to_dfa(nfa_states, initial_state, final_states, transitions)
    
   
    save_dfa(dfa_file, dfa_states, dfa_initial_state, dfa_final_states, dfa_transitions)

    
    display_dfa(dfa_states, dfa_final_states, dfa_transitions)

    
    results = test_words(dfa_states, dfa_transitions, dfa_initial_state, dfa_final_states, words_file)
    
    
    save_results(results, results_file)

    print("\nResults of the words:")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
