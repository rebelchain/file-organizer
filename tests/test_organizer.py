import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from organizer import get_category, resolve_collision, scan_directory, move_file, setup_logger, organize_directory


def test_category_mapping():
    print("--- TEST 1: Category Mapping ---")
    samples = {
        "laporan.pdf": "Documents",
        "foto.JPG": "Images",
        "arsip.tar.gz": "Archives",  
        "script": "Others",  
    }

    for filename, expected in samples.items():
        ext = Path(filename).suffix
        category = get_category(ext)
        assert category == expected, f"Fail: {filename} shoud be {expected}, but got {category}"
        print(f"PASS: {filename:<15} -> {category}")





def test_collision_resolution():
    print("\n--- TEST 2: Collision Resolution ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        dest_folder = Path(temp_dir) / "Documents"
        dest_folder.mkdir(parents=True, exist_ok=True)


        path_1 = resolve_collision(dest_folder, "data.csv")
        assert path_1.name == "data.csv", "Failed in first file"
        path_1.touch()
        print(f"PASS: First file OK -> {path_1.name}")

       
        path_2 = resolve_collision(dest_folder, "data.csv")
        assert path_2.name == "data_1.csv", "Duplicate resolution failed (1st attempt)"
        path_2.touch()
        print(f"PASS: First collision resolved -> {path_2.name}")

       
        path_3 = resolve_collision(dest_folder, "data.csv")
        assert path_3.name == "data_2.csv", "Duplicate resolution failed (2st attempt)"
        print(f"PASS: second collision resolved -> {path_3.name}")


def test_scanner_traversal():
    print("\n--- TEST 3: Scanner Directory Traversal ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)

   
        (test_dir / "tugas.pdf").touch()
        (test_dir / "foto.png").touch()

        (test_dir / ".env").touch()
        (test_dir / "FolderSudahRapi").mkdir()

      
        scanned_files = scan_directory(test_dir)
        scanned_names = [f.name for f in scanned_files]

        assert "tugas.pdf" in scanned_names, "tugas.pdf is not detected"
        assert "foto.png" in scanned_names, "foto.png is not detected"
        assert ".env" not in scanned_names, "hidden file .env leaked to the scanner"
        assert "FolderSudahRapi" not in scanned_names, "Subfolders are included"
        assert len(scanned_files) == 2, f"Total file is wrong, got: {len(scanned_files)}"

        print(f"PASS: Scanner filters correctly -> {scanned_names}")




def test_move_file_operations():
    print("\n--- TEST 4: Move File & Dry-Run Mode ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        source_file = base_dir / "draft_desain.png"
        source_file.touch()

        category_folder = base_dir / "Images"
        target_path = resolve_collision(category_folder, source_file.name)


        result_dry = move_file(source_file, target_path, dry_run=True)
        assert source_file.exists(), "Source file missing during a dry-run!"
        assert (
            not target_path.exists()
        ), "target file was actually created in dry-run mode!"
        assert (
            not category_folder.exists()
        ), "Category folders should not be created during dry-run!"
        print("PASS: Dry-Run mode successfully kept the disk intact")

        result_real = move_file(source_file, target_path, dry_run=False)
        assert (
            not source_file.exists()
        ), "The source file still exists after being moved!"
        assert target_path.exists(), "target file is not found on disk"
        assert result_real == target_path, "Return path does not match!"
        print("PASS: actual move successfully transferred files to Images folder.")






def test_logging_and_orchestrator():
    print("\n --- Test 5: Orchestrator & Logging System ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir)
        log_path = base_dir / "test_run.log"

        (base_dir / "catatan.txt").touch()
        (base_dir / gambar.jpg).touch()

        summary = organize_directory(base_dir, dry_run=False, log_file=log_path)

        assert summary["total"] == 2, "number of scanned files doesn't match"
        assert summary["moved"] == 2, "some files that failed to be moved"
        assert log_path.exists(), "Log file is not created on the disk"


        log_content =log_path.read_text(encoding="utf-8")
        assert "[SUCCESS]" in log_content, "Success log is not recorded in file"
        print(f"PASS: Log successfully written to {log_path.name}")
        print(f"PASS: Entire orchestration flow was successful")



if __name__ == "__main__":
    test_category_mapping()
    test_collision_resolution()
    test_scanner_traversal()
    test_move_file_operations()
    print("\n All unit tests ran successfully without error.")