#!/usr/bin/env bash
###
 # Script to quickly setup local project and run pytests in one command.
 ##


# Abort on error
set -e


# Import utility script.
. $(dirname ${0})/utils.sh


function main () {
    # Change to project root.
    cd ..

    # Clear any current output in terminal.
    clear

    echo -e "${text_blue}Starting project setup for Django v4.1 test environment...${text_reset}"
    echo ""

    # Import corresponding virtual environment, if not already done.
    source ./.venv/bin/activate

    # Ensure latest pip and wheel are installed.
    pip install --upgrade pip
    pip install --upgrade wheel

    # Ensure latest versions of all corresponding dependencies are installed.
    # Because this project is assumed to only be used in local development,
    # we only care about having a consistent Django major LTS version, and then
    # otherwise always wanting the latest versions/bugfixes of all other
    # corresponding packages used.
    pipenv install --dev

    # Clear out migration files if any are present.
    ./scripts/purge_migrations.sh

    # Reset local database if present.
    if [[ -f "./db.sqlite3" ]]
    then
        rm -f "./db.sqlite3"
    fi

    # Make latest project migrations.
    python manage.py makemigrations

    # Run project migrations.
    python manage.py migrate

    echo ""
    echo -e "${text_blue}Setup complete. Running project pytests.${text_reset}"
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""

    # Run project serve.
    pytest $@

}


main $@
