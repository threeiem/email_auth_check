"""
Module to check the DMARC record for a domain.
"""
from output import info, warn, error
from .base_checker import RecordChecker

class DMARCChecker(RecordChecker):
    """
    Class to check the DMARC record for a domain.
    """
    record_type = "DMARC"

    def check(self):
        """
        Check the DMARC record for the domain.
        """
        dmarc_domain = f"_dmarc.{self.domain}"
        answers = self.resolve_txt_record(dmarc_domain)
        if not answers:
            error("No DMARC record found. This may allow email spoofing.")
            return

        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.startswith(b'v=DMARC1'):
                    dmarc_record = txt_string.decode('utf-8')
                    info(dmarc_record, bold_prefix="DMARC Record:")
                    self.analyze_dmarc(dmarc_record)
                    return

        error("No DMARC record found. This may allow email spoofing.")

    def analyze_dmarc(self, dmarc_record):
        """
        Analyze the DMARC record for potential issues.
        """
        if 'p=none' in dmarc_record:
            warn("DMARC policy is set to 'none', no protection against spoofing.")
