import sys
import logging
from colorama import init, Fore, Style

class ColoredFormatter(logging.Formatter):
    """
    Custom logging Formatter to add colors to log messages.
    """
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def __init__(self, use_color=True):
        """
        Initialize the formatter with a simple format.

        Args:
        use_color (bool): Whether to use color in the output.
        """
        super().__init__('%(levelname)s: %(message)s')
        self.use_color = use_color

    def format(self, record):
        """
        Format the specified record as text.

        Args:
        record (LogRecord): The log record to format.

        Returns:
        str: The formatted log record.
        """
        if self.use_color and record.levelname in self.COLORS:
            record.levelname = f'{self.COLORS[record.levelname]}{record.levelname}{Style.RESET_ALL}'
        return super().format(record)

def setup_logging(use_color=True):
    """
    Set up logging with color support and pipe detection.

    Args:
    use_color (bool): Whether to use color in the output.
    """
    # Detect if output is being piped or redirected
    is_piped = not sys.stdout.isatty()

    # If piped or --no-color flag is set, disable color
    use_color = use_color and not is_piped

    # Initialize colorama
    init(strip=not use_color, autoreset=True)

    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setFormatter(ColoredFormatter(use_color=use_color))
    logger.addHandler(ch)

# Convenience functions
def info(message):
    """Log an info message."""
    logging.info(message)

def warn(message):
    """Log a warning message."""
    logging.warning(message)

def error(message):
    """Log an error message."""
    logging.error(message)

