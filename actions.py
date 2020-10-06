# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
import re
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from langdetect import detect


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


def getLanguage(text):
    if (detect(text)) == "ar":
        lang = "ar"
    else:
        lang = "en"

    return lang


# site take the site variable and return the website or twitter account
def getsite(text):
    if (text == "website") or (text == "موقع") or (text == "الرابط") or (text == "link"):
        site = "psau.edu.sa"
    elif (text == "twitter") or (text == "التويتر") or (text == "تويتر") or (text == "بتويتر"):
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
        site = getsite(tracker.get_slot("site"))
        dispatcher.utter_message(text=site)
        return []


##################################################################################
# this action for validate the email
# class ActionSetEmail(Action):
#     def name(self) -> Text:
#         return "action_set_email"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         email = tracker.get_slot("email")
#         emailRegex = re.search('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$', email)
#
#         if emailRegex is None:
#             email = None
#             dispatcher.utter_message(text="try again !!")
#
#         else:
#             email = emailRegex.string
#             dispatcher.utter_message(text="we save your email {}".format(email))
#
#         return [SlotSet("email", email)]
##############################################################################################################

########################################################################################################
# this action to validate the phone
# class ActionSetPhone(Action):
#     def name(self) -> Text:
#         return "action_set_phone"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         phone = tracker.get_slot("phone")
#         phoneRegex = re.search('^(009665|9665|05|5|\+966)([593076418])([0-9]{7})$', str(phone))
#         if phoneRegex is None:
#             phone = None
#             dispatcher.utter_message(text="try again !!")
#         else:
#             phone = phoneRegex.string
#             dispatcher.utter_message(text="we save your phone {}".format(phone))
#         return [SlotSet("phone", phone)]
###########################################################################################################


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

# form to collect the all information
def name_test(name):
    if name is None:
        massage = "please, return enter your name!!"
    else:
        massage = "we save your name:{}".format(name)
    return name, massage


def email_test(email):
    emailRegex = re.search('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$', email)

    if emailRegex is None:
        email = None
        massage = "please, return enter your email!!"

    else:
        email = emailRegex.string
        massage = "we save your email:{}".format(email)
    return email, massage


def phone_test(phone):
    phoneRegex = re.search('^(009665|9665|05|5|\+966)([593076418])([0-9]{7})$', str(phone))
    if phoneRegex is None:
        phone = None
        massage = "please, return enter your phone!!"
    else:
        phone = phoneRegex.string
        massage = "we save your phone:{}".format(phone)
    return phone, massage


def problem_test(problem):
    if problem is None:
        massage = "please, return enter your problem!!"
    else:
        massage = "we save your problem:{}".format(problem)
    return problem, massage


class InformationForm(FormAction):
    # return the name
    def name(self) -> Text:
        return "information_form"

    # required slots to fill
    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["name", "email", "phone", "problem"]

    # when find the slots
    def slot_mappings(self) -> Dict[Text, Any]:
        return {"name": self.from_entity(entity="name", intent=["name", "name_Ar"]),
                "email": self.from_entity(entity="email", intent=["your_email", "your_email_Ar"]),
                "phone": self.from_entity(entity="phone", intent=["your_phone", "your_phone_Ar"]),
                "problem": self.from_entity(entity="problem",
                                            intent=["my_problems_technical", "my_problems_technical_Ar"])}

    # action when the all slots fill
    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        problem = tracker.get_slot("problem")
        dispatcher.utter_message(
            text="the your information is : name: {0},phone: {1},email: {2} ,problem: {3}".format(name, phone, email,
                                                                                                  problem))

        return []

    def validate(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)

        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
            if not slot_values:
                raise ActionExecutionRejection(self.name(),
                                               "form,failed to validateSlot {0} with action {1}".format(slot_to_fill,
                                                                                                        self.name()))
        for slot, value in slot_values.items():
            if slot == 'name':
                name, massage = name_test(value)
                if name is None:
                    slot_values[slot] = None
                    dispatcher.utter_message(text=massage)
                else:
                    slot_values[slot] = value
                    dispatcher.utter_message(text=massage)
            elif slot == 'phone':
                phone, massage = phone_test(value)
                if phone is None:
                    slot_values[slot] = None
                    dispatcher.utter_message(text=massage)
                else:
                    slot_values[slot] = phone
                    dispatcher.utter_message(text=massage)
            elif slot == "email":
                email, massage = email_test(value)
                if email is None:
                    slot_values[slot] = None
                    dispatcher.utter_message(text=massage)
                else:
                    slot_values[slot] = email
                    dispatcher.utter_message(text=massage)
            elif slot == "problem":
                problem, massage = problem_test(value)
                if problem is None:
                    slot_values[slot] = None
                    dispatcher.utter_message(text=massage)
                else:
                    slot_values[slot] = problem
                    dispatcher.utter_message(text=massage)
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker,slot):
                dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT,slot)]
        return None
