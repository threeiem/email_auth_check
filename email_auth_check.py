#!/usr/bin/env python3
import argparse
from record_checkers import SPFChecker, DKIMChecker, DMARCChecker

def main():
    parser = argparse.ArgumentParser(description="Check email authentication records (SPF, DKIM, DMARC) for a domain")
    parser.add_argument("domain", help="Domain to check records")
    parser.add_argument("-s", "--selector", help="DKIM selector (default: 'default')", default="default")
    args = parser.parse_args()

    print(f"Checking email authentication records for {args.domain}:")

    checkers = [
        SPFChecker(args.domain),
        DKIMChecker(args.domain, args.selector),
        DMARCChecker(args.domain)
    ]

    for checker in checkers:
        print(f"\n{checker.record_type} Record:")
        record, warnings = checker.check()
        print(record)
        for warning in warnings:
            print(warning)

if __name__ == "__main__":
    main()
