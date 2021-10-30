env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.8.7
pyenv virtualenv 3.8.7 guiapp-env
pyenv local guiapp-env
pip install --upgrade pip
pip install requests beautifulsoup4 pandas fbs PyQt5
pip install https://github.com/pyinstaller/pyinstaller/tarball/develop
# change the source code for file:
# ~/.pyenv/versions/3.8.7/envs/guiapp-env/lib/python3.8/site-packages/fbs/installer/mac/__init__.py with the code below
# delete target dir if non-empty one ever existed before
#fbs run
fbs freeze --debug > logs.txt
#fbs installer