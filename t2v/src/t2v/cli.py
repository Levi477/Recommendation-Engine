"""Command-line interface for T2V package."""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from .core import T2VCore
from .utils import T2VUtils


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="T2V - Private Repository CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="T2V 0.1.0"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Initialize command
    init_parser = subparsers.add_parser("init", help="Initialize T2V system")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Force initialization even if already initialized"
    )
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show T2V system status")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process data through T2V")
    process_parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input data to process"
    )
    process_parser.add_argument(
        "--output",
        type=str,
        help="Output file path"
    )
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate environment")
    
    args = parser.parse_args()
    
    # Set up logging
    T2VUtils.setup_logging(level=args.log_level)
    
    # Load configuration if provided
    config = {}
    if args.config:
        try:
            config = T2VUtils.load_config(args.config)
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Execute command
    try:
        if args.command == "init":
            handle_init(config, args.force)
        elif args.command == "status":
            handle_status(config)
        elif args.command == "process":
            handle_process(config, args.input, args.output)
        elif args.command == "validate":
            handle_validate()
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_init(config: dict, force: bool) -> None:
    """Handle initialization command."""
    core = T2VCore(config)
    if core.initialize() or force:
        print("T2V system initialized successfully")
    else:
        print("Failed to initialize T2V system", file=sys.stderr)
        sys.exit(1)


def handle_status(config: dict) -> None:
    """Handle status command."""
    core = T2VCore(config)
    status = core.get_status()
    print(json.dumps(status, indent=2))


def handle_process(config: dict, input_data: str, output_file: Optional[str]) -> None:
    """Handle process command."""
    core = T2VCore(config)
    
    if not core.initialize():
        print("Failed to initialize T2V system", file=sys.stderr)
        sys.exit(1)
    
    # For simplicity, treat input as string data
    result = core.process(input_data)
    
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(str(result))
        print(f"Result saved to: {output_file}")
    else:
        print(f"Processing result: {result}")


def handle_validate() -> None:
    """Handle validate command."""
    results = T2VUtils.validate_environment()
    
    print("Environment validation results:")
    print("=" * 40)
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check:<25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("All validation checks passed!")
    else:
        print("Some validation checks failed. Please address the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()