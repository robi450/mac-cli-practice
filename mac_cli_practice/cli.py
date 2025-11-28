import argparse
from termcolor import colored

from .core import (
    generate_summary,
    list_summaries,
    configure_defaults,
    load_config,
)

def cmd_generate(name: str | None, topic: str | None):
    config = load_config()
    final_name = name or config.get("default_name") or "Example User"
    final_topic = topic or config.get("default_topic") or "General"

    path = generate_summary(final_name, final_topic)
    print(colored("✔ Summary created:", "green"))
    print(colored(f"   {path.resolve()}", "cyan"))

def cmd_list():
    files = list_summaries()
    if not files:
        print(colored("No summaries found.", "yellow"))
        return
    print(colored("📄 Existing Summary Files:", "blue"))
    for f in files:
        print(" -", f.name)

def cmd_config(name: str | None, topic: str | None):
    if not name and not topic:
        print(colored("Nothing to configure. Use --name and/or --topic.", "yellow"))
        return
    data = configure_defaults(name, topic)
    print(colored("✔ Configuration saved!", "green"))
    import json
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

    if args.command == "generate":
        cmd_generate(args.name, args.topic)
    elif args.command == "list":
        cmd_list()
    elif args.command == "config":
        cmd_config(args.name, args.topic)
    else:
        parser.print_help()

if __name__ == "__main__":
    run()
