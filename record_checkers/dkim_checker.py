"""
DKIM Checker: Class to check the DKIM record for a domain.
"""
from output import info, warn, error
from .base_checker import RecordChecker

class DKIMChecker(RecordChecker):
    """
    Class to check the DKIM record for a domain.
    """
    record_type = "DKIM"

    def __init__(self, domain, selector):
        super().__init__(domain)
        self.selector = selector

    def check(self):
        """
        Check the DKIM record for the domain.
        """
        dkim_domain = f"{self.selector}._domainkey.{self.domain}"
        answers = self.resolve_txt_record(dkim_domain)
        if not answers:
            error(f"No DKIM record found for selector '{self.selector}'. This may allow email spoofing.")
            return

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b"v=DKIM1"):
                    dkim_record = txt_string.decode("utf-8")
                    info(dkim_record, bold_prefix="DKIM Record:")
                    self.analyze_dkim(dkim_record)
                    return

        error(f"No DKIM record found for selector '{self.selector}'. This may allow email spoofing.")

    def analyze_dkim(self, dkim_record):
        """
        Analyze the DKIM record for potential issues.
        """
        if "k=rsa;" not in dkim_record:
            warn("DKIM record doesn't specify RSA as the key type.")
