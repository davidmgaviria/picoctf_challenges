# Fooling the Lockout

- Namespace: picoctf
- ID: fool-the-lockout
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Your friend is building a simple website with a login page.

To stop brute forcing and credential stuffing, they’ve added an IP-based rate limit: exceed the attempt threshold and your IP is blocked for a while. They’re convinced this makes guessing credentials impossible.

To test their defense, they’ve:
- Created a dummy account with a random username–password pair from public credential lists.
- Given you those username and password lists.
- Shared the full source code.

Can you bypass the rate limit, log in, and capture the flag?


## Details

Browse the site {{link_as('/', 'here')}}.

App source code: `{{url_for("app.py", "here")}}`.
Credentials dump `{{url_for("creds-dump.txt", "here")}}`.


## Hints
- The python requests library might be useful


## Solution Overview

Solving this challenge involves sending username - password guesses at a rate lower than the max threshold specified by the app.  This can be done and the flag acquired using the solve.py script in the solve folder.


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

Teach students about rate limiting and have them conduct credential stuffing on an mock website.

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
