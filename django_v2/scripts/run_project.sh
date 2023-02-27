#!/usr/bin/env bash
###
 # Script to quickly setup and locally serve project in one command.
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

    echo -e "${text_blue}Starting project setup for Django v2.2 test environment...${text_reset}"
    echo ""

    # Import corresponding virtual environment, if not already done.
    source ./.venv/bin/activate

    # Ensure latest versions of all corresponding dependencies are installed.
    # Because this project is assumed to only be used in local development,
    # we only care about having a consistent Django major LTS version, and then
    # otherwise always wanting the latest versions/bugfixes of all other
    # corresponding packages used.
    pipenv install --dev

    # Make latest project migrations.
    python manage.py makemigrations

    # Run project migrations.
    python manage.py migrate



    echo ""
    echo -e "${text_blue}Setup complete. Running project serve at ${text_orange}http://127.0.0.1:8022/${text_reset}"
    echo ""

    # Run project serve.
    python manage.py runserver 8022

}


main
