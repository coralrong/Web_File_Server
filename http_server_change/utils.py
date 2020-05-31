###############################################################
# 
# Module:
#
#        utils.py
#
# Author:
#
#        Coral_Rong(b17040819@njupt.edu.cn)
#
#Reference:
#
#
#        WANG HAIPING (i_free001@njupt.edu.cn)
#
##########################################################

import sys
import inspect

isa = isinstance # just for typing convenience

def main(fn):
    """Call fn with command line arguments.  Used as a decorator.

    The main decorator marks the function that starts a program. For example,

    @main
    def my_run_function():
        # function body

    Use this instead of the typical __name__ == "__main__" predicate.
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:]  # Discard the script name from command line
        fn(*args)            # Call the main function
    return fn

