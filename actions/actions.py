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
from datetime import datetime
import re
import random

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

        try:
            datetime.strptime(slot_value, "%d/%m/%y")

            is_available = random.choice([True, False])

            if is_available:
                return {"date": slot_value}
            else:
                dispatcher.utter_message(text="Désolé, la table n'est pas disponible à cette date. Veuillez choisir une autre date.")
                return {"date": None} 
            
        except ValueError:
            dispatcher.utter_message(text="La date doit être au format jj/mm/aa.")
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

        if 1 <= number <= 15:
            return {"nber_pers": number}
        else:
            dispatcher.utter_message(text="Le nombre de personnes doit être compris entre 1 et 15.")
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

        if re.fullmatch(r"\d{2}\.\d{2}\.\d{2}\.\d{2}\.\d{2}", slot_value):
            return {"tel": slot_value}
        else:
            dispatcher.utter_message(text="Le numéro de téléphone doit être au format 00.00.00.00.00")
            return {"tel": None}

    def validate_booking_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        """Validate `booking_name` value."""
        print("je suis dans nom")

        if slot_value and slot_value.strip():
            return {"booking_name": slot_value}
        else:
            dispatcher.utter_message(text="Le nom ne peut pas être vide.")
            return {"booking_name": None}


class ActionSaveBooking(Action):
    def name(self) -> str:
        return "action_save_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        print("j'enregistre")
        try:
            conn = sqlite3.connect('rasa.db')
            cursor = conn.cursor()

            # TODO a retirer sert juste à debbuger
            cursor.execute("SELECT id, booking_code, date, nber_pers, phone, comment FROM reservation")
            rows = cursor.fetchall()

            print(rows)

            date = tracker.get_slot('date')
            print(date)
            nber_pers = int(tracker.get_slot('nber_pers'))
            print(nber_pers)
            tel = tracker.get_slot('tel')
            print(tel)
            booking_name = tracker.get_slot('booking_name')
            print(booking_name)

            # création du booking code
            booking_code = random.randint(1000, 9999)

            # Connecter à la base de données
            cursor2 = conn.cursor()

            # Mettre à jour le commentaire de la réservation spécifiée
            cursor2.execute('''
            INSERT INTO reservation 
            (booking_code, date, nber_pers, phone, name) 
            VALUES (?, ?, ?, ?, ?)
            ''', (booking_code, date, nber_pers, tel, booking_name))

            # Sauvegarder les changements
            # Valider la transaction et fermer la connexion
            conn.commit()
            conn.close()

            # Confirmation à l'utilisateur
            dispatcher.utter_message(text=f"Réservation enregistrée pour {booking_name} le {date} pour {nber_pers} personnes. Nous vous contacterons au {tel}. Votre numéro de réservation est le {booking_code}, nous vous conseillons de le noter")

        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Une erreur est survenue lors de l'enregistrement de la réservation : {e}")

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

class ActionShowBooking(Action):
    def name(self) -> str:
        return "action_show_booking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Récupérer le booking_code de la réservation à partir des slots
        booking_code = tracker.get_slot("booking_code")

        if not booking_code:
            dispatcher.utter_message(text="Veuillez fournir un numéro de réservation.")
            return []

        # Connecter à la base de données SQLite
        conn = sqlite3.connect('rasa.db')
        cursor = conn.cursor()

        # Rechercher la réservation par booking_code
        cursor.execute("SELECT date, nber_pers, phone, name, comment FROM reservation WHERE booking_code = ?", (booking_code,))
        result = cursor.fetchone()

        # Fermer la connexion
        conn.close()

        if result:
            date, nber_pers, phone, name, comment = result
            message = f"Réservation pour {name}:\nNuméro de réservation: {booking_code}\nDate: {date}\nNombre de personnes: {nber_pers}\nTéléphone: {phone}\nCommentaire: {comment}"
        else:
            message = f"Aucune réservation trouvée pour le numéro {booking_code}."

        # Envoyer le message à l'utilisateur
        dispatcher.utter_message(text=message)

        return []

class ActionOpenLink(Action):
    def name(self) -> Text:
        return "action_open_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Envoyer le message avec le bouton ou l'URL cliquable
        dispatcher.utter_message(response="utter_open_link_button")

        return []


