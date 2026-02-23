"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""

from evennia.objects.objects import DefaultExit

from .objects import ObjectParent


class Exit(ObjectParent, DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property and overrides some hooks
    and methods to represent the exits.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects child classes like this.

    """

    pass
class DimensionalPortal(Exit):
    def at_traverse(self,traversing_object,destination, **kwargs):
        traversing_object.msg("As you slip into the warped air, a sudden force buffers you, twisting, turning, stretching, flattening. Gasping, you stumble out the other side.")
        self.location.msg_contents(f"{traversing_object.name} slips into a warped section of air.", exclude=traversing_object)
        super().at_traverse(traversing_object,destination,**kwargs)
        destination.msg_contents(f"{traversing_object.name} arrives, gasping, out of thin air.",exclude=traversing_object)

