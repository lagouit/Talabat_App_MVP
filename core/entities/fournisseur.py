# core/entities/fournisseur.py

from core.entities.utilisateur import Utilisateur
from core.enums.type_utilisateur import TypeUtilisateur

class Fournisseur(Utilisateur):
    """
    Classe representant un Fournisseur (Cuisinier Artisan).
    Herite de la classe Utilisateur (p. 45 du cours).
    Responsable : Noureddine
    """

    def __init__(self, id_user: int, nom: str, email: str, mot_de_passe: str, 
                 biographie: str = "", kyc_valide: bool = False, solde: float = 0.0):
        # Appel du constructeur parent avec le type FOURNISSEUR
        super().__init__(id_user, nom, email, mot_de_passe, TypeUtilisateur.FOURNISSEUR)
        
        # Attributs specifiques au Fournisseur
        self._biographie = biographie
        self._kyc_valide = kyc_valide
        self.__solde_accumule = solde # Attribut prive pour la securite financiere (p. 22)

    # --- ENCAPSULATION : GETTERS & SETTERS (p. 28) ---

    @property
    def biographie(self) -> str:
        return self._biographie

    @biographie.setter
    def biographie(self, texte: str):
        self._biographie = texte

    @property
    def kyc_valide(self) -> bool:
        """Indique si le compte est autorise par l'Admin a vendre."""
        return self._kyc_valide

    @property
    def solde(self) -> float:
        """Lecture seule du solde pour la securite."""
        return self.__solde_accumule

    # --- METHODES METIER ---

    def valider_profil(self) -> None:
        """Methode appelee lors de la validation Admin."""
        self._kyc_valide = True

    def ajouter_revenu(self, montant: float) -> None:
        """Incremente le solde apres liberation du sequestre (Action Yasmine)."""
        if montant > 0:
            self.__solde_accumule += montant

    def soumettre_kyc(self, liste_documents: list) -> None:
        """Simulation de soumission de documents."""
        print(f"[KYC] Documents recus pour le chef {self._nom}.")

    # --- IMPLEMENTATION DES METHODES ABSTRAITES (p. 95) ---

    def obtenir_details_profil(self) -> str:
        """Retourne un resume textuel du profil."""
        statut = "VALIDE" if self._kyc_valide else "EN ATTENTE"
        return (f"PROFIL CHEF :\n"
                f"- Nom : {self._nom}\n"
                f"- Statut : {statut}\n"
                f"- Solde : {self.__solde_accumule} DH\n"
                f"- Bio : {self._biographie}")

    def afficher_tableau_de_bord(self) -> None:
        """
        Affiche le menu COMPLET et UNIQUE pour Noureddine.
        Cette methode centralise les options pour eviter les doublons.
        """
        statut_label = "VALIDE [OK]" if self._kyc_valide else "NON VALIDE [X]"
        print(f"\n--- TABLEAU DE BORD CHEF : {self._nom.upper()} ---")
        print(f"Statut KYC : {statut_label}")
        print(f"Solde      : {self.__solde_accumule} DH")
        print("-" * 45)
        print("1. Gerer mon catalogue (Liste, Modif, Suppr)")
        print("2. Voir les commandes a preparer (Flux Client)")
        print("3. Consulter mes revenus")
        print("4. Soumettre/Mettre a jour documents KYC")
        print("5. Voir l'historique de mes ventes (Terminees)")
        print("0. Deconnexion")

    def __str__(self) -> str:
        return f"[Chef] {self._nom} - {self._email}"