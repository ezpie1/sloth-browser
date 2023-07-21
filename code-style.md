# Sloth browser Style Guide

# Quick info

Our style guide is almost the same as the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), so you may also follow that.

Python is the default language on which the sloth browser is build. Thus it's important to know the do and don't for writing better and acceptable code.

To help you format, Ezpie have created a `.pylintrc` file.

# Styling rules

For writing better and acceptable code you may want to run `pylint` with the configuration file. The default configuration will do good.

## Ignoring some warnings

It's important to run pylint before doing a PR.

But sometimes pylint may give warnings which we don't want.

In such cases you may just suppress the warning with line-level comment:

```python
def PUT(): # HTTP name, pylint: disable=invalid-name
  ...
```

Pylint warnings are identified by unique names(invalid-name), thus you can just add `pylint: diable=warning-name` to suppress the warning.

NOTE: You must at all conditions, no matter why not, add an explanation for suppressing the warning. In case one line isn't enough, then add a explanation in your PR.

In case you have unused variables you can add `unused_` or `dummy_` at the end. Always remember to add a comment explaining why you have that variable. "Unused" is sufficient enough.

```python
def Apple():
  variable_unused_ = "No use" # Unused
```

## Imports handling

We Would highly encourage you to use vscode extension [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort).

Also use import statements to import individual class or function, not the entire package or module.

### Applicable ways to use import

- Use `from package import class`
- Use `from package import class as cl` in one of these cases only:

  - Two classes with the same name are being used
  - it's a standard way, ex - `import numpy as np`

A good example is like this:

```python
from PyQt5.QtCore import QSize, Qt, QUrl
...
```

## Semicolon

Don't use semicolon for printing, use it only in case of debugging(if you like).

## Line length

The maximum line length is about **80 chars** only. The pylint configuration file has it defined, in case you forget, it will come in handy.

Exceptions for this case:

- Long import statement(not preferred)
- Long comments
- Long condition statement

To ignore the warning by pylint add `pylint: disable=line-too-long`.

Also don't use backslash `\` for long Explicit line joining. Instead, make use of Python’s implicit line joining inside parentheses, brackets and braces

```python
# Can do
def longUse(self, *args, **kwargs, oneMore: str,
            LongThing: str, OncesAgain: str) -> None: ...
```

```python
# Won't do
if ("hello" in msg and "1" == 1 or \
    1 == 1 and 12 - 12 == 0):
```

Same can be done with strings:

```python
msg = ('A place very very very very very very very very very '
      'very very very very very very far away')
```

## Indentation

Indent your code with _2 spaces_.

Don't use tabs rather use spaces. The Pylint configuration file is configured for this, but it won't know if the indentation is tabs or spaces.

## Commenting and docstring

### Docstring

For writing docstring at all conditions write a one line explanation - summary - and when writing more(preferred) give a one line blank and then write. For writing docstring use `"""`.

### Modules

All modules must have a docstring, pylint will find out, that docstring must have a one line explanation of what that
module is for. Also provide with some examples.

```python
""" This is an explanation. Must give one blank space for fine reading

Give a blank space and write some more stuff.
......
......
......

Usage:
foo = foo()
fooBar = foo.bar()
"""
```

### Functions

Functions also include methods, decorators, generators etc

There must be docstring for each function, even if the function is self explanatory.
You must write the docstring with as much explanation so that the code of it must not be viewed before calling it.

```python
# A helper function
def add(a, b):
  """This is a helper function that adds 2 values passed to it.

  args:
    a: int
    b: int

  returns:
    sum of a and b: int

  example:
    sum = add(12, 15) -> 27
  """
  return a + b

# The main class
class Calculator():
  """This is the main calculator class"""

  def __init__(self, a, b):
    self.a = a
    self.b = b
    self.output = None

  def add(self):
    """This method adds the two given values"""

    self.output = add(self.a, self.b)
```

### Comments

Use comments where needed, such as, code which is complex

example:

```python
def binarySearch(arr, x):
  """A binary search algorithm to find value in a sorted array

  args:
    arr: int[] -> the array in which `x` is to be found
    x: int -> the value to be found

  returns:
    index of `x` in `arr`

  example:
    index = binarySearch([1, 4, 6, 78, 345], 78)
  """

  # The index of the first item
	low = 0
  # Index of the last item
	high = len(arr) - 1
  # middle value's index
	mid = 0

  # As long as low is less then high
	while low <= high:
    # Change middle value to the middle index of the array
		mid = (high + low) // 2

		# If x is greater, ignore left half
		if arr[mid] < x:
			low = mid + 1

		# If x is smaller, ignore right half
		elif arr[mid] > x:
			high = mid - 1

		# Therefore `x` is the middle value
		else:
			return mid

	# If we reach here, then the element was not present in the array
	return -1
```

### Spacial comments

To make the comments look prettier use comments Anchor.

Anchor has spacial tags which can help you highlight any comment. Follow these rules when using comments Anchor:

- **Todo:** If you have any todo use the _TODO_ tag at the beginning of the comment.

- **Review needed:** In case you aren't sure of a piece of code use the _REVIEW_ tag.

- **Help Link:** If you have an idea and would like to share for check, use the _LINK_ tag.

- **ERROR:** If a piece of code cause's error just add a _FIXME_ tag above it.

**FIXME tag**

```python
def hello(name):
  # FIXME - This thing causes lot of error
  return f"hello {nema}"
```

**REVIEW tag**

```python
# REVIEW - Is this useful?
# def something():
#   return 1+1
```

**TODO tag**

```python
def LoadHistoryItem(self, index):
  """ This method is used to add a new tab with the history item selected."""

  # Load the selected history item in a new tab
  item = self.history_model.itemData(index, Qt.UserRole)
  if item:
    url = item[0]
    self.AddNewTab(QUrl(url), self.history_model.item(index).text())
    self.ShowHistory()

# TODO - need a download feature. Here's a recommended link
# LINK - https://example.com/download-feature
```

## Import formatting

We highly recommend you to use the isort extension. use `shift + alt + o` for import formatting.

## Naming patterns

The pylint configuration has been configured to prevent naming errors.

- As for method names use `PascalCase`
- Class names `PascalCase`
- attribute naming `camelCase`

At all conditions, no matter what makes you think not, don't use `snake_case`.

# Recommended extensions

We highly encourage you to use vscode as your code editor, the extensions listed here are as per vscode.

## Language and code styling

These extensions are for the language(python) and for code styling

1. pylance
2. comment anchors
3. isort
4. python
5. prettier

## Optional extensions

These extensions are optional, but yet recommended if you like to code in style.

1. material icon theme
2. dracula official
3. Gitlens
