import dns.resolver
from abc import ABC, abstractmethod
from output import info, warn, error

class RecordChecker(ABC):
    """
    Abstract base class for record checkers.
    """
    def __init__(self, domain):
        """
        Initialize the record checker.

        Args:
        domain (str): The domain to check.
        """
        self.domain = domain

    @abstractmethod
    def check(self):
        """
        Check the record. To be implemented by subclasses.
        """
        pass

    def resolve_txt_record(self, domain):
        """
        Resolve TXT records for a given domain.

        Args:
        domain (str): The domain to resolve.

        Returns:
        dns.resolver.Answer or None: The resolved TXT records, or None if not found or error.
        """
        try:
            return dns.resolver.resolve(domain, 'TXT')
        except dns.resolver.NXDOMAIN:
            return None
        except dns.resolver.NoAnswer:
            return None
        except Exception as e:
            raise e

