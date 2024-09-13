#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent))

from record_checkers import SPFChecker, DKIMChecker, DMARCChecker
from output import setup_logging, info, warn, error

def main():
    """
    Main function to run the email authentication checker.
    Parses command line arguments, sets up logging, and runs the checks.
    """
    parser = argparse.ArgumentParser(description="Check email authentication records (SPF, DKIM, DMARC) for a domain")
    parser.add_argument("domain", help="Domain to check records for")
    parser.add_argument("-s", "--selector", help="DKIM selector (required for DKIM check)", default=None)
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()
    
    setup_logging()
    
    info(f"Checking email authentication records for {args.domain}")
    
    # Check SPF
    spf_checker = SPFChecker(args.domain)
    spf_checker.check()
    
    # Check DKIM
    if args.selector:
        dkim_checker = DKIMChecker(args.domain, args.selector)
        dkim_checker.check()
    else:
        info("No DKIM selector provided (-s/--selector). Skipping DKIM check.")
    
    # Check DMARC
    dmarc_checker = DMARCChecker(args.domain)
    dmarc_checker.check()

if __name__ == "__main__":
    main()
