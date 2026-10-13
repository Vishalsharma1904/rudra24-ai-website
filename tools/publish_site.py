"""Create a hosting directory containing only public website files.

Keep development tools, design notes and agent skills outside the web root.
No network, dependencies or application credentials are needed.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"


def publish_site():
    OUTPUT.mkdir(exist_ok=True)
    for item in OUTPUT.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    for path in ROOT.iterdir():
        if path.is_file() and (path.suffix in {".html", ".css", ".js"} or path.name in {"robots.txt", "sitemap.xml", "_redirects", "_headers"}):
            shutil.copy2(path, OUTPUT / path.name)
    shutil.copytree(ROOT / "assets", OUTPUT / "assets")
    print(f"Public website prepared in {OUTPUT}")


if __name__ == "__main__":
    publish_site()
