# Not So Bad Nest

A Bad Nest integration, forked from https://github.com/therealryanbonham/badnest,  that uses the web api to work after Works with Nest was shut down (bad Google, go sit in your corner and think about what you did)

## Why is it bad

This isn't an advertised or public API, it's still better than web scraping, but will never be as reliable as the original API

## Features

As of now it only works with Nest Protect

## Drawbacks

- Nest could change their webapp api at any time, making this defunct

## Setup
Grab a refresh token using https://github.com/chrisjshull/homebridge-nest#using-a-google-account---refresh-token-method.
Open the integrations tab on your HA instance and search for Not So Bad Nest.
Paste the whole refresh token you got above in the empty field and press ok.

## Disclaimer
I am not a python developer, as one might see from the source code. The integration has been running fine on my instance for many days, but it could break at any time.
Do not use it for any critical process.
