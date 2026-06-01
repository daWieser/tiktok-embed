# Demo Auth

This module automatically creates a demo user and provides a URL endpoint for password-less login.

## Installation

When you install this module, it will automatically create a user with:
- **Username**: `demo`
- **Password**: `demo`

## Usage

Simply navigate to:
```
https://your.odoo.url/web/demo_login
```

You will be automatically logged in as the demo user without entering any credentials.

## Security Warning

⚠️ **This module disables authentication for the demo user.** Only use this in:
- Development environments
- Demo/showcase environments
- **Never in production** with sensitive data