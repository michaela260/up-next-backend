# Up Next
##### An iOS app that generates Spotify playlists of songs by artists with upcoming concerts in your city.

Concert lovers are often in search of upcoming shows in their area. They can turn to Spotify to see a list of concerts by artists they follow, but this list does not include artists they don't already know and it is not linked to a playlist. Up Next generates genre-filtered playlists of songs by artists with upcoming concerts in a given city to help users more easily discover new artists and decide which concerts they would be interested in attending.

Up Next was developed as a capstone project for [Ada Developer's Academy](https://adadevelopersacademy.org/), a nonprofit coding bootcamp for women and gender diverse people in Seattle, WA.

## App Features
1.  User can enter their location, a playlist name, and a music genre and get back a Spotify playlist of songs by artists with upcoming concerts in their area
2.  The created playlist is saved to the user's spotify account
    - The playlist includes a top song by each artist in the given genre with an upcoming concert in the user's area

## Technologies
- Back-end:
  - Python Flask API wrapper
- Front-end:
  - Swift (using XCode)
- Infrastructure:
  - The Flask API wrapper is deployed to Heroku
- APIs:
  - Spotify Web API
  - Ticketmaster Discovery API

## Installation
Download this repository and install the following dependencies in a virtualenv.
  - Dependencies:
    - [Python 3.7.6](https://www.python.org/)
    - [Flask 1.1.1](https://github.com/pallets/flask)
    - [Requests 2.22.0](https://requests.readthedocs.io/en/master/)
    - [Python Dotenv 0.10.3](https://pypi.org/project/python-dotenv/)
    - [Cryptography 2.8](https://cryptography.io/en/latest/)
    - [Gunicorn 20.0.4](https://gunicorn.org/)

After installing the dependencies, create a .env file within the project root directory.

You will need to create a Spotify App in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) to receive a Spotify Client ID and Client Secret. Add these to your .env as SPOT_CLIENT_ID and SPOT_CLIENT_SECRET. Additionally, you will need to register for a [Ticketmaster API key](https://developer-acct.ticketmaster.com/user/register). Add the key to your .env as TICKETMASTER_KEY.

Finally, you will need to generate an encryption key with Cryptography and decode the bytes to a string:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
key = key.decode("utf-8")
```
Do not save this key in your project code or commit it to github, instead save it in your project .env file as CRYPT_KEY. This key will be used to encrypt the Spotify Refresh Token before sending it to the application front-end.

In order to access this back-end API wrapper from the front-end of the application, you will need to deploy it to a secure server (https). I used [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) for deployment. After deploying to Heroku, you will need to add your environment variables there as well. See [here](https://devcenter.heroku.com/articles/config-vars) for instructions about adding environment variables to Heroku, and use the same variables that you stored in your .env file.

To run the app itself, download the [front-end repository](https://github.com/michaela260/up-next-frontend) and its dependencies, and build the app on an iPhone 11 or simulator with iOS 13.2+.

## Learning Goals
- Develop an iOS app using Swift and XCode
- Build an API wrapper back-end using Python and Flask
- Implement an authorization flow with OAuth 2 in a mobile application
- Better understand how to integrate external API data into a front-end mobile application