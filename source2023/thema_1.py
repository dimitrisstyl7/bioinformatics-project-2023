import math


def viterbi_algorithm():
    """
    Returns the optimal path through the hidden states for the given observations.
    """
    # Initialization
    first_obs = observation[0]  # first observation
    score_a = math.log2(emissions[first_obs]['a']) + math.log2(initial_state_probabilities[0])
    score_b = math.log2(emissions[first_obs]['b']) + math.log2(initial_state_probabilities[1])

    # Choosing the first state
    if score_a >= score_b:
        transition_path = 'a'
    else:
        transition_path = 'b'

    print("score_a: {}, score_b: {}".format(score_a, score_b))
    # Computing the optimal path
    for i in range(1, len(observation)):
        obs = observation[i]
        score_a = math.log2(emissions[obs]['a']) + max(math.log2(
            transitions['a']['a']) + score_a, math.log2(transitions['b']['a']) + score_b)
        score_b = math.log2(emissions[obs]['b']) + max(math.log2(
            transitions['a']['b']) + score_a, math.log2(transitions['b']['b']) + score_b)

        # Choosing the next state
        if score_a >= score_b:
            state_to_add = 'a'
        else:
            state_to_add = 'b'
        print("score_a: {}, score_b: {}".format(score_a, score_b))
        # Adding the next state to the transition path
        transition_path += state_to_add
    return transition_path


if __name__ == '__main__':
    observation = 'GGCT'
    first_observation = observation[0]

    """
    Initial state probabilities:
        Matrix representation: [p(a), p(b)]
        We choose the initial state probabilities to be 0.5 for each state.
        This means that we have no prior knowledge of the initial state of the system.
    """
    initial_state_probabilities = [0.5, 0.5]

    """
    Emission probabilities:  
        Dictionary representation: {emission: {state: probability}}
        e(A|a) = probability of emitting A when in state a.
        e(A|b) = probability of emitting A when in state b.
        e(G|a) = probability of emitting G when in state a.
        e(G|b) = probability of emitting G when in state b.
        e(T|a) = probability of emitting T when in state a.
        e(T|b) = probability of emitting T when in state b.
        e(C|a) = probability of emitting C when in state a.
        e(C|b) = probability of emitting C when in state b.        
    """
    emissions = {
        'A': {'a': 0.4, 'b': 0.2},
        'G': {'a': 0.4, 'b': 0.2},
        'T': {'a': 0.1, 'b': 0.3},
        'C': {'a': 0.1, 'b': 0.3}
    }

    """
    Transition probabilities (markov chain):
        Dictionary representation: {state: {state: probability}}
        p(a|a) = probability of transition from state a to state a.
        p(a|b) = probability of transition from state b to state a.
        p(b|a) = probability of transition from state a to state b.
        p(b|b) = probability of transition from state b to state b.
    """
    transitions = {
        'a': {'a': 0.9, 'b': 0.1},
        'b': {'a': 0.1, 'b': 0.9}
    }

    transitions_path = viterbi_algorithm()
    print(f'Optimal path through the hidden states: {transitions_path}')
