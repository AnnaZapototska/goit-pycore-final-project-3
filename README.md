# goit-pycore-final-project-3
final-project-group-3

## Development tools (flake8 / autopep8 / pytest)

All commands below should be run from the repository root.

### Install dependencies

- Create/activate your virtual environment (recommended), then install:
    - `python -m pip install -r requirements.txt`

### Lint with flake8

- Lint the main package and tests:
    - `python -m flake8 assistant_bot`
- Optional: show a summary:
    - `python -m flake8 assistant_bot --count --statistics`

### Format with autopep8

- Preview changes (no files modified):
    - `python -m autopep8 --diff --recursive assistant_bot`
- Apply formatting in-place:
    - `python -m autopep8 --in-place --recursive assistant_bot`

### Run tests with pytest

- Run all tests:
    - `python -m pytest`
- Run tests with a quieter output:
    - `python -m pytest -q`
- Run a single test file:
    - `python -m pytest assistant_bot/tests/test_bot.py`
- Run tests with verbose mode and with full output:
    - `python -m pytest -vv`

Internal information of the python project structure (we will change this file, just to have for use):

# structure 
```
assistant_bot/
│
├── main.py
├── bot.py
├── storage.py
│
├── models/
│   ├── contacts.py
│   ├── notes.py
│   └── fields.py
│
└── utils/
    ├── validators.py
    └── decorators.py
```



# Address functionality

The assistant bot allows managing contact addresses.

Available address commands:

add-address <name>  
Adds an address to an existing contact.  
The bot will ask for:
- street
- city
- country

Example:
add-address John

edit-address <name>  
Updates the existing address of a contact.

Example:
edit-address John

show-address <name>  
Displays the saved address for a contact.

Example:
show-address John

remove-address <name>  
Removes the address from a contact.

Example:
remove-address John