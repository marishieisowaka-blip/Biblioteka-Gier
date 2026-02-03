"""
===============================================================================
PLIK: modele.py
OPIS: Klasy modelu danych dla aplikacji Katalog Gier
===============================================================================
"""

from datetime import datetime
from typing import List


class ElementKatalogu:
    """
    Klasa bazowa dla wszystkich elementów w katalogu.
    Możliwe rozszerzenia: Gra, Film, Książka, Album muzyczny, etc.
    """
    
    def __init__(self, id: int, tytul: str, rok: int):
        """
        Konstruktor klasy bazowej
        
        Args:
            id: Unikalny identyfikator
            tytul: Tytuł elementu
            rok: Rok wydania/powstania
        """
        self.id = id
        self.tytul = tytul
        self.rok = rok
    
    def informacje_podstawowe(self) -> str:
        """
        Zwraca podstawowe informacje (dla wszystkich typów elementów)
        
        Returns:
            String z podstawowymi danymi
        """
        return f"[ID: {self.id}] {self.tytul} ({self.rok})"
    
    def __str__(self) -> str:
        """
        Reprezentacja tekstowa (może być nadpisana w klasach pochodnych)
        """
        return self.informacje_podstawowe()


class OcenaGra:
    """Reprezentuje pojedynczą ocenę gry"""
    
    def __init__(self, wartosc: int):
        """
        Args:
            wartosc: Ocena w zakresie 1-10
        """
        self.wartosc = wartosc
        self.data_dodania = datetime.now()


class Pozycja(ElementKatalogu):
    """
    Reprezentuje pojedynczą grę w katalogu.
    Dziedziczy po ElementKatalogu i rozszerza o specyficzne pola dla gier.
    """
    
    def __init__(self, id: int = 0, tytul: str = "", wydawca: str = "", 
                 gatunek: str = "", rok: int = 2020):
        """
        Args:
            id: Unikalny identyfikator
            tytul: Tytuł gry
            wydawca: Wydawca/producent gry
            gatunek: Gatunek gry
            rok: Rok wydania
        """
        super().__init__(id, tytul, rok)
        self.wydawca = wydawca
        self.gatunek = gatunek
        self.oceny: List[OcenaGra] = []
    
    def srednia_ocena(self) -> float:
        """
        Oblicza średnią ocenę gry
        
        Returns:
            Średnia ocen lub 0 jeśli brak ocen
        """
        if not self.oceny:
            return 0.0
        return sum(o.wartosc for o in self.oceny) / len(self.oceny)
    
    def ocena_gwiazdkami(self) -> str:
        """
        Konwertuje średnią ocenę na gwiazdki (5-gwiazdkowa skala)
        
        Returns:
            String z gwiazdkami ★ i ☆
        """
        if not self.oceny:
            return "☆☆☆☆☆ (Brak ocen)"
        
        srednia = self.srednia_ocena()
        pelne_gwiazdki = round(srednia / 2.0)  # 10 punktów -> 5 gwiazdek
        puste_gwiazdki = 5 - pelne_gwiazdki
        
        gwiazdki = "★" * pelne_gwiazdki + "☆" * puste_gwiazdki
        return f"{gwiazdki} ({srednia:.2f}/10)"
    
    def __str__(self) -> str:
        """
        Formatowanie gry do wyświetlenia na liście.
        
        Returns:
            Sformatowany string z wydawcą
        """
        if self.oceny:
            srednia = self.srednia_ocena()
            pelne = round(srednia / 2.0)
            puste = 5 - pelne
            gwiazdki = "★" * pelne + "☆" * puste
            ocena_str = f"{gwiazdki} {srednia:.2f}"
        else:
            ocena_str = "☆☆☆☆☆"
        
        return f"[ID: {self.id}] {self.tytul} | {self.wydawca} | {self.gatunek} ({self.rok}) | {ocena_str}"
    
    def to_dict(self) -> dict:
        """
        Konwertuje grę do słownika (dla JSON)
        
        Returns:
            Słownik z danymi gry (z wydawcą)
        """
        return {
            'id': self.id,
            'tytul': self.tytul,
            'wydawca': self.wydawca,
            'gatunek': self.gatunek,
            'rok': self.rok,
            'oceny': [{'wartosc': o.wartosc, 'data_dodania': o.data_dodania.isoformat()} 
                     for o in self.oceny]
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Pozycja':
        """
        Tworzy grę ze słownika (z JSON)
        
        Args:
            data: Słownik z danymi gry
            
        Returns:
            Obiekt Pozycja
        """
        pozycja = Pozycja(
            id=data['id'],
            tytul=data['tytul'],
            wydawca=data.get('wydawca', 'Nieznany'),  # Obsługa starych danych bez wydawcy
            gatunek=data['gatunek'],
            rok=data['rok']
        )
        
        for ocena_data in data.get('oceny', []):
            ocena = OcenaGra(ocena_data['wartosc'])
            if 'data_dodania' in ocena_data:
                ocena.data_dodania = datetime.fromisoformat(ocena_data['data_dodania'])
            pozycja.oceny.append(ocena)
        
        return pozycja
