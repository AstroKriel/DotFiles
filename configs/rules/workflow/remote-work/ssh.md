# SSH

Key pair management, config file conventions, and agent forwarding.

---

## Key Pairs

Create one key per connection from each owned device. Do not reuse keys across connections or devices.

```bash
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519_<name> -C "for <purpose> from <device> created on <YYYY-MM-DD>"
```

`<name>` identifies the connection (e.g. `github`, `roundtable`). The comment captures what the key is for, which device it came from, and when; this makes `authorized_keys` entries self-describing and revocation surgical: removing access to one service leaves all others intact.

---

## SSH Config

All connections are configured in `~/.ssh/config`. Do not pass connection flags on the command line when they belong in config.

Entry pattern:

```
Host <alias>
    HostName <hostname>
    User <username>
    IdentityFile ~/.ssh/id_ed25519_<name>
    IdentitiesOnly yes
```

`IdentitiesOnly yes` prevents SSH from offering other keys to the server. This matters on clusters that lock accounts after a small number of failed authentication attempts.

Use short aliases that match the name used elsewhere: cluster notes, job scripts, rsync commands.

---

## Agent Forwarding

Enable agent forwarding only on hosts that need it (typically a login node that must authenticate to a downstream service). Add it per host, not globally.

```
Host <login-node>
    HostName <hostname>
    User <username>
    IdentityFile ~/.ssh/id_ed25519_<name>
    IdentitiesOnly yes
    ForwardAgent yes
```

---

## Key Records

After creating a key, save a record containing the public key, the `ssh-keygen` command used, and the `~/.ssh/config` block for that connection. Store records in the machine setup repo. These are the reference when auditing which services a device has access to.
