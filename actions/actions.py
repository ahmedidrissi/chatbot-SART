# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pandas as pd

ALLOWED_PRODUCT_SIZES=["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PRODUCT_COLOR=["red","black","blue","yello","white","purple","brown","green","kaki","pink","grey"]
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


class ValidateProductForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_product_form"

    def validate_product_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_size` value."""

        if slot_value.lower() not in ALLOWED_PRODUCT_SIZES:
            dispatcher.utter_message(text=f"We only accept product sizes: s/m/l/xl.")
            return {"product_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} in the product.")
        return {"product_size": slot_value}

    def validate_product_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_color` value."""

        if slot_value not in ALLOWED_PRODUCT_COLOR:
            dispatcher.utter_message(text=f"I don't recognize the color. We serve {'/'.join(ALLOWED_PRODUCT_COLOR)}.")
            return {"product_color": None}
        dispatcher.utter_message(text=f"OK! You want to have the color {slot_value} in the product.")
        return {"product_color": slot_value}
    
    def validate_product_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_quantity` value."""
        dispatcher.utter_message(text=f"OK! You want to have the color {slot_value} in the product.")
        return {"product_quantity": slot_value}
    
