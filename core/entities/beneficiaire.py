# core/entities/beneficiaire.py

from core.entities.utilisateur import Utilisateur
from core.enums.type_utilisateur import TypeUtilisateur

class Beneficiaire(Utilisateur):
    """
    Classe representant un Beneficiaire (Client final).
    Herite de la classe Utilisateur (p. 45 du cours).
    Responsable : Yasmine
    """

    def __init__(self, id_user: int, nom: str, email: str, mot_de_passe: str, 
                 adresse_livraison: str = "", telephone: str = ""):
        # Appel du constructeur parent avec le type BENEFICIAIRE (p. 48)
        super().__init__(id_user, nom, email, mot_de_passe, TypeUtilisateur.BENEFICIAIRE)
        
        # Attributs specifiques au Beneficiaire
        self._adresse_livraison = adresse_livraison
        self._telephone = telephone

    # --- ENCAPSULATION : GETTERS & SETTERS (p. 28) ---

    @property
    def adresse_livraison(self) -> str:
        return self._adresse_livraison

    @adresse_livraison.setter
    def adresse_livraison(self, nouvelle_adresse: str):
        """Valide l'adresse avant modification."""
        if not nouvelle_adresse or len(nouvelle_adresse.strip()) < 5:
            raise ValueError("L'adresse de livraison est trop courte ou invalide.")
        self._adresse_livraison = nouvelle_adresse

    @property
    def telephone(self) -> str:
        return self._telephone

    @telephone.setter
    def telephone(self, valeur: str):
        """Valide le format du telephone (10 chiffres)."""
        if not valeur.isdigit() or len(valeur) != 10:
            raise ValueError("Le numero de telephone doit contenir exactement 10 chiffres.")
        self._telephone = valeur

    # --- METHODES METIER ---

    def confirmer_reception(self, id_commande: int) -> None:
        """Logique de confirmation pour declencher la liberation du sequestre."""
        print(f"[DOMAINE] Le client {self._nom} confirme la reception de la commande #{id_commande}.")

    # --- IMPLEMENTATION DES METHODES ABSTRAITES (p. 95) ---

    def obtenir_details_profil(self) -> str:
        """Retourne un resume complet du profil client."""
        return (f"PROFIL CLIENT :\n"
                f"- Nom : {self._nom}\n"
                f"- Email : {self._email}\n"
                f"- Tel : {self._telephone}\n"
                f"- Adresse : {self._adresse_livraison}")

    def afficher_tableau_de_bord(self) -> None:
        """Affiche les options specifiques a Yasmine sans doublons."""
        print(f"\n--- ESPACE CLIENT : {self._nom.upper()} ---")
        print("1. Explorer le catalogue (Plats, Chefs, Categories)")
        print("2. Mon Panier")
        print("3. Historique des commandes (Details)")
        print("4. Confirmer une reception (Liberer fonds)")
        print("5. Modifier mon adresse et telephone")
        print("0. Deconnexion")

    def __str__(self) -> str:
        return f"[Client] {self._nom} - {self._adresse_livraison}"