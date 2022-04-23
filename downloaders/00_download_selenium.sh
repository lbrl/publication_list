#!/bin/bash

if ! [[ -d selenium ]]; then
  wget https://files.pythonhosted.org/packages/58/76/705b5c776f783d1ba7c630347463d4ae323282bbd859a8e9420c7ff79581/selenium-4.1.0-py3-none-any.whl
  unzip selenium-4.1.0-py3-none-any.whl
fi

# Get geckodriver from here:
# https://github.com/mozilla/geckodriver/releases
if ! [[ -e geckodriver ]]; then
  wget -O- https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar zxvf -
fi

