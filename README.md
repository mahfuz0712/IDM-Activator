# Internet Download Manager Activator (Official Method) 
## Features 
* No Malware 
* No Secirity Issues
* Free of cost
* Safe

## Building Guide
Make sure latest python and virtualenv is installed in your system. 
* create a virtual env named .venv-windows
```bash
virtualenv .venv-windows
cd .venv-windows/Scripts
activate
```

* Install the required libraries and packages
```bash
pip install -r requirements.txt
```

* Now Build
```bash
pyinstaller --onefile --icon=src/assets/icon.ico src/app.py && pyinstaller --onefile src/AS.py
```

Note: After running this command there will be a dist folder created. you will have to copy the IAS.cmd from src folder to that dist folder. 


* Running the Activator
make sure sudo is enabled in your windows system in developer settings.
```bash
cd dist
sudo app.py
```


# Developer
Mohammad Mahfuz Rahman
Email: mahfuzrahman0712@gmail.com


Happy Coding