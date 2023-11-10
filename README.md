# gaftecfcblm

github actions free tier exploitation cron for cheap bastards like me

## Configuration

Example `~/.gaftecfcblm.conf` config file.

```conf
[DEFAULT]
touch = README.md

[birthdays]
path = ~/src/birthdays

[blog]
path = ~/src/blog
```

## Installation

Install it as a cron with `crontab -e`

```cron
0 0 * * 0 ~/src/gaftecfcblm/gaftecfcblm.py >> ~/Desktop/cron.log 2>&1
```

Or just use automator and iCal because Apple thinks you are too stupid to use cron.
