# core/entities/notification.py

from abc import ABC, abstractmethod
from core.entities.utilisateur import Utilisateur

class Notification(ABC):
    """
    Classe Abstraite représentant le contrat de base pour toutes les notifications.
    Respecte le principe OCP : on peut ajouter des types de notification 
    (WhatsApp, Push) sans modifier le code existant.
    """

    def __init__(self, message: str):
        # Attribut protégé pour être accessible par les classes filles (p. 24)
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    @abstractmethod
    def envoyer(self, u: Utilisateur) -> None:
        """
        Méthode abstraite forçant chaque sous-classe à implémenter 
        sa propre logique d'envoi (p. 95).
        """
        pass


class NotificationEmail(Notification):
    """Implémentation concrète pour l'envoi par Email."""

    def envoyer(self, u: Utilisateur) -> None:
        print(f"[EMAIL] Destinataire : {u.email}")
        print(f"[CONTENU] Bonjour {u.nom}, {self._message}")
        print("-" * 30)


class NotificationSMS(Notification):
    """Implémentation concrète pour l'envoi par SMS."""

    def envoyer(self, u: Utilisateur) -> None:
        # On suppose que l'utilisateur a un attribut telephone (ex: Beneficiaire)
        tel = getattr(u, 'telephone', 'Inconnu')
        print(f"[SMS] Envoi au {tel}")
        print(f"[MSG] Talabat: {self._message}")
        print("-" * 30)


class NotificationApp(Notification):
    """Implémentation concrète pour les notifications In-App (Tableau de bord)."""

    def envoyer(self, u: Utilisateur) -> None:
        print(f"[APP-NOTIF] Pour {u.nom} : {self._message}")
        print("-" * 30)