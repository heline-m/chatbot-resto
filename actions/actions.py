# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
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

class ActionSaveComment(Action):

    def name(self) -> Text:
        return "action_save_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['text']
        dispatcher.utter_message(text=last_intent)

        return [SlotSet("comment", last_intent)]

class ActionAddComment(Action):
    def name(self) -> str:
        return "action_add_comment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Récupérer l'ID de la réservation et le nouveau commentaire depuis les slots
        # reservation_id = tracker.get_slot('number_resa')

        try:
            conn = sqlite3.connect('rasa.db')
            cursor = conn.cursor()

            cursor.execute("SELECT id, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows);

            reservation_id = 1
            new_comment = tracker.get_slot('comment')
            print(new_comment)

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
            ''', (new_comment, reservation_id))

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


