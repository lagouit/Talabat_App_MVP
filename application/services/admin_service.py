# application/services/admin_service.py

from typing import List, Dict, Any
from infrastructure.repositories.utilisateur_repo import UtilisateurRepository
from infrastructure.repositories.commande_repo import CommandeRepository
from infrastructure.repositories.repas_repo import RepasRepository
from core.enums.type_utilisateur import TypeUtilisateur
from core.enums.statut_commande import StatutCommande

class AdminService:
    """
    Service de Moderation, Supervision et Gestion (Couche Application).
    Coordone les actions administratives sur les utilisateurs, le catalogue et les flux.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Inversion de dependance : utilisation des repositories specialises
        self._user_repo = UtilisateurRepository()
        self._commande_repo = CommandeRepository()
        self._repas_repo = RepasRepository()

    # --- SECTION 1 : GESTION DES UTILISATEURS (Noureddine & Yasmine) ---

    def obtenir_tous_fournisseurs(self) -> List[Dict[str, Any]]:
        """Recupere l'annuaire complet des cuisiniers."""
        return self._user_repo.recuperer_tous_fournisseurs()

    def obtenir_tous_beneficiaires(self) -> List[Dict[str, Any]]:
        """Recupere l'annuaire complet des clients."""
        return self._user_repo.recuperer_tous_beneficiaires()

    def obtenir_fournisseurs_en_attente(self) -> List[Dict[str, Any]]:
        """Liste les cuisiniers n'ayant pas encore valide leur KYC."""
        return self._user_repo.recuperer_fournisseurs_en_attente()

    def valider_dossier_fournisseur(self, fournisseur_id: int) -> bool:
        """Approuve un cuisinier et l'autorise a vendre sur le marche."""
        fournisseur = self._user_repo.trouver_par_id(fournisseur_id) 
        
        if fournisseur and fournisseur.type_utilisateur == TypeUtilisateur.FOURNISSEUR:
            # Action metier (Domaine)
            fournisseur.valider_profil()
            # Action SQL (Infrastructure)
            return self._user_repo.mettre_a_jour_statut_kyc(fournisseur_id, True)
        
        return False

    # --- SECTION 2 : GESTION DU CATALOGUE (Categories) ---

    def obtenir_toutes_categories(self) -> List[Dict[str, Any]]:
        """Liste les categories pour l'organisation de l'offre."""
        return self._repas_repo.recuperer_toutes_categories()

    def gerer_categories(self, action: str, libelle: str) -> bool:
        """Ajoute de nouvelles categories culinaires."""
        if action == "AJOUT" and libelle:
            return self._repas_repo.ajouter_categorie(libelle)
        return False

    # --- SECTION 3 : DASHBOARD ET STATISTIQUES ---

    def obtenir_dashboard_stats(self) -> Dict[str, Any]:
        """Compile les donnees de performance globale."""
        nb_chefs = self._user_repo.compter_par_type(TypeUtilisateur.FOURNISSEUR)
        nb_clients = self._user_repo.compter_par_type(TypeUtilisateur.BENEFICIAIRE)
        
        # Calcul financier dynamique via CommandeRepository
        volume = self._commande_repo.calculer_volume_total()

        return {
            "volume_daffaires": f"{volume:.2f} DH",
            "nombre_fournisseurs": nb_chefs,
            "nombre_beneficiaires": nb_clients,
            "statut_systeme": "Operationnel"
        }

    # --- SECTION 4 : FILTRAGE ET LOGISTIQUE (Flux de travail) ---

    def filtrer_commandes_details(self, statut: StatutCommande) -> List[Dict[str, Any]]:
        """
        Recupere les commandes par statut avec noms des acteurs et details des plats.
        Combine les donnees de Commandes, Utilisateurs et Lignes de Commande.
        """
        # 1. Recuperation des commandes avec les noms (JOIN SQL)
        commandes = self._commande_repo.recuperer_tout_par_statut_detaille(statut.name)
        
        # 2. Enrichissement avec la liste textuelle des articles
        for cmd in commandes:
            cmd['details'] = self._commande_repo.recuperer_lignes_format_texte(cmd['id'])
            
        return commandes

    # --- SECTION 5 : GESTION DES LITIGES (Arbitrage financier) ---

    def obtenir_commandes_pour_litige(self) -> List[Dict[str, Any]]:
        """Liste les commandes ou l'argent est encore bloque en sequestre."""
        return self._commande_repo.recuperer_commandes_pour_litige()

    def resoudre_litige_remboursement(self, commande_id: int) -> bool:
        """Annule une commande litigieuse pour proteger le client."""
        return self._commande_repo.mettre_a_jour_statut(commande_id, StatutCommande.ANNULE)