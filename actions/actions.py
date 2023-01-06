# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

import json

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

with open('horoscope_data.json', 'r') as openfile:
    json_object = json.load(openfile)


def map_date_time(s):

    return {
        "今日": "今",
        "今天": "今",
        "明日": "明",
        "明天": "明",
        "这周": "周",
        "本周": "周",
        "本月": "月",
        "这个月": "月",
        "今年": "年",
    }.get(s, "")


def map_horoscope_sign(s):
    return {
        "白羊": "aries",
        "金牛": "taurus",
        "双子": "gemini",
        "巨蟹": "cancer",
        "狮子": "leo",
        "处女": "virgo",
        "天秤": "libra",
        "天蝎": "scorpio",
        "射手": "sagittarius",
        "魔羯": "capricorn",
        "水瓶": "aquarius",
        "双鱼": "pisces"
    }.get(s[:2], "")


class ActionGetHoroscope(Action):

    def name(self) -> Text:
        return "action_get_horoscope"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_time = tracker.get_slot("date_time")
        horoscope_sign = tracker.get_slot("horoscope_sign")

        print(date_time, horoscope_sign)

        dispatcher.utter_message(text=json_object.get(map_horoscope_sign(horoscope_sign), {}).get(map_date_time(date_time), "抱歉，我目前无法找到您的运势"))
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # tell the user they are being passed to a customer service agent
        dispatcher.utter_message(text="我不明白您说的内容，请换个说法。")

        # pause the tracker so that the bot stops responding to user input
        return [UserUtteranceReverted(), ]
