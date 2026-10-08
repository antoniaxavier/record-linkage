"""Download the Amazon-GoogleProducts benchmark into data/raw/."""

import urllib.request
import zipfile
from pathlib import Path

URL = "https://dbs.uni-leipzig.de/files/datasets/Amazon-GoogleProducts.zip"
RAW_DIR = Path("data/raw")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = RAW_DIR / "Amazon-GoogleProducts.zip"
    if not zip_path.exists():  # skip download if already there
        print(f"Downloading {URL}")
        urllib.request.urlretrieve(URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(RAW_DIR)
    for f in sorted(RAW_DIR.iterdir()):
        print(f.name)


if __name__ == "__main__":
    main()
