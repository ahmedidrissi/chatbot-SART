# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import pandas as pd
from actions import SGBD

sgbd = SGBD.mySGBD()

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

        if slot_value.lower() not in sgbd.allowed_categories:
            dispatcher.utter_message(text=f"We only accept those categories: {', '.join(sgbd.allowed_categories)}.")
            return {"product_category": None}
        dispatcher.utter_message(text=f"We have in {slot_value} category those colors: {', '.join(sgbd.get_colors_by_category(slot_value))}.")
        return {"product_category": slot_value}

    def validate_product_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_color` value."""
        
        if slot_value not in sgbd.allowed_colors:
            dispatcher.utter_message(text=f"I don't recognize the color. We serve {', '.join(sgbd.allowed_colors)} in this category.")
            return {"product_color": None}
        dispatcher.utter_message(text=f"You want to have the {slot_value} color. We have those sizes: {', '.join(sgbd.get_sizes_by_color(slot_value))}")
        return {"product_color": slot_value}
    
    def validate_product_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_size` value."""

        if slot_value.lower() not in sgbd.allowed_sizes:
            dispatcher.utter_message(text=f"We only have thoses sizes: {', '.join(sgbd.allowed_sizes)}.")
            return {"product_size": None}
        dispatcher.utter_message(text=f"You want to have the {slot_value} size. We have those products in stock: {', '.join(sgbd.get_product_name_by_size(slot_value))}.")
        return {"product_size": slot_value}
        
    def validate_product_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_name` value."""

        if slot_value.lower() not in sgbd.allowed_products:
            dispatcher.utter_message(text=f"We only have those products in stock: {', '.join(sgbd.allowed_products)}.")
            return {"product_name": None}
        dispatcher.utter_message(text=f"We have {sgbd.get_product_quantity_by_size()} from {slot_value}")
        return {"product_name": slot_value}

    def validate_product_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `product_quantity` value."""
        
        if int(slot_value.lower()) < 1 or int(slot_value.lower()) > sgbd.allowed_quantity:
            dispatcher.utter_message(text=f"We only have {sgbd.allowed_quantity} from this products.")
            return {"product_quantity": None}
        dispatcher.utter_message(text=f"OK! You want to have {slot_value} from this product.")
        return {"product_quantity": slot_value}
    
class SubmitProductForm(Action):
    def name(self) -> Text:
        return "action_submit_product_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        """Submit the order and update the quantity of the ordered product."""
        # submit the order

        product_name = tracker.get_slot("product_name")
        color = tracker.get_slot("product_color")
        size = tracker.get_slot("product_size")
        ordered_quantity = tracker.get_slot("product_quantity")
        sgbd.update_quantity(product_name, color, size, ordered_quantity)
        dispatcher.utter_message(text="Your order has been successfully placed.")
        return []

class ResetProductForm(Action):
    def name(slef):
        return "action_reset_product_form"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ):
        """Reset `product form` values."""

        slots = ["product_category", "product_color", "product_size", "product_name", "product_quantity"]
        return [SlotSet(slot, None) for slot in slots]