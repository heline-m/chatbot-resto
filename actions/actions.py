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

class ActionAskReservationNumberAndComment(Action):
    def name(self):
        return "action_ask_reservation_number_and_comment"

    def run(self, dispatcher, tracker, domain):
        # Vérifie si le numéro de réservation est déjà présent dans le slot
        reservation_number = tracker.get_slot("number_resa")

        if reservation_number is None:
            dispatcher.utter_message("Quel est le numéro de votre réservation ?")
            # on set la demande du slot number_resa
            return [SlotSet("requested_slot", "number_resa")]

        # Si le numéro de réservation est déjà présent, pas besoin de demander
        dispatcher.utter_message("Quel est votre commentaire ?")
        return []

class ActionAskComment(Action):

    def name(self) -> Text:
        return "action_ask_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['text']
        dispatcher.utter_message(text=last_intent)

        return [SlotSet("comment", last_intent)]

class ActionSaveComment(FormValidationAction):
    def name(self) -> str:
        return "action_save_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        comment = tracker.latest_message.get("text")

        try:
            conn = sqlite3.connect('rasa.db')
            cursor = conn.cursor()

            cursor.execute("SELECT id, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows)

            reservation_id = tracker.get_slot('number_resa')
            print(reservation_id)
            comment = tracker.get_slot('comment')
            print(comment)

            if not reservation_id or not new_comment:
                dispatcher.utter_message(text="Je n'ai pas pu trouver le numéro de la réservation ou le commentaire.")
                return []


            # Connecter à la base de données
            cursor2 = conn.cursor()

            # Mettre à jour le commentaire de la réservation spécifiée
            cursor2.execute('''
            UPDATE reservation
            SET comment = ?
            WHERE id = ?
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

        return []


