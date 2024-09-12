# Email Authentication Checker

This script checks the SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication, Reporting, and Conformance) records for a given domain. It provides color-coded safety warnings for potentially unsafe configurations and supports output to pipes and files.

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Clone this repository or download the files.
3. Navigate to the project directory:
   ```
   cd email_auth_checker
   ```
4. (Optional but recommended) Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Ensure you're in the project directory and your virtual environment is activated (if you're using one), then run the script:

```
python email_auth_checker.py pantheon.io
```

To specify a DKIM selector (default is 'default'):

```
python email_auth_checker.py pantheon.io -s selector1
```

To disable colored output:

```
python email_auth_checker.py pantheon.io --no-color
```

Replace `pantheon.io` with the domain you want to check, and `selector1` with the DKIM selector you want to use.

## Troubleshooting

If you encounter import errors, ensure that:
1. You're running the script from the project's root directory.
2. All dependencies are installed (`pip install -r requirements.txt`).
3. Your virtual environment is activated (if you're using one).

If issues persist, try:
```
PYTHONPATH=. python email_auth_checker.py pantheon.io
```

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
