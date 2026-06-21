# duplicate-finder

A command-line tool to find and optionally remove duplicate files,
with support for images, video, and music files.

## Features

- Recursive directory scan
- Content-based duplicate detection via MD5 hashing
- Optional filtering by file type (images, video, music) or custom extensions
- Folder exclusion by keyword, catches partial matches (e.g. `selection` also excludes `selection2026`)
- CSV report export with `keep`/`delete` status per file and estimated space savings
- Separate report of files skipped by the extension filter
- Option to load a previously saved report for deletion or relocation, without re-scanning
- Dry run mode to preview changes before acting
- Safe staging mode (move duplicates to a folder) or permanent deletion
- Full logging of every run, plus a dedicated log of every file deleted or moved
- Interactive prompts when run without flags, fully scriptable with flags

## Safety

Always run with:
```
--dry-run
```
before deleting files.
The tool identifies duplicates using content hashes, not filenames.

## Requirements

Python 3.10+

## Installation

```
git clone <your-repo-url>
cd duplicate-finder
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

### Basic scan, fully interactive

```
python dupFinder.py D:\Photos
```

No flags at all. This walks you through:
1. Whether to run a dry run first to preview what would happen
2. Whether to save a CSV report (default: `output/duplicates_report.csv`, relative to the project folder)
3. What to do with the duplicates: delete, move to a staging folder, or skip

### Filter by file type

```
python dupFinder.py D:\Photos --type images
python dupFinder.py D:\Music --type music
python dupFinder.py D:\Videos --type video
```

Filtering happens before hashing. Files outside the chosen type are never read,
only their filenames are checked against the extension list. This matters on large
drives, since hashing is the slow part.

### Add custom extensions on top of a type

```
python dupFinder.py D:\Photos --type images --ext .c2c .arw
```

### Scan everything, no type filter

```
python dupFinder.py D:\Backup
```

Omit `--type` and every file is hashed regardless of extension.

### Exclude folders by keyword

```
python dupFinder.py D:\Photos --exclude selection
python dupFinder.py D:\Photos --exclude selection backup tmp
```

Any folder whose name contains one of the keywords as a substring is skipped
entirely during the scan. Matching is case-insensitive.

For example, `--exclude selection` skips both:
```
D:\Photos\selection\img.jpg
D:\Photos\selection2026\img.jpg
```

Multiple keywords can be combined. Files inside excluded folders are not hashed,
not reported, and not acted on.

### Save a report without taking any other action

```
python dupFinder.py D:\Photos --output report.csv
```

Scans, saves `report.csv` plus `skipped_files.csv` in the same folder, and exits.
No prompts, no action taken.

The report contains one row per file in each duplicate group, with columns:
`filename`, `size_bytes`, `size_mb`, `path`, `extension`, `group_hash`, `status`.

The `status` column is either `keep` (the file that would be left in place) or
`delete` (files that would be removed or moved). The file marked `keep` in each
group is always the first one alphabetically by full path.

The last row of the report shows the total estimated space that would be freed
by removing the files marked `delete`.

### Preview only, no changes

```
python dupFinder.py D:\Photos --dry-run
```

Shows which file in each duplicate group would be kept and which would be removed,
without touching anything. Combine with `--output` to also save the report.

```
python dupFinder.py D:\Photos --dry-run --output report.csv
```

### Delete duplicates

```
python dupFinder.py D:\Photos --delete
```

Asks whether to use an existing report or scan fresh. If scanning, saves a report
at the default path before acting. Asks for confirmation, then deletes. Writes a
dedicated delete log to the `logs` folder listing every file removed.

```
python dupFinder.py D:\Photos --delete --yes
```

Same, but skips the confirmation prompt. The "use existing report?" question is
always shown regardless of `--yes`.

### Use an existing report to delete or relocate

When `--delete` or `--relocate` is called, the tool first asks:

```
Do you want to load an existing duplicate report instead of re-scanning? (y/n):
```

If you answer yes, you provide the path to a previously saved CSV. The tool reads
only the rows marked `status = delete` and acts on those file paths directly,
skipping the scan and hashing entirely.

This is useful in two ways:

1. You already ran a scan and saved a report. No need to hash everything again.
2. You can open the CSV, manually delete rows you want to keep, save it, and then
   load the edited version. Only the remaining `delete` rows will be acted on.

### Move duplicates to a staging folder instead of deleting

```
python dupFinder.py D:\Photos --relocate
```

Moves duplicates into `D:\Photos\duplicates` (created automatically if missing).

```
python dupFinder.py D:\Photos --relocate D:\Staging\dupes
```

Moves duplicates into a custom folder instead. If the staging folder is inside the
scanned directory, run the tool a second time and the staging folder will be
skipped automatically only if it uses the default name `duplicates`. For a custom
path inside the scanned directory, point `--relocate` outside it to be safe.

Add `--yes` to either of the above to skip the confirmation prompt.

## Defaults

- CSV report: `output/duplicates_report.csv`, relative to the project folder.
  Used whenever a report is saved and no `--output` path was given.
- Skipped files report: always saved next to the duplicates report, named `skipped_files.csv`.
- Staging folder: `<scanned directory>/duplicates`, used when `--relocate` is
  passed without a path. This folder is automatically skipped during future scans.
- Logs: always written to the `logs` folder at the project root, regardless of
  which directory you scan. Every run produces a timestamped normal log mirroring
  console output. Runs that delete or relocate files also produce a dedicated
  `delete_<timestamp>.log` or `relocate_<timestamp>.log` containing only the
  lines for files actually removed or moved.

## All flags

| Flag | Description |
|---|---|
| `directory` | Root directory to scan (required, positional) |
| `--type {images,video,music}` | Filter by file type |
| `--ext .ext1 .ext2 ...` | Add custom extensions, combinable with `--type` |
| `--exclude KEYWORD ...` | Skip folders whose name contains any of the keywords |
| `--output PATH` | Save the duplicates report to this CSV path |
| `--dry-run` | Preview only, no changes made |
| `--relocate [PATH]` | Move duplicates to a staging folder. Defaults to `<directory>/duplicates` if no path given |
| `--delete` | Permanently delete duplicates |
| `--yes`, `-y` | Skip the confirmation prompt for `--delete` or `--relocate` |
| `--verbose` | Enable debug-level logging |