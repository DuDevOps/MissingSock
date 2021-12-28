# Running this command creates the target directory 
# (creating any parent directories that don’t exist already) 
# and places a pyvenv.cfg file in it with a home key pointing to the Python installation 
# from which the command was run (a common name for the target directory is .venv). 
# It also creates a bin (or Scripts on Windows) subdirectory containing a copy/symlink of 
# the Python binary/binaries (as appropriate for the platform or arguments used 
# at environment creation time). It also creates 
# an (initially empty) lib/pythonX.Y/site-packages subdirectory 
# (on Windows, this is Lib\site-packages). If an existing directory is specified, 
# it will be re-used.

python -m venv ./.venv
cd ./.venv/Scripts
activate.bat

# Install virtual enviroment with requirements.txt
# pip freeze > requirements.txt
# python -m pip install -r requirements.txt

python -m main.py