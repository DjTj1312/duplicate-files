# dupFinder — Quick Workflow Guide

This is a practical step-by-step guide for common use cases.
For full flag documentation see `README.md`.

---

## The safe workflow (recommended)

Always follow this order when working with a real folder.

### Step 1 — Scan and save a report, no action taken

```
python .\dupfinder.py D:\YourFolder --output D:\YourFolder\duplicates_report.csv
```

Open `duplicates_report.csv`. Review the results.
The `status` column tells you which file is kept (`keep`) and which would be
removed (`delete`). Files in the same group share the same `group_hash`.
The last row shows the total space you would free.

### Step 2 — Clean up the report manually (optional)

Open the CSV in Excel or a text editor.
Delete any rows you are unsure about or want to keep.
Save the file.

### Step 3 — Relocate using the saved report

```
python .\dupfinder.py D:\YourFolder --relocate --load-report D:\YourFolder\duplicates_report.csv
```

Files flagged as `delete` in the report are moved to `D:\YourFolder\duplicates`.
Rows you deleted from the CSV are ignored entirely.

### Step 4 — Review the staging folder

Open `D:\YourFolder\duplicates` and check the moved files look right.
When you are satisfied, delete the folder manually.

---

## Excluding folders

If you have folders you organize into manually (selections, exports, etc.),
exclude them by keyword. The keyword matches any folder whose name contains it.

```
python .\dupfinder.py D:\YourFolder --output D:\YourFolder\duplicates_report.csv --exclude auswahl selection export
```

`--exclude auswahl` also catches `Auswahl`, `auswahl2026`, and so on.
Matching is case-insensitive.

---

## Filtering by file type

```
python .\dupfinder.py D:\YourFolder --type images --output D:\YourFolder\duplicates_report.csv
python .\dupfinder.py D:\YourFolder --type music  --output D:\YourFolder\duplicates_report.csv
python .\dupfinder.py D:\YourFolder --type video  --output D:\YourFolder\duplicates_report.csv
```

Add custom extensions on top:

```
python .\dupfinder.py D:\YourFolder --type images --ext .c2c .arw --output D:\YourFolder\duplicates_report.csv
```

---


## Scripted deletion (no prompts)

Only do this after you have reviewed a report first.

```
python .\dupfinder.py D:\YourFolder --delete --yes --load-report D:\YourFolder\duplicates_report.csv
```

This deletes every file marked `delete` in the report without asking for
confirmation. A delete log is written to the `logs` folder automatically.

---

## Where things go

| Output | Default location |
|---|---|
| Duplicates report | `output\duplicates_report.csv` (project root) |
| Skipped files report | `output\duplicates_report.csv` (project root) |
| Staging folder | `<scanned directory>\duplicates` |
| Run logs | `logs\dupfinder_<timestamp>.log` (project root) |
| Delete logs | `logs\delete_<timestamp>.log` (project root) |
| Relocate logs | `logs\relocate_<timestamp>.log` (project root) |