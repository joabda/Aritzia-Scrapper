# Aritzia Scrapper

This is a script that scraps data from [Arizia's website](https://www.aritzia.com/) (Woman clothing brand). 

It will also store the metadata relative to an item into a MongoDB database as well as the pictures of that item. 

The script will mark the first and last time an item was seen on the Aritzia's website.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/cli/pip_install/) (Package Manager)
- [Chromium Web Driver](https://chromedriver.chromium.org/downloads)

## Usage
From the base directory of this project, you'll need to start the python process to start the application. 

```bash
python main.py
```

## Environment
This project is setup to use Python virtual environments. 
```bash
pip install virtualenv
```

After installing this virtual environment package, the environment need to be created.
```bash
python3 -m venv myenv
```

The virtual environment needs to be activiated in order for it to be used. 
*The activation needs to happen every time the project is used.*
```bash
myenv\Scripts\activate
```

# Dependencies
After creating the environment and activating it. Some package dependencies need to be installed for the script to work property. 
In order to install these packages execute the following command.
```bash
pip install -r Requirements.txt
```
Requirements.txt is the file that contains a list of packages with the versions used during development.

## License

[MIT](https://choosealicense.com/licenses/mit/)