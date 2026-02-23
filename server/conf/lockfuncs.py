"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False
def has_key(accessing_obj,args):
    """
    Checks if the accessing_obj possesses a specific key.
    """
    key_name = args[0] if args else "generic_key"
    return accessing_obj.db.inventory and key_name in accessing_obj.db.inventory
from evennia.locks.lockfuncs import *

def has_boat(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Checks if the accessing object (character) has a "boat" object in their inventory.
    """
    # Check the character's inventory for an object with the is_boat attribute
    for obj in accessing_obj.contents:
        if obj.db.is_boat:
            return True
    return False
