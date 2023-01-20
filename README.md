# GoogleCalendarProject

### http://127.0.0.1:8000/rest/v1/calendar/init :  This will start step 1 of the OAuth. Which will prompt user for
his/her credentials.

### http://127.0.0.1:8000/rest/v1/calendar/redirect :
This will do two things

1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar


### Demo Video Url
https://drive.google.com/file/d/1ZSB4LNZWDISUrsgxhrdODMRJbXIFeDxs/view?usp=sharing
