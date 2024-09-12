#!/usr/bin/env python3

import dns.resolver
import argparse

def check_spf(domain):
    """
    Check the SPF (Sender Policy Framework) record for a given domain.

    Args:
    domain (str): The domain to check.

    Returns:
    str: The SPF record if found, or an error message.
    """
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=spf1'):
                    return txt_string.decode('utf-8')
        return "No SPF record found"
    except dns.resolver.NXDOMAIN:
        return f"Domain {domain} does not exist"
    except dns.resolver.NoAnswer:
        return f"No TXT records found for {domain}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def check_dkim(domain, selector='default'):
    """
    Check the DKIM (DomainKeys Identified Mail) record for a given domain and selector.

    Args:
    domain (str): The domain to check.
    selector (str): The DKIM selector to use (default is 'default').

    Returns:
    str: The DKIM record if found, or an error message.
    """
    try:
        dkim_domain = f"{selector}._domainkey.{domain}"
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=DKIM1'):
                    return txt_string.decode('utf-8')
        return f"No DKIM record found for selector '{selector}'"
    except dns.resolver.NXDOMAIN:
        return f"DKIM record not found for selector '{selector}'"
    except dns.resolver.NoAnswer:
        return f"No TXT records found for DKIM (selector: {selector})"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def check_dmarc(domain):
    """
    Check the DMARC (Domain-based Message Authentication, Reporting, and Conformance) record for a given domain.

    Args:
    domain (str): The domain to check.

    Returns:
    str: The DMARC record if found, or an error message.
    """
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=DMARC1'):
                    return txt_string.decode('utf-8')
        return "No DMARC record found"
    except dns.resolver.NXDOMAIN:
        return "DMARC record not found"
    except dns.resolver.NoAnswer:
        return f"No TXT records found for DMARC"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """
    Main parses command line arguments and runs the email authentication checkers.
    """
    parser = argparse.ArgumentParser(description="Check email authentication records (SPF, DKIM, DMARC) for a domain")
    parser.add_argument("domain", help="Domain to check records for")
    parser.add_argument("-s", "--selector", help="DKIM selector (default: 'default')", default="default")
    args = parser.parse_args()

    print(f"Checking email authentication records for {args.domain}:")
    print("\nSPF Record:")
    print(check_spf(args.domain))

    print("\nDKIM Record:")
    print(check_dkim(args.domain, args.selector))

    print("\nDMARC Record:")
    print(check_dmarc(args.domain))

if __name__ == "__main__":
    main()

