# {{cookiecutter.project_name}}
[![DOI](https://img.shields.io/badge/DOI-wip-blue.svg?longCache=true)]()
[![PMID](https://img.shields.io/badge/PMID-wip-orange.svg?longCache=true)]()
<div align="center">
<img src="./logos/default.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

## User Guide
### For Windows Users
- Please make sure that you can run shell scripts and `make` cmds in your local environment.
    - you can install it using [Chocolately](https://chocolatey.org/): `choco install make`

### Setting the Virtual Env
1. fork this repository and clone it to your local environment
2. install Docker into your local environment (if already satisfied, skip this)
3. run `make init` cmd in the cloned directory. (**WARNING**: if you rather not use the make cmd, you need to run `auth.sh` to specify your user id)
4. jupyter notebook is succesfully launched (password: `jupyter`).

