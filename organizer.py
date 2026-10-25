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
     if lower_extension == ext_list:
       return category

  return "Others"


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