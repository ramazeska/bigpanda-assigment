#!/usr/bin/env python3

import sys
import os
import traceback

if __name__ == "__main__":
    current_location = os.path.dirname(os.path.abspath(__file__))
    modules_location = os.path.join(current_location, 'modules')
    sys.path.insert(0, modules_location)


    try:
        from main import main
    except ImportError:
        sys.exit('Failed to import modules, please check the script dir')

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        print(traceback.print_exc())
        sys.exit(2)


