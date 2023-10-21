# zerotier-info

Command line tool for displaying information about devices on your [ZeroTier One](https://www.zerotier.com/) network.

Mostly useful as a way to find the IP address of peers on your network, without installing a [custom DNS resolver like zeronsd](https://github.com/zerotier/zeronsd).

## Example output

    My Network Name
    
    Name                       IP                Last seen
    ───────────────────────────────────────────────────────────
    Parents-iMac               192.168.192.211   18 seconds ago
    My-MacBook-Pro             192.168.192.140   a minute ago
    DS220plus                  192.168.192.96    a minute ago
    2013-iMac                  192.168.192.131   5 months ago
    DS214se                    192.168.192.85    –
    2015-MacBook-Pro           –                 –

## Requirements

- Python 3
- An admin account on a ZeroTier One network

## Installing locally

Create a [ZeroTier Central API Access Token](https://docs.zerotier.com/central/v1/), then save it (in shell variable declaration format) to a file called `.env`:

    cd ~/path/to/this/repo
    echo 'ZEROTIER_CENTRAL_TOKEN=12345-example-key' > .env

Then run the wrapper script:

    zerotier-info.bash

The wrapper script will check for the presence of a virtualenv, and create one if not present, before then activating the virtualenv, installing dependencies (from `requirements.txt`), and running the Python script.

If you want, you can symlink the wrapper script to somewhere more accessible, eg:

    ln -s ~/path/to/this/repo/zerotier-info.bash ~/bin/zt
