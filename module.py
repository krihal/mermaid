#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys

from os.path import exists

class Module(object):

    def __init__(self):
        self.modules = {}

        # Default actions, used by event handler
        self.actions = {
            ".load": self.module_load,
            ".unload": self.module_unload,
            ".reload": self.module_reload,
            }

    # Module fallback, just cowardly return
    def action_fallback(self, nickname, str):
        return

    # Lookup module name and return True if it is loaded
    def module_loaded(self, name):
        if not name in modules:
            return False

        return True      

    # Add module to modules and register it
    def module_add(self, name):
        modules[name] = __import__("plugins/" + name)
        
        # Call the __register__ function available in all modules
        modules[name].__register__(actions)

    # Unregister module and remove references   
    def module_del(self, name):
        modules[name].__unregister__(actions)
        
        # This will remove the references to the module, not only
        # the namespace
        del sys.modules["plugins/" + name] 
        del modules[name]

    # Load module
    def module_load(self, nickname, name):
    
        # Exists in plugins/ folder?
        if not exists("plugins/" + name + ".py"):
            return "Module " + name + " not found"

        # Already loaded?
        if module_loaded(name):
            return "Module " + name + " already loaded"

        # Load it
        module_add(name)
        return "Module " + name + " loaded"

    # Unload module
    def module_unload(self, nickname, name):

        # Loaded?
        if module_loaded(name) == False:
            return "Module " + name + " not loaded"

        # Unregister and remove
        module_del(name)

        return "Module " + name + " unloaded"

    # Reload module
    def module_reload(self, nickname, name):

        # Return of not loaded
        if module_loaded(name) == False:
            return "Module " + name + " not loaded"

        # Remove and add again
        module_del(name)
        module_add(name)

        return "Module " + name + " reloaded"
