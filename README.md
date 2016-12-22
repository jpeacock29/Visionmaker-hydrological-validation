New York City Engineers for a Sustainable World's (NYC-ESW) validation of the [Visionmaker](https://visionmaker.us/nyc/) environmental modeling system's hydrological model.

Complete analysis can be reproduced by,

        mkdir outputs_1
        python3 preprocessing.py
        # run all cells in the jupyter notebook
        # ...

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch main.md' --prune-empty --tag-name-filter cat -- --all
