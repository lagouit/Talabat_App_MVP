# core/entities/utilisateur.py

from abc import ABC, abstractmethod
from core.enums.type_utilisateur import TypeUtilisateur

class Utilisateur(ABC):
    """
    Classe Abstraite (p. 92) servant de base a tous les utilisateurs.
    Elle definit le contrat que Beneficiaire, Fournisseur et Admin doivent suivre.
    """

    def __init__(self, id_user: int, nom: str, email: str, mot_de_passe: str, type_u: TypeUtilisateur):
        # Utilisation de l'attribut protege '_' pour permettre l'acces aux classes filles (p. 24)
        self._id = id_user
        self._nom = nom
        self._email = email
        self._mot_de_passe = mot_de_passe # Stocke le vrai mot de passe saisi
        self._type_utilisateur = type_u
        self._est_connecte = False

    # --- ENCAPSULATION : GETTERS & SETTERS (@property - p. 28) ---

    @property
    def id(self) -> int:
        return self._id

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, valeur: str):
        if len(valeur.strip()) < 2:
            raise ValueError("Le nom est trop court.")
        self._nom = valeur

    @property
    def email(self) -> str:
        return self._email

    @property
    def mot_de_passe(self) -> str:
        """Permet au Repository de lire le mot de passe pour la sauvegarde SQL."""
        return self._mot_de_passe

    @property
    def type_utilisateur(self) -> TypeUtilisateur:
        return self._type_utilisateur

    # --- METHODES METIER ---

    def verifier_mot_de_passe(self, mdp_saisi: str) -> bool:
        """Compare le mot de passe stocke avec la saisie clavier."""
        return self._mot_de_passe == mdp_saisi

    def se_connecter(self) -> None:
        self._est_connecte = True

    def se_deconnecter(self) -> None:
        self._est_connecte = False

    # --- CONTRATS ABSTRAITS (p. 95) ---
    # Ces methodes DOIVENT etre implementees dans Fournisseur, Beneficiaire, etc.

    @abstractmethod
    def obtenir_details_profil(self) -> str:
        """Retourne les informations specifiques au role."""
        pass

    @abstractmethod
    def afficher_tableau_de_bord(self) -> None:
        """Affiche le menu console personnalise selon l'utilisateur."""
        pass

    def __str__(self) -> str:
        return f"[{self._type_utilisateur.value}] {self._nom} ({self._email})"