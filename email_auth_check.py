#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent))

from record_checkers import SPFChecker, DKIMChecker, DMARCChecker
from output import setup_logging

def main():
    """
    Main function to run the email authentication checker.
    Parses command line arguments, sets up logging, and runs the checks.
    """
    parser = argparse.ArgumentParser(description="Check email authentication records (SPF, DKIM, DMARC) for a domain")
    parser.add_argument("domain", help="Domain to check records")
    parser.add_argument("-s", "--selector", help="DKIM selector (default: 'default')", default="default")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    setup_logging(use_color=not args.no_color)

    print(f"Checking email authentication records for {args.domain}:")

    checkers = [
        SPFChecker(args.domain),
        DKIMChecker(args.domain, args.selector),
        DMARCChecker(args.domain)
    ]

    for checker in checkers:
        print(f"\n{checker.record_type} Record:")
        checker.check()

if __name__ == "__main__":
    main()
