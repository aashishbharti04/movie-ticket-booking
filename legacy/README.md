# Legacy — Original Source

`source_code.py` is the **original** command-line script this project grew out
of. It is kept here for historical reference only and is **not** used by the
web application.

It is preserved unchanged so you can compare the starting point with the
rebuilt app. Note that it contained several issues that the new application
fixes — SQL injection via string-formatted queries, hardcoded database
credentials, plaintext passwords and no input validation. **Do not run it
against a real database.**

See the project root [README](../README.md) for the modern application.
