from pathlib import Path
ROOT: Path = Path(__name__).parent.parent.parent.resolve()
IMAGES: Path = ROOT / Path("images")

if __name__ == "__main__":
    print(ROOT)
    print(IMAGES)
