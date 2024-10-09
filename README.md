# NFA to DFA Converter

This project implements a converter that transforms a Non-deterministic Finite Automaton (NFA) with epsilon transitions into a Deterministic Finite Automaton (DFA). The conversion process is performed using Python, and the results can be tested against a set of input words.

## Features

- Reads NFA definitions from a text file.
- Converts the NFA into a DFA while handling epsilon transitions.
- Saves the resulting DFA to an output text file.
- Tests a list of input words against the DFA and records which words are accepted or rejected.
- Outputs the results to a separate text file.

## File Format

### NFA Input File (`nfa.txt`)

The NFA input file must be formatted as follows:

1. **States**: A single line containing all the states, separated by spaces.
2. **Initial State**: A single line with the initial state.
3. **Final States**: A single line containing all final states, separated by spaces.
4. **Transitions**: Each subsequent line should define a transition in the format:
   ```
   state symbol next_state
   ```
   where:
   - `state`: Current state.
   - `symbol`: Input symbol (including 'h' for epsilon transitions).
   - `next_state`: Next state resulting from the transition.

### DFA Output File (`output.txt`)

The DFA output file will be formatted as follows:

1. **States**: A single line containing all DFA states, separated by spaces.
2. **Initial State**: A single line with the DFA's initial state.
3. **Final States**: A single line containing all final states of the DFA, separated by spaces.
4. **Transitions**: Each subsequent line defines a transition in the format:
   ```
   state symbol next_state
   ```

### Word List Input File (`words.txt`)

The word list input file should contain each word on a new line. These words will be tested against the DFA.

### Results Output File (`results.txt`)

The results output file will contain the acceptance results for each word, formatted as:
```
word accepted
word **rejected**
```

## Usage

1. Place the required input files (`nfa.txt` and `words.txt`) in the project directory.
2. Run the `main` function in the script.
   ```bash
   python your_script.py
   ```
3. After execution, check the `output.txt` and `results.txt` files for the DFA definition and word testing results, respectively.



