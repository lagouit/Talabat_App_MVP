# infrastructure/factories/fabrique_notification.py

from core.entities.utilisateur import Utilisateur
from core.entities.notification import (
    NotificationEmail, 
    NotificationSMS, 
    NotificationApp
)

class FabriqueNotification:
    """
    Classe implémentant le DESIGN PATTERN: FACTORY (p. 214 du cours).
    Responsable de l'instanciation du bon canal de communication.
    Respecte le principe OCP (SOLID) : l'ajout d'un nouveau canal 
    (ex: WhatsApp) ne modifie pas la logique métier des services.
    """

    @staticmethod
    def notifier(type_canal: str, user: Utilisateur, message: str) -> None:
        """
        Méthode de fabrication et d'exécution combinée (comme sur votre diagramme).
        :param type_canal: 'EMAIL', 'SMS' ou 'APP'.
        :param user: L'objet Utilisateur (Bénéficiaire ou Fournisseur) à notifier.
        :param message: Le contenu textuel de la notification.
        """
        
        notification = None
        canal = type_canal.upper()

        # 1. Logique de création (Délégation de l'instanciation - p. 215)
        if canal == "EMAIL":
            notification = NotificationEmail(message)
        elif canal == "SMS":
            notification = NotificationSMS(message)
        elif canal == "APP":
            notification = NotificationApp(message)
        else:
            print(f"[FACTORY] Erreur : Le canal '{type_canal}' n'est pas supporté.")
            return

        # 2. Utilisation du polymorphisme (p. 61)
        # On appelle 'envoyer' sur l'abstraction, Python choisit la bonne version.
        try:
            notification.envoyer(user)
        except Exception as e:
            print(f"[FACTORY] Échec de l'envoi via {canal} : {e}")
