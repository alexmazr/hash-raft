import unittest
from pydoc import locate
import pkgutil
import threading


def suite ():
    loader = unittest.TestLoader ()
    suite = unittest.TestSuite ()

    module_names = ["tests."+name+"."+name for _, name, _ in pkgutil.iter_modules(['tests']) if name != "__main__" and name != "context"]

    for test_class in [locate(x) for x in module_names]:
        tests = loader.loadTestsFromTestCase (test_class)
        suite.addTests (tests)

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner ()
    runner.run (suite ())
    # for thread in threading.enumerate(): 
    #   print(thread.name)