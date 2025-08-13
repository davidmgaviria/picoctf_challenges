# API Secrets

- Namespace: picoctf
- ID: api-secrets
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: no
- MaxUsers: 0

## Description
Your boss has told you there is a secret message waiting for you on an API endpoint,
however the API is only accessible from inside the network.  Connect to the remote server
to access the API.


## Details
`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`


## Hints
- The wget command might be useful
- What is base64?


## Solution Overview
Connect to the remote server following the instructions in the details section.
Once on the machine, use 'wget localhost:80/api' to retrieve the base64 encoded flag.
Lastly, use 'base64 -d api' to decode the flag.


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

Utilizing wget and base64

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: ?
