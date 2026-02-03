"""
===============================================================================
PLIK: dialogi.py
OPIS: Okna dialogowe dla aplikacji Katalog Gier
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, List
from datetime import datetime


# PALETA KOLORÓW - ta sama co w main_window
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#0f3460',
    'accent': '#e94560',
    'text': '#eaeaea',
    'text_dim': '#a0a0a0',
    'success': '#00d9a5',
    'warning': '#f39c12',
    'info': '#3498db',
    'danger': '#e74c3c',
}


class DodajPozycjeDialog:
    """Dialog dodawania nowej gry """
    
    def __init__(self, parent):
        self.result = None
        
        # Okno dialogowe
        self.top = tk.Toplevel(parent)
        self.top.title("➕ Dodaj grę")
        self.top.geometry("500x540")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (540 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="➕ DODAJ NOWĄ GRĘ",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['accent']
        ).pack(expand=True)
        
        # Główny kontener z paddingiem
        main_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Tytuł gry
        tk.Label(
            main_frame,
            text="📝 Tytuł gry:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            anchor='w'
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.entry_tytul = tk.Entry(
            main_frame,
            font=("Segoe UI", 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            bd=5
        )
        self.entry_tytul.pack(fill=tk.X, ipady=8)
        self.entry_tytul.focus()
        
        # Wydawca gry
        tk.Label(
            main_frame,
            text="🏢 Wydawca:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            anchor='w'
        ).pack(fill=tk.X, pady=(20, 5))
        
        self.entry_wydawca = tk.Entry(
            main_frame,
            font=("Segoe UI", 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            bd=5
        )
        self.entry_wydawca.pack(fill=tk.X, ipady=8)
        
        # Gatunek
        tk.Label(
            main_frame,
            text="🎭 Gatunek:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            anchor='w'
        ).pack(fill=tk.X, pady=(20, 5))
        
        from katalog import Katalog
        
        self.combo_gatunek = ttk.Combobox(
            main_frame,
            values=Katalog.GATUNKI,
            state="normal",  # Można wpisać własny
            font=("Segoe UI", 12)
        )
        self.combo_gatunek.pack(fill=tk.X, ipady=8)
        self.combo_gatunek.set("RPG")  # Domyślna wartość
        
        # Rok wydania
        tk.Label(
            main_frame,
            text="📅 Rok wydania:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            anchor='w'
        ).pack(fill=tk.X, pady=(20, 5))
        
        self.spin_rok = tk.Spinbox(
            main_frame,
            from_=1900,
            to=datetime.now().year,
            font=("Segoe UI", 12),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            buttonbackground=COLORS['bg_light'],
            relief=tk.FLAT,
            bd=5
        )
        self.spin_rok.delete(0, tk.END)
        self.spin_rok.insert(0, datetime.now().year)
        self.spin_rok.pack(fill=tk.X, ipady=8)
        
        # Przyciski
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="➕ Dodaj grę",
            command=self.on_ok,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['success'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="❌ Anuluj",
            command=self.on_cancel,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(10, 0))
        
        # Bind Enter/Escape
        self.top.bind('<Return>', lambda e: self.on_ok())
        self.top.bind('<Escape>', lambda e: self.on_cancel())
        
        self.top.wait_window()
    
    def on_ok(self):
        """Obsługuje zatwierdzenie"""
        tytul = self.entry_tytul.get().strip()
        wydawca = self.entry_wydawca.get().strip()
        gatunek = self.combo_gatunek.get().strip()
        
        try:
            rok = int(self.spin_rok.get())
        except ValueError:
            messagebox.showerror("❌ Błąd", "Rok musi być liczbą!")
            return
        
        if not tytul or not wydawca or not gatunek:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Wszystkie pola są wymagane!")
            return
        
        if rok < 1900 or rok > datetime.now().year:
            messagebox.showerror("❌ Błąd", f"Rok musi być między 1900 a {datetime.now().year}!")
            return
        
        self.result = (tytul, wydawca, gatunek, rok)
        self.top.destroy()
    
    def on_cancel(self):
        """Obsługuje anulowanie"""
        self.top.destroy()


class DodajOceneDialog:
    """Dialog dodawania oceny """
    
    def __init__(self, parent, tytul_gry: str):
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title("⭐ Dodaj ocenę")
        self.top.geometry("450x400")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (400 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⭐ DODAJ OCENĘ",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['warning']
        ).pack(expand=True)
        
        # Główny kontener
        main_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Tytuł gry
        tk.Label(
            main_frame,
            text=f"🎮 Gra:",
            font=("Segoe UI", 11),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_dim'],
            anchor='w'
        ).pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(
            main_frame,
            text=tytul_gry,
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['accent'],
            anchor='w',
            wraplength=380
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Ocena
        tk.Label(
            main_frame,
            text="⭐ Ocena (1-10):",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text']
        ).pack(pady=(10, 10))
        
        self.spin_ocena = tk.Spinbox(
            main_frame,
            from_=1,
            to=10,
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['warning'],
            buttonbackground=COLORS['bg_light'],
            relief=tk.FLAT,
            bd=5,
            justify='center',
            width=8
        )
        self.spin_ocena.delete(0, tk.END)
        self.spin_ocena.insert(0, "10")
        self.spin_ocena.pack(ipady=10)
        
        # Przyciski
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="✅ Dodaj",
            command=self.on_ok,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['warning'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="❌ Anuluj",
            command=self.on_cancel,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(10, 0))
        
        self.top.bind('<Return>', lambda e: self.on_ok())
        self.top.bind('<Escape>', lambda e: self.on_cancel())
        
        self.top.wait_window()
    
    def on_ok(self):
        """Obsługuje zatwierdzenie"""
        try:
            ocena = int(self.spin_ocena.get())
        except ValueError:
            messagebox.showerror("❌ Błąd", "Ocena musi być liczbą!")
            return
        
        if ocena < 1 or ocena > 10:
            messagebox.showerror("❌ Błąd", "Ocena musi być między 1 a 10!")
            return
        
        self.result = ocena
        self.top.destroy()
    
    def on_cancel(self):
        """Obsługuje anulowanie"""
        self.top.destroy()


class WyszukajDialog:
    """Dialog wyszukiwania """
    
    def __init__(self, parent):
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title("🔍 Wyszukaj")
        self.top.geometry("500x260")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (260 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔍 WYSZUKAJ GRĘ",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['info']
        ).pack(expand=True)
        
        # Główny kontener
        main_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(
            main_frame,
            text="📝 Wpisz tytuł gry (lub fragment):",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            anchor='w'
        ).pack(fill=tk.X, pady=(10, 10))
        
        self.entry_fraza = tk.Entry(
            main_frame,
            font=("Segoe UI", 13),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            bd=5
        )
        self.entry_fraza.pack(fill=tk.X, ipady=10)
        self.entry_fraza.focus()
        
        # Przyciski
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="🔍 Szukaj",
            command=self.on_ok,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['info'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="❌ Anuluj",
            command=self.on_cancel,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(10, 0))
        
        self.top.bind('<Return>', lambda e: self.on_ok())
        self.top.bind('<Escape>', lambda e: self.on_cancel())
        
        self.top.wait_window()
    
    def on_ok(self):
        """Obsługuje zatwierdzenie"""
        fraza = self.entry_fraza.get().strip()
        
        if not fraza:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Wpisz frazę do wyszukania!")
            return
        
        self.result = fraza
        self.top.destroy()
    
    def on_cancel(self):
        """Obsługuje anulowanie"""
        self.top.destroy()


class FiltrujDialog:
    """Dialog filtrowania """
    
    def __init__(self, parent, katalog):
        self.result = None
        self.katalog = katalog
        
        self.top = tk.Toplevel(parent)
        self.top.title("🎭 Filtruj")
        self.top.geometry("520x420")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (520 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (420 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🎭 FILTRUJ GRY",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg='#9b59b6'
        ).pack(expand=True)
        
        # Główny kontener
        main_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Wybór typu filtrowania
        self.tryb = tk.StringVar(value="gatunek")
        
        # OPCJA 1: Gatunek
        radio1_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        radio1_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Radiobutton(
            radio1_frame,
            text="📚 Filtruj po gatunku",
            variable=self.tryb,
            value="gatunek",
            command=self.on_tryb_changed,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent']
        ).pack(anchor=tk.W)
        
        self.combo_gatunek = ttk.Combobox(
            main_frame,
            values=katalog.pobierz_gatunki(),
            state="readonly",
            font=("Segoe UI", 11),
            width=40
        )
        self.combo_gatunek.pack(fill=tk.X, pady=(5, 20), ipady=5)
        if katalog.pobierz_gatunki():
            self.combo_gatunek.current(0)
        
        # OPCJA 2: Rok
        radio2_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        radio2_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Radiobutton(
            radio2_frame,
            text="📅 Filtruj po roku",
            variable=self.tryb,
            value="rok",
            command=self.on_tryb_changed,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent']
        ).pack(anchor=tk.W)
        
        rok_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        rok_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(
            rok_frame,
            text="Od:",
            font=("Segoe UI", 11),
            bg=COLORS['bg_medium'],
            fg=COLORS['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.spin_od = tk.Spinbox(
            rok_frame,
            from_=1900,
            to=datetime.now().year,
            font=("Segoe UI", 11),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            width=10
        )
        self.spin_od.delete(0, tk.END)
        self.spin_od.insert(0, "2000")
        self.spin_od.pack(side=tk.LEFT, padx=(0, 30))
        
        tk.Label(
            rok_frame,
            text="Do:",
            font=("Segoe UI", 11),
            bg=COLORS['bg_medium'],
            fg=COLORS['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.spin_do = tk.Spinbox(
            rok_frame,
            from_=1900,
            to=datetime.now().year,
            font=("Segoe UI", 11),
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            width=10
        )
        self.spin_do.delete(0, tk.END)
        self.spin_do.insert(0, str(datetime.now().year))
        self.spin_do.pack(side=tk.LEFT)
        
        # Initially disable rok controls
        self.spin_od.config(state='disabled')
        self.spin_do.config(state='disabled')
        
        # Przyciski
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="🎭 Filtruj",
            command=self.on_ok,
            font=("Segoe UI", 11, "bold"),
            bg='#9b59b6',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="❌ Anuluj",
            command=self.on_cancel,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            pady=10
        ).pack(side=tk.LEFT, expand=True, padx=(10, 0))
        
        self.top.bind('<Return>', lambda e: self.on_ok())
        self.top.bind('<Escape>', lambda e: self.on_cancel())
        
        self.top.wait_window()
    
    def on_tryb_changed(self):
        """Zmienia dostępność kontrolek"""
        if self.tryb.get() == "gatunek":
            self.combo_gatunek.config(state='readonly')
            self.spin_od.config(state='disabled')
            self.spin_do.config(state='disabled')
        else:
            self.combo_gatunek.config(state='disabled')
            self.spin_od.config(state='normal')
            self.spin_do.config(state='normal')
    
    def on_ok(self):
        """Obsługuje zatwierdzenie"""
        if self.tryb.get() == "gatunek":
            gatunek = self.combo_gatunek.get()
            if not gatunek:
                messagebox.showwarning("⚠️ Ostrzeżenie", "Wybierz gatunek!")
                return
            self.result = self.katalog.filtruj_po_gatunku(gatunek)
        else:
            try:
                od_roku = int(self.spin_od.get())
                do_roku = int(self.spin_do.get())
            except ValueError:
                messagebox.showerror("❌ Błąd", "Lata muszą być liczbami!")
                return
            
            if od_roku > do_roku:
                messagebox.showerror("❌ Błąd", "'Od' musi być mniejsze niż 'Do'!")
                return
            
            self.result = self.katalog.filtruj_po_roku(od_roku, do_roku)
        
        self.top.destroy()
    
    def on_cancel(self):
        """Obsługuje anulowanie"""
        self.top.destroy()


class SortujDialog:
    """Dialog sortowania """
    
    def __init__(self, parent):
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title("🔽 Sortuj")
        self.top.geometry("480x360")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (480 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (360 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔽 SORTUJ GRY",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['warning']
        ).pack(expand=True)
        
        # Główny kontener
        main_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(
            main_frame,
            text="Wybierz kierunek sortowania:",
            font=("Segoe UI", 12),
            bg=COLORS['bg_medium'],
            fg=COLORS['text']
        ).pack(pady=(10, 20))
        
        # Wybór kierunku
        self.kierunek = tk.IntVar(value=1)
        
        tk.Radiobutton(
            main_frame,
            text="🔽 Od najlepszej do najgorszej",
            variable=self.kierunek,
            value=1,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=10)
        
        tk.Radiobutton(
            main_frame,
            text="🔼 Od najgorszej do najlepszej",
            variable=self.kierunek,
            value=0,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_medium'],
            fg=COLORS['text'],
            selectcolor=COLORS['bg_light'],
            activebackground=COLORS['bg_medium'],
            activeforeground=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=10)
        
        # Info
        tk.Label(
            main_frame,
            text="ℹ️ Gry bez ocen będą na końcu",
            font=("Segoe UI", 9),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_dim']
        ).pack(pady=(20, 10))
        
        # Przyciski - WIĘKSZE I BARDZIEJ WIDOCZNE
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Przycisk OK - duży i wyraźny
        btn_ok = tk.Button(
            button_frame,
            text="✅ Sortuj",
            command=self.on_ok,
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['success'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            height=2
        )
        btn_ok.pack(side=tk.LEFT, expand=True, padx=(0, 10))
        
        # Efekt hover dla OK
        btn_ok.bind('<Enter>', lambda e: btn_ok.config(bg='#00ffc3'))
        btn_ok.bind('<Leave>', lambda e: btn_ok.config(bg=COLORS['success']))
        
        # Przycisk Anuluj
        btn_cancel = tk.Button(
            button_frame,
            text="❌ Anuluj",
            command=self.on_cancel,
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=15,
            height=2
        )
        btn_cancel.pack(side=tk.LEFT, expand=True, padx=(10, 0))
        
        # Efekt hover dla Anuluj
        btn_cancel.bind('<Enter>', lambda e: btn_cancel.config(bg='#ff6b6b'))
        btn_cancel.bind('<Leave>', lambda e: btn_cancel.config(bg=COLORS['danger']))
        
        self.top.bind('<Return>', lambda e: self.on_ok())
        self.top.bind('<Escape>', lambda e: self.on_cancel())
        
        self.top.wait_window()
    
    def on_ok(self):
        """Obsługuje zatwierdzenie"""
        self.result = bool(self.kierunek.get())
        self.top.destroy()
    
    def on_cancel(self):
        """Obsługuje anulowanie"""
        self.top.destroy()


class StatystykiDialog:
    """Dialog statystyk - bez zmian, działa dobrze"""
    
    def __init__(self, parent, katalog):
        self.top = tk.Toplevel(parent)
        self.top.title("📊 Statystyki")
        self.top.geometry("650x550")
        self.top.transient(parent)
        self.top.grab_set()
        self.top.configure(bg=COLORS['bg_medium'])
        
        # Centruj okno
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (650 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (550 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Nagłówek
        header = tk.Frame(self.top, bg=COLORS['bg_light'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 STATYSTYKI KATALOGU 📊",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_light'],
            fg=COLORS['info']
        ).pack(expand=True)
        
        # Tekst ze statystykami
        text_frame = tk.Frame(self.top, bg=COLORS['bg_medium'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        scrollbar = tk.Scrollbar(text_frame, bg=COLORS['bg_medium'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text = tk.Text(
            text_frame,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)
        
        # Generuj statystyki
        self.generuj_statystyki(katalog)
        
        # Przycisk zamknij
        tk.Button(
            self.top,
            text="❌ Zamknij",
            command=self.top.destroy,
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['danger'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=20,
            pady=10
        ).pack(pady=15)
        
        self.top.bind('<Escape>', lambda e: self.top.destroy())
    
    def generuj_statystyki(self, katalog):
        """Generuje tekst statystyk"""
        stats = []
        
        stats.append("=" * 60)
        stats.append("          STATYSTYKI KATALOGU GIER")
        stats.append("=" * 60)
        stats.append("")
        
        # Liczba gier
        stats.append(f"Liczba gier w katalogu: {katalog.liczba_gier()}")
        stats.append("")
        
        # Średnia ocena
        srednia = katalog.srednia_ocena_katalogu()
        if srednia > 0:
            pelne = round(srednia / 2.0)
            puste = 5 - pelne
            gwiazdki = "★" * pelne + "☆" * puste
            stats.append(f"Średnia ocena katalogu: {srednia:.2f} / 10")
            stats.append(f"Wizualizacja: {gwiazdki}")
        else:
            stats.append("Średnia ocena: Brak ocen")
            stats.append("Wizualizacja: ☆☆☆☆☆")
        stats.append("")
        
        # Najlepsza gra
        najlepsza = katalog.najlepsza()
        if najlepsza:
            srednia_top = najlepsza.srednia_ocena()
            pelne_top = round(srednia_top / 2.0)
            puste_top = 5 - pelne_top
            gwi_top = "★" * pelne_top + "☆" * puste_top
            
            stats.append("-" * 60)
            stats.append("NAJLEPSZA GRA:")
            stats.append(f"  Tytuł: {najlepsza.tytul}")
            stats.append(f"  Gatunek: {najlepsza.gatunek}")
            stats.append(f"  Rok: {najlepsza.rok}")
            stats.append(f"  Ocena: {gwi_top} {srednia_top:.2f}/10")
            stats.append(f"  Liczba ocen: {len(najlepsza.oceny)}")
        stats.append("")
        
        # Najgorsza gra
        najgorsza = katalog.najgorsza()
        if najgorsza and (not najlepsza or najgorsza.id != najlepsza.id):
            srednia_bot = najgorsza.srednia_ocena()
            pelne_bot = round(srednia_bot / 2.0)
            puste_bot = 5 - pelne_bot
            gwi_bot = "★" * pelne_bot + "☆" * puste_bot
            
            stats.append("-" * 60)
            stats.append("NAJGORSZA GRA:")
            stats.append(f"  Tytuł: {najgorsza.tytul}")
            stats.append(f"  Gatunek: {najgorsza.gatunek}")
            stats.append(f"  Rok: {najgorsza.rok}")
            stats.append(f"  Ocena: {gwi_bot} {srednia_bot:.2f}/10")
            stats.append(f"  Liczba ocen: {len(najgorsza.oceny)}")
        stats.append("")
        
        # Rozkład gatunków
        rozklad = katalog.rozklad_gatunkow()
        if rozklad:
            stats.append("-" * 60)
            stats.append("ROZKŁAD GATUNKÓW:")
            for gatunek, liczba in sorted(rozklad.items()):
                procent = (liczba / katalog.liczba_gier()) * 100
                bar = "█" * int(procent / 5)
                stats.append(f"  {gatunek:15s} : {liczba:2d} gier ({procent:5.1f}%) {bar}")
        stats.append("")
        
        # Zakres lat
        od, do = katalog.zakres_lat()
        if od > 0:
            stats.append("-" * 60)
            stats.append(f"ZAKRES LAT WYDANIA: {od} - {do}")
        
        stats.append("")
        stats.append("=" * 60)
        
        # Wstaw do Text widget
        self.text.insert('1.0', '\n'.join(stats))
        self.text.config(state='disabled')
