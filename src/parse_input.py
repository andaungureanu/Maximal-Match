import itertools
from DFA import DFA
import re


def parse(input_file):
    file = open(input_file, "r")
    text = file.readlines()
    auto = []

    while text:
        alphabet = []
        states = set()
        fin_states = set()
        for alpha in text[0]:
            if alpha == "\\n":
                alphabet.append("\\n")
            elif alpha != '\n':
                alphabet.append(alpha)  # alfabetul
            else:
                break
        for i in range(len(alphabet)):
            if alphabet[i] == "\\" and alphabet[i + 1] == "n":
                alphabet[i] = "\n"
                alphabet.pop(i + 1)
                break
        name = text[1]
        name = name[:-1]  # numele
        init_state = text[2][0]  # starea initiala
        new_text = text[3:]
        for line in new_text:
            if ',' not in line:
                break
            regex_pattern = r"[,']"
            aux = re.split(regex_pattern, line)
            states.add(int(aux[0]))
            states.add(int(aux[4]))  # toate starile pentru dictionar
        merged = itertools.product(states, sorted(alphabet))
        delta = dict.fromkeys(merged)
        text = text[3:]
        for line in text:
            if ',' not in line:
                break
            regex_pattern = r"[,']"
            aux = re.split(regex_pattern, line)
            delta[int(aux[0]), aux[2]] = int(aux[4])  # contruiesc dictionarul
            text = text[1:]
        for key in delta:
            if delta[key] is None:
                delta[key] = key[0]  # unde nu am tranzitie in input inseamna ca starea ramane aceeasi
        aux = text[0].split()
        for elem in aux:
            if elem != '\n':
                fin_states.add(int(elem))  # starile finale
        auto.append(DFA(sorted(alphabet), delta, init_state, fin_states, name))
        text = text[2:]
    return auto
