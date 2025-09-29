# Nuki Web API Python Client

![PyPI version](https://img.shields.io/pypi/v/nuki-web-api.svg)](https://pypi.org/project/nuki-web-api/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/barghest89/nuki-web-api/python-build-on-push.yml)
![PyPI - License](https://img.shields.io/pypi/l/nuki-web-api)

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

[nuki-web-api reference](https://barghest89.github.io/nuki-web-api/)

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

