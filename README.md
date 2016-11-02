# gwapit-technical-test

Technical test for Gwapit. 

That simple Django and Angular web application allow a user to register using the google API and to fetch his last 100 emails from Gmail.

You can deploy the application using docker:

```
docker-compose up
```

The application is now available on:

```
http://127.0.0.1:8040/
```

Now, click on login button to register through Gmail and display your emails!

* Please note that the application should run on port number 8040 to handle Google API callbacks.
