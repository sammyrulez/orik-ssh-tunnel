# Orik-SSH

[![Build App Package](https://github.com/sammyrulez/orik-ssh-tunnel/workflows/Build%20App%20Package/badge.svg)](https://github.com/sammyrulez/orik-ssh-tunnel/releases/download/refs%2Fheads%2Fbuild-app/OrikSSH.dmg)


Mac OS SSH tunnel manager UI

Tired of having a hard time remembering what tulle was active and not, what remote service was what, port number binding... I end up building this tool. I hope it helps you as well.

If there is any feature you that would be usefullplease open an issue


## Features

* Read your _~/.ssh/config_ file and build a top bar menu
* Open an ssh tunnel on the selected item
* Preferences and labeling: you can label remote hosts (especially those that do not have DNS or very long hostnames ) with a short name ( ie _"Database"_ ) for each bastion. Preferences are managed with a simple CSV file and you can share it (or portions of it )with your coworkers 
* _"copy url in clipboard"_: if you set in the preferences CVS file the protocol to use on a specific port, the ready to use url will be copied into the clipboard. Supported protocols : _http, https, ssh_. If no protol is specified then _localhost:local_port_number_ format will be used


## Planned Features


* Ask for password and support password protected custom key files
* Preferences GUI

## Installation

You can download the image with the app from the [Releases tab](https://github.com/sammyrulez/orik-ssh-tunnel/releases/download/refs%2Fheads%2Fbuild-app/OrikSSH.dmg)

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




