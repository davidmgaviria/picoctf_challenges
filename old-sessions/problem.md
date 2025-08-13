# Old Sessions

- Namespace: picoctf
- ID: old-sessions
- Type: custom
- Category: General Skills
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Proper session timeout controls are critical for securing user accounts. If a user logs in on a public or shared computer but doesn’t explicitly log out (instead simply closing the browser tab), and session expiration dates are misconfigured, the session may remain active indefinitely.

This then allows an attacker using the same browser later to access the user’s account without needing credentials, exploiting the fact that sessions never expire and remain authenticated.


## Details

Your friend tells you to check out a new social media platform he built a few years ago.  Although its still under development, he said the site is almost complete. He also mentioned that he hates constantly logging into sites, and so has made his page that 'once you login, you never have to log-out again'!  

Browse {{link_as('/', 'here')}}, and find the flag!


## Hints

- Do you know how to use the web inspector?  
- Where are cookies stored?


## Solution Overview

Create an account to login to the website.  Once logged in, go to /sessions
and copy the admin's session id.  Using the web inspector, go to your storage 
and replace your session id with the admin's.  Go back to the homepage to 
acquire the flag.


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

Teach students about the importance of setting session expirations, and also
how to manipulate one's cookies using the web browser.


## Tags

- OWASP_Top10


## Attributes

- author: David Gaviria
- organization: picoCTF
- event: picoCTF Problem Developer Training
