import argparse
import sys
from pathlib import Path

from organizer import organize_directory


def main():

  parser = argparse.ArgumentParser(
    description="Automated file organizer: merapikan file ke dalam subfolder kategori secara otomatis",
    epilog="Example execution: python main.py C:/Users/Downloads --dry-run"
  )

  parser.add_argument(
    "path",
    type=str,
    help="Hanya jalankan simulasi pencatatan (tidak akan memindahkan file sungguhan)"
  )

  args = parser.parse_args()

  target_path = Path(args.path)

  print("=" * 60)
  print(f"Automated File Organizer")
  print(f"Target : {target_path.resolve()}")
  print(f"Mode   : {'Dry-Run Simulation' if args.dry_run else 'Live: Actual Move'}")
  print("=" * 60)

  try:

    summary = organize_directory(target_path, dry_run=args.dry_run)

    print("\n" "=" * 60)
    print("Process Complete")
    print(f"Total file found     : {summary['total']}")
    print(f"Success to be moved  : {summary['moved']}")
    print(f"Failed or locked     : {summary['failed']}")
    print("=" * 60)
    print("Log detail was saved in organizer.log")

  except FileNotFoundError as e:
    print(f"\n Failed: {e}")
    sys.exit(1)

  except NotADirectoryError as e:

    print(f"\n Failed: {e}")
    sys.exit(1)

  except KeyboardInterrupt:

    print("\n\n Cancelled: process was disturbed by user (CTRL+C)")
    sys.exit(1)




if __name__ == "__main__":
  main()

