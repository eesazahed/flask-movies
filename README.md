# flask-movies ([View Live](https://flask-movies.eesa.hackclub.app))

A CRUD app made with Flask

Steps to get it on Nest:

- Write a setup.sh script similar to [this](https://github.com/eesazahed/flask-movies/blob/main/setup.sh)
- Get verified on Nest
- SSH into your nest `ssh [USERNAME]@hackclub.app`
- Run `git clone https://github.com/eesazahed/flask-movies.git`
- Find an empty nest port by `nest get_port` and remember what the number is
- Now, run `nano .config/systemd/user/flask-movies.service`
- Write:

```
[Unit]
Description=Flask Movies Service

[Service]
WorkingDirectory=%h/flask-movies
ExecStart=/bin/bash setup.sh [PORT NUMBER]
Restart=on-failure

[Install]
WantedBy=default.target
```

- Run `systemctl --user daemon-reload`
  - If you come across the error message: _"Failed to connect to user scope bus via local transport: $DBUS_SESSION_BUS_ADDRESS and $XDG_RUNTIME_DIR not defined (consider using --machine=<user>@.host --user to connect to bus of other user)"_
  - Try to run `export XDG_RUNTIME_DIR="/run/user/$UID" export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"`
  - Then try again and run `systemctl --user daemon-reload`
- Then, run `systemctl --user enable --now flask-movies.service`
- Now run `nest caddy add flask-movies.[USERNAME].hackclub.app`
- Edit your Caddyfile by going into `nano Caddyfile`
- Add this to the bottom of the file:

```
http://flask-movies.[USERNAME].hackclub.app {
        bind unix//home/[USERNAME]/.flask-movies.[USERNAME].hackclub.app.webserver.sock|777
        reverse_proxy :[PORT NUMBER]
}
```

- Exit and save
- Reload Caddy with `systemctl --user reload caddy`
- Head over to https://flask-movies.[USERNAME].hackclub.app and check out the site!
- If you ever want to update your code push it to your GitHub repository for the project. Then run `systemctl --user restart flask-movies.service` and wait a minute or two
