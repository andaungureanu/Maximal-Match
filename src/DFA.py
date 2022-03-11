class DFA:
    def __init__(self, alpha, delta, init_state, fin_states, name):
        self.alpha = alpha
        self.delta = delta
        self.init_state = init_state
        self.fin_states = fin_states
        self.name = name
        self.sink = []

    def next_config(self, current):
        current_state = current[0]
        if current[1][0] == "\n":
            current_letter = "\\n"
        else:
            current_letter = current[1][0]
        next_word = current[1][1:]
        if current_state == 'n' or current_state is None:
            return "nothing"
        else:
            pair = (int(current_state), current_letter)
            if pair in self.delta:
                next_state = self.delta[pair]
                return next_state, next_word
            else:
                return "nothing"

    def find_sink(self):
        no_of_states = len(self.delta) / len(self.alpha)
        cycle = [int(0)] * int(no_of_states)
        for key in self.delta:
            if self.delta[key] == key[0]:
                cycle[key[0]] += 1
        for elem in cycle:
            if elem == len(self.alpha):
                self.sink.append(cycle.index(elem))