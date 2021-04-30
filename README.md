About
======
This is a collection of templates to create different web apps components on the basis of Python 3.x

Overview
=========

# Preliminary steps

1) First check the version - it should be 3.9.x (3.9.1 in our case)

```
python --version

Python 3.9.1
```

2) Create a virtual environment

```
python -m venv env
```
As a result a folder env with python libs will be created

3) Activate virtual env:

```
.\env\Scripts\activate
```
The prompt will be changed to (env)

4) Update environmental variables (needed for both Windows and *nix systems, see
https://cryptography.io/en/latest/installation/#building-cryptography-on-windows and 
   https://www.scivision.dev/python-windows-visual-c-14-required):
   
   
4.1) Download and install Win64OpenSSL-1.1.1.exe
4.2) Set the env variables
```
set LIB="c:\Program Files\OpenSSL-Win64\lib";%LIB%
set INCLUDE="c:\Program Files\OpenSSL-Win64\include";%INCLUDE%
```
Note, that for build Microsoft Visual C++ 14.0 or greater will be required (install it from 
https://visualstudio.microsoft.com/visual-cpp-build-tools/ -on clean installation about 1.5GB files 
will be needed to download and install)

Microsoft Visual C++ 14.2 standalone: Build Tools for Visual Studio 2019 (x86, x64, ARM, ARM64)
This is a standalone version of Visual C++ 14.2 compiler, you don't need to install Visual Studio 2019.

https://wiki.python.org/moin/WindowsCompilers


Install Microsoft Build Tools for Visual Studio 2019.

In Build tools, install C++ build tools and ensure the latest versions of MSVCv142 - VS 2019 C++ x64/x86 build tools and Windows 10 SDK are checked.

The setuptools Python package version must be at least 34.4.0.


5) Install necessary dependencies into virtual environment:

```
pip install -r requirements.txt
```
As a result all extra dependencies will be added

Installation
=============

Get the local database ready

```
python init_db.py
```

Start the development server

```
FLASK_APP=wsgi.py flask run
```
Check the service at http://127.0.0.1:5000/


Tests
------

Run the unit tests with

```
pytest
```



Dependencies
------

ThoughtsBackend uses Flask as a web framework, Flask RESTplus for creating the interface, 
and SQLAlchemy to handle the database models. It uses a SQLlite database for local development.



Requirements
=============

In order to execute the code the following toolkit is needed:

- Virtualenv
- Python 3.9
- pgAdmi
- Docker
