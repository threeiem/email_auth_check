"""
This module contains checkers for various email authentication records.

Available checkers:
- SPFChecker: Checks Sender Policy Framework (SPF) records
- DKIMChecker: Checks DomainKeys Identified Mail (DKIM) records
- DMARCChecker: Checks Domain-based Message Authentication, Reporting and Conformance (DMARC) records
"""

from .spf_checker import SPFChecker
from .dkim_checker import DKIMChecker
from .dmarc_checker import DMARCChecker
