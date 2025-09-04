# Tabbing About

- Namespace: picoctf
- ID: tabbing-about
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Have you heard of tab auto-complete?  It can be a useful tool!  Connect to this box and get the flag!

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

## Hints

- Search up what 'tab auto-complete' is

## Solution Overview

Login to the remote machine and use 'tab auto-complete' to enter the filenames of the corrupted flag files.  Get the two parts of the flag and put them together to win.

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Learning Objective

Usage of tab auto-complete

## Tags

- bash

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
