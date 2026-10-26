import shutil
from pathlib import Path
import tempfile

CATEGORIES = {
  "Images": [".jpg", ".jpeg", ".png", ".gif"],
  "Documents": [".pdf", ".docx", ".txt", ".txt", ".xlsx"],
  "Archives": [".zip", ".rar", ".tar", ".gz"] 
}

def get_category(extension: str) -> str:
  if not extension:
    return "Others"

  lower_extension = extension.lower()

  for category, ext_list in CATEGORIES.items():
     if lower_extension in ext_list:
       return category

  return "Others"




def scan_directory(target_path: Path) -> list[Path]:
  """scan target directory and return list of files that are valid to be moved. 
  
    Ignoring subdirectories and hidden files.
  """

  if not target_path.exists():
    raise FileNotFoundError(f"'{target_path} directory is not found in the system'")

  if not target_path.is_dir():
    raise NotADirectoryError(f"'{target_path}' path is not directory or folder")

  valid_files: list[Path] = []

  for item in target_path.iterdir():
    if item.is_file() and not item.name.startswith("."):
      valid_files.append(item)

  return valid_files





def resolve_collision(destination_folder: Path, file_name: str) -> Path:
  """Prevents files from being overwritten by appending _1, _2, etc., if a file with the same name already exists."""

  target_path = destination_folder / file_name

  if not target_path.exists():
    return target_path

  file_path = Path(file_name)
  stem = file_path.stem
  suffix = file_path.suffix

  counter = 1
  while True:
    new_name = f"{stem}_{counter}{suffix}"
    new_target_path = destination_folder / new_name

    if not new_target_path.exists():
      return new_target_path

    counter += 1






def move_file(source_path: Path, destination_path: Path, dry_run: bool = False) -> Path:
  """
  Move file to the destination path securely

  if dry_run == True, only print simulation without modifying the disk.
  Returns the destination_path used.
  """

  if dry_run:
    print(f"DRY RUN: Relocation plan: {source_path} -> {destination_path}")
    return destination_path

  destination_path.parent.mkdir(parents=True, exist_ok=True)

  shutil.move(str(source_path), str(destination_path))
  print(f"Moved: {source_path.name} -> {destination_path}")

  return destination_path