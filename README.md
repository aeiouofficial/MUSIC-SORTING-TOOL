================================================================================
                    MUSIC SORTING TOOL - USER GUIDE
================================================================================

📖 OVERVIEW
-----------
This tool automatically organizes .wav music files into genre-based folders
based on keywords found in filenames. It handles versioning, favorites, and
provides detailed progress tracking.

⚡ FEATURES
-----------
✓ Batch processing for optimal performance
✓ Automatic genre classification based on filename keywords
✓ No file overwrites - automatic versioning (v2, v3, etc.)
✓ Special handling for favorite tracks (+++prefix)
✓ Progress tracking and statistics
✓ Handles stems, remixes, and production files
✓ Preserves original files (copies, doesn't move)

📁 FOLDER STRUCTURE CREATED
----------------------------
SORTED_MUSIC/
├── 01_Electronic_Dance/
│   ├── House/
│   ├── Techno/
│   ├── Psytrance/
│   ├── Electro/
│   └── IDM/
├── 02_Atmospheric_Electronic/
│   ├── Hypnotic/
│   ├── Ethereal/
│   ├── Melodic/
│   └── Ambient/
├── 03_Rock_Alternative/
│   └── Rock/
├── 04_Pop_Mainstream/
│   └── Pop/
├── 05_Remixes_Edits/
│   ├── Artist_Remixes/
│   └── Extended_Versions/
├── 06_Stems_Production/
│   ├── Vocals/
│   ├── Instrumental/
│   └── Stems/
├── 07_German_Electronic/
│   └── Deutsche_Tracks/
└── 99_Uncategorized/
    └── Other/

🔧 USAGE
--------

METHOD 1: Command Line (Recommended)
-------------------------------------
Open PowerShell or Command Prompt and run:

    python D:\MusicSortingTool\sort_music.py "C:\Path\To\Your\Music"

The script will create a SORTED_MUSIC folder inside your music directory.

To specify a different output location:

    python D:\MusicSortingTool\sort_music.py "C:\Path\To\Source" "D:\Path\To\Output"


METHOD 2: Python Environment
-----------------------------
If you're in a Python environment (VS Code, Jupyter, etc.):

    import sys
    sys.path.append(r'D:\MusicSortingTool')
    from sort_music import sort_music
    
    sort_music(r'C:\Path\To\Your\Music')


METHOD 3: Drag & Drop (Windows)
--------------------------------
Create a batch file for easy drag-and-drop:

1. Create a new file called "sort_music.bat" with this content:

    @echo off
    python D:\MusicSortingTool\sort_music.py "%~1"
    pause

2. Drag your music folder onto this batch file


🎯 CLASSIFICATION RULES
-----------------------
Files are classified in priority order (first match wins):

PRIORITY 1 - Stems & Production:
  - (vocals), (vocal) → Vocals
  - (bass), (drums), (other), (stems) → Stems
  - instrumental, (instrumental) → Instrumental

PRIORITY 2 - Remixes & Edits:
  - anyma, argy, klingande, jubel, "son of son" → Artist_Remixes
  - remix, edit, ext v1, extended → Extended_Versions

PRIORITY 3 - Electronic Subgenres:
  - house, deep house, progressive house → House
  - techno, melodic techno → Techno
  - psytrance, psychedelic, psych → Psytrance
  - idm, intelligent dance → IDM
  - electro, electronic, electronica → Electro

PRIORITY 4 - Atmospheric:
  - hypnotic, trance → Hypnotic
  - ethereal, dream, dreamy → Ethereal
  - melodic, euphoric, mellow, soothing → Melodic
  - ambient, atmospheric, cosmic, space → Ambient

PRIORITY 5 - Rock & Pop:
  - rock, alternative, indie, punk, metal → Rock
  - pop, synthpop → Pop

PRIORITY 6 - German Electronic:
  - der, die, das, zeit, tanz, wald, schwingung, etc. → Deutsche_Tracks

PRIORITY 999 - Uncategorized:
  - Everything else → Other


⭐ FAVORITES HANDLING
---------------------
Files starting with "+++" are considered favorites:

Example: "+++Awesome Track.wav"

These files are copied to TWO locations:
1. Their normal genre folder
2. A _FAVORITES subfolder within that genre

Example:
  01_Electronic_Dance/House/+++Awesome Track.wav
  01_Electronic_Dance/House/_FAVORITES/+++Awesome Track.wav


🔄 VERSIONING
-------------
If a file with the same name already exists at the destination, the script
will NOT overwrite it. Instead, it appends a version number:

Original:  track.wav
Already exists at destination
New file:  track v2.wav

If track v2.wav also exists:
New file:  track v3.wav

And so on...


⚙️ CUSTOMIZATION
----------------
You can customize the classification rules by editing sort_music.py:

1. Open D:\MusicSortingTool\sort_music.py in a text editor
2. Find the GENRE_RULES dictionary (near top of file)
3. Add/modify/remove rules as needed

Example - Adding a new genre:

    'electronic_dubstep': {
        'folder': '01_Electronic_Dance/Dubstep',
        'keywords': [r'\bdubstep\b', r'\bbrostep\b'],
        'priority': 3
    },

Tips for keywords:
- Use \b for word boundaries (matches "techno" but not "biotechno")
- Use regular expressions for flexible matching
- Lower priority number = checked first


📊 OUTPUT & STATISTICS
----------------------
The script provides detailed statistics:

- Total files found
- Classification breakdown by genre
- Number of favorites
- Processing progress (real-time updates)
- Time elapsed
- Any errors encountered


❗ IMPORTANT NOTES
------------------
1. Original files are NEVER modified or moved - only copied
2. The script skips any existing SORTED_MUSIC folder when scanning
3. Progress updates appear every 50 files (configurable via BATCH_SIZE)
4. File metadata (creation date, etc.) is preserved during copying
5. Special characters in filenames are sanitized automatically


🐛 TROUBLESHOOTING
------------------

Problem: "No .wav files found"
Solution: Make sure the path is correct and contains .wav files

Problem: "Permission denied" errors
Solution: Run with administrator privileges or check folder permissions

Problem: Script runs slowly
Solution: Increase BATCH_SIZE in sort_music.py (default: 50)

Problem: Wrong genre classifications
Solution: Customize GENRE_RULES in sort_music.py

Problem: Python not found
Solution: Install Python from python.org or use full path to python.exe


📝 REQUIREMENTS
---------------
- Python 3.6 or higher
- Standard library only (no external packages needed)
- Windows, macOS, or Linux


💡 TIPS & BEST PRACTICES
------------------------
1. Test on a small folder first before processing large collections
2. Backup important files before first run
3. Review the classification summary before proceeding
4. Customize genre rules to match your music collection
5. Use the favorites feature (++!) for quick access to best tracks
6. Check the Uncategorized folder for misclassified files


📧 SUPPORT
----------
For issues or questions:
1. Check this README file
2. Review the classification rules in sort_music.py
3. Test with a small sample folder
4. Check Python version (python --version)


================================================================================
                              VERSION 1.0
                         Created: November 2025
================================================================================
