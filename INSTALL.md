# Instalacja globalnego dostępu do komendy `optimize`
 
## Szybka instalacja

Aby komenda `optimize` była dostępna z dowolnego miejsca w systemie, dodaj alias do swojego `.zshrc`:

```bash
echo 'alias optimize="/Users/user/python-image-optimizer/venv/bin/python /Users/user/learn/python-image-optimizer/optimize.py"' >> ~/.zshrc
source ~/.zshrc
```

**UWAGA**: Zmień ścieżkę `/Users/user/python-image-optimizer/` na właściwą ścieżkę do tego projektu na Twoim systemie.

## Weryfikacja

Po dodaniu aliasu, sprawdź czy działa:

```bash
cd ~/Downloads
optimize --help
```

Powinieneś zobaczyć pomoc dla komendy.

## Przykładowe użycie po instalacji

```bash
# Z dowolnego miejsca w systemie
cd ~/Photos/vacation
optimize --input *.jpg --format webp --quality 85

# Lub z GUI picker
cd ~/Documents
optimize --format webp
```

## Deinstalacja

Jeśli chcesz usunąć alias, edytuj plik `~/.zshrc` i usuń linię z aliasem `optimize`, następnie:

```bash
source ~/.zshrc
```
