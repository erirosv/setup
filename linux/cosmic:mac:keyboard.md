# COSMIC – Mac Keyboard Symbol Fix

If you are using **COSMIC on CachyOS with Wayland** and most of your Mac keyboard works correctly, but symbols such as:

```text
@  £  $  €  {  [  ]  }  \  <  >
```

do not work correctly, the problem is likely related to the **XKB keyboard layout/variant**.

COSMIC uses **Wayland**, so we should avoid relying on X11-specific tools such as `setxkbmap`.

The goal is to fix the keyboard at the **system/XKB level**.

---

## 1. Check the current keyboard configuration

Run:

```bash
localectl status
```

Then:

```bash
localectl list-x11-keymap-layouts | grep -E 'se|mac'
```

And:

```bash
cat /etc/vconsole.conf
```

Look for something similar to:

```text
X11 Layout: se
```

or a Mac-specific keyboard variant.

---

## 2. Check available Swedish keyboard variants

Run:

```bash
localectl list-x11-keymap-variants se
```

This will show the available variants for the Swedish keyboard layout.

We are particularly interested in whether there is a **Mac/Apple-specific variant**.

---

## 3. Do not change the configuration yet

Do **not** run `localectl set-x11-keymap` until you know which variant is available.

If a suitable Mac variant exists, the command will look something like:

```bash
sudo localectl set-x11-keymap se <variant>
```

Replace:

```text
<variant>
```

with the actual variant shown by:

```bash
localectl list-x11-keymap-variants se
```

After changing the configuration, restart your COSMIC session.

---

## 4. Symbols we want to fix

The goal is to make the following symbols work correctly on the Mac keyboard:

```text
@
£
$
€
{
[
]
}
\
<
>
```

while keeping the rest of the Swedish keyboard layout working correctly.

---

## 5. Send the output

If the correct Mac variant is unclear, send the output from these commands:

```bash
localectl status
```

```bash
localectl list-x11-keymap-layouts | grep -E 'se|mac'
```

```bash
cat /etc/vconsole.conf
```

```bash
localectl list-x11-keymap-variants se
```

From that information, the correct COSMIC/XKB configuration can be determined without changing the existing keyboard configuration blindly.
