"""
===============================================================================
PLIK: katalog.py
OPIS: Zarządza kolekcją gier - główna logika biznesowa
===============================================================================
"""

import json
import os
from typing import List, Optional, Tuple, Dict
from modele import Pozycja, OcenaGra
class Katalog:
    """
    Zarządza całą kolekcją gier
    """
    
    # Predefiniowana lista gatunków gier
    GATUNKI = [
        "RPG",
        "Akcja",
        "Przygodowa",
        "Strategia",
        "Symulacja",
        "Wyścigi",
        "Sportowa",
        "Strzelanka (FPS/TPS)",
        "Platformówka",
        "Puzzle",
        "Horror",
        "Survival",
        "Sandbox",
        "MMORPG",
        "MOBA",
        "Battle Royale",
        "Roguelike",
        "Indie",
        "Fighting",
        "Rhythm",
        "Visual Novel",
        "Tower Defense",
        "RTS",
        "Turn-Based",
        "Metroidvania",
        "Stealth",
        "Open World",
        "Casual",
        "Edukacyjna",
        "Party",
        "Karciana",
        "Inne"
    ]
    
    def __init__(self):
        """Konstruktor katalogu"""
        self.pozycje: List[Pozycja] = []
        self.sciezka_pliku = "katalog.json"
    
    # =========================================================================
    # ZARZĄDZANIE DANYMI (CRUD)
    # =========================================================================
    
    def dodaj_pozycje(self, tytul: str, wydawca: str, gatunek: str, rok: int) -> Pozycja:  # MŻ
        """
        Dodaje nową grę do katalogu
        
        Args:
            tytul: Tytuł gry
            wydawca: Wydawca/producent gry
            gatunek: Gatunek
            rok: Rok wydania
            
        Returns:
            Nowo utworzona pozycja
        """
        # Znajdź najmniejsze wolne ID
        uzyte_id = {p.id for p in self.pozycje}
        nowe_id = 1
        while nowe_id in uzyte_id:
            nowe_id += 1
        
        pozycja = Pozycja(nowe_id, tytul, wydawca, gatunek, rok)
        self.pozycje.append(pozycja)
        self.zapisz()
        return pozycja
    
    def usun_pozycje(self, id: int) -> bool:  # MŻ
        """
        Usuwa grę z katalogu
        
        Args:
            id: ID gry do usunięcia
            
        Returns:
            True jeśli usunięto, False jeśli nie znaleziono
        """
        pozycja = self.pobierz_pozycje(id)
        if pozycja:
            self.pozycje.remove(pozycja)
            self.zapisz()
            return True
        return False
    
    def pobierz_pozycje(self, id: int) -> Optional[Pozycja]:
        """
        Pobiera grę po ID
        
        Args:
            id: ID gry
            
        Returns:
            Pozycja lub None jeśli nie znaleziono
        """
        for pozycja in self.pozycje:
            if pozycja.id == id:
                return pozycja
        return None
    
    def pobierz_wszystkie(self) -> List[Pozycja]:
        """
        Zwraca wszystkie gry
        
        Returns:
            Lista wszystkich pozycji
        """
        return self.pozycje.copy()
    
    def liczba_gier(self) -> int:
        """
        Zwraca liczbę gier w katalogu
        
        Returns:
            Liczba gier
        """
        return len(self.pozycje)
    
    # =========================================================================
    # OCENY
    # =========================================================================
    
    def dodaj_ocene(self, id: int, ocena: int) -> bool:  # MŻ
        """
        Dodaje ocenę do gry
        
        Args:
            id: ID gry
            ocena: Ocena w zakresie 1-10
            
        Returns:
            True jeśli dodano, False jeśli nie znaleziono gry
        """
        pozycja = self.pobierz_pozycje(id)
        if pozycja and 1 <= ocena <= 10:
            pozycja.oceny.append(OcenaGra(ocena))
            self.zapisz()
            return True
        return False
    
    # =========================================================================
    # WYSZUKIWANIE I FILTROWANIE
    # =========================================================================
    
    def wyszukaj(self, fraza: str) -> List[Pozycja]:  # MŻ
        """
        Wyszukuje gry po tytule
        
        Args:
            fraza: Fraza do wyszukania
            
        Returns:
            Lista znalezionych gier
        """
        fraza_lower = fraza.lower()
        return [p for p in self.pozycje if fraza_lower in p.tytul.lower()]
    
    def filtruj_po_gatunku(self, gatunek: str) -> List[Pozycja]:  # MŻ
        """
        Filtruje gry po gatunku
        
        Args:
            gatunek: Gatunek do filtrowania
            
        Returns:
            Lista przefiltrowanych gier
        """
        return [p for p in self.pozycje if p.gatunek == gatunek]
    
    def filtruj_po_roku(self, od_roku: int, do_roku: int) -> List[Pozycja]:  # AY
        """
        Filtruje gry po zakresie lat
        
        Args:
            od_roku: Początkowy rok
            do_roku: Końcowy rok
            
        Returns:
            Lista przefiltrowanych gier
        """
        return [p for p in self.pozycje if od_roku <= p.rok <= do_roku]
    
    def pobierz_gatunki(self) -> List[str]:
        """
        Zwraca listę unikalnych gatunków
        
        Returns:
            Posortowana lista gatunków
        """
        gatunki = set(p.gatunek for p in self.pozycje)
        return sorted(gatunki)
    
    # =========================================================================
    # STATYSTYKI
    # =========================================================================
    
    def najlepsza(self) -> Optional[Pozycja]:  # AY
        """
        Zwraca najlepiej ocenioną grę
        
        Returns:
            Gra z najwyższą średnią oceną lub None
        """
        ocenione = [p for p in self.pozycje if p.oceny]
        if not ocenione:
            return None
        return max(ocenione, key=lambda p: p.srednia_ocena())
    
    def najgorsza(self) -> Optional[Pozycja]:  # AY
        """
        Zwraca najgorzej ocenioną grę
        
        Returns:
            Gra z najniższą średnią oceną lub None
        """
        ocenione = [p for p in self.pozycje if p.oceny]
        if not ocenione:
            return None
        return min(ocenione, key=lambda p: p.srednia_ocena())
    
    def sortuj_po_ocenie(self, malejaco: bool = True) -> List[Pozycja]:  # AY
        """
        Sortuje gry po średniej ocenie
        
        Args:
            malejaco: True = od najlepszej do najgorszej (domyślnie)
                     False = od najgorszej do najlepszej
        
        Returns:
            Posortowana lista gier (gry ocenione + nieocenione na końcu)
        """
        # Rozdziel gry ocenione od nieocenionych
        ocenione = [p for p in self.pozycje if p.oceny]
        nieocenione = [p for p in self.pozycje if not p.oceny]
        
        # Sortuj gry ocenione
        ocenione.sort(key=lambda p: p.srednia_ocena(), reverse=malejaco)
        
        # Zwróć ocenione + nieocenione
        return ocenione + nieocenione
    
    def srednia_ocena_katalogu(self) -> float:  # AY
        """
        Oblicza średnią ocenę wszystkich gier
        
        Returns:
            Średnia ocena lub 0
        """
        ocenione = [p for p in self.pozycje if p.oceny]
        if not ocenione:
            return 0.0
        
        suma = sum(p.srednia_ocena() for p in ocenione)
        return suma / len(ocenione)
    
    def rozklad_gatunkow(self) -> Dict[str, int]:
        """
        Zwraca rozkład gier po gatunkach
        
        Returns:
            Słownik {gatunek: liczba_gier}
        """
        rozklad = {}
        for pozycja in self.pozycje:
            rozklad[pozycja.gatunek] = rozklad.get(pozycja.gatunek, 0) + 1
        return rozklad
    
    def zakres_lat(self) -> Tuple[int, int]:
        """
        Zwraca zakres lat wydania gier
        
        Returns:
            (najstarszy_rok, najnowszy_rok)
        """
        if not self.pozycje:
            return (0, 0)
        lata = [p.rok for p in self.pozycje]
        return (min(lata), max(lata))
    
    # =========================================================================
    # ZAPIS/ODCZYT JSON
    # =========================================================================
    
    def zapisz(self) -> None:
        """Zapisuje katalog do pliku JSON"""
        data = {
            'pozycje': [p.to_dict() for p in self.pozycje]
        }
        
        with open(self.sciezka_pliku, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def wczytaj(self) -> bool:
        """
        Wczytuje katalog z pliku JSON
        
        Returns:
            True jeśli wczytano, False jeśli plik nie istnieje
        """
        if not os.path.exists(self.sciezka_pliku):
            return False
        
        try:
            with open(self.sciezka_pliku, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.pozycje = [Pozycja.from_dict(p) for p in data['pozycje']]
            # nastepne_id nie jest już używane - ID są teraz dynamicznie przydzielane
            return True
        except Exception as e:
            print(f"Błąd wczytywania: {e}")
            return False
    
    # =========================================================================
    # DANE TESTOWE
    # =========================================================================
    
    def dodaj_dane_testowe(self) -> None:
        """Dodaje 100 przykładowych gier do katalogu - ze wszystkich 32 gatunków"""
        

        # RPG (Role-Playing Games) - 4 gry

        gra = self.dodaj_pozycje("Wiedźmin 3: Dziki Gon", "CD Projekt Red", "RPG", 2015)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Elden Ring", "FromSoftware", "RPG", 2022)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Baldur's Gate 3", "Larian Studios", "RPG", 2023)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Dark Souls III", "FromSoftware", "RPG", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # AKCJA (Action) - 4 gry

        gra = self.dodaj_pozycje("God of War (2018)", "Santa Monica Studio", "Akcja", 2018)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("The Last of Us", "Naughty Dog", "Akcja", 2013)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Spider-Man (2018)", "Insomniac Games", "Akcja", 2018)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Devil May Cry 5", "Capcom", "Akcja", 2019)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # PRZYGODOWA (Adventure) - 3 gry

        gra = self.dodaj_pozycje("The Legend of Zelda: BotW", "Nintendo", "Przygodowa", 2017)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Uncharted 4", "Naughty Dog", "Przygodowa", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("A Way Out", "Hazelight Studios", "Przygodowa", 2018)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # STRATEGIA (Strategy) - 3 gry

        gra = self.dodaj_pozycje("Civilization VI", "Firaxis Games", "Strategia", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("XCOM 2", "Firaxis Games", "Strategia", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Total War: Warhammer III", "Creative Assembly", "Strategia", 2022)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        

        # SYMULACJA (Simulation) - 3 gry

        gra = self.dodaj_pozycje("Stardew Valley", "ConcernedApe", "Symulacja", 2016)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("The Sims 4", "Maxis", "Symulacja", 2014)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 7)
        
        gra = self.dodaj_pozycje("Cities: Skylines", "Colossal Order", "Symulacja", 2015)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # WYŚCIGI (Racing) - 3 gry

        gra = self.dodaj_pozycje("Forza Horizon 5", "Playground Games", "Wyścigi", 2021)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Gran Turismo 7", "Polyphony Digital", "Wyścigi", 2022)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Need for Speed Heat", "Ghost Games", "Wyścigi", 2019)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 8)
        

        # SPORTOWA (Sports) - 3 gry

        gra = self.dodaj_pozycje("FIFA 23", "EA Sports", "Sportowa", 2022)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 7)
        
        gra = self.dodaj_pozycje("NBA 2K23", "Visual Concepts", "Sportowa", 2022)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Rocket League", "Psyonix", "Sportowa", 2015)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # STRZELANKA (FPS/TPS) - 4 gry

        gra = self.dodaj_pozycje("DOOM Eternal", "id Software", "Strzelanka (FPS/TPS)", 2020)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Valorant", "Riot Games", "Strzelanka (FPS/TPS)", 2020)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Call of Duty: Modern Warfare II", "Infinity Ward", "Strzelanka (FPS/TPS)", 2022)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Titanfall 2", "Respawn Entertainment", "Strzelanka (FPS/TPS)", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # PLATFORMÓWKA (Platformer) - 3 gry

        gra = self.dodaj_pozycje("Celeste", "Maddy Makes Games", "Platformówka", 2018)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Super Mario Odyssey", "Nintendo", "Platformówka", 2017)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Crash Bandicoot 4", "Toys for Bob", "Platformówka", 2020)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # PUZZLE - 3 gry

        gra = self.dodaj_pozycje("Portal 2", "Valve", "Puzzle", 2011)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("The Witness", "Thekla", "Puzzle", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Tetris Effect", "Monstars & Resonair", "Puzzle", 2018)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # HORROR - 3 gry

        gra = self.dodaj_pozycje("Resident Evil Village", "Capcom", "Horror", 2021)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Outlast", "Red Barrels", "Horror", 2013)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Dead Space", "EA Redwood Shores", "Horror", 2008)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # SURVIVAL - 3 gry

        gra = self.dodaj_pozycje("The Forest", "Endnight Games", "Survival", 2018)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Subnautica", "Unknown Worlds", "Survival", 2018)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Don't Starve", "Klei", "Survival", 2013)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        

        # SANDBOX - 3 gry

        gra = self.dodaj_pozycje("Minecraft", "Mojang", "Sandbox", 2011)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Terraria", "Re-Logic", "Sandbox", 2011)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Garry's Mod", "Facepunch Studios", "Sandbox", 2006)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # MMORPG - 3 gry

        gra = self.dodaj_pozycje("Final Fantasy XIV", "Square Enix", "MMORPG", 2013)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("World of Warcraft", "Blizzard", "MMORPG", 2004)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Guild Wars 2", "ArenaNet", "MMORPG", 2012)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # MOBA - 3 gry

        gra = self.dodaj_pozycje("League of Legends", "Riot Games", "MOBA", 2009)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Dota 2", "Valve", "MOBA", 2013)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Heroes of the Storm", "Blizzard", "MOBA", 2015)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 8)
        

        # BATTLE ROYALE - 3 gry

        gra = self.dodaj_pozycje("Fortnite", "Epic Games", "Battle Royale", 2017)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 7)
        
        gra = self.dodaj_pozycje("Apex Legends", "Respawn Entertainment", "Battle Royale", 2019)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("PUBG: Battlegrounds", "PUBG Corporation", "Battle Royale", 2017)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 7)
        

        # ROGUELIKE - 3 gry

        gra = self.dodaj_pozycje("Hades", "Supergiant Games", "Roguelike", 2020)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        
        gra = self.dodaj_pozycje("Dead Cells", "Motion Twin", "Roguelike", 2018)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("The Binding of Isaac", "Edmund McMillen", "Roguelike", 2011)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # INDIE - 3 gry

        gra = self.dodaj_pozycje("Undertale", "Toby Fox", "Indie", 2015)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Cuphead", "Studio MDHR", "Indie", 2017)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Hollow Knight", "Team Cherry", "Indie", 2017)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 10)
        

        # FIGHTING - 3 gry

        gra = self.dodaj_pozycje("Street Fighter 6", "Capcom", "Fighting", 2023)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Tekken 7", "Bandai Namco", "Fighting", 2017)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Super Smash Bros. Ultimate", "Nintendo", "Fighting", 2018)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        

        # RHYTHM - 3 gry

        gra = self.dodaj_pozycje("Beat Saber", "Beat Games", "Rhythm", 2019)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Guitar Hero III", "Neversoft", "Rhythm", 2007)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Geometry Dash", "RobTop Games", "Rhythm", 2013)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # VISUAL NOVEL - 3 gry

        gra = self.dodaj_pozycje("Doki Doki Literature Club", "Team Salvato", "Visual Novel", 2017)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Phoenix Wright: Ace Attorney", "Capcom", "Visual Novel", 2001)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Steins;Gate", "5pb.", "Visual Novel", 2009)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # TOWER DEFENSE - 3 gry

        gra = self.dodaj_pozycje("Bloons TD 6", "Ninja Kiwi", "Tower Defense", 2018)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Plants vs. Zombies", "PopCap Games", "Tower Defense", 2009)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Kingdom Rush", "Ironhide Game Studio", "Tower Defense", 2011)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # RTS (Real-Time Strategy) - 3 gry

        gra = self.dodaj_pozycje("StarCraft II", "Blizzard", "RTS", 2010)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Age of Empires II", "Ensemble Studios", "RTS", 1999)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Command & Conquer: Red Alert", "Westwood Studios", "RTS", 1996)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # TURN-BASED - 3 gry

        gra = self.dodaj_pozycje("Divinity: Original Sin 2", "Larian Studios", "Turn-Based", 2017)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Fire Emblem: Three Houses", "Intelligent Systems", "Turn-Based", 2019)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Into the Breach", "Subset Games", "Turn-Based", 2018)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # METROIDVANIA - 3 gry

        gra = self.dodaj_pozycje("Metroid Dread", "MercurySteam", "Metroidvania", 2021)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Ori and the Will of the Wisps", "Moon Studios", "Metroidvania", 2020)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Blasphemous", "The Game Kitchen", "Metroidvania", 2019)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # STEALTH - 3 gry

        gra = self.dodaj_pozycje("Metal Gear Solid V", "Kojima Productions", "Stealth", 2015)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Hitman 3", "IO Interactive", "Stealth", 2021)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Dishonored 2", "Arkane Studios", "Stealth", 2016)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        

        # OPEN WORLD - 3 gry

        gra = self.dodaj_pozycje("Red Dead Redemption 2", "Rockstar Games", "Open World", 2018)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("The Elder Scrolls V: Skyrim", "Bethesda", "Open World", 2011)
        self.dodaj_ocene(gra.id, 10); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Horizon Zero Dawn", "Guerrilla Games", "Open World", 2017)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        

        # CASUAL - 3 gry

        gra = self.dodaj_pozycje("Animal Crossing: New Horizons", "Nintendo", "Casual", 2020)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Candy Crush Saga", "King", "Casual", 2012)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 7)
        
        gra = self.dodaj_pozycje("Angry Birds", "Rovio", "Casual", 2009)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 7)
        

        # EDUKACYJNA (Educational) - 2 gry

        gra = self.dodaj_pozycje("Kerbal Space Program", "Squad", "Edukacyjna", 2015)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Human Resource Machine", "Tomorrow Corporation", "Edukacyjna", 2015)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        

        # PARTY - 3 gry

        gra = self.dodaj_pozycje("Among Us", "Innersloth", "Party", 2018)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Mario Party Superstars", "Nintendo", "Party", 2021)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Fall Guys", "Mediatonic", "Party", 2020)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 8)
        

        # KARCIANA (Card Game) - 3 gry

        gra = self.dodaj_pozycje("Hearthstone", "Blizzard", "Karciana", 2014)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Slay the Spire", "Mega Crit Games", "Karciana", 2019)
        self.dodaj_ocene(gra.id, 9); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Gwent", "CD Projekt Red", "Karciana", 2018)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 7)
        

        # INNE (Other) - 3 gry

        gra = self.dodaj_pozycje("Death Stranding", "Kojima Productions", "Inne", 2019)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 9)
        
        gra = self.dodaj_pozycje("Phasmophobia", "Kinetic Games", "Inne", 2020)
        self.dodaj_ocene(gra.id, 8); self.dodaj_ocene(gra.id, 8)
        
        gra = self.dodaj_pozycje("Goat Simulator", "Coffee Stain Studios", "Inne", 2014)
        self.dodaj_ocene(gra.id, 7); self.dodaj_ocene(gra.id, 7)
