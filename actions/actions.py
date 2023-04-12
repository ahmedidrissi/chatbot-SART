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

ALLOWED_PRODUCT_NAMES = ["jeans", "coats", "jackets", "shirts", "pants"]
ALLOWED_PRODUCT_CATEGORIES = ["jeans", "coats", "jackets", "shirts", "pants"]
ALLOWED_PRODUCT_SIZES=["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PRODUCT_COLOR=["red","black","blue","yello","white","purple","brown","green","kaki","pink","grey"]
df = pd.read_csv("./actions/products.csv", sep='|')

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
            dispatcher.utter_message(text=f"We only accept those categories: {'/'.join(ALLOWED_PRODUCT_CATEGORIES)}.")
            return {"product_category": None}
        dispatcher.utter_message(text=f"OK! You choosed {slot_value}.")
        return {"product_category": slot_value}

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
        dispatcher.utter_message(text=f"OK! You want to have the {slot_value} color.")
        return {"product_color": slot_value}
    
    def validate_product_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_size` value."""

        if slot_value.lower() not in ALLOWED_PRODUCT_SIZES:
            dispatcher.utter_message(text=f"We only accept product sizes: {'/'.join(ALLOWED_PRODUCT_SIZES)}.")
            return {"product_size": None}
        dispatcher.utter_message(text=f"OK! You want to have the {slot_value} size.")
        return {"product_size": slot_value}
        
    def validate_product_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_name` value."""

        if slot_value.lower() not in ALLOWED_PRODUCT_CATEGORIES:
            dispatcher.utter_message(text=f"We only have those products in the choosen category: {'/'.join(ALLOWED_PRODUCT_NAMES)}.")
            return {"product_name": None}
        dispatcher.utter_message(text=f"OK! You choosed {slot_value}.")
        return {"product_name": slot_value}

    def validate_product_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_quantity` value."""
        MIN = 1
        MAX = 20
        if int(slot_value.lower()) < MIN or int(slot_value.lower()) > MAX:
            dispatcher.utter_message(text=f"We only have {MAX} from this products.")
            return {"product_quantity": None}
        dispatcher.utter_message(text=f"OK! You want to have {slot_value} from this product.")
        return {"product_quantity": slot_value}
    
