import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from organizer import get_category, resolve_collision, scan_directory


def test_category_mapping():
    print("--- [TEST 1: Category Mapping] ---")
    samples = {
        "laporan.pdf": "Documents",
        "foto.JPG": "Images",
        "arsip.tar.gz": "Archives",  
        "script": "Others",  
    }

    for filename, expected in samples.items():
        ext = Path(filename).suffix
        category = get_category(ext)
        assert category == expected, f"Gagal: {filename} harusnya masuk {expected}, tapi dapat {category}"
        print(f"PASS: {filename:<15} -> {category}")


def test_collision_resolution():
    print("\n--- [TEST 2: Collision Resolution] ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        dest_folder = Path(temp_dir) / "Documents"
        dest_folder.mkdir(parents=True, exist_ok=True)


        path_1 = resolve_collision(dest_folder, "data.csv")
        assert path_1.name == "data.csv", "Gagal pada file pertama"
        path_1.touch()
        print(f"PASS: File pertama aman -> {path_1.name}")

       
        path_2 = resolve_collision(dest_folder, "data.csv")
        assert path_2.name == "data_1.csv", "Gagal resolusi duplikat ke-1"
        path_2.touch()
        print(f"PASS: Tabrakan ke-1 teratasi -> {path_2.name}")

       
        path_3 = resolve_collision(dest_folder, "data.csv")
        assert path_3.name == "data_2.csv", "Gagal resolusi duplikat ke-2"
        print(f"PASS: Tabrakan ke-2 teratasi -> {path_3.name}")


def test_scanner_traversal():
    print("\n--- [TEST 3: Scanner Directory Traversal] ---")
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)

   
        (test_dir / "tugas.pdf").touch()
        (test_dir / "foto.png").touch()

        (test_dir / ".env").touch()
        (test_dir / "FolderSudahRapi").mkdir()

      
        scanned_files = scan_directory(test_dir)
        scanned_names = [f.name for f in scanned_files]

        assert "tugas.pdf" in scanned_names, "tugas.pdf tidak terdeteksi"
        assert "foto.png" in scanned_names, "foto.png tidak terdeteksi"
        assert ".env" not in scanned_names, "File hidden .env bocor ke scanner"
        assert "FolderSudahRapi" not in scanned_names, "Subfolder ikut terbawa"
        assert len(scanned_files) == 2, f"Total file salah, dapat: {len(scanned_files)}"

        print(f"PASS: Scanner menyaring dengan benar -> {scanned_names}")


if __name__ == "__main__":
    test_category_mapping()
    test_collision_resolution()
    test_scanner_traversal()
    print("\nSemua unit test berhasil dijalankan tanpa error.")