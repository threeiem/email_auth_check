import dns.resolver
import re
from abc import ABC, abstractmethod

class RecordChecker(ABC):
    def __init__(self, domain):
        self.domain = domain

    @abstractmethod
    def check(self):
        pass

    def resolve_txt_record(self, domain):
        try:
            return dns.resolver.resolve(domain, 'TXT')
        except dns.resolver.NXDOMAIN:
            return None
        except dns.resolver.NoAnswer:
            return None
        except Exception as e:
            raise e

class SPFChecker(RecordChecker):
    record_type = "SPF"

    def check(self):
        answers = self.resolve_txt_record(self.domain)
        if not answers:
            return "No SPF record found", ["WARNING: No SPF record found. This may allow email spoofing."]

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=spf1'):
                    spf_record = txt_string.decode('utf-8')
                    return spf_record, self.analyze_spf(spf_record)

        return "No SPF record found", ["WARNING: No SPF record found. This may allow email spoofing."]

    def analyze_spf(self, spf_record):
        warnings = []
        rules = [
            (lambda r: ' +all' in r, "WARNING: SPF record uses '+all', which allows all senders and is extremely permissive."),
            (lambda r: ' ?all' in r, "CAUTION: SPF record uses '?all', which is neutral and doesn't provide protection."),
            (lambda r: ' ~all' not in r and ' -all' not in r, "CAUTION: SPF record doesn't end with '~all' or '-all', which may allow unauthorized senders."),
            (lambda r: 'ip4:0.0.0.0/0' in r or 'ip6:::0/0' in r, "WARNING: SPF record allows all IP addresses, which is extremely permissive."),
            (lambda r: len(re.findall(r'\s([+-?~]?(?:ip4|ip6|a|mx|ptr|exists|include|all)(?::[^\s]+)?)', r)) > 10, "CAUTION: SPF record has more than 10 mechanisms, which may cause lookup limits."),
            (lambda r: 'ptr' in r, "CAUTION: SPF record uses 'ptr' mechanism, which is inefficient and not recommended.")
        ]

        for rule, warning in rules:
            if rule(spf_record):
                warnings.append(warning)

        return warnings

class DKIMChecker(RecordChecker):
    record_type = "DKIM"

    def __init__(self, domain, selector):
        super().__init__(domain)
        self.selector = selector

    def check(self):
        dkim_domain = f"{self.selector}._domainkey.{self.domain}"
        answers = self.resolve_txt_record(dkim_domain)
        if not answers:
            return f"No DKIM record found for selector '{self.selector}'", ["WARNING: No DKIM record found. This may allow email spoofing."]

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=DKIM1'):
                    dkim_record = txt_string.decode('utf-8')
                    return dkim_record, self.analyze_dkim(dkim_record)

        return f"No DKIM record found for selector '{self.selector}'", ["WARNING: No DKIM record found. This may allow email spoofing."]

    def analyze_dkim(self, dkim_record):
        # Implement DKIM-specific checks here
        return []

class DMARCChecker(RecordChecker):
    record_type = "DMARC"

    def check(self):
        dmarc_domain = f"_dmarc.{self.domain}"
        answers = self.resolve_txt_record(dmarc_domain)
        if not answers:
            return "No DMARC record found", ["WARNING: No DMARC record found. This may allow email spoofing."]

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=DMARC1'):
                    dmarc_record = txt_string.decode('utf-8')
                    return dmarc_record, self.analyze_dmarc(dmarc_record)

        return "No DMARC record found", ["WARNING: No DMARC record found. This may allow email spoofing."]

    def analyze_dmarc(self, dmarc_record):
        # Implement DMARC-specific checks here
        return []

