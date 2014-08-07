# USC Academic Calendar Web-Scraper
------

As a university student, there are times in the semester where it'd be nice to know when exactly school-wide holidays and events are taking place. As a student at the University of Southern California, I have access to this information through a simple web page on the school's website. 

But while this simple web page helps, it'd be more convenient for this information to be available in the form of a Google Calendar, so that students like myself could store these dates within our personal calendars.

Thus, the creation of this little scraping script. The script makes a Google Calendar for Academic Calendar Years on USC's website. I'm not really sure how useful others will find it, but I figure it can't hurt to share!

## How the heck do you use this?
  
  First off, it's worth noting that I didn't include some important credentials for utilizing the Google Calendar API.
  If you want to try this script for some reason, you'll have to get your own copy of the following:
  
  * [Google Developer API Key](https://developers.google.com/api-client-library/python/guide/aaa_apikeys)
    * [Plug in here](https://github.com/jpugliesi/USC-Academic-Calendar-Scraper/blob/add-files/create_calendar_events.py#L39)   
  * [OAuth2 Web Client ID](https://developers.google.com/accounts/docs/OAuth2#basicsteps)
    * [Plug in here](https://github.com/jpugliesi/USC-Academic-Calendar-Scraper/blob/add-files/create_calendar_events.py#L17)
  * [OAuth2 client secret key](https://developers.google.com/accounts/docs/OAuth2#basicsteps)
    * [Plug in here](https://github.com/jpugliesi/USC-Academic-Calendar-Scraper/blob/add-files/create_calendar_events.py#L18)
  * [A google calendar id (for the calendar the events will be added to)](https://www.drupal.org/node/589310)
    * [Plug in here](https://github.com/jpugliesi/USC-Academic-Calendar-Scraper/blob/add-files/create_calendar_events.py#L48)
  
