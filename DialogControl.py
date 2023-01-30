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

    def handleChooseCityAndEvent(self):
        if self.city in events_data:
            if self.event in events_data[self.city]:
                self.textResponse = "Following events are available: "
                for event in events_data[self.city][self.event]:
                    self.textResponse += str(event) + " "
                self.textResponse += "Which show are you interested in?"
                return
        self.textResponse = "Unfortunately there is no {} in {}. Maybe try with different city?".format(self.event.lower(), self.city)

    def handleNoAvailableEvents(self):
        self.handleChooseCityAndEvent()

    def handleChooseAvailableEvents(self):
        self.textResponse = "Following dates are available: "
        for date in events_data[self.city][self.event][self.artist]:
            self.textResponse += str(date)

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
