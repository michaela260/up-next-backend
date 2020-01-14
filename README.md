# Product Plan - Michaela Morrow
# Project Name: Up Next

## Learning Goals
- Learn how to develop an iOS app using Swift
- Learn how to build an API wrapper backend using Python and Flask
- Better understand how to integrate external API data into a frontend mobile application

## Problem Statement

Live-music lovers are often in search of upcoming concerts in their area. Although they could turn to Spotify to see a list of concerts by artists they follow, this list does not include artists that they don't already know. Furthermore, this list of concerts is not linked to a playlist of the artists' songs. Users would benefit from a playlist of songs by artists with upcoming concerts in their area so that they could more easily decide which concerts they would be interested in attending. My app will help users discover new artists and concerts in a fast and easy manner.

## Market Research

- Competitor apps:
    - Next Week's Playlist
      - https://www.nextweeksplaylist.com/
      - This is a web application that generates a playlist based on upcoming concerts in your city. It lets you filter by music venue and genre. It is fairly similar to what I want to build, but its limitation is that it only includes shows for the upcoming week, rather than a longer timeframe. Also, it is a website rather than mobile app (I plan to build for mobile).
    - Setify
      - This is a web app that generates playlists based on the recent setlists of specific artists. It is different from what I want to create, because it does not generate a multi-artist playlist, and it does not find which artists are coming to your city.
    - Funkavinci (no longer supported)
      - https://www.freecodecamp.org/news/the-machine-made-playlist-faec2c8bc7ba/
      - This was a project where people signed up to receive a weekly playlist of songs by artists with upcoming concerts in San Francisco. It was limited to only San Francisco, and the creator curated the songs herself rather tha automatically generating them. The project is no longer running.
    - Music Tonight (deprecated)
      - https://developer.spotify.com/community/showcase/music-tonight/
      - This was an app and website that made playlists of songs by artists with shows near you tonight. The app is different from mine because it only included shows on the same night that the request was made. Also, this app seems to be deprecated - the website brings up an error message, and the app is not currently available in the app store.

- My product is different because...
  - I have not found any competitors that are exactly the same as my application. Next Week's Playlist is the most similar app I have found, but it is limited to only a week's worth of data and it is not a mobile application.

## Target Audience

My app targets concert-goers who are characterized by their love of music and desire to discover new artists and events. It also targets anyone hoping to find upcoming events that they will enjoy in their city.

## Technologies

- Back-end Technology:
  - Python Flask API wrapper that will make calls to the Spotify and Ticketmaster APIs
- Front-end Technology
  - Swift (using XCode)
- Infrastructure
  - The Flask API wrapper will be deployed to Heroku
  - The iOS app will be downloaded onto my iPhone
- APIs:
  - Spotify Web API
  - Ticketmaster Discovery API

## Wireframes

  - Homepage: https://wireframe.cc/aqdu7v

## MVP Feature Set

1.  User can enter their location and get back a playlist of songs by artists with upcoming concerts in their area
    - This will either be manually entered location or automatic
    - User might be able to select distance away and timeframe...or these might just be the same for all users
2.  The created playlist will be saved to the user's spotify account
    - The playlist will include a top song by artists with upcoming concerts in the user's area