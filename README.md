## LinkedIn Mining Application

#####What does it do?
This application, using a cookie with dynamically refreshed values for the leo_auth_token and jsessionid, will mine and persist the data contained in the "Who's Viewed Your Profile" section of your LinkedIn homepage.  For unmasked, publicly identifiable profiles, this data includes the name, the profile url, the job title, location, and region.  In addition to this, it also will note if the profile has either groups or connections in common with you.

For semi-known profiles (IE "Software Engineer from Cyberdyne Corporation"), LinkedIn provides a list of 10 people, one of which viewed your profile.
In this case, the app will crawl all 10 profiles, persisting each one.

As currently written, the data will be saved to a MySQL database, the build scripts for which have been provided as part of this project.

#####Why did you write this application?  Can't LinkedIn provide me the same information?
Currently the LinkedIn free account will provide you the most recent five people who've viewed your profile.  So what this application will provide you is a way to 
start harvesting that data moving forward.  The application runs in approximately 10 seconds from start to finish....I have been running it four times a day via
cron and that seems to be more than adequate for the amount of attention my profile tends receive on a daily basis.

#####Doesn't LinkedIn have an API which can access this data?
As of the writing of this README file in November 2012, to my knowledge, LinkedIn has not opened up this data to be pulled through their API.  My guess is that is
because one of the features they offer in the premium paid account is the full history of everyone who has ever viewed you profile.

#####What applications do I need to run this?

Python

MySQL
http://dev.mysql.com/downloads/

#####How do I refresh the Cookie?
There's a few ways to do it...since I'm running the application on a headless Linux server, my options were fairly limited.  Here was my solution:

1. I extracted the entire contents of my LinkedIn cookie to a file (ulimately this file is referenced in the app.config).  This only needs to be done once.
2. I generate a new jsession_id through wget
3. I generate a new leo_auth_token using lynx.  Essentially i created a login script to LinkedIn and persisted/extracted the value
4. Once I have the two values, I perform a text replace on my cookie with the newly generated values.  This guarantees that I won't ever log in
with stale credentials.  You can take a look in the bash script in my BashScript project.  PLEASE NOTE: The bash script included is for instructional purposes only and 
should be used as a template for how to solve the problem.
