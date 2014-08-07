from event_scraper import getAcademicCalendarEvents

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0
# PLUG IN YOUR CLIENT_ID AND CLIENT_SECRET KEY HERE
FLOW = OAuth2WebServerFlow(
    client_id='', # Throw in that OAuth Web Client ID
    client_secret='', # and that client secret key
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='usc_academic_calendar')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. 
service = build(serviceName='calendar', version='v3', http=http,
        developerKey='') # Plug in the developer api key here!

#### Creating the Events ####


# Set up array of years (where year starts in Fall) to obtain
years = [13, 14, 15]

# USC Google Calendar ID 
calendar_id = '' # Plug in your google calendar's id here!

#Browse to USC Calendar Websites
for year in years:
    
    semesters = getAcademicCalendarEvents("http://academics.usc.edu/calendar/20{0}-20{1}/".format(year, year+1))

    for semester in semesters:
        for event_info in semesters[semester]:
            # Events look like:
            # (u'Winter Recess', "2015-12-17", "2016-1-10")
            
            # Event JSON-like object
            event = {
                'summary': event_info[0],
                'start': {
                    'date': event_info[1]
                },
                'end': {
                    'date': event_info[2]
                },
            }

            # create the event via Google Calendar API
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

            print created_event['id'], created_event['summary']
