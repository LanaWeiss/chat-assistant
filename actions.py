from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo

# Replace with your MongoDB connection details
client = pymongo.MongoClient("mongodblink")
db = client["purchase_history"]
collection = db["purchases"]

class ActionGetTotalSpent(Action):

    def name(self) -> Text:
        return "action_get_total_spent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        time_range = tracker.get_slot("time_range")

        query = {"Supplier Name": provider}
        if time_range:
            query["Fiscal Year"] = {"$regex": time_range}

        try:
            total_spent = sum([doc["Total Price"] for doc in collection.find(query) if "Total Price" in doc])
            dispatcher.utter_message(template="utter_total_spent", total_spent=total_spent, provider=provider, time_range=time_range)
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch purchase details (item name)
class ActionGetPurchaseDetails(Action):

    def name(self) -> Text:
        return "action_get_purchase_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        time_range = tracker.get_slot("time_range")

        query = {"Supplier Name": provider}
        if time_range:
            query["Fiscal Year"] = {"$regex": time_range}

        try:
            items = [doc["Item Name"] for doc in collection.find(query) if "Item Name" in doc]
            if items:
                dispatcher.utter_message(template="utter_purchase_details", items=", ".join(items), provider=provider, time_range=time_range)
            else:
                dispatcher.utter_message(text=f"No purchases found for {provider} in {time_range}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while fetching the purchase details: {str(e)}")

        return []

# Action to fetch creation date
class ActionGetCreationDate(Action):

    def name(self) -> Text:
        return "action_get_creation_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            creation_date = collection.find_one(query).get("Creation Date", "N/A")
            dispatcher.utter_message(text=f"The creation date for {provider} is {creation_date}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch fiscal year
class ActionGetFiscalYear(Action):

    def name(self) -> Text:
        return "action_get_fiscal_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            fiscal_year = collection.find_one(query).get("Fiscal Year", "N/A")
            dispatcher.utter_message(text=f"The fiscal year for {provider} is {fiscal_year}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch unit price
class ActionGetUnitPrice(Action):

    def name(self) -> Text:
        return "action_get_unit_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            unit_price = collection.find_one(query).get("Unit Price", "N/A")
            dispatcher.utter_message(text=f"The unit price for {provider} is {unit_price}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch supplier name
class ActionGetSupplierName(Action):

    def name(self) -> Text:
        return "action_get_supplier_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        supplier_code = tracker.get_slot("supplier_code")
        query = {"Supplier Code": supplier_code}

        try:
            supplier_name = collection.find_one(query).get("Supplier Name", "N/A")
            dispatcher.utter_message(text=f"The supplier name for the code {supplier_code} is {supplier_name}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch classification codes
class ActionGetClassificationCodes(Action):

    def name(self) -> Text:
        return "action_get_classification_codes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            classification_codes = collection.find_one(query).get("Classification Codes", "N/A")
            dispatcher.utter_message(text=f"The classification codes for {provider} are {classification_codes}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch normalized UNSPSC
class ActionGetNormalizedUNSPSC(Action):

    def name(self) -> Text:
        return "action_get_normalized_unspsc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            unspsc = collection.find_one(query).get("Normalized UNSPSC", "N/A")
            dispatcher.utter_message(text=f"The normalized UNSPSC for {provider} is {unspsc}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []

# Action to fetch location
class ActionGetLocation(Action):

    def name(self) -> Text:
        return "action_get_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        provider = tracker.get_slot("provider")
        query = {"Supplier Name": provider}

        try:
            location = collection.find_one(query).get("Location", "N/A")
            dispatcher.utter_message(text=f"The location for {provider} is {location}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []


# class ActionGetTotalSpent(Action):

#     def name(self) -> Text:
#         return "action_get_total_spent"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         time_range = tracker.get_slot("time_range")

#         query = {"Supplier Name": provider}
#         if time_range:
#             query["Fiscal Year"] = {"$regex": time_range}

#         try:
#             total_spent = sum([doc["Total Price"] for doc in collection.find(query) if "Total Price" in doc])
#             dispatcher.utter_message(template="utter_total_spent", total_spent=total_spent, provider=provider, time_range=time_range)
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetPurchaseDetails(Action):

#     def name(self) -> Text:
#         return "action_get_purchase_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         time_range = tracker.get_slot("time_range")

#         query = {"Supplier Name": provider}
#         if time_range:
#             query["Fiscal Year"] = {"$regex": time_range}

#         try:
#             items = [doc["Item Name"] for doc in collection.find(query) if "Item Name" in doc]
#             if items:
#                 dispatcher.utter_message(template="utter_purchase_details", items=", ".join(items), provider=provider, time_range=time_range)
#             else:
#                 dispatcher.utter_message(text=f"No purchases found for {provider} in {time_range}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred while fetching the purchase details: {str(e)}")

#         return []


# class ActionGetCreationDate(Action):

#     def name(self) -> Text:
#         return "action_get_creation_date"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             creation_date = collection.find_one(query).get("Creation Date", "N/A")
#             dispatcher.utter_message(text=f"The creation date for {provider} is {creation_date}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetFiscalYear(Action):

#     def name(self) -> Text:
#         return "action_get_fiscal_year"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             fiscal_year = collection.find_one(query).get("Fiscal Year", "N/A")
#             dispatcher.utter_message(text=f"The fiscal year for {provider} is {fiscal_year}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetLpaNumber(Action):

#     def name(self) -> Text:
#         return "action_get_lpa_number"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             lpa_number = collection.find_one(query).get("LPA Number", "N/A")
#             dispatcher.utter_message(text=f"The LPA number for {provider} is {lpa_number}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetPurchaseOrderNumber(Action):

#     def name(self) -> Text:
#         return "action_get_purchase_order_number"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             po_number = collection.find_one(query).get("Purchase Order Number", "N/A")
#             dispatcher.utter_message(text=f"The purchase order number for {provider} is {po_number}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetRequisitionNumber(Action):

#     def name(self) -> Text:
#         return "action_get_requisition_number"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             req_number = collection.find_one(query).get("Requisition Number", "N/A")
#             dispatcher.utter_message(text=f"The requisition number for {provider} is {req_number}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []


# class ActionGetAcquisitionType(Action):

#     def name(self) -> Text:
#         return "action_get_acquisition_type"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         query = {"Supplier Name": provider}

#         try:
#             acquisition_type = collection.find_one(query).get("Acquisition Type", "N/A")
#             dispatcher.utter_message(text=f"The acquisition type for {provider} is {acquisition_type}.")
#         except Exception as e:
#             dispatcher.utter_message(text=f"An error occurred: {str(e)}")

#         return []

# class ActionGetTotalSpent(Action):

#     def name(self) -> Text:
#         return "action_get_total_spent"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")  # Assuming 'Supplier Name' is the provider
#         time_range = tracker.get_slot("time_range")  # Assuming 'Creation Date' or 'Fiscal Year' is used for time range

#         # Query MongoDB to calculate total spent
#         query = {"Supplier Name": provider} # Start with provider filter

#         # Add time range filter if available
#         if time_range:
#             # Adjust based on your time range format and field
#             # Example: if time_range is a year, you might use 'Fiscal Year'
#             query["Fiscal Year"] = {"$regex": time_range}
#             # Example: if time_range is a specific date or range, adjust accordingly

#         total_spent = sum([doc["Total Price"] for doc in collection.find(query) if "Total Price" in doc])

#         dispatcher.utter_message(template="utter_total_spent", total_spent=total_spent, provider=provider, time_range=time_range)

#         return []

# class ActionGetPurchaseDetails(Action):

#     def name(self) -> Text:
#         return "action_get_purchase_details"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         provider = tracker.get_slot("provider")
#         time_range = tracker.get_slot("time_range")

#         # Query MongoDB to get purchase details
#         query = {"Supplier Name": provider}
#         if time_range:
#             # Adjust based on your time range format and field
#             query["Fiscal Year"] = {"$regex": time_range}

#         items = [doc["Item Name"] for doc in collection.find(query) if "Item Name" in doc]

#         dispatcher.utter_message(template="utter_purchase_details", items=", ".join(items), provider=provider, time_range=time_range)

#         return []
