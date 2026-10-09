import sys
import os
import shutil
import json
import argparse
from pathlib import Path

def prompt_yes_no(question: str, default_choice: bool = None) -> bool:
    """
    Helper function to prompt user with a yes/no question.
    If default_choice is set (from --assume-yes or --assume-no), it skips prompting.
    """
    if default_choice is True:
        print(f"{question} [y/N]: Auto-answered 'yes' (--assume-yes)")
        return True
    elif default_choice is False:
        print(f"{question} [y/N]: Auto-answered 'no' (--assume-no)")
        return False

    while True:
        response = input(f"{question} [y/N]: ").strip().lower()
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no', '']:
            return False
        print("Please answer with 'y' or 'n'.")

def validate_files(source_path: Path, target_path: Path):
    """Ensure files exist and check preliminary permissions."""
    if not source_path.exists():
        sys.exit(f"Error: Source file '{source_path}' does not exist.")
    if not os.access(source_path, os.R_OK):
        sys.exit(f"Error: Source file '{source_path}' is not readable.")

    if not target_path.exists():
        sys.exit(f"Error: Target file '{target_path}' does not exist.")
    if not (os.access(target_path, os.R_OK) and os.access(target_path, os.W_OK)):
        sys.exit(f"Error: Target file '{target_path}' must have both read and write permissions.")

def create_backup(target_path: Path, default_choice: bool = None):
    """Handles the creation of the .sync-backup file with user prompts."""
    backup_path = target_path.with_name(f"{target_path.name}.sync-backup")

    # Prompt if backup already exists
    if backup_path.exists():
        print(f"Warning: Backup file '{backup_path.name}' already exists.")
        if not prompt_yes_no("Do you want to overwrite the existing backup?", default_choice):
            print("Operation canceled by user.")
            sys.exit(0)

    # Attempt to copy target file to backup destination
    try:
        shutil.copy2(target_path, backup_path)
        print(f"Backup created successfully: '{backup_path.name}'")
    except (PermissionError, OSError) as e:
        print(f"Warning: Could not create backup file due to permission/system error ({e}).")
        if not prompt_yes_no("Do you want to continue without creating a backup?", default_choice):
            print("Terminating script.")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Sync 'ignore' object from a source JSON file to a target JSON file."
    )
    parser.add_argument("source", type=Path, help="Path to source JSON file (read-only)")
    parser.add_argument("target", type=Path, help="Path to target JSON file (read-write)")

    # Group flags so --assume-yes and --assume-no cannot be used simultaneously
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-y", "--assume-yes",
        action="store_true",
        help="Automatically answer 'yes' to all prompts"
    )
    mode_group.add_argument(
        "-n", "--assume-no",
        action="store_true",
        help="Automatically answer 'no' to all prompts"
    )

    args = parser.parse_args()

    # Determine default choice state (True for yes, False for no, None for interactive)
    default_choice = None
    if args.assume_yes:
        default_choice = True
    elif args.assume_no:
        default_choice = False

    source_path = args.source.resolve()
    target_path = args.target.resolve()

    # 1. Validate file existence and permissions
    validate_files(source_path, target_path)

    # 2. Read source JSON and verify 'ignore' key
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error parsing source JSON file: {e}")
    except Exception as e:
        sys.exit(f"Error reading source file: {e}")

    if 'ignore' not in source_data:
        sys.exit("Error: Source JSON does not contain an 'ignore' object/key.")

    # 3. Read target JSON
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            target_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error parsing target JSON file: {e}")
    except Exception as e:
        sys.exit(f"Error reading target file: {e}")

    # 4. Handle backup routine
    create_backup(target_path, default_choice)

    # 5. Update target object and write back
    target_data['ignore'] = source_data['ignore']

    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, indent=4)
        print(f"Successfully updated 'ignore' key in '{target_path.name}'.")
    except Exception as e:
        sys.exit(f"Error writing updated data to target file: {e}")

if __name__ == '__main__':
    main()
