import re
import datetime
import parsedatetime
from robobrowser import RoboBrowser

def getAcademicCalendarEvents(url):
    #Initialize ParseDateTime
    cal = parsedatetime.Calendar()
    
    # Initialize robobrowser
    browser = RoboBrowser(history=False)
    browser.open(url)

    event_tags = browser.select("#content-main tr")

    # Dictionary of semesters
    # in the form: {Spring_2015: [<events>], Fall_2014: [<events>]}
    semesters = {}

    # cycle through the event rows, adding them to the event array
    year = None
    season_year = "" # i.e. Spring_2015, to be used as a key for semesters Dict
    for event in event_tags:

            ##### Scraping the web-pages #####

        # Headers in the Schedules are within <th></th>
        if len(event.find_all("th")) > 0:
            # grab the first word of the header (Usually the Season)
            match = re.search(r'(\w+).*(\d\d\d\d)', event.find("th").text)
            season = match.group(1)
            year = match.group(2)
            
            season_year = season + "_" + year
            # Create a new entry in the semester dict
            semesters[season_year] = []
            
        else:
            # Event data is stored in 3 <td> tags:
            #   The first tag is the name of the event
            #   The second is the days of the week of the event (useless)
            #   The third is the Month and date(s) of the event
            event_info = event.find_all("td")
            event_name = event_info[0].text
            messy_event_date = event_info[2].text

                ##### Extracting event info #####
           
            # These dates are pretty messy, so get the important stuff with regex
            match = re.search(r'(\w+)\s(\d+)-*(\d*)(\w*)\s*(\d*)', messy_event_date)
            
            start_date = match.group(1) + " " + match.group(2) # i.e. December 1
            start_date_and_year = match.group(1) + " " + match.group(2) + " " + str(year) # i.e. December 1 2014
            source_date = match.group(1) + " " + str(year) # i.e. December 2014
            
            # Determine End Date based on single or multi-day event
            if len(match.group(3)) > 0:
                # Multi-Day Event
                # i.e. December 13-15
                end_date = match.group(1) + " " + match.group(3)
            elif len(match.group(4)) > 0:
                # i.e. December 13 - January 12
                end_date = match.group(4) + " " + match.group(5)
            else:
                # Single Day Event
                end_date = start_date = start_date_and_year

            date_range_pair = None
            if start_date is end_date:
                # Single Day Event
                # Note that this is repetitive, consider refactoring into above if-else statements
                event_start_date = event_end_date = cal.parseDateText(start_date_and_year)
            else:
                date_range_string = start_date + "-" + end_date
                date_range_pair = cal.evalRanges(date_range_string, cal.parseDateText(source_date))
                event_start_date = date_range_pair[0]
                event_end_date = date_range_pair[1]

            # Grab Year, Month, Day from dates
            event_start_date = [event_start_date[0], event_start_date[1], event_start_date[2]]
            event_end_date = [event_end_date[0], event_end_date[1], event_end_date[2]]
                            
            ##### Convert dates to datetime.date objects #####
        
            # This allows easy addition of days with timedelta (to make sure it works across months)

            start_date = datetime.date(event_start_date[0], event_start_date[1], event_start_date[2])
            end_date = datetime.date(event_end_date[0], event_end_date[1], event_end_date[2]) 

            # Fix off-by-one with multi-day event creation by adding a day to multi-day events
            # i.e. Google Calendar API interprets the end of an event to be the beginning of the
            #      provided end date (12:00a.m.). We want that end date to be included, so add 1 day
            
            if not start_date == end_date:
                end_date += datetime.timedelta(days=1)

            # Format date in Google Calendar API style: YYYY-MM-DD
            # (since these are all all-day events)
            
            start_date = str(start_date.year) + "-" + str(start_date.month).zfill(2) + "-" + str(start_date.day).zfill(2)
            end_date = str(end_date.year) + "-" + str(end_date.month).zfill(2) + "-" + str(end_date.day).zfill(2)

            # Add event to the appropriate semester

            semesters[season_year].append((event_name, start_date, end_date))
    
    return semesters
