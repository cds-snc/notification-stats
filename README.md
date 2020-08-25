# Notification

Contains:

- the public-facing metrics REST API for Notification

## Setting Up

### Local installation instruction

On OS X:

1. Install PyEnv with Homebrew. This will preserve your sanity.

`brew install pyenv`

2. Install Python 3.6.9 or whatever is the latest

`pyenv install 3.6.9`

3. If you expect no conflicts, set `3.6.9` as you default

`pyenv global 3.6.9`

4. Ensure it installed by running

`python --version`

if it did not, take a look here: https://github.com/pyenv/pyenv/issues/660

5. Install `virtualenv`:

`pip install virtualenvwrapper`

6. Add the following to your shell rc file. ex: `.bashrc` or `.zshrc`

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source  ~/.pyenv/versions/3.6.9/bin/virtualenvwrapper.sh
```

7. Restart your terminal and make your virtual environtment:

`mkvirtualenv -p ~/.pyenv/versions/3.6.9/bin/python notifications-stats`

8. You can now return to your environment any time by entering

`workon notifications-stats`

9. Get a copy of the environment variables (same as api)

10. Install all dependencies

`pip3 install -r requirements.txt`

11. Generate the version file ?!?

`make generate-version-file`

12. Run the service

`flask run -p 6015 --host=0.0.0.0`

13. To test

`pip3 install -r requirements_for_test.txt`

`make test`

### Python version

This codebase is Python 3 only. At the moment we run 3.6.9 in production. You will run into problems if you try to use Python 3.4 or older, or Python 3.7 or newer.

## To update application dependencies

`requirements.txt` file is generated from the `requirements-app.txt` in order to pin
versions of all nested dependencies. If `requirements-app.txt` has been changed (or
we want to update the unpinned nested dependencies) `requirements.txt` should be
regenerated with

```
make freeze-requirements
```

`requirements.txt` should be committed alongside `requirements-app.txt` changes.

## Frequent problems

**Problem** : `E999 SyntaxError: invalid syntax` when running `flake8`

**Solution** : Check that you are in your correct virtualenv, with python 3.5 or 3.6

---

**Problem**:

```
/bin/sh: 1: Syntax error: "(" unexpected
make: *** [Makefile:31: freeze-requirements] Error 2
```

when running `make freeze-requirements`

**Solution**: Change `/bin/sh` to `/bin/bash` in the `Makefile`

---

**Problem**: `ImportError: failed to find libmagic. Check your installation`

**Solution**:Install `libmagic`, ex: `brew install libmagic`

---
