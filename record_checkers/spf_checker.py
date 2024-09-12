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
            error("No SPF record found. This may allow email spoofing.")
            return

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=spf1'):
                    spf_record = txt_string.decode('utf-8')
                    info(f"SPF record found: {spf_record}")
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
            (lambda r: ' +all' in r, "SPF record uses '+all', which allows all senders and is extremely permissive.", error),
            (lambda r: ' ?all' in r, "SPF record uses '?all', which is neutral and doesn't provide protection.", warn),
            (lambda r: ' ~all' not in r and ' -all' not in r, "SPF record doesn't end with '~all' or '-all', which may allow unauthorized senders.", warn),
            (lambda r: 'ip4:0.0.0.0/0' in r or 'ip6:::0/0' in r, "SPF record allows all IP addresses, which is extremely permissive.", error),
            (lambda r: len(re.findall(r'\s([+-?~]?(?:ip4|ip6|a|mx|ptr|exists|include|all)(?::[^\s]+)?)', r)) > 10, "SPF record has more than 10 mechanisms, which may cause lookup limits.", warn),
            (lambda r: 'ptr' in r, "SPF record uses 'ptr' mechanism, which is inefficient and not recommended.", warn)
        ]

        for rule, message, level in rules:
            if rule(spf_record):
                level(message)

