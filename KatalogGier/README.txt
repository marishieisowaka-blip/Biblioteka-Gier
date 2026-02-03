===============================================================================
                         KATALOG GIER - PYTHON
                    APLIKACJA GUI Z TKINTER 🎨
===============================================================================

Aplikacja do zarządzania kolekcją gier wideo napisana w Pythonie z tkinter.


===============================================================================
URUCHOMIENIE
===============================================================================

python main.py

lub

python3 main.py


===============================================================================
WYMAGANIA
===============================================================================

Python:          3.7+
Biblioteki:      tkinter (biblioteka standardowa)
System:          Windows, Linux, macOS


===============================================================================
FUNKCJONALNOŚĆ
===============================================================================

✅ Pełne programowanie obiektowe (4 filary OOP)
   ├─ Enkapsulacja
   ├─ Dziedziczenie (ElementKatalogu → Pozycja)
   ├─ Polimorfizm
   └─ Abstrakcja

✅ Zarządzanie grami
   ├─ Dodawanie, usuwanie gier
   ├─ Ocenianie gier (1-10)
   ├─ Wydawca, gatunek, rok wydania
   └─ Automatyczny zapis do JSON

✅ Wyszukiwanie i filtrowanie
   ├─ Wyszukiwanie po tytule
   ├─ Filtrowanie po gatunku
   ├─ Filtrowanie po roku
   └─ Sortowanie po ocenie

✅ Statystyki
   ├─ Najlepsza/najgorsza gra
   ├─ Średnia ocena katalogu
   ├─ Rozkład gatunków
   └─ Zakres lat wydania

✅ 100 przykładowych gier
   ├─ Ze wszystkich 32 gatunków
   ├─ Prawdziwe tytuły i wydawcy
   └─ Automatyczne ładowanie przy pierwszym uruchomieniu


===============================================================================
STRUKTURA PROJEKTU
===============================================================================

KatalogGierPython/
├─ main.py              - Punkt startowy aplikacji
├─ main_window.py       - Główne okno GUI
├─ katalog.py           - Logika zarządzania grami
├─ modele.py            - Klasy: ElementKatalogu, Pozycja, OcenaGra
├─ dialogi.py           - Okna dialogowe
└─ katalog.json         - Automatyczny zapis danych


===============================================================================
GATUNKI GIER (32)
===============================================================================

RPG, Akcja, Przygodowa, Strategia, Symulacja, Wyścigi, Sportowa,
Strzelanka (FPS/TPS), Platformówka, Puzzle, Horror, Survival, Sandbox,
MMORPG, MOBA, Battle Royale, Roguelike, Indie, Fighting, Rhythm,
Visual Novel, Tower Defense, RTS, Turn-Based, Metroidvania, Stealth,
Open World, Casual, Edukacyjna, Party, Karciana, Inne


===============================================================================
PALETA KOLORÓW
===============================================================================

Ciemny motyw (Dark Theme):
├─ Tło główne:     #1a1a2e
├─ Tło średnie:    #16213e
├─ Tło jasne:      #0f3460
├─ Akcent:         #e94560
├─ Sukces:         #00d9a5
├─ Ostrzeżenie:    #f39c12
└─ Niebezpiecz.:   #e74c3c


===============================================================================
STATYSTYKI
===============================================================================

Pliki:          5
Linie kodu:     ~2,500
Klasy:          9
Funkcje:        ~50
Gier testowych: 100


===============================================================================

Miłego korzystania! 🎮✨
