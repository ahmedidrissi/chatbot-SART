# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import pandas as pd

df = pd.read_csv("./actions/products.csv", sep='|')
ALLOWED_PRODUCT_CATEGORIES = list(df['category'].unique())
ALLOWED_PRODUCT_SIZES = ["s", "m", "l", "xl"]
ALLOWED_PRODUCT_COLORS = ["red","black","blue","yellow","white","purple","brown","green","kaki","pink","grey"]
ALLOWED_PRODUCT_NAMES = []

class ValidateProductForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_product_form"

    def validate_product_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_category` value."""

        if slot_value.lower() not in ALLOWED_PRODUCT_CATEGORIES:
            dispatcher.utter_message(text=f"We only accept those categories: {', '.join(ALLOWED_PRODUCT_CATEGORIES)}.")
            return {"product_category": None}
        dispatcher.utter_message(text=f"We have {slot_value}.")
        return {"product_category": slot_value}

    def validate_product_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_color` value."""

        #TODO: get available colors for the chosen category

        if slot_value not in ALLOWED_PRODUCT_COLORS:
            dispatcher.utter_message(text=f"I don't recognize the color. We serve {', '.join(ALLOWED_PRODUCT_COLORS)}.")
            return {"product_color": None}
        dispatcher.utter_message(text=f"You want to have the {slot_value} color.")
        return {"product_color": slot_value}
    
    def validate_product_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_size` value."""

        #TODO: get available sizes for the chosen category

        if slot_value.lower() not in ALLOWED_PRODUCT_SIZES:
            dispatcher.utter_message(text=f"We only accept product sizes: {', '.join(ALLOWED_PRODUCT_SIZES)}.")
            return {"product_size": None}
        dispatcher.utter_message(text=f"You want to have the {slot_value} size.")
        return {"product_size": slot_value}
        
    def validate_product_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_name` value."""

        category = tracker.get_slot("product_category")
        data = df[df['category'] == category]
        names = data['name']
        ALLOWED_PRODUCT_NAMES = list(map(str.lower, names))

        if slot_value.lower() not in ALLOWED_PRODUCT_NAMES:
            dispatcher.utter_message(text=f"We only have those products in the chosen category: {', '.join(ALLOWED_PRODUCT_NAMES)}.")
            return {"product_name": None}
        dispatcher.utter_message(text=f"You choosed {slot_value}.")
        return {"product_name": slot_value}

    def validate_product_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_quantity` value."""

        #TODO: get available quantities for the chosen category
        MIN = 1
        MAX = 20
        if int(slot_value.lower()) < MIN or int(slot_value.lower()) > MAX:
            dispatcher.utter_message(text=f"We only have {MAX} from this products.")
            return {"product_quantity": None}
        dispatcher.utter_message(text=f"OK! You want to have {slot_value} from this product.")
        return {"product_quantity": slot_value}
    
class SubmitProductForm(Action):
    def name(slef):
        return "action_submit_product_form"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Your order has been successfully placed.")
        return []

class ResetProductForm(Action):
    def name(slef):
        return "action_reset_product_form"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        """Reset `product form` values."""

        return [
        {"product_category": None},
        {"product_color": None},
        {"product_size": None},
        {"product_name": None},
        {"product_quantity": None}]