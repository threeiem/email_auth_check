import re
from .base_checker import RecordChecker
from output import info, warn, error

class SPFChecker(RecordChecker):
    """
    Checker for SPF (Sender Policy Framework) records.
    """
    record_type = "SPF"

    def check(self):
        """
        Check the SPF record for the domain.
        """
        answers = self.resolve_txt_record(self.domain)
        if not answers:
            error("SPF record not found (allows email spoofing)")
            return

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=spf1'):
                    spf_record = txt_string.decode('utf-8')
                    info(f"{spf_record}", bold_prefix="SPF Record:")
                    self.analyze_spf(spf_record)
                    return

        error("No SPF record found. This may allow email spoofing.")

    def analyze_spf(self, spf_record):
        """
        Analyze the SPF record for potential issues.

        Args:
        spf_record (str): The SPF record to analyze.
        """
        rules = [
            (lambda r: 'ip4:0.0.0.0/0' in r or 'ip6:::0/0' in r, "SPF record allows all IP addresses (extremely permissive)", error),
            (lambda r: ' +all' in r, "'+all', SPF record allows all senders (extremely permissive)", error),
            (lambda r: ' ?all' in r, "'?all', SPF record is neutral (no provide protection)", warn),
            (lambda r: ' ~all' not in r and ' -all' not in r, "SPF record is missing closing '~all' or '-all' (allows unauthorized senders)", warn),
            (lambda r: len(re.findall(r'\s([+-?~]?(?:ip4|ip6|a|mx|ptr|exists|include)(?::[^\s]+)?)', r)) > 10, "SPF record has over 10 mechanisms (lookups limited)", warn),
            (lambda r: 'ptr' in r, "SPF record uses 'ptr' mechanism (inefficient/not recommended)", warn),
            (lambda r: '_spf.smart.ondmarc.com' in r, "SPF record references '_spf.smart.ondmarc.com' (third-party SPF management detected)", warn),
            (lambda r: re.search(r'include:[^.\s]+\.[^.\s]+\.[^.\s]+\._spf\.', r), "SPF record has an unusual 'include' for multiple subdomains (unexpected/resolution issues)", warn)
        ]

        for rule, message, level in rules:
            if rule(spf_record):
                level(message)

