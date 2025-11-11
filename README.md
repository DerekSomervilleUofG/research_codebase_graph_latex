## Install
- python -m venv .venv
- .venv\Scripts\activate or source .venv/bin/activate
-   
- pip install -r requirement.txt
- https://miktex.org/

## Generate
- pdflatex main.tex
## Unix symbloic link
mkdir repository
mkdir resource
mkdir resource/database
cd resource/database
ln -s ../../../research_developer_experience/resource/database/codebase_start.db codebase_start.db
