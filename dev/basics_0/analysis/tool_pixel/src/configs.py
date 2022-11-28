from pathlib import Path

ROOT: Path = Path(__name__).parent.parent.parent.resolve()

IMAGES: Path = ROOT / Path("images")
DATA: Path = ROOT / Path("data")
LOGS: Path = ROOT / Path("logs")

DIRS = []
DIRS.append(IMAGES)
DIRS.append(DATA)
DIRS.append(LOGS)
for a_dir in DIRS:
    a_dir.mkdir(exist_ok=True)

if __name__ == "__main__":
    from pprint import pprint
    pprint(DIRS)
