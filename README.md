# Innit

CLI utility to create project scaffolding following a project templates. Current version is Python/Cython specific.

# Table of contents

  * [Overview](#innit)
  * [Version](#version)
  * [Use](#use)
  * [Features](#features)
  * [Why not Cookiecutter?](#why-not-cookiecutter)
  * [Known Issues](#known-issues)
  * [License](#license)

# version

* The current version is 0.1.

# Use

* Simply execute the `new.sh` script, passing it arguments for project name (`--name`) and destination directory (`--path`):

`~>./new.sh --name MyProject --path some/path`

* (Destination directory defaults to user home directory: `~`)

# Features

* Handles scaffolding of a new Cython project, including build source and target directories, with scripts to build for local or target architecture.

* Optionally, initalize Git repository with `--git` flag.

# Why Not Cookiecutter?

* Ultimately this script could easily be ported to a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template. For this prototypical version however, that's significant overkill. Nothing against overkill, mind you, but rather than having to maintain consistency (updating, etc.) with an overly complicated approach (for such purposes), a more straightforward shell script and template files gets the job done.

# Known Issues

* None currently reported.

# License

* Released under the Apache Software License.
