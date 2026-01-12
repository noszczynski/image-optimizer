#!/usr/bin/env python3
""" 
Image Optimizer - Lokalny optymalizator zdjęć
Konwertuj obrazy z kompresją i usuwaniem metadanych
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image


# Supported formats
SUPPORTED_OUTPUT_FORMATS = ['png', 'jpeg', 'webp']
SUPPORTED_INPUT_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff', '.tif']

# Limits
MAX_FILES = 20


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Optymalizuj i konwertuj obrazy z kompresją i usuwaniem metadanych',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s --input cat.jpg dog.png --format webp
  %(prog)s --input photos/*.jpg --format jpeg --quality 85
  %(prog)s --format webp  # Otworzy GUI picker
        """
    )
    
    parser.add_argument(
        '--input',
        nargs='+',
        metavar='FILE',
        help='Pliki wejściowe (do 20 plików). Jeśli nie podano, otworzy się GUI picker'
    )
    
    parser.add_argument(
        '--format',
        choices=SUPPORTED_OUTPUT_FORMATS,
        default='webp',
        help='Format wyjściowy (domyślnie: webp)'
    )
    
    parser.add_argument(
        '--quality',
        type=int,
        default=80,
        metavar='N',
        help='Jakość kompresji 1-100 (domyślnie: 80)'
    )
    
    return parser.parse_args()


def open_file_picker() -> List[Path]:
    """Open GUI file picker and return selected files"""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("❌ Błąd: tkinter nie jest zainstalowany.")
        print("   GUI file picker wymaga tkinter. Zainstaluj go przez:")
        print("   brew install python-tk@3.14")
        print("\n   Lub użyj flagi --input aby podać pliki bezpośrednio.")
        sys.exit(1)
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    root.attributes('-topmost', True)  # Bring to front
    
    # Get current working directory
    current_dir = Path.cwd()
    
    file_paths = filedialog.askopenfilenames(
        title='Wybierz obrazy do optymalizacji (max 20)',
        initialdir=str(current_dir),
        filetypes=[
            ('Obrazy', ' '.join(f'*{ext}' for ext in SUPPORTED_INPUT_EXTENSIONS)),
            ('Wszystkie pliki', '*.*')
        ]
    )
    
    root.destroy()
    
    if not file_paths:
        print("Nie wybrano żadnych plików.")
        sys.exit(0)
    
    return [Path(fp) for fp in file_paths]


def validate_files(file_paths: List[Path]) -> List[Path]:
    """Validate input files and return valid ones"""
    if len(file_paths) > MAX_FILES:
        print(f"❌ Błąd: Można przetwarzać maksymalnie {MAX_FILES} plików na raz.")
        print(f"   Wybrano: {len(file_paths)} plików")
        sys.exit(1)
    
    valid_files = []
    
    for file_path in file_paths:
        if not file_path.exists():
            print(f"⚠️  Pominięto: {file_path} (plik nie istnieje)")
            continue
        
        if not file_path.is_file():
            print(f"⚠️  Pominięto: {file_path} (nie jest plikiem)")
            continue
        
        if file_path.suffix.lower() not in SUPPORTED_INPUT_EXTENSIONS:
            print(f"⚠️  Pominięto: {file_path} (nieobsługiwany format)")
            continue
        
        # Try to open with Pillow to verify it's a valid image
        try:
            with Image.open(file_path) as img:
                img.verify()
            valid_files.append(file_path)
        except Exception as e:
            print(f"⚠️  Pominięto: {file_path} (nie można otworzyć: {e})")
    
    if not valid_files:
        print("❌ Nie znaleziono poprawnych plików do przetworzenia.")
        sys.exit(1)
    
    return valid_files


def validate_quality(quality: int) -> None:
    """Validate quality parameter"""
    if not 1 <= quality <= 100:
        print(f"❌ Błąd: Jakość musi być w zakresie 1-100 (podano: {quality})")
        sys.exit(1)


def get_output_path(input_path: Path, output_format: str) -> Path:
    """Generate output file path"""
    return input_path.parent / f"{input_path.stem}.{output_format}"


def prompt_overwrite(output_path: Path) -> str:
    """Ask user what to do if output file exists. Returns: 'skip', 'overwrite', or new filename"""
    while True:
        response = input(f"  Plik {output_path.name} już istnieje. Nadpisać? [y/n/r(ename)]: ").lower().strip()
        
        if response in ['y', 'yes', 't', 'tak']:
            return 'overwrite'
        elif response in ['n', 'no', 'nie']:
            return 'skip'
        elif response in ['r', 'rename']:
            new_name = input(f"  Podaj nową nazwę pliku (bez rozszerzenia): ").strip()
            if new_name:
                return new_name
            print("  Nieprawidłowa nazwa, spróbuj ponownie.")
        else:
            print("  Nieprawidłowa odpowiedź. Użyj: y (yes), n (no), r (rename)")


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def optimize_image(input_path: Path, output_format: str, quality: int) -> Tuple[Path, int, int]:
    """
    Optimize and convert image.
    Returns: (output_path, original_size, optimized_size)
    """
    original_size = input_path.stat().st_size
    
    # Open image
    with Image.open(input_path) as img:
        # Convert color mode if necessary
        if output_format == 'jpeg':
            # JPEG doesn't support transparency, convert RGBA to RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
        else:
            # For PNG and WebP, preserve transparency
            if img.mode in ('P', 'L', 'LA'):
                img = img.convert('RGBA')
            elif img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
        
        # Generate output path
        output_path = get_output_path(input_path, output_format)
        
        # Check if output file exists
        if output_path.exists():
            action = prompt_overwrite(output_path)
            
            if action == 'skip':
                return None, original_size, 0
            elif action != 'overwrite':
                # Custom name provided
                output_path = input_path.parent / f"{action}.{output_format}"
                # Check again if new name exists
                if output_path.exists():
                    print(f"  ⚠️  Plik {output_path.name} również istnieje. Pomijam.")
                    return None, original_size, 0
        
        # Save with optimization
        save_kwargs = {
            'optimize': True,
            'quality': quality,
        }
        
        # Remove metadata (no EXIF data saved)
        if output_format == 'jpeg':
            save_kwargs['exif'] = b''
        
        img.save(output_path, format=output_format.upper(), **save_kwargs)
    
    optimized_size = output_path.stat().st_size
    return output_path, original_size, optimized_size


def main():
    """Main function"""
    args = parse_arguments()
    
    # Validate quality
    validate_quality(args.quality)
    
    # Get input files
    if args.input:
        input_files = [Path(f) for f in args.input]
    else:
        print("🖼️  Otwieranie GUI file picker...")
        input_files = open_file_picker()
    
    # Validate files
    valid_files = validate_files(input_files)
    
    print(f"\n📊 Przetwarzanie {len(valid_files)} plików...\n")
    
    # Process files
    processed_count = 0
    skipped_count = 0
    total_original_size = 0
    total_optimized_size = 0
    
    for idx, input_path in enumerate(valid_files, 1):
        print(f"[{idx}/{len(valid_files)}] {input_path.name} → {input_path.stem}.{args.format}")
        
        try:
            result = optimize_image(input_path, args.format, args.quality)
            
            if result[0] is None:
                print(f"  ⏭️  Pominięto")
                skipped_count += 1
            else:
                output_path, original_size, optimized_size = result
                total_original_size += original_size
                total_optimized_size += optimized_size
                processed_count += 1
                
                reduction = 100 * (1 - optimized_size / original_size) if original_size > 0 else 0
                
                if optimized_size < original_size:
                    print(f"  ✓ {format_size(original_size)} → {format_size(optimized_size)} ({reduction:.0f}% redukcji)")
                elif optimized_size > original_size:
                    increase = 100 * (optimized_size / original_size - 1)
                    print(f"  ✓ {format_size(original_size)} → {format_size(optimized_size)} (+{increase:.0f}% większy)")
                else:
                    print(f"  ✓ {format_size(optimized_size)} (bez zmiany rozmiaru)")
        
        except Exception as e:
            print(f"  ❌ Błąd: {e}")
            skipped_count += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print("📈 Podsumowanie:")
    print(f"  Przetworzono: {processed_count}/{len(valid_files)} plików")
    
    if skipped_count > 0:
        print(f"  Pominięto: {skipped_count} plików")
    
    if processed_count > 0:
        total_saved = total_original_size - total_optimized_size
        if total_saved > 0:
            avg_reduction = 100 * total_saved / total_original_size
            print(f"  Zaoszczędzono: {format_size(total_saved)} ({avg_reduction:.0f}% średniej redukcji)")
        elif total_saved < 0:
            total_increase = total_optimized_size - total_original_size
            avg_increase = 100 * total_increase / total_original_size
            print(f"  Zwiększono o: {format_size(total_increase)} ({avg_increase:.0f}% średniego wzrostu)")
        else:
            print(f"  Rozmiar bez zmian")
    
    print(f"{'='*60}\n")
    
    if processed_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Przerwano przez użytkownika")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)
