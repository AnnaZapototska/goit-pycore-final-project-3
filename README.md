# 🌳 DREVO CLI Assistant

<p align="center">
  <b>Command Line Assistant for managing contacts, notes, groups and reminders</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue)
![CLI](https://img.shields.io/badge/interface-CLI-orange)
![Package](https://img.shields.io/badge/python-package-ready-green)
![Build](https://img.shields.io/badge/build-working-brightgreen)
![Course](https://img.shields.io/badge/course-GoIT%20Python%20Core-purple)

</p>

---

## 🌳 About the Project

**DREVO CLI Assistant** is a command-line tool designed to help users manage personal information directly from the terminal.

The assistant allows users to store and organize:

- contacts
- phone numbers
- emails
- birthdays
- addresses
- groups of contacts
- notes
- tags for notes

The project was created as the **final project for the GoIT Python Core course**.


---

# ⚡ Quick Start

Clone repository

git clone https://github.com/AnnaZapototska/project-drevo-team.git

Enter project directory

cd project-drevo-team

Run assistant

python assistant_bot/main.py

---

# 📦 Installation

Install dependencies

pip install -r requirements.txt

---

# ▶ Running the Assistant

Run the assistant from project root

python assistant_bot/main.py

You will see CLI prompt

assistant>

Example usage

assistant> add-contact John  
assistant> add-phone John 123456789  
assistant> add-email John john@email.com  
assistant> all-contacts

---

# 🧾 Command Cheat Sheet

## Global Commands

hello — greet the assistant  
help — show help  
exit / close — exit assistant

---

## Contact Management

add-contact — create new contact  
edit-contact — edit contact  
delete-contact — remove contact  
show-primary-phone — show main phone  
search-contact — search contacts  
all-contacts — list all contacts

---

## Address Management

add-address — add address  
edit-address — edit address  
show-address — show address  
delete-address — remove address

---

## Birthdays

add-birthday — add birthday  
show-birthday — show birthday  
all-birthdays — upcoming birthdays

---

## Contact Groups

add-contact-group — create group  
add-contacts-to-group — add contacts  
delete-contact-group — delete group  
show-contact-groups — show groups  
search-contacts-by-group — search contacts

---

## Notes

add-note — create note  
edit-note — edit note  
delete-note — delete note  
search-notes — search notes  
all-notes — show notes

---

## Note Tags

add-note-tag — add tag  
remove-note-tag — remove tag  
show-notes-tags — show tags  
search-notes-by-tag — search notes  
sort-notes-by-tags — sort notes  
all-notes-tags — show tags

---

# 🏗 Architecture

Project structure

assistant_bot

├── main.py        CLI entry point  
├── bot.py         command handlers  
├── storage.py     data persistence  

├── commands       CLI commands  
├── models         data models  
├── services       business logic  
├── utils          helper utilities  

└── tests          project tests

Architecture flow

User (CLI)  
↓  
main.py  
↓  
Command Handlers (bot.py)  
↓  
Services Layer  
↓  
Storage Layer

---

# 📦 Packaging

The project can be built as a Python package.

Install build tools

pip install build

Build package

python -m build

Artifacts appear in

dist/

Example files

assistant_bot-0.1.0.tar.gz  
assistant_bot-0.1.0-py3-none-any.whl

Install locally

pip install dist/*.whl

Then you can import the package

import assistant_bot

---

# 🧰 Development

Development tools used

flake8 — code style checking  
autopep8 — automatic formatting  
pytest — testing

Run linter

flake8

Run formatter

autopep8 --in-place --recursive .

Run tests

pytest

---

# 🌳 Why the Name DREVO

**DREVO** means **tree** in Ukrainian.

Just like a tree has branches, the assistant organizes user data into structured categories:

- contacts
- groups
- notes
- tags

This structure helps keep information organized and easy to navigate.

---

# 👥 Contributors

This project was developed by

Anna Zapototska  
Bohdan Shcherbak  
Roman Zhrun  
Yuliia Herasymiuk

---

# 🎓 Educational Project

DREVO CLI Assistant was created as part of the **GoIT Python Core course**.

---

# ⭐ Support

If you like this project consider giving it a ⭐ on GitHub