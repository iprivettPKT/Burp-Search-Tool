# Burp-Search-Tool
Python tool to search all the burp requests/responses for a term

## Save the XML file
1. Highlight all the items in your burp HTTP history.
2. Right-click > save items.
3. Name your file with a .xml extension.
4. Make sure the base64 encoding checkbox is checked at the bottom of the window.
5. Save.

## Install the requirements
1. python3 -m pip install wxPython

## Using the script
1. Type Python3 burpsearch.py into the terminal
2. Click Browse to browse to your saved burp XML file
3. Type in the search term
4. Click Start Search
5. The program will automatically create a folder in the current directory with all the results.

Please note that in the current iteration, searches are case sensitive
