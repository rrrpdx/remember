# remember
Simple command-line twitter like script that saves to Google Sheets. This script parses a text string given in the command line, extract tags and parameters, updates a row in a Google Sheet, and applies formatting to the row. Tags are prefaced by a hashtag (#), and all tags from the input are extracted and stored in column D. Paramters are enclosed in square brackets, and the values enclosed are stored in consecutive columns starting with column F. Rows are color coded based on day of the week. There are special tags/qualifiers that will apply additional formatting to rows.

# Getting Started
1. Create a Google Sheet (for example "daily_log"). 
    - Set the column headings to be ["ID", "Date", "Day", "Tags", "Text"].
    - Set Cell A2 to be 1.
2. Enable OAuth authorization by following these directions: https://pygsheets.readthedocs.io/en/latest/authorization.html
3. Adjust the python executable location in the bash shebang, secret file, secret location, and name of your Google Sheet in remember.py
4. Run sample commands

# Sample Commands
- Show usage: `remember`
- Text with tags & parameters: `remember "#reading #book #gates [How to avoid a climate disaster] by [Bill Gates]"`
- Text with tags & parameters: `remember "#ran [3.2] miles in [0:29:54]"`
- Bold text (by adding tag P1): `remember "#finished big milestone #P1"`
- Strikethru text (by referencing ID with ~): `remember "#done ~2"`


