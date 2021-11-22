# Not So Bad Nest

A Bad Nest integration, forked from https://github.com/therealryanbonham/badnest,  that uses the web api to work after Works with Nest was shut down (bad Google, go sit in your corner and think about what you did)

## Why is it bad

This isn't an advertised or public API, it's still better than web scraping, but will never be as reliable as the original API

## Features

As of now it only works with Nest Protect

## Drawbacks

- Nest could change their webapp api at any time, making this defunct

## Refresh Token Method
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
11. Paste the whole refresh token you got above in the empty Refresh Token field, leave Issue Token and Cookie empty. Press submit

## Issue Token and Cookie Method
1. You should try the method described above before using this method. The cookie could expire or otherwise be set invalid. You will then have to repeat the steps below to get it working again. Refresh tokens wont expire unless you change your google account password :)
2. Open a Chrome browser tab in Incognito Mode (or clear your cache).
3. Open Developer Tools (View/Developer/Developer Tools).
4. Click on 'Network' tab. Make sure 'Preserve Log' is checked.
5. In the 'Filter' box, enter `issueToken`
6. Go to `home.nest.com`, and click 'Sign in with Google'. Log into your account.
7. One network call (beginning with `iframerpc`) will appear in the Dev Tools window. Click on it.
8. In the Headers tab, under General, copy the entire `Request URL` (beginning with `https://accounts.google.com`, ending with `nest.com`). Put this in the empty Issue Token field
9. In the 'Filter' box, enter `oauth2/iframe`
10. Several network calls will appear in the Dev Tools window. Click on the last `iframe` call.
11. In the Headers tab, under Request Headers, copy the entire `cookie` (beginning `OCAK=...` - **include the whole string which is several lines long and has many field/value pairs** - do not include the `cookie:` name). Put this in the empty Cookie field. Leave Refresh Token empty and press submit

## Disclaimer
I am not a python developer, as one might see from the source code. The integration has been running fine on my instance for many days, but it could break at any time.
Do not use it for any critical process.
