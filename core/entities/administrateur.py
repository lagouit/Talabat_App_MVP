# core/entities/administrateur.py

from core.entities.utilisateur import Utilisateur
from core.enums.type_utilisateur import TypeUtilisateur

class Administrateur(Utilisateur):
    """
    Classe représentant l'Administrateur de la plateforme Talabat.
    Hérite de la classe Utilisateur (Héritage simple - p. 45).
    Rôle : Modération, validation KYC et supervision globale.
    """

    def __init__(self, id_user: int, nom: str, email: str, mot_de_passe: str, matricule: str):
        # Appel du constructeur parent avec le type ADMIN (p. 48)
        super().__init__(id_user, nom, email, mot_de_passe, TypeUtilisateur.ADMIN)
        
        # Attribut spécifique à l'admin
        self._matricule = matricule

    # --- ENCAPSULATION ---

    @property
    def matricule(self) -> str:
        return self._matricule

    # --- MÉTHODES MÉTIER (Gestion et Modération) ---

    def valider_kyc(self, fournisseur_nom: str, id_fournisseur: int) -> None:
        """
        Simule la validation d'un dossier fournisseur.
        Dans la logique de service, cela passera le booléen 'kyc_valide' à True.
        """
        print(f"[MODÉRATION] Validation des documents de : {fournisseur_nom} (ID: {id_fournisseur})")
        print(f"[SYSTÈME] Le fournisseur est désormais autorisé à vendre sur la plateforme.")

    def gerer_litige(self, id_commande: int, action: str) -> None:
        """
        Permet d'intervenir sur une commande en cas de problème entre Yasmine et Noureddine.
        action : 'REMBOURSER' ou 'FORCER_PAIEMENT'
        """
        print(f"[LITIGE] Intervention sur la commande #{id_commande}.")
        print(f"[ACTION] Décision de l'administrateur : {action}")

    def consulter_statistiques(self) -> None:
        """Affiche un résumé global de l'activité (Volume de ventes, nouveaux inscrits)."""
        print(f"[STATS] Rapport généré par l'admin {self._nom} (Matricule: {self._matricule})")
        print("- Nombre de commandes aujourd'hui : 12")
        print("- Volume total du séquestre : 2500.00 DH")

    # --- IMPLÉMENTATION DES MÉTHODES ABSTRAITES (p. 95) ---

    def obtenir_details_profil(self) -> str:
        return (f"PROFIL ADMINISTRATEUR :\n"
                f"- Nom : {self._nom}\n"
                f"- Matricule : {self._matricule}\n"
                f"- Email : {self._email}\n"
                f"- Niveau d'accès : Accès Total")

    def afficher_tableau_de_bord(self) -> None:
        print(f"\n--- CONSOLE D'ADMINISTRATION : {self._nom.upper()} ---")
        print("1. Valider les dossiers KYC (Fournisseurs)")
        print("2. Gerer les categories de repas")
        print("3. Voir les statistiques globales")
        print("4. Gestion des litiges et remboursements")
        print("5. Annuaire des Utilisateurs (Listes)")
        print("6. Filtrer les commandes par statut") 
        print("0. Deconnexion")