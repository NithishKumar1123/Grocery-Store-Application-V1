#! /bin/sh
echo "Welcome to the setup. Ths will setup the local virtual env and install all the required python libraries."
echo "You can rerun this without any issues."

if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
.env/Scripts/activate
export ENV=development
python GroceryStore.py