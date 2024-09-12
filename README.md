# Email Authentication Checker

This script checks the SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication, Reporting, and Conformance) records for a given domain. It also provides safety warnings for potentially unsafe configurations.

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Clone this repository or download the files.
3. Navigate to the project directory:
   ```
   cd email_auth_checker
   ```
4. Create a virtual environment:
   ```
   python -m venv venv
   ```
5. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
6. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Ensure your virtual environment is activated, then run the script from the command line, providing a domain as an argument:

```
python email_auth_check.py example.com
```

To specify a DKIM selector (default is 'default'):

```
python email_auth_check.py example.com -s selector1
```

Replace `example.com` with the domain you want to check, and `selector1` with the DKIM selector you want to use.

The script will provide warnings for potentially unsafe configurations.

To deactivate the virtual environment when you're done, simply run:

```
deactivate
```

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
