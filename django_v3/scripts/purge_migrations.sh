#!/usr/bin/env bash
###
 # Script to purge all project migrations, for fresh database.
 ##


# Abort on error
set -e


# Import utility script.
. $(dirname ${0})/utils.sh


function main () {
    # Change to project root.
    cd ..

    # Loop through all files in migration folder.
    for file in "./test_app/migrations/"*
    do
        # Check if actually a file.
        if [[ -f ${file} ]]
        then
            # Check that file follows migration name format.
            if [[ "${file}" == *"/migrations/0"*".py" ]]
            then
                # Remove found migration file.
                rm -f ${file}
            fi
        fi
    done
}


main
