import argparse
from datetime import datetime
from pathlib import Path
import json
import logging
from termcolor import colored

# Paths
OUTPUT_DIR = Path("outputs")
CONFIG_FILE = Path("config.json")

# Logging setup
logging.basicConfig(
    filename="cli.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_summary(name: str, topic: str):
    """Generate a simple summary file."""
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

    print(colored("✔ Summary created:", "green"))
    print(colored(f"   {filename.resolve()}", "cyan"))

def list_summaries():
    """List all summary files in outputs/."""
    if not OUTPUT_DIR.exists():
        print(colored("No summaries found.", "yellow"))
        return

    print(colored("📄 Existing Summary Files:", "blue"))
    for file in sorted(OUTPUT_DIR.iterdir()):
        if file.is_file():
            print(" -", file.name)

def configure_defaults(name: str | None, topic: str | None):
    """Save default name/topic to config.json."""
    data = load_config()
    if name:
        data["default_name"] = name
    if topic:
        data["default_topic"] = topic
    save_config(data)
    print(colored("✔ Configuration saved!", "green"))
    print(json.dumps(data, indent=4))

def run():
    parser = argparse.ArgumentParser(description="Multi-command CLI for macOS practice.")
    subparsers = parser.add_subparsers(dest="command")

    # generate
    gen_cmd = subparsers.add_parser("generate", help="Generate a new summary file.")
    gen_cmd.add_argument("--name", "-n", help="Name or label (e.g., 'Example User')")
    gen_cmd.add_argument("--topic", "-t", help="Topic (e.g., 'Testing the CLI')")

    # list
    subparsers.add_parser("list", help="List all summary files.")

    # config
    config_cmd = subparsers.add_parser("config", help="Save default settings.")
    config_cmd.add_argument("--name", "-n", help="Default name")
    config_cmd.add_argument("--topic", "-t", help="Default topic")

    args = parser.parse_args()
    config = load_config()

    if args.command == "generate":
        name = args.name or config.get("default_name") or "Example User"
        topic = args.topic or config.get("default_topic") or "General"
        generate_summary(name, topic)

    elif args.command == "list":
        list_summaries()

    elif args.command == "config":
        if not args.name and not args.topic:
            print(colored("Nothing to configure. Use --name and/or --topic.", "yellow"))
            return
        configure_defaults(args.name, args.topic)

    else:
        parser.print_help()

if __name__ == "__main__":
    run()
