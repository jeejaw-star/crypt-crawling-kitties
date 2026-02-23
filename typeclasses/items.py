from typeclasses.objects import Object
from evennia import utils
class Coin(Object):
    key="coin"
    def on_object_creation(self):
        self.db.desc = "This is a rusty gold coin."
class Sign(Object):
    def on_object_creation(self):
        self.db.text = "placeholder text"
class Sword(Object):
    key="sword"
    def on_object_creation(self):
        self.db.desc = "This is a sword."
class LogBook(Object):
    def on_object_creation(self):
        self.db.text = "Write text in me!"
        self.db.is_writable=True
class MagicStone(Object):
    key = "magic stone"
    def on_object_creation(self):
        self.db.health = 10
        self.db.get_err_message = "As you bend over to get it, it sends out a burst of heat, startling you."
        self.locks.add("get:false()")
    def msg(self, text,from_obj=None, data=None,**kwargs):
        for thing in self.location.contents:
            if thing != self:
                thing.msg(f"The stone yells in a squeaky voice '{text}'")
class Key(Object):
    def on_object_creation(self):
        self.is_key = True
class Boat(Object):
    """
    This is the boat object typeclass.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.is_boat = True
        self.locks.add("get:all()") # assuming the boat can be picked up
class FakeCrystal(Object):
    def at_pick_up(self, player, **kwargs):
        # This method is called when the item is picked up
        # Call the parent class's at_pick_up method to handle default behavior

        # Get the destination from an attribute on the item

        destination = utils.search_object("The Cat Inn")
        if not destination:
            player.msg("You cannot teleport to the destination.")
            return

        # Move the player to the destination
        player.move_to(destination)

        # Send a message to the player
        player.msg("As you reach for the world crystal, the world blurs around you and you teleport to the cat inn.")