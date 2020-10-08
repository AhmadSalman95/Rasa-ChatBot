from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
import re
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from langdetect import detect
# this package helpful to sends emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# site take the site variable and return the website or twitter account
def getsite(text):
    if (text == "website") or (text == "موقع") or (text == "الرابط") or (text == "link"):
        site = "psau.edu.sa"
    elif (text == "twitter") or (text == "التويتر") or (text == "تويتر") or (text == "بتويتر"):
        site = "https://twitter.com/@itdl_psau"
    else:
        site = "psau.edu.sa"
    return site


# this class detect the languge(ar or en) from the first massage from the user and put in lang slot
class ActionDetectLang(Action):
    def name(self) -> Text:
        return "action_detect_lang"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        massage = tracker.latest_message.get('text')
        if (detect(massage)) == "ar":
            lan = "ar"
        else:
            lan = "en"

        return [SlotSet("lang", lan)]


# this class to detect any site the customer need
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

# this function to check the name
def name_test(name):
    if name is None:
        massage = "please, return enter your name!!"
    else:
        massage = "we save your name:{}".format(name)
    return name, massage


# this function to check the email
def email_test(email):
    emailRegex = re.search('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$', email)

    if emailRegex is None:
        email = None
        massage = "please, return enter your email!!"

    else:
        email = emailRegex.string
        massage = "we save your email:{}".format(email)
    return email, massage


# this function to check the phone
def phone_test(phone):
    phoneRegex = re.search('^(009665|9665|05|5|\+966)([593076418])([0-9]{7})$', str(phone))
    if phoneRegex is None:
        phone = None
        massage = "please, return enter your phone!!"
    else:
        phone = phoneRegex.string
        massage = "we save your phone:{}".format(phone)
    return phone, massage


# this function to check the problem
def problem_test(problem):
    if problem is None:
        massage = "please, return enter your problem!!"
    else:
        massage = "we save your problem:{}".format(problem)
    return problem, massage


def send_email(massage):
    my_address = ''
    password = ''
    user_email = ''
    # this smtp for outlook
    # s=smtplib.SMTP(host='smtp-mail.outlook.com',port=587)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(my_address, password)
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = user_email
    msg['Subject'] = "test chatbot"
    msg.attach(MIMEText(massage, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()


# this class to collect the information of user (name,phone,email,problem)
# the response language detect from lang slot
class InformationForm(FormAction):
    # return the name
    def name(self) -> Text:
        return "information_form"

    # required slots to fill
    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["name", "email", "phone", "problem"]

    # where find the required slots
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
        massage = " name : {0}\n email : {1}\n phone : {2}\n the problem description : {3}".format(name, email, phone,
                                                                                                   problem)

        dispatcher.utter_message(text=massage)
        send_email(massage)

        return []

    # this function to validate the request slot
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

    # this function to ask the user fill the request slot
    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        lang = tracker.get_slot("lang")
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if lang == "ar":
                    dispatcher.utter_message(template=f"utter_ask_{slot}_Ar", **tracker.slots)
                else:
                    dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)

                return [SlotSet(REQUESTED_SLOT, slot)]
        return None
