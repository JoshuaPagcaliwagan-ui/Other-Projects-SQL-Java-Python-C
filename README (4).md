# CMSC-127-project
Student Organization Management System
This application allows students to manage their organization memberships through a command-line interface connected to a MariaDB database.

# Project Setup Guide

This guide outlines the step-by-step process for setting up the MariaDB database and running the application.

---

## Prerequisites

The following should be installed:

- Python 3.8 or higher
- pip (Python package manager)
- MariaDB 
- A Linux-like environment is recommended (e.g., **WSL on Windows**, native Linux, or even macOS)

---

## Environment Setup

In running our project, we highly recommend using **WSL (Windows Subsystem for Linux)** on Windows, or any environment where:

- `pip` installs packages correctly
- `python3` pointing to the proper interpreter
- MariaDB can be installed and run via a package manager

For Windows using WSL:
```bash
  wsl --install
  sudo apt update && sudo apt upgrade -y
  sudo apt install libmariadb-dev
  pip install mariadb
```

# Launch MySQL shell and initialize database with the SQL set-up file
```bash
sudo mysql -u root -p
CREATE DATABASE 127project;
CREATE USER 'project'@'localhost' IDENTIFIED BY 'project';
GRANT ALL PRIVILEGES ON 127project.* TO 'project'@'localhost';
FLUSH PRIVILEGES;
EXIT;
exit
```

# Back to terminal
```bash
sudo mysql -u project -p 127project < 127project.sql
Enter password: project
```
# Run the app
```bash
python3 main.py
```
# Inserting in SQL
```bash
INSERT INTO member (student_number, password, first_name, last_name)
VALUES ('202312345', 'pass123', 'Sabrina', 'Carpenter');
```


