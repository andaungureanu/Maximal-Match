from parse_input import parse


def runlexer(lex_file, in_file, out_file):
    auto = parse(lex_file)
    file = open(in_file, "r")
    text = file.readlines()
    string_default = ""
    alphabet = set()
    out = open(out_file, "w+")
    for elem in text:
        string_default = string_default + elem
    string = "" + string_default
    for automata in auto:
        automata.find_sink()
        for char in automata.alpha:
            alphabet.add(char)
    result = ""
    auto_states = []
    another_ok = 0
    copy = ""
    no_of_letters = 0
    word = ""
    if string[0] not in alphabet:  # daca prima litera nu este in alfabetul niciunuia dintre automate, cuvantul e
        # respins din start
        result = "No viable alternative at character " + str(0) + ", line 0"
        out.write(result)
        return
    while string:
        index_of_auto = 1000
        word = ""
        auto_states = []
        initial = []
        copy = "" + string
        for dfa in auto:  # toate automatele se afla in starea 0, gasesc urmatoarele stari in care se duc + daca
            # acestea sunt stari finale (accept), stari de sink din care nu mai pot iesi (reject) sau alte stari (seeking)
            next_state = dfa.next_config((dfa.init_state, copy))[0]
            if copy[0] not in dfa.alpha:
                initial.append((next_state, "r"))  # daca nu e litera in alfabetul automatului
            elif next_state in dfa.fin_states:
                initial.append((next_state, "a"))  # accept
            elif next_state in dfa.sink:
                initial.append((next_state, "r"))  # reject
            else:
                initial.append((next_state, "s"))  # seeking
        auto_states.append(initial)
        if copy[0] == "\n":
            word = word + "\\n"
        else:
            word = word + copy[0]
        copy = copy[1:]
        while copy:
            ok = 0
            for state in auto_states[-1]:  # verific daca ultimele stari ale automatelor sunt reject toate
                if state[1] != "r":
                    ok = 1
                    break
            if ok == 0:  # daca da, dau break si merg la cautarea ultimului cuvant acceptat
                break
            new_entry = []
            for dfa in auto:  # daca nu, continui sa aflu urmatoarele stari in care merg automatele
                index = auto.index(dfa)
                next_state = dfa.next_config((auto_states[-1][index][0], copy))[0]
                if copy[0] not in dfa.alpha:
                    new_entry.append((next_state, "r"))  # daca nu e litera in alfabetul automatului
                elif next_state in dfa.fin_states:
                    new_entry.append((next_state, "a"))
                elif next_state in dfa.sink or next_state == 'n':
                    new_entry.append((next_state, "r"))
                else:
                    new_entry.append((next_state, "s"))
            auto_states.append(new_entry)
            if copy[0] == "\n":
                word = word + "\\n"
            else:
                word = word + copy[0]
            copy = copy[1:]
        another_copy = auto_states.copy()
        another_copy.reverse()
        another_ok = 0
        for states in another_copy:  # parcurg de la final spre inceput pentru a gasi ultimul accept
            for elem in states:
                if elem[1] == "a":
                    no_of_letters = len(auto_states) - another_copy.index(states)
                    index_of_auto = states.index(elem)
                    another_ok = 1  # am gasit, trebuie sa ies si din for-ul mare
                    break  # break pentru prioritate (de ex, daca si A3 si A5 accepta, voi alege A3)
            if another_ok == 1:
                break
        if another_ok == 0:  # nu am avut niciun accept
            break
        if word.startswith("\\n"):
            result = result + str(auto[index_of_auto].name) + " " + word[:no_of_letters + 1] + "\n"
        else:
            result = result + str(auto[index_of_auto].name) + " " + word[:no_of_letters] + "\n"
        string = string[no_of_letters:]
    if another_ok == 0:  # nu mai avem niciun accept => nu putem desparti in lexeme
        if len(copy) == 0:  # daca am ajuns la finalul sirului
            for state in auto_states[-1]:
                if state[1] == 's':  # daca vreun automat este inca in seeking
                    result = "No viable alternative at character EOF, line 0"
                    out.write(result)
                    return
            # daca toate automatele sunt pe reject
            result = "No viable alternative at character " + str(len(string_default) - len(word)) + ", line 0"
            out.write(result)
            return
        else:  # daca sunt undeva in interiorul sirului
            result = "No viable alternative at character " + str(len(string_default) - len(copy) - len(word) + 1) + ", line 0"
            out.write(result)
            return
    else:
        out.write(result[:-1])




