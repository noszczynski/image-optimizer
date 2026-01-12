# Image Optimizer
 
Prosty, lokalny optymalizator zdjęć z CLI. Konwertuj obrazy do formatu WebP, JPEG lub PNG z kompresją i automatycznym usuwaniem metadanych.

## Wymagania

- Python 3.11 lub nowszy
- Pillow (instalacja poniżej)
- tkinter (opcjonalne, wymagane tylko dla GUI file pickera)

**Uwaga**: Jeśli Python został zainstalowany przez Homebrew, tkinter może nie być dostępny. Zainstaluj go przez:

```bash
brew install python-tk@3.14
```

(Zamień 3.14 na swoją wersję Pythona)

## Instalacja

1. Sklonuj lub pobierz to repozytorium
2. Stwórz virtual environment i zainstaluj zależności:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Ustaw uprawnienia wykonywalne:

```bash
chmod +x optimize.py
```

4. (Opcjonalnie) Dodaj alias do swojego `.zshrc` dla globalnego dostępu - zobacz [INSTALL.md](INSTALL.md) dla szczegółowych instrukcji

## Użycie

### Podstawowe użycie

```bash
# Z GUI picker (otworzy Finder do wyboru plików)
optimize --format webp --quality 80

# Podaj pliki w CLI
optimize --input cat.jpg dog.png --format webp

# Używaj wildcards
optimize --input photos/*.jpg --format webp --quality 85

# Domyślne wartości (format: webp, quality: 80)
optimize --input image.png
```

### Opcje

- `--input` - Ścieżki do plików wejściowych (do 20 plików). Jeśli nie podano, otworzy się GUI picker
- `--format` - Format wyjściowy: `webp` (domyślnie), `jpeg`, `png`
- `--quality` - Jakość kompresji 1-100 (domyślnie: 80). Wyższa wartość = lepsza jakość, większy rozmiar

## Funkcje

- ✅ Konwersja między formatami: PNG, JPEG, WebP
- ✅ Kompresja z konfigurowalnją jakością
- ✅ Automatyczne usuwanie metadanych EXIF
- ✅ GUI file picker (Finder na macOS)
- ✅ Obsługa do 20 plików jednocześnie
- ✅ Wykrywanie konfliktów nazw z interaktywnym wyborem
- ✅ Raportowanie oszczędności miejsca

## Przykładowy output

```
Processing 3 files...
[1/3] cat.jpg → cat.webp
  Output file exists. Overwrite? [y/n/r(ename)]: y
  ✓ 2.4 MB → 856 KB (64% reduction)
[2/3] dog.png → dog.webp
  ✓ 1.8 MB → 423 KB (76% reduction)
[3/3] vacation.jpg → vacation.webp
  ✓ 3.1 MB → 1.2 MB (61% reduction)

Summary:
  Processed: 3/3 files
  Total saved: 5.5 MB (65% average reduction)
```

## Obsługiwane formaty

**Wejściowe**: PNG, JPEG, JPG, WebP, BMP, GIF, TIFF

**Wyjściowe**: PNG, JPEG, WebP

## Licencja

MIT
