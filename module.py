#
# 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys
import log
import imp

from os.path import exists

class Module(object):
    def __init__(self):
        sys.path.append("plugins/")

        self.log = log.Logger("module")
        self.modules = {}
        self.actions = {
            ".load": self.module_load,
            ".unload": self.module_unload,
            ".reload": self.module_reload,
            }

        self.modules_autoload("plugins/")

    # Module fallback, just cowardly return
    def action_fallback(self, nickname, str):
        return

    # Lookup module name and return True if it is loaded
    def module_loaded(self, name):
        if not name in self.modules:
            self.log.debug("Module " + name + " not loaded")
            return False

        self.log.debug("Module " + name + " is loaded")
        return True      

    # Add module to modules and register it
    def module_add(self, module_name):
        name = os.path.splitext(os.path.basename(module_name))[0]
        full_name = os.path.splitext(module_name)[0].replace(os.path.sep, '.')

        # Add module
        self.modules[name] = imp.load_module(full_name, *imp.find_module(name, ["plugins/"]))

        # Call the __register__ function available in all modules
        self.modules[name].__register__(self.actions)

    # Unregister module and remove references   
    def module_del(self, name):
        self.modules[name].__unregister__(self.actions)
        
        # This will remove the references to the module, not only
        # the namespace
        del self.modules[name]

    # Load module
    def module_load(self, nickname, name):
        # Exists in plugins/ folder?
        if not exists("plugins/" + name + ".py"):
            self.log.debug("Module " + name + " not found in directory")
            return "Module " + name + " not found"

        # Already loaded?
        if self.module_loaded(name):
            return "Module " + name + " already loaded"

        # Load it
        self.module_add(name)
        self.log.debug("Module " + name + " added")

        return "Module " + name + " loaded"

    # Unload module
    def module_unload(self, nickname, name):
        # Loaded?
        if self.module_loaded(name) == False:
            return "Module " + name + " not loaded"

        # Unregister and remove
        self.module_del(name)

        return "Module " + name + " unloaded"

    # Reload module
    def module_reload(self, nickname, name):
        # Return of not loaded
        if self.module_loaded(name) == False:
            return "Module " + name + " not loaded"

        # Remove and add again
        self.module_unload(nickname, name);

        return "Module " + name + " reloaded"

    # Autoload all modules in plugins/ folder
    def modules_autoload(self, path):
        modules = [file for file in os.listdir(path) if file.lower().endswith(".py")]
        for module in modules:
            self.log.debug("Loading module " + module)
            self.module_load("None", module)

 if __name__ == '__main__':
     m = Module()
     m.module_load("test", "nextep")
     m.module_reload("test", "nextep")
     m.module_unload("test", "nextep")
     m.modules_autoload("plugins/")
