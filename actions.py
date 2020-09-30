# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
from rasa_sdk.events import SlotSet


# from langdetect import detect
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# def getLanguage(text):
# print("text "+text)
# if ((detect(text))=="ar"):
#     lang="AR"
# print("detect lang "+lang)
# return lang
# getLanguage("السلام عليكم")

# site take the site variable and return the website or twitter account
def getSite(text):
    if ((text == "website") or (text == "موقع") or (text == "الرابط") or (text == "link")):
        site = "psau.edu.sa"
    elif ((text == "twitter") or (text == "التويتر") or (text == "تويتر") or (text == "بتويتر")):
        site = "https://twitter.com/@itdl_psau"
    else:
        site = "psau.edu.sa"
    return site


class ActionSite(Action):
    def name(self) -> Text:
        return "action_site"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # site= getSite(tracker.latest_message['text'])
        site = getSite(tracker.get_slot("site"))
        dispatcher.utter_message(text=site)
        return []


class ActionSetName(Action):
    def name(self) -> Text:
        return "action_set_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        dispatcher.utter_message(text=("we save your name :{}".format(name)))
        return []


class ActionSetEmail(Action):
    def name(self) -> Text:
        return "action_set_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        emailRegex = re.search('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$', email)

        if emailRegex is None:
            email = None
            dispatcher.utter_message(text="try again !!")

        else:
            email = emailRegex.string
            dispatcher.utter_message(text="we save your email {}".format(email))

        return [SlotSet("email", email)]


class ActionSetPhone(Action):
    def name(self) -> Text:
        return "action_set_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        phone = tracker.get_slot("phone")
        phoneRegex = re.search('^(009665|9665|05|5|\+966)([593076418])([0-9]{7})$', str(phone))
        if phoneRegex is None:
            phone = None
            dispatcher.utter_message(text="try again !!")
        else:
            phone = phoneRegex.string
            dispatcher.utter_message(text="we save your phone {}".format(phone))
        return [SlotSet("phone", phone)]


class ActionSetProblem(Action):
    def name(self) -> Text:
        return "action_set_problem"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        problem = tracker.get_slot("problem")
        dispatcher.utter_message(text="we save your problem : {}".format(problem))

        return []


class ActionGetInformation(Action):
    def name(self) -> Text:
        return "action_get_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        problem = tracker.get_slot("problem")

        dispatcher.utter_message(
            text="the your information is : name {0},phone {1},email {2} ,problem {3}".format(name, phone, email,
                                                                                              problem))
        return []

# class to get the variable from the user
# class ActionGets(Action):
#     def name(self) -> Text:
#         return "action_gets"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         name=tracker.get_slot("name")
#         phone=tracker.get_slot("phone")
#         email=tracker.get_slot("email")
#         problem=tracker.get_slot("problem")
#         dispatcher.utter_message("nice to meet you {},{},{},{}".format(name,phone,email,problem))
#
#         return []


# class ActionGreet(Action):
#     def name(self) -> Text:
#         return "action_greet"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         lang = getLanguage(tracker.latest_message['text'])
#         dispatcher.utter_message(text=lang)
#         return []


############################################################################################################
# class if you want MappingPolicy is running with add triggers in domain.yml=>intents
# class ActionRoboHistory(Action):
#     def name(self):
#         return "action_robo_history"
#     def run(self, dispatcher,tracker,domain):
#         dispatcher.utter_template("utter_bot_history",tracker)
#         return [UserUtteranceReverted()]
############################################################################################################
