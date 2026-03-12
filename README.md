# goit-pycore-final-project-3
final-project-group-3

Internal information of the python project structure (we will change this file, just to have for use):

# structure 
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