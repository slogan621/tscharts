tscharts service

login
   post
/tscharts/v1/login/
   {"username":username, "password":password}
   returns token and id of user
   use the token as a header in all subsequent requests as in this example:

Authorization: Token b4e9102f85686fda0239562e4c8f7d3773438dae 

logout
   post
/tscharts/v1/logout/
