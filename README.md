# systemd-analyze-dependency-parser
A hassle-free python based parser for parsing dependencies from [systemd-analyze](https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html) output.

## Requirements

To run this script, you need:

- [Python 3.x](https://www.python.org/downloads/)
  - [pydot](https://pypi.org/project/pydot/)
  - [argparse](https://pypi.org/project/argparse/)

You can install the required packages using:

`pip install pydot argparse`

## Usage

Run the parser script with below flags to perform appropriate tasks;

`python-parser-v2.py [-h] -f FILE [-r] -u UNIT_FILES [UNIT_FILES ...]`
 
**options:**

  - -h, --help            show this help message and exit

  - -f FILE, --file FILE  pass the systemd-analyze's output dot file to be parsed

  - -r, --reverse         pass to get the reverse dependency for the systemd unit file

  - -u UNIT_FILES [UNIT_FILES ...], --unit-files UNIT_FILES [UNIT_FILES ...]
                        pass one or more unit files to find dependencies

**systemd-analyze dot file:**

This script is designed to analyze and extract dependencies from systemd unit files represented in a Graphviz DOT file format. The script provides functionality to both forward and reverse dependency analysis for specified systemd unit files. To generate a systemd-analyze.dot dotfile we need to run `systemd-analyze dot >> <custom-dot-file-name>.dot`. A dot file is a directed graph representation in text format.


## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for details.