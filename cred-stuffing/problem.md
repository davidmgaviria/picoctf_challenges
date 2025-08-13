# Credential Stuffing

- Namespace: picoctf
- ID: cred-stuffing
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Credential stuffing is the automated injection of stolen username and password pairs (“credentials”) in to website login forms, in order to fraudulently gain access to user accounts.

Since many users will re-use the same password and username/email, when those credentials are exposed (by a database breach or phishing attack, for example) submitting those sets of stolen credentials into dozens or hundreds of other sites can allow an attacker to compromise those accounts too.


## Details

There was a recent data breach at a famous department store, in which the login credentials of thousands of users were stolen and dumped online.  You're hoping at least one person reused their credentials from the 
department store for an account at a local bank.  Stuff those credentials and get the flag!

Connect to the service with `nc {{server("app")}} {{port("app")}}` 

Download the credentials dump `{{url_for("creds-dump.txt", "here")}}`.


## Hints
- 


## Solution Overview
- Download the `creds-dump.txt` file, then utilize a script to test all the username-password pairs
until you find a valid login.


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

Teach students about credential stuffing and the danger of resuing login credentials.

## Tags

- OWASP_Top10

## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
