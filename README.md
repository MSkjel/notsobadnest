# Not So Bad Nest

A Bad Nest integration, forked from https://github.com/therealryanbonham/badnest,  that uses the web api to work after Works with Nest was shut down (bad Google, go sit in your corner and think about what you did)

## Why is it bad

This isn't an advertised or public API, it's still better than web scraping, but will never be as reliable as the original API

## Features

As of now it only works with Nest Protect

## Drawbacks

- Nest could change their webapp api at any time, making this defunct

## Setup Node.JS And Grab Refresh Token
1. Download and install Node.JS https://nodejs.org/en/download/
2. Restart the computer. Important, or you are going to get npm is not recognized as an internal or an external command operable program errors
3. Download the whole homebridge-nest repository https://codeload.github.com/chrisjshull/homebridge-nest/zip/refs/heads/master
4. Extract the folder from the .zip file
5. Navigate to the folder where login.js is located
6. Shift + Right click in the folder and click Open PowerShell window here
7. Paste `npm install readline; npm install querystring; npm install axios` in the PowerShell window and press enter
8. Paste `node login.js` in the PowerShell window and follow the script's instructions carefully
9. Add this repository to your HACS custom repositories.
10. Open the integrations tab on your HA instance and search for Not So Bad Nest.
11. Paste the whole refresh token you got above in the empty field and press ok.

## Disclaimer
I am not a python developer, as one might see from the source code. The integration has been running fine on my instance for many days, but it could break at any time.
Do not use it for any critical process.
