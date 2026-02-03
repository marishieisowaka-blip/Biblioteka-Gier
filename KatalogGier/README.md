# 🎮 Katalog Gier

Aplikacja desktopowa do zarządzania kolekcją gier wideo napisana w Pythonie z interfejsem graficznym Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Opis projektu

**Katalog Gier** to kompleksowe narzędzie do organizacji i analizy kolekcji gier komputerowych. Aplikacja demonstruje praktyczne zastosowanie programowania obiektowego w Pythonie z persystencją danych w formacie JSON.

### ✨ Główne funkcje

- ➕ **Dodawanie gier** — tytuł, wydawca, gatunek (32 kategorie), rok wydania
- ⭐ **System oceniania** — wielokrotne oceny w skali 1-10 z automatycznym obliczaniem średniej
- 🔍 **Wyszukiwanie** — case-insensitive po tytułach
- 🎭 **Filtrowanie** — po gatunku i zakresie lat
- 🔽 **Sortowanie** — według średniej oceny
- 📊 **Statystyki** — najlepsza/najgorsza gra, średnia ocena kolekcji, rozkład gatunków
- 💾 **Automatyczny zapis** — persistencja danych w JSON
- 🎨 **Ciemny interfejs** — gamingowa stylistyka z kolorystycznymi akcentami

## 🚀 Uruchomienie

### Wymagania
- Python 3.8 lub nowszy
- Tkinter (zazwyczaj instalowane z Pythonem)

### Instalacja i uruchomienie

1. Pobierz projekt:
```bash
git clone https://github.com/TWOJ_USERNAME/KatalogGierPython.git
cd KatalogGierPython
```

2. Uruchom aplikację:
```bash
python main.py
```

## 📖 Jak używać

1. **Pierwsze uruchomienie** — aplikacja automatycznie załaduje 100 przykładowych gier
2. **Dodawanie gry** — kliknij "➕ Dodaj" i wypełnij formularz
3. **Ocenianie** — zaznacz grę i kliknij "⭐ Oceń" (1-10)
4. **Wyszukiwanie** — kliknij "🔍 Szukaj" i wpisz frazę
5. **Filtrowanie** — kliknij "🎭 Filtruj", wybierz gatunek i zakres lat
6. **Sortowanie** — kliknij "🔽 Sortuj" i wybierz kierunek
7. **Statystyki** — kliknij "📊 Statystyki" aby zobaczyć analizę kolekcji

## 🏗️ Architektura

Projekt zbudowany według wzorca **separacji warstw**:

```
KatalogGierPython/
├── main.py              # Entry point (15 linii)
├── modele.py            # Warstwa danych (170 linii)
├── katalog.py           # Logika biznesowa (730 linii)
├── main_window.py       # GUI - główne okno (560 linii)
├── dialogi.py           # Okna modalne (540 linii)
└── README.txt           # Dokumentacja użytkownika
```

## 🎯 4 Filary OOP

### 1. Enkapsulacja
Ukrywanie logiki biznesowej za metodami (`srednia_ocena()`, `to_dict()`).

### 2. Dziedziczenie
`Pozycja` dziedziczy po `ElementKatalogu` — reużywalny kod bazowy.

### 3. Polimorfizm
Nadpisana metoda `__str__()` — każda klasa formatuje się inaczej.

### 4. Abstrakcja
Proste API ukrywa złożoność (`katalog.wyszukaj()`, `katalog.zapisz()`).

## 💾 Persistencja danych

Wszystkie dane są automatycznie zapisywane do pliku `katalog.json` po każdej modyfikacji.

## 🔧 Technologie

- **Python 3.8+**
- **Tkinter** — natywny framework GUI
- **JSON** — format przechowywania danych
- **Type hints** — pełna adnotacja typów

## 👥 Autorzy

Projekt edukacyjny - demonstracja OOP w Pythonie.

## 📊 Statystyki projektu

- 5 plików źródłowych Python
- ~1400 linii kodu
- 32 kategorie gatunków gier
- 100 gier testowych
- 4 filary OOP w pełni zaimplementowane

## 📝 Licencja

MIT License - projekt edukacyjny
