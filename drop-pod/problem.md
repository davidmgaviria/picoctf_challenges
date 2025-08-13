# Drop Pod

- Namespace: picoctf
- ID: drop-pod
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

You'll be dropping into a brand new enviroment -- can you find your way around?

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

## Hints

- Finding a cheatsheet for bash would be really helpful!
- The 'find' command might be useful

## Solution Overview

Login to the remote machine and use `find ./ -name "flag.txt"` to locate the flag. 

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

Usage of ssh and basic bash commands

## Tags

- ssh
- bash
- example

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
