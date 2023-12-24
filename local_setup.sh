#! /bin/sh
echo "Welcome to the setup. Ths will setup the local virtual env and install all the required python libraries."
echo "You can rerun this without any issues."

if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and installing using pip"
    python -m venv .env
fi

# Activate
.env/Scripts/activate

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt

# Work done. So, deactivate the virtual env
deactivate