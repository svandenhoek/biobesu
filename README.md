# Bioinformatics Benchmark Suite

A suite for testing bioinformatics tools.

## Installation
### How-to
```bash
git clone git@github.com:molgenis/biobesu.git
cd biobesu
pip install .
```

## Structure

```
helper/ # General helper scripts
    |- <name>.py

suite/ # Benchmark suites
    |- <suitename>
        |- cli.py # Entry point for suite
        |- helper/ # Suite helper scripts
            |- <name>.py
        |- runner/ # Scripts runnable through suite entry point
            |- <name>.py
```

## Developers (work-in-progress)
### Installation
#### Command line
```bash
git clone git@github.com:molgenis/biobesu.git
cd biobesu
pip install --editable .[test]
pytest test/
```

#### Intellij IDEA
1. `git clone git@github.com:molgenis/biobesu.git`
2. In Intellij IDEA, install the Python module if not yet installed (Preferences -> Plugins).
3. Open the project folder in Intellij IDEA.
4. Go to "File -> Project Structure -> SDKs" and select/create a Python virtual environment.
5. Open `setup.py` and install any missing packages.
