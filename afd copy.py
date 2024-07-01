from afnd import AFND, State

class AFD(AFND):

    def __init__(self, path) -> None:
        self.afd = AFND()
        super().__init__()
        self.afd.fromFile(path)
        self.__determine()
    
    def __determine(self):
        while True:
            new_state = None
            nd_transition = None
            for state in self.afd.states.values():
                non_deterministic = False
                for transition in state.transitions.values(): # para cada transicao por um simbolo
                    if (transition is not None and len(transition) > 1): # se tiver >1 transicao por simbolo
                        nd_transition = [t for t in transition]
                        state_ids = [str(s.id) for s in transition]
                        new_state = State(id=f"[{', '.join(state_ids)}]")
                        transition.clear()
                        transition.append(new_state)
                        #print(transition)
                        non_deterministic = True
                        break
                if(non_deterministic): break
            if (new_state is not None):
                self.afd.addState(new_state)
            else:
                break # determinizado
            for state in nd_transition: # adiciona transicoes dos states que compoem ao novo state
                for symbol, transition in self.afd.states[state.id].transitions.items():
                    for target_state in transition:
                        self.afd.states[new_state.id].addTransition(symbol, target_state)
                if (self.afd.states[state.id].final):
                    new_state.final = True
            for state in nd_transition:
                self.afd.states.pop(state.id)
        self.afd.printWithError()