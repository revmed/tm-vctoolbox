# R Project Setup with `renv`
This project uses [`renv`](https://rstudio.github.io/renv/) to manage R packages.
Follow the steps below to install required system libraries and R packages.

I've added `renv` to the root where I store my repos though that may not be best practice.

---

## Prerequisites
- (macOS) [Homebrew](https://brew.sh)
    - Install Homebrew if you haven't already:
        ```bash
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
- [R (4.4.1)](https://cran.r-project.org)
    - I use rig to manage R versions:
        - [rig](https://github.com/r-lib/rig?tab=readme-ov-file#id-macos-homebrew): `brew install r-lib/rig/rig`
        - then do `rig add 4.4.1` to install R 4.4.1
        - do `rig ls` to see available versions
        - you can set defualt version with `rig default <name>` by replacing `<name>` with the name you see after calling `rig ls`
    - You can use homebrew to install R as well:
        ```bash
        brew install r
        ```
- [VSCode](https://code.visualstudio.com/) with R extensions
    - Make sure to add the appropriate R extension for VSCode, such as:
        - [R](https://marketplace.visualstudio.com/items?itemName=reditorsupport.r)
        - [R Syntax](https://marketplace.visualstudio.com/items?itemName=Ikuyadeu.r)
        - [radian](https://github.com/randy3k/radian)
        - in my `settings.json`, I have the following to use `radian` as the R terminal:
            ```json
            {
                "r.rterm.mac": "path/to/radian",
                "r.alwaysUseActiveTerminal": true,
                "r.sessionWatcher": true,
                "r.lsp.debug": false,
                "r.rpath.mac": "/usr/local/bin/R",
                "r.rterm.option": ["--no-save", "--no-restore-data"],
                "[r]": {
                    "editor.defaultFormatter": "REditorSupport.r",
                    "editor.formatOnSave": true
                },
            }
            ```
        - In my `keybindings.json`, I have the following to run R code with `cmd+enter`:
            ```json
            [
                {
                "key": "cmd+enter",
                "command": "r.runSelection",
                "when": "editorTextFocus && editorLangId == 'r'"
                },
            ]
            ```

---

## Step-by-step setup
### 1. Install system dependencies
Before installing the R packages, you need native libraries to compile packages 
like `textshaping` and `ragg`.

- Run the shell script from your terminal
    - note: if the shell script is not executable, run `chmod +x install_r_dev_deps_homebrew.sh`

### 2. Initialize the R enviornment
From VSCode, open the integrated R terminal
```
source("/path/to/setup_env.R")
```
- The above will initialize a project-local renv environment
- install all necessary R packages
- create a renv.lock file for reproducibility

### 3. Restore the environment (on a new machine)
```renv::restore()```

### 4. Snapshot changes (if you add new packages)
```
install.packages("new_package")
renv::snapshot()
```

---

# Files Overview

| File | Purpose|
|------|--------|
|`setup_env.R`| Installs an intializes `renv`. Installs other packages & subsequently snapshots the environment|
|`install_r_dev_deps_homebrew.sh`|Installs macOS system libraries via Homebrew|
|`renv.lock`|Exact package versions + sources|
|`.RProfile`|Auto-activates `renv` on session start. See more notes below|

This is what I put in my `.RProfile`
> ```r
> # Activate renv
> source("/path/to/renv/activate.R")
>
> # Activate Python virtual environment via reticulate
> library(reticulate)
> use_virtualenv("/path/to/tm-vctoolbox/.venv", required = TRUE)
> ```



---

# Notes
- Always restart your R session after installing system libraries
- Run `renv::status()` anytime to check if your environment is consistent.
- Use `renv::diagnostics()` if something breaks (this checks your setup).
- in my `~/.zshrc`, I've added: 
    >`export PATH="/path/to/tm-vctoolbox/.venv/bin:$PATH"`