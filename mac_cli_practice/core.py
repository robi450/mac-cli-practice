from datetime import datetime
from pathlib import Path
import json
import logging

OUTPUT_DIR = Path("outputs")
CONFIG_FILE = Path("config.json")

# Logging setup (shared by CLI and API)
logging.basicConfig(
    filename="cli.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data: dict) -> dict:
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return data

def generate_summary(name: str, topic: str) -> Path:
    """Generate a simple summary file and return its path."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = name.strip().replace(" ", "_")
    filename = OUTPUT_DIR / f"summary_{safe_name}_{timestamp}.txt"

    content = f"""Simple Summary Generator
==========================

Name: {name}
Topic: {topic}
Created: {datetime.now().isoformat(timespec='seconds')}
"""

    filename.write_text(content, encoding="utf-8")
    logging.info(f"Generated summary file: {filename}")
    return filename

def list_summaries() -> list[Path]:
    """Return a list of existing summary files."""
    if not OUTPUT_DIR.exists():
        return []
    return sorted([p for p in OUTPUT_DIR.iterdir() if p.is_file()])

def configure_defaults(name: str | None, topic: str | None) -> dict:
    """Save default name/topic into config.json and return config."""
    data = load_config()
    if name:
        data["default_name"] = name
    if topic:
        data["default_topic"] = topic
    return save_config(data)
