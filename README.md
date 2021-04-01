# FriendFinder

FriendFinder helps you search for pets available for adoption through PetFinder's API. 


## Prerequisites 

In order to use the PetFinder API, you will need to register for an account [PetFinder API][https://www.petfinder.com/developers/v2/docs/]

Follow the instructions to obtain an access token. 
Access tokens are only available for 1 hour. 


## Installation 

* Flask
* Flask-SQLAlchemy
* ipython
* petpy
* SQLAlchemy
* WTForms

## Features

Features of this app include a user registering, logging in and logging out of the app, viewing random pets 
from the PetFinder API, viewing pet's description and adoption organization details, and searching for pets based on the following criteria: species, age, color, size, gender.

## User Flow

A user can either register, or login if they already have an account. Once logged in, they will be taken to 
the homepage which shows a list of 20 random pets available for adoption. Each pet card has a button named 
'About me!". When clicked, the user will be redirected to a page with a description of the pet. The user will 
be presented with a second button named "Adopt me!" This button will redirect the user to view the adoption organizations' contact info. The user has the option to go back to a list of 20 random pets, or to search based on certain criteria: species, age, color, size, gender. 

## Technology stack 

* Bootstrap
* Python 
* MySQL

## Deployment

https://git.heroku.com/petfinder-capstone.git


