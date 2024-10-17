# tg-assistant
This is a small personal assistant that sends you a message each morning over Telegram.

## Purpose
The weather in Edinburgh is notoriously unpredictable.
Most commercially available weather apps are clunky to use.
I don't want to waste time searching my phone for the right app when I'm in the middle of getting dressed!
They also don't directly tell you the most important fact of the day: when is it going to rain?

Surprisingly, I've found OpenWeatherMap to have very reliable predictions for precipitation.
So, I made this bot that sends me the temperature and predicted hours of rain each morning.

## Usage
Clone the repo, and install the dependencies.
If you use nix, then you can open a shell to install them automatically.
If you don't use nix, good luck.

Create a Telegram bot via @botfather, and paste the token into `.envrc`. Do the same with OWM.
