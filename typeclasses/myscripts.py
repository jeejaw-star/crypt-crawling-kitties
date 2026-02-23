import random
from evennia import DefaultScript
class Weather(DefaultScript):
        """
        A timer script that displays weather info. Meant to
        be attached to a room.
          
        """
        def at_script_creation(self):
            self.key = "weather_script"
            self.desc = "Gives random weather messages."
            self.interval = 60 * 5  # every 5 minutes
            self.persistent = True  # will survive reload

        def at_repeat(self):
            "called every self.interval seconds."
            rand = random.random()
            if rand < 0.5:
                weather = "A faint breeze is felt."
            elif rand < 0.7:
                weather = "Clouds sweep across the sky."
            else:
                weather = "There is a light drizzle of rain."
                lightning = random.randint(1,100)
                if lightning == 1:
                    self.obj.msg_contents("Lightning strikes nearby, sending a jolt through your body.")
                    
            # send this message to everyone inside the object this
            # script is attached to (likely a room)
            self.obj.msg_contents(weather)

class HpBar(DefaultScript):
     def at_script_creation(self):
          self.key = "hp bar"
          self.desc= "This makes health bars update."
          self.interval=0.1
          self.persistant=True
     def at_repeat(self):
            import time
            from evennia.contrib.rpg.health_bar import display_meter
            health_bar = display_meter(self.db.health,100)
            self.msg(prompt=health_bar)
            if self.db.health <=0:
                self.account.msg("Everything fades to black.")
                self.account.move_to(2)
                time.sleep(10)
                self.account.msg("You wake up in the cat inn.")
                self.account.db.health = 100
from evennia.scripts.script import Script
from evennia.prototypes import spawner
from random import randint
from twisted.internet import task
from evennia.utils.utils import lazy_import

PROTOTYPES = lazy_import("world.prototypes")

class MonsterSpawnerScript(Script):
    """
    A script that spawns monsters in its location at random intervals.
    """
    def at_script_creation(self):
        """
        Called when script is first created.
        """
        self.key = "monster_spawner"
        self.desc = "Handles timed monster spawns."
        self.interval_min = 30  # Minimum spawn interval in seconds
        self.interval_max = 120 # Maximum spawn interval in seconds
        self.max_monsters = 3   # Maximum number of monsters in the room
        self.prototype_key = "goblin" # Key of the prototype to spawn

    def _spawn_monster(self):
        """
        Spawns a single monster in the script's location.
        """
        if not self.obj:
            return

        # Check current monster count in the room
        current_monsters = self.obj.contents_get(tag="mob")
        if len(current_monsters) >= self.max_monsters:
            return

        # Use the spawner to create a new monster
        prototype = getattr(PROTOTYPES, f"{self.prototype_key.upper()}_PROTOTYPE")
        if prototype:
            spawned_list = spawner.spawn(prototype)[0]
            if spawned_list:
                monster = spawned_list[0]
                monster.location = self.obj # Move the new monster to the room
                self.obj.msg_contents(f"A {monster.key} slithers out of the shadows!") # Notify room occupants

        # Schedule the next spawn
        self.start_next_timer()

    def start_next_timer(self):
        """
        Stops any existing timer and starts a new one with a random interval.
        """
        # Remove any existing delayed calls
        if hasattr(self, 'deferred') and self.deferred:
            self.deferred.cancel()
        
        # Determine random interval
        interval = randint(self.interval_min, self.interval_max)
        
        # Use Evennia's inline delayed events (Twisted's callLater)
        from evennia.utils.delays import delay
        self.deferred = delay(interval, self._spawn_monster)

    def at_start(self):
        """
        Starts the spawner timer when the script starts running.
        """
        self.start_next_timer()

    def at_stop(self):
        """
        Cleans up the timer when the script stops.
        """
        if hasattr(self, 'deferred') and self.deferred:
            self.deferred.cancel()

    def at_obj_move(self, moved_obj, old_location):
        """
        Optional: can add logic here to check if players are present and only spawn if they are.
        """
        pass