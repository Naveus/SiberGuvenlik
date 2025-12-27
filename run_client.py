#!/usr/bin/env python3
"""
Client uygulamasini baslat
"""

import sys
import os

# Path ayari
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.client_gui import main

if __name__ == "__main__":
    main()
