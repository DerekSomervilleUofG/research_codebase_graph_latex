## Install
- python -m venv .venv
- .venv\Scripts\activate or source .venv/Scripts/activate
-   
- pip install -r requirement.txt
- https://miktex.org/

## Generate
- pdflatex main_1.tex

## Test
python -m unittest discover -v -s ./test -p test_*.py
## Unix symbloic link
mkdir repository
mkdir resource
mkdir resource/database
cd resource/database
ln -s ../../../research_developer_experience/resouce/database/codebase_start.db codebase_start.db
