# Pylipt

Programming language written in Python.

---

## Overview

This is a project I'm working on to understand how programming languages working.
The end goal is to create a functional, interpreted programming language.
Based on the tutorial at [craftinginterpreters.com](craftinginterpreters.com).

---
## Goals

- [ ] Implement a parser to construct abstract syntax trees (AST)
- [ ] Enable control flow using conditionals and loops
- [ ] Implement functions and objects
- [ ] Provide type definition
- [ ] Document syntax and usage
- [ ] Create unit tests for every component 

---

## Features

- REPL
- Lexer
- Interpreter

---

## Installation

- Setup virtual environment

```bash
python -m venv .venv
```
- Activate virtual environment

```bash
source .venv/bin/activate  # Linux, MacOS
```
```bash
.venv\Scripts\activate  # Windows
```

- Install dependencies

```bash
pip install -r requirements.txt
````

- Install the project in the virtual environment

```bash
pip install -e .
```

---

## Usage

#### REPL

```bash
python -m pylipt
```

 or

```bash
python src/pylipt/main.py
```

#### Run Script

```bash
python -m pylipt [path to script]
```

 or

```bash
python src/pylipt/main.py [path to script]
```

---

## Tests

```bash
python -m unittest discover tests
```

