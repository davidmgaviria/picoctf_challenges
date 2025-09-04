# Directory Travels 3

- Namespace: picoctf
- ID: dir-travels3
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

The third traveling challenge! They say all roads lead to root -- or was it Rome?  Connect to this box and get the flag!

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

## Hints

- The cd and ls manpage might be useful
- Go to root (cd /)
- Use ls -la 

## Solution Overview

Login to the remote machine and do cd /, then use ls -la to see the hidden flag.  Then use cat .flag.txt to get the flag.

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

Usage of cd, ls and related arguments 

## Tags

- bash

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
