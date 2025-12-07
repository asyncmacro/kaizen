
Obsidian displays the error `unrecognized protocol SSH` which means the ssh protocol is not supported by android natively.

For that, we have to use Termux and set it up for automatic git syncing.

First, we need to install needed packages:

```bash
pkg upgrade
pkg install cronie termux-services openssh git

### restart Termux, then issue:
sv-enable crond
```

