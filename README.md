# C2 sync ignores
 Python tool to sync the "ignores" block of two Chatterino2 profiles. It 
 should work with Chatterino2 forks (Chatterino7, homies etc)
 
## Requirements
You need base Python3. No extra deps.

Linux, BSD users: grab it from your package repository. Chances that its installed already.

Windows users grab it from [Python.org](https://www.python.org/downloads/)

## Usage
```
python3 sync_c2_ignores.py source_c2_profile_directory/Settings/settings.json target_c2_profile_directory/Settings/settings.json
```
Optional parameters
* --assume-yes or -y : assume replying yes to questions (see below)
* --assume-no or -n : assume replying N OMEGALUL to questions

## Checks
* source must be readable
* target must exist and be writeable
* the program will create a backup of the target. It will ask you what to do if the backup already exists or cannot be created

# License
All the code are purely AI generated, therefore ineligible for copyright and
is in the public domain. No warranty of any kind.

Just DO WHAT THE FUCK YOU WANT TO.

