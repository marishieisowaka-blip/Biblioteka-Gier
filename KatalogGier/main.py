#!/usr/bin/env python3
"""
===============================================================================
PLIK: main.py
OPIS: Punkt startowy aplikacji Katalog Gier
===============================================================================

URUCHOMIENIE:
    python main.py

WYMAGANIA:
    - Python 3.7+
    - tkinter (biblioteka standardowa)

===============================================================================
"""

import tkinter as tk
from main_window import MainWindow


def main():
    """Główna funkcja aplikacji"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
