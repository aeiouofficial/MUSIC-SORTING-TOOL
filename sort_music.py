"""
OPTIMIZED MUSIC SORTING SCRIPT
===============================
Efficiently organizes .wav files into genre-based folders with batch processing.
Handles versioning, favorites (+++), and provides detailed progress tracking.
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict
import time

# ============================================================================
# CONFIGURATION - MODIFY THESE AS NEEDED
# ============================================================================

GENRE_RULES = {
    # Priority 1: Stems and Production Files (highest priority)
    'stems_vocals': {
        'folder': '06_Stems_Production/Vocals',
        'keywords': [r'\(vocals?\)'],
        'priority': 1
    },
    'stems_instrumental': {
        'folder': '06_Stems_Production/Instrumental',
        'keywords': [r'\binstrumental\b', r'\(instrumental\)'],
        'priority': 1
    },
    'stems_other': {
        'folder': '06_Stems_Production/Stems',
        'keywords': [r'\(bass\)', r'\(drums?\)', r'\(other\)', r'\(stem'],
        'priority': 1
    },
    
    # Priority 2: Remixes and Edits
    'remixes_artists': {
        'folder': '05_Remixes_Edits/Artist_Remixes',
        'keywords': [r'\banyma\b', r'\bargy\b', r'\bklingande\b', r'\bjubel\b', r'son of son'],
        'priority': 2
    },
    'remixes_extended': {
        'folder': '05_Remixes_Edits/Extended_Versions',
        'keywords': [r'\bremix\b', r'\bedit\b', r'\bext v\d+', r'\bextended\b'],
        'priority': 2
    },
    
    # Priority 3: Electronic Subgenres
    'electronic_house': {
        'folder': '01_Electronic_Dance/House',
        'keywords': [r'\bhouse\b', r'\bdeep house\b', r'\bprogressive house\b'],
        'priority': 3
    },
    'electronic_techno': {
        'folder': '01_Electronic_Dance/Techno',
        'keywords': [r'\btechno\b', r'\bmelodic techno\b'],
        'priority': 3
    },
    'electronic_psytrance': {
        'folder': '01_Electronic_Dance/Psytrance',
        'keywords': [r'\bpsytrance\b', r'\bpsychedelic\b', r'\bpsych\b'],
        'priority': 3
    },
    'electronic_idm': {
        'folder': '01_Electronic_Dance/IDM',
        'keywords': [r'\bidm\b', r'\bintelligent dance\b'],
        'priority': 3
    },
    'electronic_electro': {
        'folder': '01_Electronic_Dance/Electro',
        'keywords': [r'\belectro\b', r'\belectronic\b', r'\belectronica\b'],
        'priority': 3
    },
    
    # Priority 4: Atmospheric Electronic
    'atmospheric_hypnotic': {
        'folder': '02_Atmospheric_Electronic/Hypnotic',
        'keywords': [r'\bhypnotic\b', r'\btrance\b'],
        'priority': 4
    },
    'atmospheric_ethereal': {
        'folder': '02_Atmospheric_Electronic/Ethereal',
        'keywords': [r'\bethereal\b', r'\bdream\b', r'\bdreamy\b'],
        'priority': 4
    },
    'atmospheric_melodic': {
        'folder': '02_Atmospheric_Electronic/Melodic',
        'keywords': [r'\bmelodic\b', r'\beuphoric\b', r'\bmellow\b', r'\bsoothing\b'],
        'priority': 4
    },
    'atmospheric_ambient': {
        'folder': '02_Atmospheric_Electronic/Ambient',
        'keywords': [r'\bambient\b', r'\batmospheric\b', r'\bcosmic\b', r'\bspace\b'],
        'priority': 4
    },
    
    # Priority 5: Rock and Pop
    'rock': {
        'folder': '03_Rock_Alternative/Rock',
        'keywords': [r'\brock\b', r'\balternative\b', r'\bindie\b', r'\bpunk\b', r'\bmetal\b'],
        'priority': 5
    },
    'pop': {
        'folder': '04_Pop_Mainstream/Pop',
        'keywords': [r'\bpop\b', r'\bsynthpop\b'],
        'priority': 5
    },
    
    # Priority 6: German Electronic (catches remaining German tracks)
    'german': {
        'folder': '07_German_Electronic/Deutsche_Tracks',
        'keywords': [r'\bder\b', r'\bdie\b', r'\bdas\b', r'\bzeit\b', r'\btanz\b', 
                    r'\bwald\b', r'\bschwingung\b', r'\bkreist\b', r'\bhalsband\b',
                    r'\bflimmern\b', r'\bsymbole\b', r'\binkubation\b', r'\bnur\b'],
        'priority': 6
    },
}

UNCATEGORIZED_FOLDER = '99_Uncategorized/Other'
FAVORITES_SUBFOLDER = '_FAVORITES'
BATCH_SIZE = 50  # Process files in batches for better performance

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_next_version_filename(dest_path):
    """Get versioned filename if file already exists."""
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    parent = dest_path.parent
    counter = 2
    
    while True:
        new_name = f"{stem} v{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def classify_file(filename_lower):
    """Classify file based on keywords in filename. Returns (folder, priority) or None."""
    # Sort rules by priority
    sorted_rules = sorted(GENRE_RULES.items(), key=lambda x: x[1]['priority'])
    
    for rule_name, rule_data in sorted_rules:
        for pattern in rule_data['keywords']:
            if re.search(pattern, filename_lower, re.IGNORECASE):
                return (rule_data['folder'], rule_data['priority'])
    
    return (UNCATEGORIZED_FOLDER, 999)

def is_favorite(filename):
    """Check if file is marked as favorite (starts with +++)."""
    return filename.startswith('+++')

def copy_file_with_versioning(source_path, dest_folder, base_path):
    """Copy file to destination with automatic versioning if needed."""
    dest_folder_path = base_path / dest_folder
    dest_folder_path.mkdir(parents=True, exist_ok=True)
    
    dest_file = dest_folder_path / source_path.name
    final_dest = get_next_version_filename(dest_file)
    
    shutil.copy2(source_path, final_dest)
    return final_dest

# ============================================================================
# MAIN SORTING LOGIC
# ============================================================================

def scan_files(source_dir, exclude_folders=None):
    """Scan directory for .wav files and return list of paths."""
    if exclude_folders is None:
        exclude_folders = ['SORTED_MUSIC']
    
    wav_files = []
    source_path = Path(source_dir)
    
    print("📁 Scanning for .wav files...")
    for root, dirs, files in os.walk(source_path):
        # Remove excluded folders from traversal
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        
        for file in files:
            if file.lower().endswith('.wav'):
                wav_files.append(Path(root) / file)
    
    return wav_files

def sort_music(source_dir, output_dir=None):
    """Main function to sort music files."""
    source_path = Path(source_dir)
    
    if output_dir is None:
        output_path = source_path / 'SORTED_MUSIC'
    else:
        output_path = Path(output_dir)
    
    print("=" * 70)
    print("🎵 MUSIC SORTING SCRIPT - OPTIMIZED VERSION")
    print("=" * 70)
    print(f"Source Directory: {source_path}")
    print(f"Output Directory: {output_path}")
    print()
    
    # Step 1: Scan files
    start_time = time.time()
    all_files = scan_files(source_path, exclude_folders=['SORTED_MUSIC'])
    print(f"✓ Found {len(all_files)} .wav files\n")
    
    if len(all_files) == 0:
        print("❌ No .wav files found!")
        return
    
    # Step 2: Classify all files (fast, no I/O)
    print("🔍 Classifying files...")
    classification_map = {}
    stats = defaultdict(int)
    favorites_count = 0
    
    for file_path in all_files:
        filename_lower = file_path.name.lower()
        folder, priority = classify_file(filename_lower)
        classification_map[file_path] = folder
        stats[folder] += 1
        
        if is_favorite(file_path.name):
            favorites_count += 1
    
    print(f"✓ Classification complete\n")
    
    # Step 3: Display statistics
    print("📊 CLASSIFICATION SUMMARY:")
    print("-" * 70)
    for folder in sorted(stats.keys()):
        count = stats[folder]
        percentage = (count / len(all_files)) * 100
        print(f"{folder:50} {count:5} files ({percentage:5.1f}%)")
    print(f"\n⭐ Favorites (+++): {favorites_count} files\n")
    
    # Step 4: Process files in batches
    print("📦 Copying files...")
    processed = 0
    errors = []
    
    for i in range(0, len(all_files), BATCH_SIZE):
        batch = all_files[i:i + BATCH_SIZE]
        
        for source_file in batch:
            try:
                dest_folder = classification_map[source_file]
                
                # Copy to main folder
                copy_file_with_versioning(source_file, dest_folder, output_path)
                
                # If favorite, also copy to _FAVORITES subfolder
                if is_favorite(source_file.name):
                    fav_folder = f"{dest_folder}/{FAVORITES_SUBFOLDER}"
                    copy_file_with_versioning(source_file, fav_folder, output_path)
                
                processed += 1
                
                # Progress update every batch
                if processed % BATCH_SIZE == 0:
                    progress = (processed / len(all_files)) * 100
                    print(f"  Progress: {processed}/{len(all_files)} ({progress:.1f}%)")
                
            except Exception as e:
                errors.append((source_file.name, str(e)))
    
    # Final stats
    elapsed_time = time.time() - start_time
    print()
    print("=" * 70)
    print("✅ SORTING COMPLETE!")
    print("=" * 70)
    print(f"Total files processed: {processed}")
    print(f"Favorites copied: {favorites_count}")
    print(f"Errors: {len(errors)}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Output location: {output_path}")
    
    if errors:
        print("\n⚠️  ERRORS:")
        for filename, error in errors[:10]:  # Show first 10 errors
            print(f"  - {filename}: {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    print("=" * 70)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sort_music.py <source_directory> [output_directory]")
        print("\nExample:")
        print('  python sort_music.py "C:\\Music\\Unsorted"')
        print('  python sort_music.py "C:\\Music\\Unsorted" "D:\\Music\\Sorted"')
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    sort_music(source_dir, output_dir)
