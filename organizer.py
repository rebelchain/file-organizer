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

if __name__ == "__main__":

  with tempfile.TemporaryDirectory() as temp_dir:
    base_dir = Path(temp_dir)
    print(f"Temporary test directory: {base_dir}\n")

    test_files = [
      "final_document.pdf", # get in "Documents"
      "holiday_photo.PNG", # get in "Images" (case-insensitive test)
      "arsip_lama.zip", # get in "Archives"
      "secret_notes" # get in "Others" (no extension)
    ]

    print("---- Test 1: Determination  of Category & Initial Path -----")
    for filename in test_files:
      file_path = Path(filename)
      category = get_category(file_path.suffix)
      dest_folder = base_dir / category
      dest_folder.mkdir(parents=True, exist_ok=True)

      safe_path = resolve_collision(dest_folder, file_path.name)
      print(f"File: {filename:<18} -> Folder: {category:<10} -> Target: {safe_path.name}")

      print(f"--- Tes 2: Collision Simulation ----")

      docs_folder = base_dir / "Documents"

      file_1 = docs_folder / "laporan.pdf"
      file_1.touch()
      print(f"Create Dummy: {file_1.name} already exist in destination folder.")

      target_aman_1 = resolve_collision(docs_folder, "laporan.pdf")
      print(f"collision resolution 1: {target_aman_1.name}")

      target_aman_1.touch()
      print(f"create dummy: {target_aman_1} file was intentionally created on the disk.")

      target_aman_2 = resolve_collision(docs_folder, "laporan.pdf")
      print(f"collision resolution 3: {target_aman_2.name}")