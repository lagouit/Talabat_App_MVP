# infrastructure/database/gestionnaire_bdd.py

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# On charge les variables d'environnement du fichier .env (sécurité)
load_dotenv()

class GestionnaireBDD:
    """
    Classe implémentant le DESIGN PATTERN: SINGLETON (p. 211 du cours).
    Garantit une instance unique de la connexion à la base de données MySQL.
    """
    _instance = None

    def __new__(cls):
        """
        Méthode magique appelée avant __init__. 
        C'est ici qu'on contrôle l'unicité de l'objet (p. 209).
        """
        if cls._instance is None:
            # Création de l'instance unique
            cls._instance = super(GestionnaireBDD, cls).__new__(cls)
            cls._instance._connexion = None
            cls._instance._initialiser_connexion()
        return cls._instance

    def _initialiser_connexion(self):
        """Méthode interne pour configurer la connexion MySQL."""
        try:
            self._connexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "Lagouit123@"),
                database=os.getenv("DB_NAME", "talabat_db"),
                port=os.getenv("DB_PORT", "3306")
            )
            if self._connexion.is_connected():
                print("[DATABASE] Succès : Connexion unique établie (Singleton).")
        except Error as e:
            print(f"[DATABASE] Erreur lors de la connexion à MySQL : {e}")
            self._connexion = None

    @property
    def connexion(self):
        """Getter pour récupérer l'objet de connexion mysql-connector."""
        # Si la connexion a été perdue, on tente de la réinitialiser
        if self._connexion is None or not self._connexion.is_connected():
            self._initialiser_connexion()
        return self._connexion

    def fermer_connexion(self):
        """Méthode pour fermer proprement la ressource en fin d'application."""
        if self._connexion and self._connexion.is_connected():
            self._connexion.close()
            print("[DATABASE] Connexion MySQL fermée.")

