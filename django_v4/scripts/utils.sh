#!/usr/bin/env bash
###
 # A helper/utility script to be imported by other scripts.
 #
 # Intended to hold very common functionality (that's surprisingly not built into bash) such as string upper/lower,
 # and checking current user value, and prompts of yes/no user input.
 #
 # https://git.brandon-rodriguez.com/scripts/bash/utils
 # Version 1.3.1
 ##


#region Global Utility Variables.

# Color Output Variables.
text_reset="\033[0m"
text_black="\033[0;30m"
text_red="\033[0;31m"
text_green="\033[0;32m"
text_orange="\033[0;33m"
text_blue="\033[0;34m"
text_purple="\033[0;35m"
text_cyan="\033[1;36m"
text_yellow="\033[1;33m"
text_white="\033[1;37m"

# Arg, Kwarg, and Flag Return Variables.
args=()
flags=()
declare -A kwargs=()
global_args=()
global_flags=()
declare -A global_kwargs=()
help_flags=false

# Function Return Variables.
return_value=""
file_name=""
file_extension=""

#endregion Global Utility Variables


#region Script Setup Functions

###
 # Normalizes the location of the terminal to directory of utils.sh file.
 #
 # The point is so that the execution of a script will handle the same, regardless of terminal directory location at
 # script start. Ex: User can start script at either their home folder, or project root, (or any other directory) and
 # relative directory handling will still function the same in either case.
 #
 # Automatically called on script import.
 #
 # Return Variable(s): return_value
 ##
function normalize_terminal () {
    cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
}


###
 # Handles passed values.
 #
 # Splits into "args", "kwargs", and "flags":
 #  * Args are any other values that don't match below two formats.
 #      * Ex: "True", "5", and "test".
 #  * Kwargs are key-value pairs, where the key comes first and starts with "--" or "-".
 #      * Note that the associated value must come immediately after the key.
 #      * Ex: "--type int", "--dir ./test", and "--name Bob".
 #  * Flags are any variable that starts with "-" or "--", and must be defined by the calling script.
 #      * To define flags, populate a "possible_flags" array with flag values prior to calling util script.
 #      * These are effectively treated as booleans. True if present, false otherwise.
 #      * Ex: "-a", "--b", "-run", and "--test".

 #
 # Ordering of provided args, kwargs, and flags should not matter, aside from kwarg keys needing a corresponding value
 # as the direct next processed value.
 #
 # Note that "-h" and "--help" are handled separately, and considered to both be "help flags".
 # If either one is provided, then a "help_flags" global variable is set to true.
 # The expectation is that some kind of "display help" function will run instead of normal script functionality.
 #
 # Return Variable(s): help_flags, args, kwargs, flags, global_args, global_kwargs, and global_flags
 ##
handle_args_kwargs () {
    local handle_kwarg=false
    local kwarg_key=""
    set_global_args=false
    set_global_flags=false
    set_global_kwargs=false

    # On first run, set "global" arg/kwarg values, as backup.
    # Useful in case any functions ever call this for additional arg/kwarg/flag handling.
    # Prevents original passed values from being overriden by a function's passed values.
    if [[ ${#global_args[@]} == 0 && ${#global_flags[@]} == 0 && ${#global_kwargs[@]} == 0 ]]
    then
        set_global_args=true
        set_global_flags=true
        set_global_kwargs=true
    else
        args=()
        flags=()
        kwargs=()
    fi

    # Parse all args.
    for arg in ${@}
    do
        # Check arg type, based on substring match.
        if [[ "${arg}" == "-h" || "${arg}" == "--help" ]]
        then
            # Special handling for help flags.
            help_flags=true

        # Handle for flags.
        elif [[ ${#possible_flags[@]} > 0 && ${possible_flags[@]} =~ "${arg}" ]]
        then
            # Check for kwarg handling bool.
            if [[ ${handle_kwarg} == true ]]
            then
                # Expected arg to fill value for key-value pair. Got flag. Raise error.
                echo -e "${text_red}Expected value for kwarg key of \"${kwarg_key}\". Got a flag of \"${arg}\" instead.${text_reset}"
                exit 1
            else
                # Save kwarg key and process next value.
                if [[ "${arg}" == "--"* ]]
                then
                    # Handle for double dash flag.
                    local new_flag=${arg#--}
                elif [[ "${arg}" == "-"* ]]
                then
                    # Handle for single dash flag.
                    local new_flag=${arg#-}
                else
                    # Unexpected kwarg value.
                    echo -e "${text_red}Unexpected flag type of \"${arg}\". Unable to proceed.${text_reset}"
                    exit 1
                fi

                flags+=( ${new_flag} )

                # Optionally populate global flags.
                if [[ ${set_global_flags} == true ]]
                then
                    global_flags+=( ${new_flag} )
                fi
            fi

        # Handle for kwargs.
        elif [[ ("${arg}" == "-"* || "${arg}" == "--"*) && "${arg}" != "---"*  ]]
        then
            # Check for kwarg handling bool.
            if [[ ${handle_kwarg} == true ]]
            then
                # Expected arg to fill value for key-value pair. Got kwarg key. Raise error.
                echo -e "${text_red}Expected value for kwarg key of \"${kwarg_key}\". Got another key of \"${arg}\" instead.${text_reset}"
                exit 1
            else
                # Save kwarg key and process next value.
                if [[ "${arg}" == "--"* ]]
                then
                    # Handle for two dash kwarg.
                    kwarg_key=${arg#--}
                    handle_kwarg=true
                elif [[ "${arg}" == "-"* ]]
                then
                    # Handle for one dash kwarg.
                    kwarg_key=${arg#-}
                    handle_kwarg=true
                else
                    # Unexpected kwarg value.
                    echo -e "${text_red}Unexpected kwarg key type of \"${arg}\". Unable to proceed.${text_reset}"
                    exit 1
                fi
            fi

        # Handle for args.
        else
            # Check for kwarg handling bool.
            if [[ ${handle_kwarg} == true ]]
            then
                # Set key-value kwarg pair.
                kwargs[${kwarg_key}]=${arg}
                handle_kwarg=false

                # Optionally populate global kwargs.
                if [[ ${set_global_kwargs} == true ]]
                then
                    global_kwargs[${kwarg_key}]=${arg}
                fi

            else
                # Add arg to list of args.
                args+=( ${arg} )

                # Optionally populate global args.
                if [[ ${set_global_args} == true ]]
                then
                    global_args+=( ${arg} )
                fi
            fi
        fi

    done
}

#endregion Script Setup Functions


#region Directory Functions

###
 # Gets absolute path of passed location.
 #
 # Return Variable(s): return_value
 ##
function get_absolute_path () {

    # Check number of passed function args.
    if [[ ${#} == 1 ]]
    then
        # Expected number of args passed. Continue.

        # Check location type.
        if [[ -f ${1} ]]
        then
            # Handle for file.
            return_value="$(cd "$(dirname "${1}")"; pwd -P)/$(basename "${1}")"

        elif  [[ -d ${1} ]]
        then
            # Handle for directory.

            # Extra logic to properly handle values of "./" and "../".
            local current_dir="$(pwd -P)"
            cd ${1}

            # Then call this to have consistent symlink handling as files.
            return_value="$(cd "$(dirname "$(pwd -P)")"; pwd -P)/$(basename "$(pwd -P)")"

            # Change back to original location once value is set.
            cd ${current_dir}
        else
            echo -e "${text_red}Passed value ( ${1} ) is not a valid file or directory.${text_reset}"
            exit 1
        fi

    # Handle for too many args.
    elif [[ ${#} > 1 ]]
    then
        echo -e "${text_red}Too many args passed. Expected one arg, received ${#}.${text_reset}"
        exit 1

    # Handle for too few args.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}


###
 # If no arg is provided, returns full path of current directory.
 # If arg is passed, then returns absolute path if was directory, or full path of parent directory if was file.
 #
 # Return Variable(s): return_value
 ##
function get_directory_path () {

    # Check number of passed function args.
    if [[ ${#} == 0 ]]
    then
        # No args passed. Handle for current directory.
        get_absolute_path ./

    # Handle for one arg.
    elif [[ ${#} == 1 ]]
    then

        # Check location type.
        if [[ -f ${1} ]]
        then
            # Handle for file.
            get_absolute_path ${1}
            return_value=${return_value%/*}

        elif [[ -d ${1} ]]
        then
            # Handle for directory.
            get_absolute_path ${1}

        else
            echo -e "${text_red}Passed value ( ${1} ) is not a valid file or directory.${text_reset}"
            exit 1
        fi

    # Handle for too many args.
    else
        echo -e "${text_red}Too many args passed. Expected zero or one args, received ${#}.${text_reset}"
        exit 1
    fi
}


###
 # If no arg is provided, then returns name of current directory.
 # If arg is passed, then returns name of directory, or parent directory of file.
 #
 # Return Variable(s): return_value
 ##
function get_directory_name () {

    # Check number of passed function args.
    if [[ ${#} == 0 ]]
    then
        # No args passed. Pass current directory to parent function.
        get_directory_path ./
        return_value=${return_value##*/}

    # Handle for one arg.
    elif [[ ${#} == 1 ]]
    then

        # Pass provided value to parent function.
        get_directory_path ${1}
        return_value=${return_value##*/}

    # Handle for too many args.
    else
        echo -e "${text_red}Too many args passed. Expected zero or one args, received ${#}.${text_reset}"
        exit 1
    fi
}


###
 # Parses passed file, getting base file name and file extension.
 #
 # Return Variable(s): return_value
 ##
function parse_file_name () {

    # Check number of passed function args.
    if [[ ${#} == 1 ]]
    then
        # Expected number of args passed. Continue.
        if [[ -f ${1} ]]
        then
            # Handle for file.
            get_absolute_path ${1}
            return_value=${return_value##*/}

            file_name=""
            file_extension=""
            _recurse_file_extension ${return_value}
        else
            echo -e "${text_red}Passed value ( ${1} ) is not a valid file.${text_reset}"
            exit 1
        fi

    # Handle for too many args.
    elif [[ ${#} > 1 ]]
    then
        echo -e "${text_red}Too many args passed. Expected one arg, received ${#}.${text_reset}"
        exit 1

    # Handle for too few args.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}


###
 # Recursive helper function for parse_file_name().
 # Determines base file name and full file extension.
 #
 # Return Variable(s): file_name and file_extension
 ##
function _recurse_file_extension () {
    local passed_value=${1}
    local parsed_extension=${passed_value##*.}

    # Check if file extension was found. Occurs when variables are not identical.
    if [[ ${parsed_extension} != ${passed_value} ]]
    then
        # Extension found. Iterate once more.
        file_name=${passed_value%.${parsed_extension}}

        # Handle if global var is currently empty or not.
        if [[ ${file_extension} == "" ]]
        then
            file_extension=".${parsed_extension}"
        else
            file_extension=".${parsed_extension}${file_extension}"
        fi

        # Call recursive function once more.
        _recurse_file_extension ${file_name}
    fi
}


#endregion Directory Functions


#region User Check Functions

###
 # Checks if current username matches passed value.
 # In particular, is used to check if user is sudo/root user.
 #
 # Return Variable(s): None
 ##
function check_is_user () {

    # Check number of passed function args.
    if [[ ${#} == 1 ]]
    then
        # Expected number of args passed. Continue.
        local username=$USER
        local check_user=$1

        # Determine user to check for.
        to_lower ${check_user}
        if [[ "${return_value}" == "root" || "${return_value}" == "sudo" ]]
        then
            # Special logic for checking if "sudo"/"root" user.
            if [[ "$EUID" != 0 ]]
            then
                echo -e "${text_red}Sudo permissions required. Please run as root.${text_reset}"
                exit
            fi
        else
            # Standard logic for all other user checks.
            if [[ "${username}" != "${check_user}" ]]
            then
                echo -e "${text_red}User check (${check_user}) failed. Current user is ${username}.${text_reset}"
                exit 1
            fi
        fi

    # Handle for too many args.
    elif [[ ${#} > 1 ]]
    then
        echo -e "${text_red}Too many args passed. Expected one arg, received ${#}.${text_reset}"
        exit 1

    # Handle for too few args.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}


###
 # Checks if current username does not match passed value.
 # In particular, is used to check if user is not sudo/root user.
 #
 # Return Variable(s): None
 ##
function check_is_not_user () {

    # Check number of passed function args.
    if [[ ${#} == 1 ]]
    then
        # Expected number of args passed. Continue.
        local username=$USER
        local check_user=$1

        # Determine user to check for.
        to_lower ${check_user}
        if [[ "${return_value}" == "root" || "${return_value}" == "sudo" ]]
        then
            # Special logic for checking if "sudo"/"root" user.
            if [[ "$EUID" == 0 ]]
            then
                echo -e "${text_red}Standard permissions required. Please run as non-root user.${text_reset}"
                exit
            fi
        else
            # Standard logic for all other user checks.
            if [[ "${username}" == "${check_user}" ]]
            then
                echo -e "${text_red}Not-user check (${check_user}) failed. Current user is ${username}.${text_reset}"
                exit 1
            fi
        fi

    # Handle for too many args.
    elif [[ ${#} > 1 ]]
    then
        echo -e "${text_red}Too many args passed. Expected one arg, received ${#}.${text_reset}"
        exit 1

    # Handle for too few args.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}

#endregion User Check Functions


#region Text Manipulation Functions

###
 # Converts one or more passed args to uppercase characters.
 #
 # Return Variable(s): return_value
 ##
function to_upper () {

    # Check number of passed function args.
    if [[ ${#} > 0 ]]
    then
        # At least one arg passed. Loop through each one.
        return_value=()
        for arg in ${@}
        do
            return_value+=( $(echo "${arg}" | tr '[:lower:]' '[:upper:]') )
        done

    # No args passed.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}


###
 # Convers one or more passed args to lowercase characters.
 #
 # Return Variable(s): return_value
 ##
function to_lower () {

    # Check number of passed function args.
    if [[ ${#} > 0 ]]
    then
        # At least one arg passed. Loop through each one.
        return_value=()
        for arg in ${@}
        do
            return_value+=( $(echo "${arg}" | tr '[:upper:]' '[:lower:]') )
        done

    # No args passed.
    else
        echo -e "${text_red}Too few args passed. Expected one arg, received 0.${text_reset}"
        exit 1
    fi
}

#endregion Text Manipulation Functions


#region Display Functions

###
 # Prompts user for yes/no confirmation. Returns True if yes.
 # Accepts "yes", "ye", and "y". Input values are treated as case insensitive.
 # All other values are treated as "no".
 #
 # Return Variable(s): return_value
 ##
function get_user_confirmation () {
    # Check number of passed function args.
    if [[ ${#} == 0 ]]
    then
        # Handle prompt for no args passed.
        echo -e "[${text_cyan}Yes${text_reset}/${text_cyan}No${text_reset}]"

    elif [[ ${#} == 1 ]]
    then
        # Handle prompt for one arg passed.
        echo -e "${1} [${text_cyan}Yes${text_reset}/${text_cyan}No${text_reset}]"

    else
        # Handle for too many args.
        echo -e "${text_red}Too many args passed. Expected zero or one arg, received ${#}.${text_reset}"
        exit 1
    fi

    # Get user input.
    read -p " " return_value
    echo ""

    # Convert input to lower for easy parsing.
    to_lower "${return_value}"

    # Finally parse user input.
    if [[ "${return_value}" == "y" || "${return_value}" == "ye" || "${return_value}" == "yes" ]]
    then
        # User provided "yes". Return True.
        return_value=true
    else
        # For all other values, return False.
        return_value=false
    fi
}


###
 # Prints out all available text colors provided by this script.
 #
 # Return Variable(s): None
 ##
function display_text_colors () {
    echo ""
    echo "Displaying all available text colors:"
    echo -e "   ${text_black}Black${text_reset}"
    echo -e "   ${text_red}Red${text_reset}"
    echo -e "   ${text_green}Green${text_reset}"
    echo -e "   ${text_orange}Orange${text_reset}"
    echo -e "   ${text_blue}Blue${text_reset}"
    echo -e "   ${text_purple}Purple${text_reset}"
    echo -e "   ${text_cyan}Cyan${text_reset}"
    echo -e "   ${text_yellow}Yellow${text_reset}"
    echo -e "   ${text_white}White${text_reset}"
    echo ""
}


###
 # Prints out all current flags, args, and kwargs, as determined by handle_args_kwargs() function.
 # If function has been called multiple times, then will also print out global values.
 #
 # Return Variable(s): None
 ##
function display_args_kwargs () {
    echo ""
    echo -e "${text_blue}Displaying processed flags, args, and kwargs.${text_reset}"
    echo ""

    # Display for flags.
    if [[ ${#flags[@]} > 0: ]]
    then
        echo -e " ${text_purple}Flags${text_reset} (${#flags[@]} Total):"
        echo "    ${flags[@]}"
    else
        echo " No Flags Set."
    fi

    # Display for args.
    if [[ ${#args[@]} > 0 ]]
    then
        echo -e " ${text_purple}Args${text_reset} (${#args[@]} Total):"
        for index in ${!args[@]}
        do
            echo "    ${index}: ${args[${index}]}"
        done
    else
        echo " No Args Set."
    fi

    # Display for kwargs.
    if [[ ${#kwargs[@]} > 0 ]]
    then
        echo -e " ${text_purple}Kwargs${text_reset} (${#kwargs[@]} Total):"
        for key in ${!kwargs[@]}
        do
            echo "    ${key}: ${kwargs[${key}]}"
        done
    else
        echo " No Kwargs Set."
    fi

    # Only display if global values are different.
    if [[ ${flags[@]} != ${global_flags[@]} || ${args[@]} != ${global_args[@]} || ${kwargs[@]} != ${global_kwargs[@]} ]]
    then
        echo ""
        echo ""

        # Display for global flags.
        if [[ ${#global_flags[@]} > 0: ]]
        then
            echo -e " ${text_purple}Global Flags${text_reset} (${#global_flags[@]} Total):"
            echo "    ${global_flags[@]}"
        else
            echo " No Global Flags Set."
        fi

        # Display for global args.
        if [[ ${#global_args[@]} > 0 ]]
        then
            echo -e " ${text_purple}Global Args${text_reset} (${#global_args[@]} Total):"
            for index in ${!global_args[@]}
            do
                echo "    ${index}: ${global_args[${index}]}"
            done
        else
            echo " No Global Args Set."
        fi

        # Display for global kwargs.
        if [[ ${#global_kwargs[@]} > 0 ]]
        then
            echo -e " ${text_purple}Global Kwargs${text_reset} (${#global_kwargs[@]} Total):"
            for key in ${!global_kwargs[@]}
            do
                echo "    ${key}: ${global_kwargs[${key}]}"
            done
        else
            echo " No Global Kwargs Set."
        fi
    fi

    echo ""
}

#endregion Display Functions


# Functions to call on script import.
normalize_terminal
handle_args_kwargs ${@}
