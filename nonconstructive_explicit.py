from typing import List, Union, Dict, TypeVar
import random
import numpy
import matplotlib.pyplot

Molecule = TypeVar("Molecule")

class Molecule:
    """
    A single molecule, represented by a symbol (e.g. A, B)
    """

    def __init__(self, name):
        self.name = name

    @staticmethod
    def molecules_to_amounts(all_molecules: List[Molecule], molecules: List[Molecule]) -> Dict[Molecule, int]:
        """
        Turn a list of single Molecules such as [A, A, B, A, B] into a dict of amounts,
        such as {A: 3, B:2}. Use all_molecules so that molecules which aren't present
        will be set to zero rather than lost.
        """
        molecule_amounts = {}
        for type_of_molecule in all_molecules:
            molecule_amounts[type_of_molecule] = 0
        for molecule in molecules:
            molecule_amounts[molecule] += 1

        return molecule_amounts

    def __str__(self):
        return self.name

class Reaction:
    """
    A single reaction rule, thought of as a1s1 + a2s2 [...] -> b1s1 + b2s2 [...]
    However, because of the limited nonconstructive rules, we can pass product as
    the single additional molecule produced, in addition to the reactants which
    we know will remain the same.
    """

    def __init__(self, reactants_needed: Dict[Molecule, int], product: Molecule):
        self.reactants_needed = reactants_needed
        self.product = product
    
    def can_occur(self, reactants_amounts: Dict[Molecule, int]):
        # Test if the reactants_amounts provided is sufficient for this rule to occur
        for reactant, amount in reactants_amounts.items():
            if amount < self.reactants_needed[reactant]:
                return False
        else:
            return True

class Vessel:
    """
    Simulate a reaction vessel with explicit stochastic reactions. The simulation
    is "nonconstructive" because total number of molecules is kept constant.
    """
    
    def __init__(self, molecule_types: List[Molecule], molecule_amounts: Dict[Molecule, int], reactions: List[Reaction]):
        # Store a list "molecule_types" to keep track of all possible molecules in the simulation.
        self.molecule_types = molecule_types

        # Store a list "molecules" where each item is a single Molecule, based on the
        # number of each provided by molecule_amounts.
        self.molecules = []
        for molecule, amount in molecule_amounts.items():
            self.molecules.extend(molecule for _ in range(amount))
        
        # Store a list "reactions" where each item is a Reaction rule.
        self.reactions = reactions
    
    def simulate_step(self, number_to_select):
        # Select number_to_select molecules at random
        reactants = random.sample(self.molecules, number_to_select)
        reactants_amounts = Molecule.molecules_to_amounts(self.molecule_types, reactants)
        
        # Find the reaction rule that can occur, and carry it out
        for reaction in self.reactions:
            if reaction.can_occur(reactants_amounts):
                product = reaction.product
                self.molecules[random.randrange(len(self.molecules))] = product
                break


def simulate_basic():
    # Initialize with the molecules described on page 232/233.
    all_molecules = [Molecule("A"), Molecule("B")]
    initial_amount_each = 5000
    total_amount = initial_amount_each * len(all_molecules)
    molecule_amounts = {molecule:initial_amount_each for molecule in all_molecules}

    # Create the reaction table shown on page 232.
    reactions = []
    for i in range(2):
        for j in range(2):
            reactants = [all_molecules[i], all_molecules[j]]
            reactants_amounts = Molecule.molecules_to_amounts(all_molecules, reactants)
            product = all_molecules[0 if i and j else 1]
            reactions.append(Reaction(reactants_amounts, product))

    # Initialize the reaction vessel
    vessel = Vessel(all_molecules, molecule_amounts, reactions)

    # Set number of reactions to carry out before ending the simulation.
    iters = 4*total_amount

    # Initialize graph of population that will update each step.
    plot_A, = matplotlib.pyplot.plot([0], [initial_amount_each], marker=None)
    plot_B, = matplotlib.pyplot.plot([0], [initial_amount_each], marker=None)
    matplotlib.pyplot.title(f"Population Size M={total_amount}")
    matplotlib.pyplot.xlim(0, iters)
    matplotlib.pyplot.ylim(30, 70)
    matplotlib.pyplot.xlabel("Step")
    matplotlib.pyplot.ylabel("Concentration (%)")

    for i in range(iters):
        # Simulate a step, selecting 2 molecules at random to react, like in the paper.
        vessel.simulate_step(2)

        # Calculate the resulting percentage concentrations after this step
        amounts_each = Molecule.molecules_to_amounts(all_molecules, vessel.molecules)
        percentages_each = [amount * 100.0 / total_amount for amount in amounts_each.values()]
        plot_A.set_xdata(numpy.append(plot_A.get_xdata(), [i+1]))
        plot_A.set_ydata(numpy.append(plot_A.get_ydata(), [percentages_each[0]]))
        plot_B.set_xdata(numpy.append(plot_B.get_xdata(), [i+1]))
        plot_B.set_ydata(numpy.append(plot_B.get_ydata(), [percentages_each[1]]))

        # Only graph this new data on the chart every so often, to avoid too much wasted processing power.
        if i%(total_amount/10) != 0:
            continue
        
        matplotlib.pyplot.draw()
        matplotlib.pyplot.pause(0.00001)

if __name__ == "__main__":
    simulate_basic()
    print("Simulation complete!")
    matplotlib.pyplot.show()