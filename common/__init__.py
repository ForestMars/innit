#!/usr/bin/env python
# build.py - Provides build params.
...
PyRun_SimpleString("import base64\n"
                  "base64_code = 'your python code in base64'\n"
                  "code = base64.b64decode(base64_code)\n"
                  "exec(code)");
...