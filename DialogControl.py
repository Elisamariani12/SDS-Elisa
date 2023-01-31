import intents
from events_data import events_data

global_context_id = "projects/sympatycznyagent-ptvg/agent/sessions/8585a0a9-7949-ea1b-a10d-74b6ef61d44b/contexts/global"


class DialogControl:
    def __init__(self, request):
        intent = request.get('queryResult').get('intent').get('displayName')

        for context in request.get('queryResult').get('outputContexts'):
            if context['name'] == global_context_id:
                parameters = context.get('parameters')

        self.intent = intent
        self.parameters = parameters

        if 'geo-city' in parameters:
            self.city = parameters['geo-city']
        if 'event' in parameters:
            self.event = parameters['event']
        if 'music-artist' in parameters:
            self.artist = parameters['music-artist']

        self.textResponse = ""
        self.followupIntent = None

    def handleChooseCityAndEvent(self,df):
        if self.event in df[(df.city == self.city)].event:
            self.textResponse = "Following events are available: "
            count=0;
            for index,a in df[(df.city == self.city) &(df.event ==self.event)].iterrows():
                self.textResponse += ("Show #"+str(count)+": "+a.shows+", "+a.weekday+" "+a.dates+" "+a.times)
                count=count+1
            self.textResponse += "Which show are you interested in?"
            return
        self.textResponse = "Unfortunately there is no {} in {}. Maybe try with different city?".format(self.event.lower(), self.city)

    def handleNoAvailableEvents(self):
        self.handleChooseCityAndEvent()

    def handleChooseAvailableEvents(self):
        self.textResponse = "Following dates are available: "
        self.textResponse += df[(df.city == self.city) &(df.event ==self.event)&(df.shows==self.artist)].dates.astype(str)

    def getResponse(self):
        response = {
            'fulfillmentText': self.textResponse,
        }

        if self.followupIntent is not None:
            response['followupEventInput'] = {'name': self.followupIntent}

        return response

    def handleRequest(self):
        if self.intent == intents.choose_city_and_event:
            self.handleChooseCityAndEvent()
        if self.intent == intents.no_available_events:
            self.handleNoAvailableEvents()
        if self.intent == intents.choose_available_events:
            self.handleChooseAvailableEvents()
