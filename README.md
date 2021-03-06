# Orik-SSH

[![Build App Package](https://github.com/sammyrulez/orik-ssh-tunnel/workflows/Build%20App%20Package/badge.svg)](https://github.com/sammyrulez/orik-ssh-tunnel/releases/download/v0.5.1/OrikSSH.dmg)  <img src="https://github.com/sammyrulez/orik-ssh-tunnel/raw/main/screenshot.png " height="24"> 
<p align="center">
  <img src="https://github.com/sammyrulez/orik-ssh-tunnel/raw/main/dwarf-helmet.png" width="400">
  </p>

Mac OS SSH tunnel manager UI

Tired of having a hard time remembering what tulle was active and not, what remote service was what, port number binding... I end up building this tool. I hope it helps you as well.

If there is any feature you that would be usefullplease open an issue


## Features

* Read your _~/.ssh/config_ file and build a top bar menu

* Open a ssh tunnel on the selected item
* Preferences and labeling: you can label remote hosts (ecpetialy those that do not have dns or very long host names ) with a short name ( ie _"Database"_ ) for each bastion. Preferences are managed with a simple CSV file and you can share it (or portions of it )with your coworkers 
* _"copy url in clipboard"_



## Planned Features


* Ask for password and support password protected custom key files
* Preferences GUI


## Installation

You can download the image with the app from the [Releases tab](https://github.com/sammyrulez/orik-ssh-tunnel/releases/download/v0.5.1/OrikSSH.dmg)

Orik is currently not code-signed for macOS. See the last section of [This page ]https://support.apple.com/en-us/HT202491) for instructions on allowing Orik to run anyway.


## Build from sources:

```
git clone https://github.com/sammyrulez/orik-ssh-tunnel.git
cd orik-ssh-tunnel
```

The creation of a virtual env is recommended

```
pip install py2app
pip install -r requirements.txt
python setup.py py2app --iconfile dwarf-helmet.icns
```

The app build is in `dist/orik_ssh.app`

## Configuration

The configuration file is located in your home directory: `/Users/[username/].orik_ssh/config.csv` . If you have a `.ssh/config` the  csv file  it is automaticaly created when you run Orik for the first time. The schema is the following

```
Bastion,Host Name,User,Remote Host,Remote Port,Local Port,Alias,Protocol,Ask for password,Custom cert
```

* Bastion
* Host Name
* User
* Remote Host
* Remote Port
* Local Port
* Alias label for the tunnel/remote host
* Protocol supported for url creation http, https, ssh
* Ask for password
* Custom cert



## Todos

- [ ] More unit tests
- [x] Proper logging
- [x] Issue template
- [x] Github actions
- [x] Publish app package
- [ ] Add  coverage badge
- [ ] Add  version badge
- [ ] Embed python3 runtime
- [x] build a website
- [ ] Close all tunnels on quit
- [ ] Find meaning full label for_"Copy url"_



## Where the name Orik came from?

Orik is the name of my son's D&D player. He is a Storm Cleric Dwarf. Sentinel of the tunnels  .




