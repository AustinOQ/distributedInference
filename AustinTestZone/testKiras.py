import importlib
import sys


def splitFinder(netName):
    BASE_ADDRESS = "/home/austin/Desktop/canary_jenna/canary3/" # edit /home/austin/Desktop/canary_jenna/canary3/nnLib
    module_path = 'nnLib.' + netName  # Convert file path to module path

    # Ensure the directory is in the Python path
    if BASE_ADDRESS not in sys.path:
        sys.path.append(BASE_ADDRESS)

    # Import the module using the correct module path
    module = importlib.import_module(module_path)

    splitList = module.supported_splits

    # Remove the module from sys.modules if necessary
    del sys.modules[module_path]

    return splitList
splitFinder("defonet")