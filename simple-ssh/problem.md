# Simple SSH

- Namespace: picoctf
- ID: simple-ssh
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Do you know how to use ssh?  Connect to the remote server and locate the flag!

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

## Hints

- Finding a cheatsheet for bash would be really helpful!

## Solution Overview

Login to the remote machine and use 'ls' to find the flag directory, then cd into it and use 'cat flag.txt' to get the flag. 

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
