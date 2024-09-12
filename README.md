# Email Authentication Checker

This script checks the SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication, Reporting, and Conformance) records for a given domain.

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Clone this repository or download the files.
3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line, providing a domain as an argument:

```
python email_auth_checker.py pantheon.io
```

To specify a DKIM selector (default is 'default'):

```
python email_auth_checker.py pantheon.io -s selector1
```

Replace `pantheon.io` with the domain you want to check, and `selector1` with the DKIM selector you want to use.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
