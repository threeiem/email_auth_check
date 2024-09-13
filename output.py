"""
Output management module for the Email Authentication Checker.

Key components:
- TimestampedFormatter is a custom log formatter with color-coding
- OutputManager: Manages output formatting with convenience methods

The module also sets up a global OutputManager instance and exposes
convenience functions (info, warn, error).

Usage:
    from output import setup_logging, info, warn, error

    setup_logging()
    info("This is an info message")
    warn("This is a warning")
    error("This is an error")

Note: Color output is automatically disabled when the output is piped
or when running in a non-interactive terminal.
"""
import sys
import logging
from datetime import datetime
from colorama import init, Fore, Style

class TimestampedFormatter(logging.Formatter):
    """
    A custom log formatter that adds timestamps and color-coding to log messages.

    This formatter prepends a timestamp to each log message and applies color-coding
    based on the log level when color output is enabled.
    """

    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.RED + Style.BRIGHT,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def __init__(self, use_color=True):
        """
        Initialize the TimestampedFormatter.

        Args:
            use_color (bool): Whether to use color in the output.
        """
        super().__init__('%(message)s')
        self.use_color = use_color

    def format(self, record):
        """
        Format the specified log record as text.

        Args:
            record (LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = super().format(record)

        if self.use_color:
            message = self._apply_color(record, message)
            timestamp = f"{Fore.CYAN}{timestamp}{Style.RESET_ALL}"
        else:
            message = self._remove_formatting(message)

        return f"{timestamp} {message}"
    
    def _apply_color(self, record, message):
        if record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            message = f"{color}{message}{Style.RESET_ALL}"
            message = message.replace('[BOLD]', Style.BRIGHT)
            message = message.replace('[/BOLD]', Style.RESET_ALL)

        return message

class OutputManager:
    """
    Manages the output formatting and logging for the application.

    This class provides methods for setting up logging, and convenience methods
    for outputting information, warnings, and errors with appropriate formatting.
    """

    def __init__(self, use_color=True):
        """
        Initialize the OutputManager.

        Args:
            use_color (bool): Whether to use color in the output.
        """
        self.use_color = use_color and sys.stdout.isatty()
        init(strip=not self.use_color, autoreset=True)

    def setup_logging(self):
        """
        Set up logging with the custom TimestampedFormatter.

        This method configures the root logger to use the TimestampedFormatter
        and sets the logging level to INFO.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        ch = logging.StreamHandler()
        ch.setFormatter(TimestampedFormatter(use_color=self.use_color))
        logger.addHandler(ch)

    def info(self, message, bold_prefix=None):
        """
        Log an info message, optionally with a bold prefix.

        Args:
            message (str): The message to log.
            bold_prefix (str, optional): A prefix to be displayed in bold.
        """
        if bold_prefix:
            logging.info("[INFO] [BOLD]%s[/BOLD] %s", bold_prefix, message)
        else:
            logging.info("[INFO] %s", message)

    def warn(self, message, bold_prefix=None):
        """
        Log a warning message.

        Args:
            message (str): The warning message to log.
        """
        if bold_prefix:
            logging.warning("[WARN] [BOLD]%s[/BOLD] %s", bold_prefix, message)
        else:
            logging.warning("[WARN] %s", message)

    def error(self, message, bold_prefix=None):
        """
        Log an error message.

        Args:
            message (str): The error message to log.
        """
        if bold_prefix:
            logging.error("[ERROR] [BOLD]%s[/BOLD] %s", bold_prefix, message)
        else:
            logging.error("[ERROR] %s", message)

# Create a global instance of OutputManager
output_manager = OutputManager()

# Expose convenience functions
setup_logging = output_manager.setup_logging
info = output_manager.info
warn = output_manager.warn
error = output_manager.error
