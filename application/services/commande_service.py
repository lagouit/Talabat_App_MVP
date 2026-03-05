# application/services/commande_service.py

import uuid
from typing import List, Dict, Any, Optional
from core.entities.commande import Commande
from core.enums.statut_commande import StatutCommande
from infrastructure.repositories.commande_repo import CommandeRepository
from infrastructure.repositories.utilisateur_repo import UtilisateurRepository
from infrastructure.factories.fabrique_notification import FabriqueNotification

class CommandeService:
    """
    Service central orchestrant le cycle de vie des commandes.
    Gere le flux financier (Sequestre) et les interactions entre acteurs.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Inversion de dependance : utilisation des repositories specialises
        self._commande_repo = CommandeRepository()
        self._user_repo = UtilisateurRepository()

    # --- SECTION 1 : FLUX D'ACHAT (Yasmine) ---

    def initialiser_commande(self, beneficiaire_id: int, fournisseur_id: int, panier: List[Dict[str, Any]]) -> bool:
        """
        Cree une commande, calcule le total et bloque les fonds.
        panier: [{'repas': Repas, 'quantite': int}, ...]
        """
        # 1. Creation de l'objet metier Commande (ID 0 auto-increment)
        nouvelle_commande = Commande(0, beneficiaire_id, fournisseur_id)
        
        try:
            for item in panier:
                nouvelle_commande.ajouter_produit(item['repas'], item['quantite'])

            # 2. Securite : On genere un ID de transaction unique
            transaction_id = str(uuid.uuid4())[:18].upper()
            
            # 3. Changement d'etat vers le Sequestre (p. 20 du cours)
            nouvelle_commande.changer_statut(StatutCommande.PAYE_SEQUESTRE)

            # 4. Sauvegarde atomique (Commande + Lignes + PaiementSequestre)
            succes = self._commande_repo.sauvegarder_nouvelle_commande(nouvelle_commande, transaction_id)
            
            if succes:
                # 5. Notification au Chef (Noureddine) via Factory
                chef = self._user_repo.trouver_par_id(fournisseur_id)
                if chef:
                    msg = f"Nouvelle commande recue ({nouvelle_commande.montant_total} DH). A vous de cuisiner !"
                    FabriqueNotification.notifier("EMAIL", chef, msg)
                return True
            
            return False

        except Exception as e:
            print(f"[SERVICE] Erreur lors de l'initialisation : {e}")
            return False

    def obtenir_historique_detaille_client(self, client_id: int) -> List[Dict[str, Any]]:
        """Recupere les commandes d'un client avec la liste textuelle des articles."""
        commandes = self._commande_repo.recuperer_commandes_beneficiaire(client_id)
        for cmd in commandes:
            # On enrichit chaque dictionnaire avec le detail des plats
            cmd['articles'] = self._commande_repo.recuperer_lignes_format_texte(cmd['id'])
        return commandes

    # --- SECTION 2 : WORKFLOW DE PRODUCTION (Noureddine) ---

    def mettre_a_jour_flux_travail(self, commande_id: int, nouveau_statut: StatutCommande) -> bool:
        """Permet au cuisinier de changer l'etat (EN_PREPARATION, PRET, LIVRE)."""
        return self._commande_repo.mettre_a_jour_statut(commande_id, nouveau_statut)

    # --- SECTION 3 : FINALISATION ET PAIEMENT (Yasmine) ---

    def obtenir_commandes_en_attente_confirmation(self, client_id: int) -> List[Dict[str, Any]]:
        """Liste les commandes au statut 'LIVRE' pour validation finale."""
        return self._commande_repo.recuperer_commandes_a_confirmer_par_client(client_id)

    def finaliser_reception_et_payer_chef(self, commande_id: int, fournisseur_id: int, montant: float) -> bool:
        """
        ACTION CRITIQUE : Debloque l'argent du sequestre pour payer Noureddine.
        Ne peut etre declenchee que par l'action de Yasmine.
        """
        # 1. Mise a jour du Sequestre en BDD (est_bloque = 0)
        if self._commande_repo.liberer_fonds_sequestre(commande_id):
            
            # 2. Passage de la commande au statut final
            self._commande_repo.mettre_a_jour_statut(commande_id, StatutCommande.CONFIRME)
            
            # 3. Mise a jour du solde reel du Chef
            chef = self._user_repo.trouver_par_id(fournisseur_id)
            if chef:
                # Methode metier de l'entite (Domaine)
                chef.ajouter_revenu(montant)
                # Persistance du nouveau solde (Infrastructure)
                self._user_repo.mettre_a_jour_solde(fournisseur_id, chef.solde)
                
                # 4. Notification In-App de succes financier
                FabriqueNotification.notifier("APP", chef, f"Fonds liberes ! {montant} DH ajoutes a votre solde.")
                return True
        
        return False

    # --- SECTION 4 : SUPERVISION (Admin) ---

    def obtenir_commandes_details_admin(self, statut: StatutCommande) -> List[Dict[str, Any]]:
        """Permet a l'Admin de voir les flux avec noms des acteurs et articles."""
        # On utilise la jointure SQL complexe du repository
        commandes = self._commande_repo.recuperer_tout_par_statut_detaille(statut.name)
        
        # On ajoute le detail des plats
        for cmd in commandes:
            cmd['details'] = self._commande_repo.recuperer_lignes_format_texte(cmd['id'])
            
        return commandes