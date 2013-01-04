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

    def action_fallback(self, nickname, str):
        return

    def module_loaded(self, name):
        if not name in self.modules:
            self.log.debug("Module " + name + " not loaded")
            return False

        self.log.debug("Module " + name + " is loaded")
        return True      

    def module_add(self, module_name):
        name = os.path.splitext(os.path.basename(module_name))[0]

        self.modules[name] = imp.load_module(name, *imp.find_module(name, ["plugins/"]))
        self.modules[name].__register__(self.actions)

    def module_del(self, name):
        self.modules[name].__unregister__(self.actions)
        del self.modules[name]

    def module_load(self, nickname, name):
        if os.path.isfile("plugins/" + name + ".py") == True:
            self.log.debug("Module " + name + ".py not found in directory")
            return "Module " + name + " not found"

        if self.module_loaded(name):
            return "Module " + name + " already loaded"

        self.module_add(name)
        self.log.debug("Module " + name + " added")

        return "Module " + name + " loaded"

    def module_unload(self, nickname, name):
        if self.module_loaded(name) == False:
            return "Module " + name + " not loaded"

        self.module_del(name)

        return "Module " + name + " unloaded"

    def module_reload(self, nickname, name):
        if self.module_loaded(name) == False:
            return "Module " + name + " not loaded"

        self.module_unload(nickname, name);

        return "Module " + name + " reloaded"

    def modules_autoload(self, path):
        modules = [file for file in os.listdir(path) if file.lower().endswith(".py")]
        for module in modules:
            module = os.path.splitext(module)[0]
            self.log.debug("Loading module " + module)
            self.module_load("None", "plugins/" + module)

if __name__ == '__main__':
    m = Module()
#    m.module_load("test", "nextep")
#    m.module_reload("test", "nextep")
#    m.module_unload("test", "nextep")
#    m.modules_autoload("plugins/")
