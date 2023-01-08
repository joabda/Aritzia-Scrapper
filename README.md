# Aritzia Scrapper

This is a script that scraps data from [Arizia's website](https://www.aritzia.com/) (Woman clothing brand). 

It will also store the metadata relative to an item into a MongoDB database as well as the pictures of that item. 

The script will mark the first and last time an item was seen on the Aritzia's website.

#### Flow diagram
![Flow Control Diagram](https://github.com/joabda/Aritzia-Scrapper/blob/main/Aritzia%20Scrapper.jpg?raw=true)

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/cli/pip_install/) (Package Manager)

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

### Variables
- **MONGODB_URL** => URL of the desired MongoDB database.
- **URL_FILE** => Name of the file containing all the Aritzia URL(s) to be scanned
- **SAVE_HTML_TO_FILE** => If you want the webpage to be saved as HTML file set as 1, if not set as 0
- **WAIT_BETWEEN_EXECUTIONS_IN_SECONDS** => Time to be elapsed between the executions of the scrapping

# Dependencies
After creating the environment and activating it. Some package dependencies need to be installed for the script to work property. 
In order to install these packages execute the following command.
```bash
pip install -r Requirements.txt
```
Requirements.txt is the file that contains a list of packages with the versions used during development.

## Usage
From the base directory of this project, you'll need to start the python process to start the application. 

```bash
python main.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)