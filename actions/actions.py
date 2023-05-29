# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import pandas as pd
import test

df = pd.read_csv("./actions/products.csv", sep='|')
pc = pd.read_csv("./actions/product_color.csv",sep=',')
ps = pd.read_csv("./actions/product_size.csv",sep=',')
ALLOWED_PRODUCT_CATEGORIES = list(df['category'].unique())
ALLOWED_PRODUCT_SIZES = list(pc['color'].unique())
ALLOWED_PRODUCT_COLORS = list(ps['size'].unique())
ALLOWED_PRODUCT_NAMES = list(df['name'].unique())


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
         # Get the value of the `product_category` slot
         product_category = tracker.get_slot('product_category')
        

        # get available colors for the chosen category
        colors=test.get_color_by_category(product_category)
        if slot_value not in colors:
            dispatcher.utter_message(text=f"I don't recognize the color. We serve {', '.join(colors)} in this categoryw.")
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

        # get available sizes for the chosen category

        category = tracker.get_slot("product_category")
        color = tracker.get_slot("product_color")
        size=test.get_size_by_color(color,category)
        data = df[df['category'] == category]
        names = data['name']
        ALLOWED_PRODUCT_NAMES = list(map(str.lower, names))
        

        if slot_value.lower() not in size:
            dispatcher.utter_message(text=f"We have those sizes in the category and the color you choosed: {', '.join(size)}.")
            return {"product_size": None}
        dispatcher.utter_message(text=f"You want to have the {slot_value} size.\nWe have those products in the chosen category : {', '.join(ALLOWED_PRODUCT_NAMES)}.")
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
        color = tracker.get_slot("product_color")
        size=tracker.get_slot("product_size")
        names=test.get_product_name(category, color, size)

        if slot_value.lower() not in names:
            dispatcher.utter_message(text=f"We only have those products in the chosen category , color and size: {', '.join(names)}.")
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

        # get available quantities for the chosen name, color and size
        name = tracker.get_slot("product_name")
        color = tracker.get_slot("product_color")
        size=tracker.get_slot("product_size")
        quantity=test.get_product_quantity_by_size(color, size, name)
        
        if int(slot_value.lower()) < 1 or int(slot_value.lower()) > quantity:
            dispatcher.utter_message(text=f"We only have {quantity} from this products.")
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
    ):
        """Reset `product form` values."""

        slots = ["product_category", "product_color", "product_size", "product_name", "product_quantity"]
        return [SlotSet(slot, None) for slot in slots]