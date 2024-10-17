# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    requests
    APScheduler
    cachetools
    python-telegram-bot
    pytz
    more-itertools
  ];
  my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
