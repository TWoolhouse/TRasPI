import importlib
import time
import os
import json

try:
    import core
except ImportError as e:
    raise OSError("FAILURE TO LOAD CORE!") from e
try:
    with open (f"{core.sys.PATH}core/system/system.cfg", 'r') as file:
        system_config = json.load(file)
except:
    print("Failed to load system config file, continuing")
try:
    module = importlib.import_module("home")
except Exception as e:
    raise core.error.FatalCoreException("FAILURE TO BOOT!") from e

if not hasattr(module, "main"):
    msg = "FAIL! '{}' has no 'main'!".format(module.__name__)
    raise core.error.FatalCoreException(msg)

if not isinstance(module.main, core.render.Window):
    msg = "FAIL! {}.main <{} '{}'> is not an instance of 'core.render.Window'!".format(module.__name__, type(module.main).__name__, module.main)
    raise core.error.FatalCoreException(msg)

while True:
    try:
        module.main.show()
        core.render.loop()
    except core.error.RenderError as e:
        try:
            core.render.loop()
        except core.error.RenderError as e:
            try:
                raise core.error.FatalCoreException() from e
            except core.error.FatalCoreException as e:
                core.system.log.Log.error("MAIN", e.log())
                print(e.log())
