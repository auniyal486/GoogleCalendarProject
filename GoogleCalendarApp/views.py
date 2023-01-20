from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import os
from datetime import datetime


CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), 'client_secret.json')#file that consist of client id and client secret
SCOPES = ['https://www.googleapis.com/auth/calendar'] #oauth2 scope information
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@api_view(['GET'])
def GoogleCalendarInitView(request):

    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES) 

    flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect' #redirection link
    
    authorization_url, state = flow.authorization_url(access_type='offline',prompt='consent',include_granted_scopes='true')

    request.session['state'] = state

    return redirect(authorization_url)

@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    try:
        state = request.session.get('state')
        flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        current_time=datetime.utcnow().isoformat() + 'Z' 
        result = service.events().list(calendarId='primary',singleEvents=True,timeZone='Asia/Kolakata',timeMin=current_time,
        orderBy='startTime').execute()
        events = result.get('items', [])

        if not events:
            return Response({'Message': 'No upcoming events found.'})
        else:
            events_list = []
            for event in events:
                title=None
                if event['summary']!=None:
                    title=event['summary']
                event_dict = {
                    'event_id': event['id'],
                    'title': title,
                    'start_time': event['start'],
                    'end_time': event['end']
                }
                events_list.append(event_dict)

            return Response(events_list)

    except Exception as error:
        return Response({'Message': 'An error occurred: %s' % error})

