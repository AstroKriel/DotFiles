# Python: Classes and Data Structures

How classes, enums, and dataclasses are defined and structured.

---

## Classes

| Rule | |
|---|---|
| Private classes | leading underscore; implementation details supporting public classes; not re-exported |

```python
class _<Name>:
    ...
```

---

## Enums

| Enum type | Base classes |
|---|---|
| Used as strings | `str, Enum` |
| Pure value holder | `Enum` |

```python
class <Name>(str, Enum): ...   # used as strings
class <Name>(Enum): ...        # pure value holder
```

Enum members may hold dataclass instances as values to carry rich metadata per member:

```python
class <EnumName>(Enum):
    <MEMBER> = <DataclassType>(
        <arg>,
        <arg>,
        <arg>,
    )
```

---

## Dataclasses

| Rule | |
|---|---|
| Containers | prefer `@dataclass(frozen=True)`, immutability by default |
| Derived attributes | use `@cached_property` |
| Alternative constructors | `@classmethod` methods named for the operation and source: `from_<type>` for pure type conversion, `load_from_<source>` for I/O reads |
| Resource lifecycle | use context managers (`__enter__` / `__exit__`) |
| `@property` vs `get_*` | use `@property` for attributes derived from existing state: no parameters, no side effects, cheap to compute; use `get_*` for operations that take parameters, involve I/O, or significant cost |

Method ordering within dataclasses:

1. `__post_init__` (validation on construction)
2. Private helper methods (`_` prefix)
3. `@property` methods
4. `@cached_property` methods
5. Regular instance methods
6. `@classmethod` methods
