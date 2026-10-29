import shutil
import logging
from pathlib import Path
import tempfile

CATEGORIES = {
  "Images": [".jpg", ".jpeg", ".png", ".gif"],
  "Documents": [".pdf", ".docx", ".txt", ".txt", ".xlsx"],
  "Archives": [".zip", ".rar", ".tar", ".gz"] 
}



def setup_logger(log_file: Path = Path("organizer.log")) -> logging.Logger:
  """Configuring logger to log to file and display to the console"""

  logger = logging.getLogger("FileOrganizer")
  logger.setLevel(logging.INFO)

  if logger.handlers:
    return logger

  formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

  file_handler = logging.FileHandler(log_file, encoding="utf-8")
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  logger.addHandler(console_handler)

  return logger








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






def move_file(source_path: Path, destination_path: Path, dry_run: bool = False, logger: logging.Logger | None = None) -> bool:
  """

  Move file to the destination path securely with defensive exception handling

  return True if success or simulation success, False if fail happen
  """

  log = logger or logging.getLogger("FIleOrganizer")
  if dry_run:
    log.info(f"DRY RUN: Relocation plan: {source_path} -> {destination_path}")
    return True

  try:
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    # str(source_path): Although `shutil` in modern versions of Python supports `Path` objects, explicitly converting them to `str` ensures compatibility, allowing the script to run across different OS environments without issues related to type references.
    shutil.move(str(source_path), str(destination_path))
    
    log.info(f"Moved: {source_path.name} -> {destination_path}")
    return True

  except PermissionError:
    log.error(f"Permission Denied -> Failed to move {source_path.name}: " f"file is either locked another application or access permission has been denied")
    return False

  except OSError as e:
    log.error(f"OS ERROR: failed to move {source_path.name}: {e}")
    return False

  except Exception as e:
    log.error(f"Unexpected Error: unexpected error in {source_path.name}: {e} ")
    return False












def organize_directory(target_dir: Path, dry_run: bool = False, log_file: Path = Path("organizer.log")) -> dict[str, int]:
  """
  execute the entire folder-organizing workflow from scanning to move file

  returns a summary of the transfe statistics
  """

  logger = setup_logger(log_file)
  logger.info(f"starting the directory organization process: {target_dir} (Dry-Run Mode: {dry_run})")

  stats = {"total": 0, "moved": 0, "failed": 0, "skipped": 0}

  files = scan_directory(target_dir)
  stats["total"] = len(files)

  if not files:
    logger.warning(f"{target_dir} Directory is empty or contains no valid file")
    return stats


  for file_path in files:
    category = get_category(file_path.suffix)
    dest_folder = target_dir / category
    safe_targer = resolve_collision(dest_folder, file_path.name)

    is_success = move_file(file_path, safe_targer, dry_run=dry_run, logger=logger)

    if is_success:
      stats["moved"] += 1
    else:
      stats["failed"] += 1

  logger.info(f"Done! Summary: Total={stats['total']}, " f"Success={stats['moved']}, Failed={stats['failed']}")

  return stats
