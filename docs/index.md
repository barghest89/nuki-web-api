# Nuki Web API Python Client

[![PyPI version](https://img.shields.io/pypi/v/nukiwebapi.svg)](https://pypi.org/project/nukiwebapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/nukiwebapi.svg)](https://pypi.org/project/nukiwebapi/)
[![License](https://img.shields.io/github/license/barghest89/nuki-web-api.svg)](https://github.com/barghest89/nuki-web-api/blob/main/LICENSE)
[![Build Status](https://github.com/barghest89/nuki-web-api/actions/workflows/tests.yml/badge.svg)](https://github.com/barghest89/nuki-web-api/actions)

A Python client for the [Nuki Web API](https://developer.nuki.io/page/nuki-web/2/), providing convenient access to smartlock management, accounts, and related features.

## Features
- Full client for the Nuki Web API
- Pythonic classes for Smartlock, Account, ApiKey, etc.
- Async-friendly (compatible with httpx or aiohttp)
- Typed for better IDE support
- Integrated with mkdocstrings for auto-generated docs

## Installation

```bash
pip install nukiwebapi
```

## Usage
```Python
from nukiwebapi import NukiWebAPI

client = NukiWebAPI("YOUR_ACCESS_TOKEN")

for lock_id, lock in client.lock_instances:
    print(lock.name)
    print(lock.hex_id)

    print(lock.is_locked)
    print(lock.battery_charge)
```

## Documentation
    
[API Reference](https://api.nuki.io/)

## Development
Clone the repository and install in editable mode:

```bash
git clone https://github.com/barghest89/nuki-web-api.git
cd nuki-web-api
pip install -e ".[dev]"
```
Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT license.

