"""
===============================================================================
PLIK: main_window.py
OPIS: Główne okno aplikacji Katalog Gier
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Optional, List
from katalog import Katalog
from modele import Pozycja
from dialogi import *


class MainWindow:
    """Główne okno aplikacji Katalog Gier"""
    
    # PALETA KOLORÓW
    COLORS = {
        'bg_dark': '#1a1a2e',
        'bg_medium': '#16213e',
        'bg_light': '#0f3460',
        'accent': '#e94560',
        'accent_hover': '#ff5c7a',
        'text': '#eaeaea',
        'text_dim': '#a0a0a0',
        'success': '#00d9a5',
        'warning': '#f39c12',
        'info': '#3498db',
        'purple': '#9b59b6',
        'danger': '#e74c3c',
        'star': '#ffd700',
    }
    
    def __init__(self, root: tk.Tk):
        """Konstruktor głównego okna"""
        self.root = root
        self.katalog = Katalog()
        self.katalog.wczytaj()
        
        # Lista aktualnie wyświetlanych pozycji (może być przefiltrowana)
        self.aktualne_pozycje: List[Pozycja] = []
        
        # Automatyczne ładowanie przykładowych gier przy pierwszym uruchomieniu
        if self.katalog.liczba_gier() == 0:
            self.katalog.dodaj_dane_testowe()
            self.katalog.zapisz()
        
        # Konfiguracja okna
        self.root.title("🎮 Katalog Gier")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg=self.COLORS['bg_dark'])
        
        # Pełne skalowanie
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Ikona
        try:
            self.root.iconbitmap("app.ico")
        except:
            pass
        
        # Czcionki
        self.setup_fonts()
        
        # Stwórz interfejs
        self.stworz_interface()
        
        # Odśwież listę
        self.odswiez_liste()
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)
        self.last_width = 1200
        self.last_height = 700
        
        # KRYTYCZNE: Obsługa zamykania okna
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_fonts(self):
        """Konfiguracja czcionek"""
        self.font_title = font.Font(family="Segoe UI", size=22, weight="bold")
        self.font_heading = font.Font(family="Segoe UI", size=13, weight="bold")
        self.font_button = font.Font(family="Segoe UI", size=10, weight="bold")
        self.font_text = font.Font(family="Consolas", size=11)
        self.font_detail = font.Font(family="Segoe UI", size=11)
        self.font_star = font.Font(family="Segoe UI", size=20, weight="bold")
    
    def stworz_interface(self):
        """Tworzy piękny interfejs użytkownika"""
        
        # NAGŁÓWEK - BEZ PODTYTUŁU
        header_frame = tk.Frame(self.root, bg=self.COLORS['bg_medium'], height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Tytuł - WIĘKSZY, bez podtytułu
        title_label = tk.Label(
            header_frame,
            text="🎮 KATALOG GIER 🎮",
            font=self.font_title,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['accent']
        )
        title_label.pack(expand=True)
        
        # GŁÓWNY KONTENER
        main_container = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Lewy panel - menu
        left_frame = tk.Frame(
            main_container,
            bg=self.COLORS['bg_medium'],
            relief=tk.FLAT
        )
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_frame.config(width=200)
        
        # Nagłówek menu
        menu_label = tk.Label(
            left_frame,
            text="AKCJE",
            font=self.font_heading,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['text']
        )
        menu_label.pack(pady=(10, 15))
        
        # Separator
        separator1 = tk.Frame(left_frame, height=2, bg=self.COLORS['accent'])
        separator1.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Przyciski
        buttons = [
            ("➕ Dodaj", self.dodaj_gre, self.COLORS['success']),
            ("🗑️ Usuń", self.usun_gre, self.COLORS['danger']),
            ("⭐ Oceń", self.ocen_gre, self.COLORS['warning']),
            ("🔍 Szukaj", self.wyszukaj, self.COLORS['info']),
            ("🎭 Filtruj", self.filtruj, self.COLORS['purple']),
            ("🔽 Sortuj", self.sortuj, self.COLORS['warning']),
            ("📊 Statystyki", self.pokaz_statystyki, self.COLORS['info']),
            ("🔄 Odśwież", self.odswiez_liste, self.COLORS['bg_light']),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                left_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=self.font_button,
                relief=tk.FLAT,
                cursor='hand2',
                width=18,
                pady=8  # Zmniejszone z 12 na 8
            )
            btn.pack(pady=4, padx=10)  # Zmniejszone z 6 na 4
            
            # Zapisz oryginalny kolor
            btn.original_color = color
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: self.on_button_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_button_hover(b, False))
        
        # Separator przed przyciskiem Zamknij
        separator2 = tk.Frame(left_frame, height=2, bg=self.COLORS['accent'])
        separator2.pack(fill=tk.X, padx=20, pady=(10, 10))
        
        # PRZYCISK ZAMKNIJ
        btn_zamknij = tk.Button(
            left_frame,
            text="❌ Zamknij",
            command=self.on_closing,
            bg=self.COLORS['danger'],
            fg='white',
            font=self.font_button,
            relief=tk.FLAT,
            cursor='hand2',
            width=18,
            pady=8
        )
        btn_zamknij.pack(pady=4, padx=10, side=tk.BOTTOM)
        btn_zamknij.bind('<Enter>', lambda e: btn_zamknij.config(bg=self.COLORS['accent_hover']))
        btn_zamknij.bind('<Leave>', lambda e: btn_zamknij.config(bg=self.COLORS['danger']))
        
        # ŚRODKOWY PANEL - LISTA GIER
        middle_frame = tk.Frame(main_container, bg=self.COLORS['bg_medium'])
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Nagłówek listy - ZMIENIONY TEKST
        header_list = tk.Frame(middle_frame, bg=self.COLORS['bg_light'], height=50)
        header_list.pack(fill=tk.X)
        header_list.pack_propagate(False)
        
        tk.Label(
            header_list,
            text="📚 BAZA GIER",  # ZMIENIONE z "TWOJE GRY"
            font=self.font_heading,
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Licznik gier
        self.label_licznik = tk.Label(
            header_list,
            text="0 gier",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text_dim']
        )
        self.label_licznik.pack(side=tk.RIGHT, padx=15)
        
        # Lista z scrollbar
        list_container = tk.Frame(middle_frame, bg=self.COLORS['bg_medium'])
        list_container.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        scrollbar = tk.Scrollbar(list_container, bg=self.COLORS['bg_medium'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_gry = tk.Listbox(
            list_container,
            font=self.font_text,  # Większa czcionka (11pt)
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text'],
            selectbackground=self.COLORS['accent'],
            selectforeground='white',
            relief=tk.FLAT,
            highlightthickness=0,
            borderwidth=0
        )
        self.listbox_gry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_gry.bind('<<ListboxSelect>>', self.on_selection_changed)
        
        scrollbar.config(command=self.listbox_gry.yview)
        
        # PRAWY PANEL - SZCZEGÓŁY
        right_frame = tk.Frame(
            main_container,
            bg=self.COLORS['bg_medium']
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_frame.config(width=320)
        
        # Nagłówek szczegółów
        header_details = tk.Frame(right_frame, bg=self.COLORS['bg_light'], height=50)
        header_details.pack(fill=tk.X)
        header_details.pack_propagate(False)
        
        tk.Label(
            header_details,
            text="ℹ️ SZCZEGÓŁY",
            font=self.font_heading,
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text']
        ).pack(pady=10)
        
        # Kontener szczegółów
        details_container = tk.Frame(right_frame, bg=self.COLORS['bg_medium'])
        details_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Gwiazdki
        self.label_gwiazdki = tk.Label(
            details_container,
            text="☆☆☆☆☆",
            font=self.font_star,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['star']
        )
        self.label_gwiazdki.pack(pady=(0, 20))
        
        # Separator
        separator2 = tk.Frame(details_container, height=2, bg=self.COLORS['accent'])
        separator2.pack(fill=tk.X, pady=(0, 15))
        
        # Szczegóły
        detail_style = {
            'bg': self.COLORS['bg_medium'],
            'font': self.font_detail,
            'anchor': 'w',
            'justify': 'left'
        }
        
        # ID
        tk.Label(details_container, text="🆔 ID:", fg=self.COLORS['text_dim'], **detail_style).pack(fill=tk.X, pady=2)
        self.label_id = tk.Label(details_container, text="-", fg=self.COLORS['text'], **detail_style)
        self.label_id.pack(fill=tk.X, pady=(0, 10))
        
        # Tytuł
        tk.Label(details_container, text="📝 TYTUŁ:", fg=self.COLORS['text_dim'], **detail_style).pack(fill=tk.X, pady=2)
        self.label_tytul = tk.Label(
            details_container,
            text="-",
            fg=self.COLORS['accent'],
            font=("Segoe UI", 12, "bold"),
            **{k:v for k,v in detail_style.items() if k != 'font'}
        )
        self.label_tytul.pack(fill=tk.X, pady=(0, 10))
        
        # Gatunek
        tk.Label(details_container, text="🎭 GATUNEK:", fg=self.COLORS['text_dim'], **detail_style).pack(fill=tk.X, pady=2)
        self.label_gatunek = tk.Label(details_container, text="-", fg=self.COLORS['text'], **detail_style)
        self.label_gatunek.pack(fill=tk.X, pady=(0, 10))
        
        # Rok
        tk.Label(details_container, text="📅 ROK:", fg=self.COLORS['text_dim'], **detail_style).pack(fill=tk.X, pady=2)
        self.label_rok = tk.Label(details_container, text="-", fg=self.COLORS['text'], **detail_style)
        self.label_rok.pack(fill=tk.X, pady=(0, 10))
        
        # Oceny
        tk.Label(details_container, text="⭐ OCENY:", fg=self.COLORS['text_dim'], **detail_style).pack(fill=tk.X, pady=2)
        self.label_oceny = tk.Label(
            details_container,
            text="-",
            fg=self.COLORS['text'],
            wraplength=280,
            **detail_style
        )
        self.label_oceny.pack(fill=tk.X, pady=(0, 10))
    
    def on_button_hover(self, button, is_entering):
        """Efekt hover dla przycisków"""
        if is_entering:
            button['bg'] = self.COLORS['accent_hover']
        else:
            # Przywróć oryginalny kolor
            if hasattr(button, 'original_color'):
                button['bg'] = button.original_color
    
    def on_window_resize(self, event):
        """Obsługuje zmianę rozmiaru okna"""
        if event.widget != self.root:
            return
        
        new_width = event.width
        new_height = event.height
        
        if abs(new_width - self.last_width) < 10 and abs(new_height - self.last_height) < 10:
            return
        
        self.last_width = new_width
        self.last_height = new_height
        
        # Dostosuj czcionki dla małych okien
        if new_width < 900:
            self.font_button.configure(size=9)
            self.font_text.configure(size=10)
        else:
            self.font_button.configure(size=10)
            self.font_text.configure(size=11)
    
    # METODY INTERFEJSU
    
    def odswiez_liste(self):  # AY
        """Odświeża listę gier"""
        self.listbox_gry.delete(0, tk.END)
        
        pozycje = self.katalog.pobierz_wszystkie()
        self.aktualne_pozycje = pozycje  # Zapisz aktualnie wyświetlane
        
        for pozycja in pozycje:
            self.listbox_gry.insert(tk.END, str(pozycja))
        
        self.label_licznik.config(text=f"{len(pozycje)} gier")
    
    def wyswietl_szczegoly(self, pozycja: Optional[Pozycja]):  # AY
        """Wyświetla szczegóły wybranej gry"""
        if pozycja is None:
            self.wyczysc_szczegoly()
            return
        
        self.label_id.config(text=str(pozycja.id))
        self.label_tytul.config(text=pozycja.tytul)
        self.label_gatunek.config(text=pozycja.gatunek)
        self.label_rok.config(text=str(pozycja.rok))
        
        if pozycja.oceny:
            oceny_str = ", ".join(str(o.wartosc) for o in pozycja.oceny)
            self.label_oceny.config(text=oceny_str)
            
            srednia = pozycja.srednia_ocena()
            pelne = round(srednia / 2.0)
            puste = 5 - pelne
            gwiazdki = "★" * pelne + "☆" * puste
            self.label_gwiazdki.config(text=f"{gwiazdki}\n{srednia:.1f}/10")
        else:
            self.label_oceny.config(text="Brak ocen")
            self.label_gwiazdki.config(text="☆☆☆☆☆\nBrak ocen")
    
    def wyczysc_szczegoly(self):
        """Czyści panel szczegółów"""
        self.label_id.config(text="-")
        self.label_tytul.config(text="-")
        self.label_gatunek.config(text="-")
        self.label_rok.config(text="-")
        self.label_oceny.config(text="-")
        self.label_gwiazdki.config(text="☆☆☆☆☆")
    
    def pobierz_wybrana_pozycje(self) -> Optional[Pozycja]:  # AY
        """Zwraca aktualnie wybraną grę z listy"""
        selection = self.listbox_gry.curselection()
        if not selection:
            return None
        
        index = selection[0]
        
        # Używaj aktualnie wyświetlanych pozycji (może być przefiltrowana lista)
        if 0 <= index < len(self.aktualne_pozycje):
            return self.aktualne_pozycje[index]
        return None
    
    # EVENT HANDLERY
    
    def on_selection_changed(self, event):
        """Obsługuje zmianę selekcji w liście"""
        pozycja = self.pobierz_wybrana_pozycje()
        self.wyswietl_szczegoly(pozycja)
    
    def dodaj_gre(self):  # MŻ
        """Obsługuje dodawanie nowej gry"""
        dialog = DodajPozycjeDialog(self.root)
        
        if dialog.result:
            tytul, wydawca, gatunek, rok = dialog.result
            self.katalog.dodaj_pozycje(tytul, wydawca, gatunek, rok)
            self.odswiez_liste()
            messagebox.showinfo("✅ Sukces", f"Dodano grę:\n{tytul}\nWydawca: {wydawca}")
    
    def usun_gre(self):  # MŻ
        """Obsługuje usuwanie gry"""
        pozycja = self.pobierz_wybrana_pozycje()
        
        if not pozycja:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Nie wybrano gry do usunięcia!")
            return
        
        odpowiedz = messagebox.askyesno(
            "❓ Potwierdzenie",
            f"Czy na pewno usunąć grę:\n\n{pozycja.tytul}?"
        )
        
        if odpowiedz:
            self.katalog.usun_pozycje(pozycja.id)
            self.odswiez_liste()
            self.wyczysc_szczegoly()
            messagebox.showinfo("✅ Sukces", "Gra została usunięta")
    
    def ocen_gre(self):  # MŻ
        """Obsługuje dodawanie oceny"""
        pozycja = self.pobierz_wybrana_pozycje()
        
        if not pozycja:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Nie wybrano gry do oceny!")
            return
        
        # Zapamiętaj indeks przed odświeżeniem
        selection = self.listbox_gry.curselection()
        selected_index = selection[0] if selection else None
        
        dialog = DodajOceneDialog(self.root, pozycja.tytul)
        
        if dialog.result:
            ocena = dialog.result
            self.katalog.dodaj_ocene(pozycja.id, ocena)
            self.odswiez_liste()
            
            # Przywróć zaznaczenie
            if selected_index is not None and selected_index < self.listbox_gry.size():
                self.listbox_gry.selection_set(selected_index)
                self.listbox_gry.see(selected_index)
            
            self.wyswietl_szczegoly(self.pobierz_wybrana_pozycje())
            messagebox.showinfo("✅ Sukces", f"Dodano ocenę: {ocena}/10 ⭐")
    
    def wyszukaj(self):  # MŻ
        """Obsługuje wyszukiwanie gier"""
        dialog = WyszukajDialog(self.root)
        
        if dialog.result:
            fraza = dialog.result
            wyniki = self.katalog.wyszukaj(fraza)
            
            self.aktualne_pozycje = wyniki  # Zapisz wyniki wyszukiwania
            
            self.listbox_gry.delete(0, tk.END)
            for pozycja in wyniki:
                self.listbox_gry.insert(tk.END, str(pozycja))
            
            self.label_licznik.config(text=f"{len(wyniki)} gier")
            
            if not wyniki:
                messagebox.showinfo("🔍 Wynik", f"Nie znaleziono:\n'{fraza}'")
            else:
                messagebox.showinfo("🔍 Wynik", f"Znaleziono: {len(wyniki)} gier")
    
    def filtruj(self):  # MŻ
        """Obsługuje filtrowanie gier"""
        dialog = FiltrujDialog(self.root, self.katalog)
        
        if dialog.result:
            wyniki = dialog.result
            
            self.aktualne_pozycje = wyniki  # Zapisz wyniki filtrowania
            
            self.listbox_gry.delete(0, tk.END)
            for pozycja in wyniki:
                self.listbox_gry.insert(tk.END, str(pozycja))
            
            self.label_licznik.config(text=f"{len(wyniki)} gier")
            messagebox.showinfo("🎭 Wynik", f"Znaleziono: {len(wyniki)} gier")
    
    def sortuj(self):  # AY
        """Obsługuje sortowanie gier po ocenie"""
        if self.katalog.liczba_gier() == 0:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Katalog jest pusty!")
            return
        
        dialog = SortujDialog(self.root)
        
        if dialog.result is not None:
            malejaco = dialog.result
            posortowane = self.katalog.sortuj_po_ocenie(malejaco)
            
            self.aktualne_pozycje = posortowane  # Zapisz posortowane wyniki
            
            self.listbox_gry.delete(0, tk.END)
            for pozycja in posortowane:
                self.listbox_gry.insert(tk.END, str(pozycja))
            
            kierunek = "najlepszej do najgorszej" if malejaco else "najgorszej do najlepszej"
            messagebox.showinfo("🔽 Posortowano", f"Gry posortowane od {kierunek}!")
    
    def pokaz_statystyki(self):  # AY
        """Wyświetla okno ze statystykami"""
        StatystykiDialog(self.root, self.katalog)
    
    def on_closing(self):
        """Obsługuje zamykanie aplikacji"""
        self.katalog.zapisz()
        
        odpowiedz = messagebox.askyesno(
            "❓ Zamknąć program?",
            "Czy na pewno chcesz zamknąć Katalog Gier?\n\n"
            "Wszystkie dane zostały zapisane."
        )
        
        if odpowiedz:
            self.root.quit()
            self.root.destroy()
