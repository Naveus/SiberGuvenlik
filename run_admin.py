#!/usr/bin/env python3
"""
Admin uygulamasini baslat
"""

import sys
import os

# Path ayari
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from admin.admin_gui import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\n[HATA] Uygulama baslatilirken bir hata olustu!")
        print(f"Hata detayi: {e}")
        input("\nCikmak icin Enter'a basin...")
