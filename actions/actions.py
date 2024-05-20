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

class ValidateCommentForm(FormValidationAction):
    def name(self):
        return "validate_comment_form"

    def validate_number_resa(
             self,
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `number_resa` value."""
        # Vérifie si le numéro de réservation est déjà présent dans le slot

        print("je suis la")
        number = int(slot_value)

        if number > 0:
            return {"number_resa": slot_value}
        else:
            dispatcher.utter_message(text=f"Votre numéro de réservation ne peut pas être 0")
            return {"number_resa": None}

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
            cursor.execute("SELECT id, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows)

            reservation_id = tracker.get_slot('number_resa')
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


