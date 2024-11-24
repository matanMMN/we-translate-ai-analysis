if [ -f .env ]; then
    # This will load all variables defined in the .env file into the script
    export $(cat .env | xargs)
fi
