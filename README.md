```
Target Directory
       │
       ▼
1. Validate Target Directory (is path valid? is empty folder?)
       │
       ▼
2. Get all items (only process items where .is_file() == True)
       │
       ▼
3. Extract extension (file.suffix.lower())
       │
       ├─ Found in Dictionary Category ──> Set category subfolder name
       └─ Unknown / No extension ──> Put it in the "Others" subfolder
       │
       ▼
4. prepare destination path (target_folder / category / file.name)
       │
       ▼
5. check for name conflicts (Collision Check)
       │
       ├─ Not yet available ──> use real name
       └─ Already available ──> Increment counter: {stem}_{counter}{suffix} until unique
       │
       ▼
6. Dry-Run Check?
       │
       ├─ True  ──> record the transfer simulation to the console/log (STOP here)
       └─ False ──> execute shutil.move() in a try-except block
                         │
                         ├─ Success ──> Log Info (Success)
                         └─ Fail (PermissionError dsb) ──> Log Error & move to the next file
```
