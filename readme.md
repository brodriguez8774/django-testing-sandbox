# Django Test Projects


## Description

Includes basic project setups of each LTS version of Django, starting with Django 2.2.

Each project has minimal adjustments to settings file, essentially using the default settings provided with the given
version of Django.

Each project also has common things set up, such as a view that requires a user login to access, a view that requires
a specific permissions to access, etc.

The goal is to be able to easily/quickly test various common properties of Django projects, across multiple Django
versions.


## Included Django Versions

Currently included in this project are:

| Django Version | Version Notes     | Official Support End |
| -------------- | ----------------- | -------------------- |
| Django v4.1    | See below note    | December 2023        |
| Django v3.2    | LTS               | April 2024           |
| Django v2.2    | LTS (End of Life) | No Longer Supported  |

Version 4.1 currently included because 4.x LTS is not yet out.
Will switch over once v4 LTS is released.
