# Burp Bulk Search Tool

A desktop application built with `wxPython` to facilitate bulk searches within XML files, specifically tailored for analyzing Burp Suite exports.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- User-friendly graphical interface for searching within XML files.
- Decodes Base64-encoded request and response data from Burp Suite's XML exports.
- Displays request and response data in separate panels for a comprehensive view.
- Highlights search term occurrences in request and response displays for easier navigation.
- Efficient file management with the option to browse, refresh, and open specific files.

## Installation
1. Ensure you have Python3 and `wxPython` installed.
2. Clone this repository:
```git clone https://github.com/iprivettPKT/Burp-Search-Tool.git```
3. Navigate to the repository's directory:
```cd Burp-Search-Tool```

## Usage
1. Launch the application:
```python3 burpsearch.py```
2. Enter a search term in the "Enter Search Term" textbox.
3. Browse and select the XML file you wish to search in.
4. Click "Start Search" to initiate the search process.
5. The results will be saved in a dedicated directory and displayed in the "Generated Files" listbox.
6. Use the "Refresh List", "Open Selected File", and other interactive buttons for additional functionalities.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
