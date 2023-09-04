# Music2.0
The second generation of the #Music project, rebuilt soup to nuts and ready for
you to implement yourself.

## Development

### pyenv

We recommend using [`pyenv`](https://github.com/pyenv/pyenv) to manage local
Python versions.

To install it and install the recommended version of Python, run the following
commands:

```shell
# Install pyenv
curl https://pyenv.run | bash

# Set up your shell to use pyenv
# These instructions assume bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Restart your shell to make sure the changes take effect
exec "$SHELL"

# Update to latest pyenv, just in case
pyenv update

# Install the version of Python specified in the .python-version file
pyenv install
```

See also the [`pyenv-installer`](https://github.com/pyenv/pyenv-installer)
project for more help, if needed.

### poetry

We use `poetry` to manage our package dependencies.

After you've set up your local Python version, install the latest version of
`poetry` and set up your environment with the following commands:

```shell
# Install poetry
curl -sSL https://install.python-poetry.org | python -

# Set up environment
poetry install --no-root
```

### run

Once your environment is set up, you can use the `run` script to perform various
development tasks. Execute `./run` without any arguments to see the full
documentation.

To test the server, `./run server`. This will run the development server, which
can be accessed at `http://127.0.0.1:8080/`. Once running, you can test this by hitting it with curl:

```shell
curl http://127.0.0.1:8080/system/ping
```
