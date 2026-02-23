from typeclasses.objects import Object
class Monster(Object):

    

    def move_around(self):
        print(f"{self.key} is moving!")
class Dragon(Monster):
    """
    This is a dragon monster.
    """

    def move_around(self):
        super().move_around()
        print("The earth trembles.")

    def firebreath(self):
        """
        Let our dragon breathe fire.
        """
        print(f"{self.key} breathes fire!")
