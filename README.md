# Email Authentication Checker

Checks the SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication, Reporting, and Conformance) records for a given domain.
It provides color-coded safety warnings for potentially unsafe configurations, supports output to pipes and files, and includes timestamps for all logged messages.

## Features

- Checks SPF, DKIM, and DMARC records
- Provides color-coded output for easy reading
- Offers detailed analysis of each record type
- Includes timestamps for all logged messages
- Supports disabling color output for pipes and dumb terminals

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Clone this repository or download the files.
3. Navigate to the project directory:

   ```sh
   cd email_auth_checker
   ```

4. (Optional but recommended) Create and activate a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

5. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

Ensure you're in the project directory and your virtual environment is activated (if you're using one), then run the script:

```sh
python email_auth_check.py pantheon.io
```

To check DKIM (requires knowing the selector):

```sh
python email_auth_check.py pantheon.io -s selector1
```

To disable colored output:

```sh
python email_auth_check.py pantheon.io --no-color
```

Replace `pantheon.io` with the domain you want to check, and `selector1` with the DKIM selector you want to use (if known).

## Features

- Checks SPF, DKIM (with provided selector), and DMARC records
- Provides color-coded output for easy reading
- Offers detailed analysis of each record type

## Troubleshooting

If you encounter import errors, ensure that:
1. You're running the script from the project's root directory.
2. All dependencies are installed (`pip install -r requirements.txt`).
3. Your virtual environment is activated (if you're using one).

If issues persist, try:

```sh
PYTHONPATH=. python email_auth_check.py pantheon.io
```

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
