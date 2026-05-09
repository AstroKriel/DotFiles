# Bash Style

---

## Preamble

Every script opens with the shebang and strict mode on the first two lines, with no blank line between them:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

---

## Variables

| Rule | |
|---|---|
| Configurable state | `UPPER_CASE`; placed at the top of the script before any logic |
| Internal variables | `lower_case`; derived values, loop variables, local paths |
| Braces | always use `"${var}"`, not `"$var"` |
| Quoting | always quote variable expansions; unquoted expansions are only acceptable inside `[[ ]]` |

---

## Script Location

Scripts that reference paths relative to themselves resolve the script directory at runtime:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
```

---

## Comments and Sections

| Rule | |
|---|---|
| Standalone marker | `##` |
| Inline marker | `#`, two spaces between code and marker |
| When to comment | section structure and non-obvious constraints only; never restate what the code does |
| Section headers | `##\n## === NAME\n##`; use only when the script has multiple distinct logical phases |
| Short scripts | no section headers; a flat structure is clearer |

---

## Terminal Output

| Rule | |
|---|---|
| Case | lower case throughout |
| Errors | `echo "error: <message>"` |
| Warnings | `echo "warning: <message>"` |
| Informational | `echo "<message>"`; no prefix |

---

## Checks and Guards

Checks that abort with a message are preferred over silent failures. The message names the problem and what to do:

```bash
if compgen -G "<pattern>" > /dev/null 2>&1; then
    echo "error: <explanation>; <what to do>"
    exit 1
fi
```
