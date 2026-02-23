# in mygame/commands/mycommands.py

from commands.command import Command
from evennia import CmdSet, default_cmds,create_object
import typeclasses.items
class CmdQuickFind(Command):
    """ 
    Find an item in your current location.

    Usage: 
        quickfind <query>
        
	"""

    key = "quickfind"

    def func(self):
        query = self.args
        result = self.caller.search(query)
        if not result:
            return
        self.caller.msg(f"Found match for {query}: {result}")
class CmdRead(Command):
    """Read a sign, or a book if in the library."

    Usage:
        to read a sign:
        read <thing>
        to read a book in the library:
        read"""
    key = "read"
    def func(self):
        import time
        if not self.args:
                books=["News article: Random person gets a new cat!",
                       "Old tome: Don't mess with magic if you don't know what it does, but here's a magic word: XYZZY"]
                import random
                book=random.choice(books)
                time.sleep(1)
                self.caller.msg(book)
        else:
            sign = self.caller.location.search(self.args.strip())
            try:
                self.caller.msg(sign.db.text)
            except:
                self.caller.msg(f"Could not find {self.args}")
class CmdXYZZY(Command):
    """A magic word.
    
    Usage:
        XYZZY"""
    key = "XYZZY"
    def func(self):
        from evennia import search_object
        from evennia.accounts.models import AccountDB
        dest=search_object("The Cat Inn")[0]
        import random
        if random.randint(0,3) == 0:
            self.caller.msg("You whisper the magic word, and a beam of light sucks you to the Cat Inn.")
            self.caller.move_to(dest)
        else:
            self.caller.msg("You whisper XYZZY and feel a change in the weave, but nothing happens.")
            for account in AccountDB.objects.all():
                account.msg("You feel something change.")
class CmdDiminsionalTransporter(Command):
    """A command to use a diminsional transporter.
    
    Usage:
        dimensional transporter <dimensional frequency>"""
    key="dimensional transporter"
    def func(self):
        from evennia import search_object
        caller = self.caller
        required_item_key = "dimensional transporter" # The key of the required item

        # Check if the caller has the item in their inventory or location
        # self.caller.search() automatically checks inventory/location and handles error messages
        has_item = caller.search(required_item_key, quiet=True, location=caller, 
                                 nofound_string="", multimatch_string="")
        if has_item:
            if self.args=="123456789":
                self.caller.move_to(search_object("Ephraim's dimension")[0])
        else:
            self.caller.msg("You need a dimensional transporter to use this.")
class CmdPLUGH(Command):
    """A magic word.
    
    Usage:
        PLUGH"""
    key = "PLUGH"
    def func(self):
        self.caller.msg("Say XYZZY")
class CmdEmote(Command):
    """Emote.
    Usage:
        c <what you do>
    Output(what others see):
        <your name> <what you do>."""
    key="c"
    def func(self):
        x=self.caller.location.contents
        for i in x:
            if i != self.caller:
                i.msg(f"{self.caller.name}{self.args}.")
            else:
                i.msg(f"You{self.args}")
class CmdTeleport(Command):
    """Teleport.
    Usage:
        teleport <where you want to go>"""
    key = "teleport"
    locks="cmd:false()"
    def func(self):
        from evennia import search_object
        index=0
        dest=search_object(self.args.strip())[index]
        while dest == self.caller.location:
            index+=1
            dest=search_object(self.args.strip())[index]
        self.caller.move_to(dest)
        x=self.caller.location.contents
        for i in x:
            if i != self.caller:
                i.msg("The air warps in the sky, and the next thing you see is a glowing figure thunderbolting down from a dark crack in the sky.")
class CmdDimension(Command):
    """Use this command to use the dimensional transport.
    
    Usage:
        freq <frequency>"""
    key = "freq"
    def func(self):
        from evennia import search_object
        self.args = self.args.strip()
        x=search_object("#722")[0]
        if self.caller.location == x:
            if self.args=="12.345":
                x=search_object("#713")[0]
            elif self.args == "11.111":
                x=search_object("#2")[0]
            else:
                self.caller.msg("That dimension doesn't exist.")
        self.caller.move_to(x)
class CmdOpen(Command):
    """Open an openable thing.
    
    Usage:
        open <query>"""

    key = "open"
    def func(self):
        import random
        chest = self.caller.location.search("chest")
        if chest.db.contains == "coin":
            self.caller.msg(f"You open the chest and there are some coins inside. You take it.")
            self.caller.db.gold += random.randint(1,10)
        elif chest.db.contains == "sword":
            self.caller.msg("There is a sword in the chest, which you take.")
            create_object(typeclasses.items.Sword, key = "sword",location=self.caller)
        elif chest.db.contains == "key":
            self.caller.msg("There is a key in the chest.")
            create_object(key="key",location=self.caller)
        else:
            self.caller.msg(chest.db.contains)
        

class CmdEcho(Command):
    """
    A simple echo command

    Usage:
        echo <something>

    """
    key = "echo"

    def func(self):
        self.caller.msg(f"Echo: '{self.args.strip()}'")
class MyCmdGet(default_cmds.CmdGet):

    def func(self):
        super().func()
        if self.args == "rose":
            self.caller.msg("The rose pricks your finger, doing 10 damage.")
            self.caller.db.health-=10
class CmdQuit(default_cmds.CmdQuit):
    """Quits the game.
    
    Usage:
        quit"""
    key = "quit"
    def func(self):
        character = self.caller.character
        if character and character.location:
            character.location.msg_contents(f"{self.caller.name} whispers something, and they vanish in a beam of light.")
            super().func()

class CmdWrite(Command):
        """Write in a nearby book.
        
        Usage:
            write <text>"""
        key="write"
        def func(self):
            if not self.args:
                self.caller.msg("What do you want to write?")
                return
            book = self.caller.location.search("book")
            book.db.text+=self.args
            for x in self.caller.location.contents:
                if x == self.caller:
                    x.msg(f"You write{self.args} in the book.")
                else:
                    x.msg(f"{self.caller} writes in a book.")
class CmdSetDesc(Command):
    """Set your description.
    
    Usage:
        setdesc <description>"""
    key="setdesc"
    def func(self):
        self.caller.db.desc = self.args
class CmdSay(Command):
    """
    Say something.
    
    Usage:
      say <message>"""
    key = "say"
    def func(self):
        if not self.args:
            self.caller.msg("What do you want to say?")
            return
        for char in self.caller.location.contents:
            char.msg(f"{self.caller} says {self.args}.")
class CmdMove(Command):
    """Move something.
    
    Usage:
        move <thing>"""
    def func(self):
        thing=self.caller.location.search(self.args)
        if thing:
            thing.moved = not thing.moved
        painting = self.caller.search("painting")
        safe = self.caller.search("button") # You may need to search by dbref if it's currently hidden
        if painting:
            painting.moved = not painting.moved
            if safe:
             # Update the safe's attribute to satisfy its own lock
                safe.locks = "get:false()" 
                self.caller.msg("You move the painting, revealing a hidden button!")
class CmdHit(Command):
    """
    Hit a target.

    Usage:
      hit <target>

    """
    key = "hit"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""

    def func(self):
        if not self.args:
            self.caller.msg("Who do you want to hit?")
            return
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return
        # get and handle the weapon
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "bare fists"
        if target.key == "magic stone":
            self.caller.msg("|gThe stone shatters, then comes back together and waves a tiny fist at you.|n")
            return
        self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        target.msg(f"You got hit by {self.caller.key} with {weaponstr}!")
        try:
            target.db.health -= 1
        except:
            self.caller.msg("The target seems unaffected.")
        for x in self.caller.location.contents:
            if x!= self.caller or x!= target:
                x.msg(f"You see {self.caller.key} hit {target.key} with {weaponstr}")


class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        from world import npcs,quests
        self.add(CmdEcho)
        self.add(CmdHit)
        self.add(CmdOpen)
        self.add(CmdQuickFind)
        self.add(MyCmdGet)
        self.add(CmdQuit)
        self.add(CmdSay)
        self.add(CmdRead)
        self.add(CmdWrite)
        self.add(CmdSetDesc)
        self.add(CmdXYZZY)
        self.add(CmdDiminsionalTransporter)
        self.add(CmdEmote)
        self.add(CmdTeleport)
        self.add(CmdDimension)
        self.add(npcs.CmdTalk)
        self.add(npcs.CmdBuy)
        self.add(quests.CmdQuests)
        self.add(quests.CmdFinishQuest)
        self.add(CmdMove)