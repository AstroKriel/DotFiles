# Arch X11 Extras

Optional user-level X11/XFCE configs for the Arch Framework 13 setup.

## Included Configs

| Extra | Target | Purpose | Dependencies |
|---|---|---|---|
| `arch-x11/lightdm-locale.xprofile` | `~/.xprofile` | Sets `LC_TIME=en_GB.UTF-8` for XFCE/LightDM | generated `en_GB.UTF-8` locale |
| `arch-x11/mouse-workspace-buttons.xbindkeysrc` | `~/.xbindkeysrc` | Maps Logitech side buttons to previous/next workspace | `xbindkeys`, `xdotool` |
| `arch-x11/touchpad-workspace-gestures.conf` | `~/.config/libinput-gestures.conf` | Maps three-finger swipes to previous/next workspace | `libinput-gestures`, `xdotool` |
| `arch-x11/xfce-theme-toggle` | `~/.local/bin/xfce-theme-toggle` | Toggles XFCE/GTK between light and dark mode | `xfconf-query`, `gsettings` |
| `arch-x11/xfce-window-behavior.sh` | manual one-time run | Makes activated apps switch to their existing workspace instead of moving to the current one | `xfconf-query`, `xfwm4` |
| `arch-x11/conky/conky.conf` | `~/.config/conky/conky.conf` | Conky system monitor config | `conky` |
| `arch-x11/conky/conky.desktop` | `~/.config/autostart/conky.desktop` | Autostart entry for Conky | `conky` |
| `arch-x11/conky/conky-battery` | `~/.local/bin/conky-battery` | Battery percentage helper for Conky | `conky` |
| `arch-x11/conky/conky-gpu` | `~/.local/bin/conky-gpu` | GPU usage helper for Conky | `conky` |
| `arch-x11/conky/conky-cpu-temp` | `~/.local/bin/conky-cpu-temp` | CPU temperature helper for Conky | `conky` |
| `arch-x11/conky/conky-gpu-temp` | `~/.local/bin/conky-gpu-temp` | GPU temperature helper for Conky | `conky` |
| `arch-x11/window-management/center-window` | `~/.local/bin/center-window` | Centers active window at 70% of monitor | `xdotool` |
| `arch-x11/window-management/tile-window` | `~/.local/bin/tile-window` | Tiles active window left or right at 75% width | `xdotool` |
| `arch-x11/zathura/zathurarc` | `~/.config/zathura/zathurarc` | Zathura PDF viewer config with SyncTeX editor | `zathura`, `zathura-pdf-mupdf` |

## One-Time Setup

Install runtime tools:

```bash
sudo pacman -S xbindkeys xdotool
paru -S libinput-gestures
```

Allow `libinput-gestures` to read touchpad events:

```bash
sudo usermod -aG input $USER
```

Log out or reboot after changing group membership.

Enable touchpad gesture autostart:

```bash
libinput-gestures-setup start autostart
```

Configure XFCE window activation behavior:

```bash
./xfce-window-behavior.sh
```

This sets `/general/activate_action` to `switch`, so clicking a URL opens it
in the browser's existing workspace and moves your view there instead of
pulling the browser window into the current workspace.

Install the theme toggle extra, then run it directly or bind it in XFCE Keyboard settings:

```bash
uv run -m setup_scripts.extras --which arch-x11/xfce-theme-toggle
xfce-theme-toggle
xfce-theme-toggle light
xfce-theme-toggle dark
xfce-theme-toggle status
```

Generate the locale used by `xprofile`:

```bash
sudo sed -i 's/#en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen
sudo locale-gen
```

## More Detail

See the ArchSetup docs:

- `~/Documents/ArchSetup/extras-peripherals.md`
- `~/Documents/ArchSetup/keybindings-session.md`
- `~/Documents/ArchSetup/arch-framework13-install.md`
