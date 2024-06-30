from afnd import AFND, State

class AFD(AFND):

    def __init__(self) -> None:
        self.afd = AFND()
        super().__init__()
        self.__determine()
    
    def __determine(self):
        while True:
            new_state = None
            transition_nd = None
            for state in self.afd.states.values():
                non_deterministic = False
                for transition in state.transitions.values(): # para cada transicao por um simbolo
                    if (transition is not None and len(transition) > 1): # se tiver >1 transicao por simbolo
                        transition_nd = [t for t in transition]
                        new_state = State(id=f"[{', '.join(transition)}]")
                        transition.clear()
                        transition.append(new_state.id)
                        non_deterministic = True
                        break
                if(non_deterministic): break
            if (new_state is not None):
                self.afd.addState(new_state)
            else: break # determinizado
            for state in transition_nd: # adiciona transicoes dos states que compoem ao novo state
                for simbolo, transition in self.states[state].transitions.items():
                    for state_destino in transition:
                        self.states[new_state.id].adcTransicao(simbolo, state_destino)
                if (self.states[state].final):
                    new_state.final = True
            for state in transition_nd:
                self.states.pop(state)