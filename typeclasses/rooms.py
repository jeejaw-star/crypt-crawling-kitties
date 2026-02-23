"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    pass
from typeclasses.rooms import Room as DefaultRoom
from evennia.utils.utils import delay
from evennia import create_script
class MonsterRoom(DefaultRoom):
    """
    A room that automatically manages monster spawning via a script.
    """
    def at_object_creation(self):
        """
        Called when the room is first created.
        """
        super().at_object_creation()
        # Create and attach the spawner script
        # The script will handle the timing logic itself
        create_script("typeclasses.scripts.MonsterSpawnerScript", obj=self)

    def at_object_delete(self):
        """
        Ensures the script is cleaned up if the room is deleted.
        """
        # Find and delete the spawner script
        for script in self.scripts.all():
            if script.key == "monster_spawner":
                script.delete()
        super().at_object_delete()