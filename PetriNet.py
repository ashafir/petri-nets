#!/usr/bin/python3

class PetriNet:
    """
    Simplest basic structure implementind the Petri net
    functionality. The class PetriNet is used here as namespace
    only. The code patternn demonstrated here can not be used for
    running multiple instances of the same model with different states
    of their markings. So, it’s essentially a pattern for creating a
    single Petri net model. All arcs have a weight of 1.
    """

    places = {}
    transitions = {}

    class Place:
        """
        Base class for modelling places. Can be used as is or as a
        base for richer functionaly if there will be something other
        than the token counter needed.
        """
        def __init__(self, tokens=0):
            self.tokens = tokens

    class Transition:
        """ Base class for modelling transitions. """

        def __init__(self, input, output):
            self.input = input
            self.output = output

        def fire(self):
            "Fire the transition."
            if not self.enabled:
                raise RuntimeError('attempt to fire disabled transition')

            for x in self.input:    # Remove tokens from input places
                x.tokens -= 1

            # Calling any transition processing needed. Supposed to be
            # implemented in the derived class
            self.process()

            for x in self.output:   # Assing tokens to output places
                x.tokens += 1

        def process(self):
            """
            Supposed to be implemented in the derived class. Just a
            placeholder method here.
            """
            print('transition processing is supposed to be implemented '
                  'in the derived class')

        @property
        def enabled(self):
            "Is transition enabled?"
            return all([x.tokens for x in self.input])

    @classmethod
    def markings(cls):
        "Returns a dictionary of places with token counter values"
        return {k: v.tokens for (k, v) in PetriNet.places.items()}

    @classmethod
    def enabled(cls):
        "Returns a dictionary of enabled transitions"
        return {k: v for (k, v) in PetriNet.transitions.items() if v.enabled}

    @classmethod
    def reset(cls, **kwargs):
        """Initializing the model and assigning initial markings."""
        if not PetriNet.places:
            for key, value in cls.__dict__.items():
                if isinstance(value, PetriNet.Place):
                    PetriNet.places[key] = value
        if not PetriNet.transitions:
            for key, value in cls.__dict__.items():
                if isinstance(value, PetriNet.Transition):
                    PetriNet.transitions[key] = value
        for key, value in kwargs.items():
            if key in PetriNet.places:
                PetriNet.places[key].tokens = value
            else:
                raise NameError(f'place {key} not found')


# Classic example taken from
# http://people.cs.pitt.edu/~chang/231/y16/231sem/semObrien.pdf
class CandyMachine(PetriNet):
    """ It's just a namespace containing the model graph. """

    # Places:
    start = PetriNet.Place(1)
    five = PetriNet.Place()
    ten = PetriNet.Place()
    fifteen = PetriNet.Place()
    twenty = PetriNet.Place()

    # Transitions:
    payFive1 = PetriNet.Transition(input=[start], output=[five])
    payFive2 = PetriNet.Transition(input=[five], output=[ten])
    payFive3 = PetriNet.Transition(input=[ten], output=[fifteen])
    payFive4 = PetriNet.Transition(input=[fifteen], output=[twenty])
    payTen1 = PetriNet.Transition(input=[start], output=[ten])
    payTen2 = PetriNet.Transition(input=[five], output=[fifteen])
    payTen3 = PetriNet.Transition(input=[ten], output=[twenty])
    buyFifteen = PetriNet.Transition(input=[fifteen], output=[start])
    buyTwenty = PetriNet.Transition(input=[twenty], output=[start])


if __name__ == '__main__':
    # Set initial markings:
    CandyMachine.reset(start=1)
    while True:
        print(CandyMachine.markings())
        enabled = CandyMachine.enabled()
        print(list(enabled.keys()))

        # First emabled transition fired. Other strategies possible
        # depending upon which pattern of handling concurrency will be
        # used.
        enabled = list(enabled.items())
        if enabled:
            name, transition = enabled[0]
            print(f'will fire transition {name}')
            transition.fire()
        else:
            print('no enabled transitions')
            break

        input('Press RETURN to continue:')
