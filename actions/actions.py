# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from rasa_sdk.events import SlotSet

# example:
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

class ValidateBookingForm(FormValidationAction):
    def name(self):
        return "validate_booking_form"

    def validate_date(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `date` value."""
        # Vérifie si le numéro de réservation est déjà présent dans le slot

        print("je suis dans booking date")
        # TODO vérification de la date sous la forme **/**/**

        if number > 0:
            return {"date": slot_value}
        else:
            dispatcher.utter_message(text=f"La date doit être sous la forme jj/mm/aa")
            return {"date": None}

    def validate_nber_pers(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `nber_pers` value."""
        print("je suis dans nombre pers")

        number = int(slot_value)
        # TODO validation : le nombre doit être compris entre 1 et 15

        if number > 0:
            return {"nber_pers": slot_value}
        else:
            dispatcher.utter_message(text=f"Votre numéro de réservation ne peut pas être 0")
            return {"nber_pers": None}

    def validate_tel(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

    """Validate `tel` value."""
    print("je suis dans nombre pers")

    number = int(slot_value)
    # TODO validation : le numéro doit être sous la forme 00.00.00.00.00

    if number > 0:
        return {"tel": slot_value}
    else:
        dispatcher.utter_message(text=f"Votre numéro doit être sous la forme 00.00.00.00.00")
        return {"tel": None}

    def validate_booking_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

    """Validate `nber_pers` value."""
    print("je suis dans nom")

    # TODO validation : le nom ne peut pas être null

    if number > 0:
        return {"booking_name": slot_value}
    else:
        dispatcher.utter_message(text=f"Votre nom est incorrect")
        return {"booking_name": None}


class ActionSaveBooking(Action):
    def name(self) -> str:
        return "action_save_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        try:
            conn = sqlite3.connect('rasa.db')
            cursor = conn.cursor()

            # TODO a retirer sert juste à debbuger
            cursor.execute("SELECT id, booking_code, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows)

            # TODO --------------- à modifier ----------------------------
            reservation_id = tracker.get_slot('booking_code')
            print(reservation_id)
            comment = tracker.get_slot('comment')
            print(comment)

            if not reservation_id or not comment:
                dispatcher.utter_message(text="Je n'ai pas pu trouver le numéro de la réservation ou le commentaire.")
                return []


            # Connecter à la base de données
            cursor2 = conn.cursor()

            # Mettre à jour le commentaire de la réservation spécifiée
            cursor2.execute('''
            UPDATE reservation
            SET comment = ?
            WHERE booking_code = ?
            ''', (comment, reservation_id))

            # Sauvegarder les changements
            conn.commit()

            if cursor2.rowcount == 0:
                dispatcher.utter_message(text=f"Aucune réservation trouvée avec le numéro: {reservation_id}.")
            else:
                dispatcher.utter_message(text="Le commentaire a été ajouté à la réservation avec succès.")

            conn.close()
        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Une erreur est survenue lors de la mise à jour de la réservation : {e}")

        # TODO --------------- à modifier FIN  ----------------------------
        return [SlotSet("booking_code", booking_code), SlotSet("date", None), SlotSet("nber_pers", None), SlotSet("tel", None), SlotSet("booking_name", None)]






class ValidateCommentForm(FormValidationAction):
    def name(self):
        return "validate_comment_form"

    def validate_booking_code(
             self,
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `booking_code` value."""
        # Vérifie si le numéro de réservation est déjà présent dans le slot

        print("je suis la")
        number = int(slot_value)

        if number > 0:
            return {"booking_code": slot_value}
        else:
            dispatcher.utter_message(text=f"Votre numéro de réservation ne peut pas être 0")
            return {"booking_code": None}

    def validate_comment(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `comment` value."""
        print("je suis dans comment")

        if isinstance(slot_value, str) and len(slot_value.strip()) > 5:
            return {"comment": slot_value.strip()}
        else:
            dispatcher.utter_message(text="Le commentaire ne peut pas être vide")
            return {"comment": None}


class ActionSaveComment(Action):
    def name(self) -> str:
        return "action_save_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        comment = tracker.latest_message.get("text")

        try:
            conn = sqlite3.connect('rasa.db')
            cursor = conn.cursor()

            # TODO a retirer sert juste à debbuger
            cursor.execute("SELECT id, booking_code, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows)

            reservation_id = tracker.get_slot('booking_code')
            print(reservation_id)
            comment = tracker.get_slot('comment')
            print(comment)

            if not reservation_id or not comment:
                dispatcher.utter_message(text="Je n'ai pas pu trouver le numéro de la réservation ou le commentaire.")
                return []


            # Connecter à la base de données
            cursor2 = conn.cursor()

            # Mettre à jour le commentaire de la réservation spécifiée
            cursor2.execute('''
            UPDATE reservation
            SET comment = ?
            WHERE booking_code = ?
            ''', (comment, reservation_id))

            # Sauvegarder les changements
            conn.commit()

            if cursor2.rowcount == 0:
                dispatcher.utter_message(text=f"Aucune réservation trouvée avec le numéro: {reservation_id}.")
            else:
                dispatcher.utter_message(text="Le commentaire a été ajouté à la réservation avec succès.")

            conn.close()
        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Une erreur est survenue lors de la mise à jour de la réservation : {e}")

        return [SlotSet("booking_code", None), SlotSet("comment", None)]


