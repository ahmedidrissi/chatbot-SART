# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd

df = pd.read_csv("./actions/products.csv", sep='|')

class ActionCheckStock(Action):

    def name(self) -> Text:
        return "action_check_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_category = next(tracker.get_latest_entity_values("product_category"), None)

        if not product_category:
            dispatcher.utter_message(text="Sorry, I didn't understand. Can you specify the category please?")
            return []
        data = df[df['category'] == product_category]
        products = list(data['name'])

        if len(products) == 0:
            dispatcher.utter_message(text=f"Sorry, but the category {product_category} doesn't exist :(")
            return []

        dispatcher.utter_message(text=f"We have : {products}")
        return []
