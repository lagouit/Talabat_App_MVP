# presentation/cli/menu_admin.py

import os
from application.services.admin_service import AdminService
from core.entities.administrateur import Administrateur
from core.enums.statut_commande import StatutCommande

class MenuAdmin:
    """
    Interface CLI finale pour l'Administrateur de Talabat.
    Responsable de la moderation, du catalogue, des stats, des litiges et du filtrage.
    Responsable : Equipe Talabat (Yasmine & Noureddine)
    """

    def __init__(self, admin: Administrateur):
        self._admin = admin
        self._admin_service = AdminService()
        self._en_cours = True

    def _nettoyer_console(self):
        """Efface l'ecran pour une navigation fluide."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher(self):
        """Boucle principale du tableau de bord Administrateur."""
        while self._en_cours:
            self._nettoyer_console()
            
            # Appel unique a l'entite pour eviter les doublons (p. 61)
            self._admin.afficher_tableau_de_bord()
            
            choix = input("\nVotre choix : ")

            if choix == '1':
                self._moderation_kyc()
            elif choix == '2':
                self._gestion_categories()
            elif choix == '3':
                self._consulter_statistiques()
            elif choix == '4':
                self._gestion_litiges()
            elif choix == '5':
                self._voir_annuaire_utilisateurs()
            elif choix == '6':
                self._voir_commandes_par_statut()
            elif choix == '0':
                self._en_cours = False
            else:
                input("[!] Choix invalide. Appuyez sur Entree...")

    def _moderation_kyc(self):
        """Valide les dossiers des cuisiniers en attente."""
        self._nettoyer_console()
        print("="*60)
        print("   MODERATION : FOURNISSEURS EN ATTENTE DE VALIDATION")
        print("="*60)
        en_attente = self._admin_service.obtenir_fournisseurs_en_attente()
        
        if not en_attente:
            input("\nAucun dossier en attente. Entree pour retour...")
            return

        print(f"{'ID':<5} | {'NOM':<25} | {'EMAIL':<30}")
        print("-" * 60)
        for f in en_attente:
            print(f"{f['id']:<5} | {f['nom']:<25} | {f['email']:<30}")
        
        try:
            id_f = int(input("\nID du fournisseur a valider (0 pour retour) : "))
            if id_f != 0 and self._admin_service.valider_dossier_fournisseur(id_f):
                input(f"\n[OK] Fournisseur #{id_f} valide ! Reconnexion requise pour lui.")
            elif id_f != 0:
                input("\n[!] Echec : ID introuvable.")
        except ValueError:
            input("\n[!] Erreur de saisie.")

    def _voir_annuaire_utilisateurs(self):
        """Affiche les listes completes des acteurs du systeme."""
        self._nettoyer_console()
        print("--- ANNUAIRE DES UTILISATEURS ---")
        print("1. Liste des Clients | 2. Liste des Cuisiniers | 0. Retour")
        choix = input("\nChoix : ")
        
        if choix == '1':
            res = self._admin_service.obtenir_tous_beneficiaires()
            print("\nID | NOM | TELEPHONE | EMAIL")
            print("-" * 70)
            for u in res: print(f"{u['id']} | {u['nom']} | {u['telephone']} | {u['email']}")
        elif choix == '2':
            res = self._admin_service.obtenir_tous_fournisseurs()
            print("\nID | NOM | STATUT | SOLDE")
            print("-" * 70)
            for u in res: 
                statut = "VALIDE" if u['kyc_valide'] else "BLOQUE"
                print(f"{u['id']} | {u['nom']} | {statut} | {u['solde_accumule']} DH")
        input("\nEntree pour continuer...")

    def _voir_commandes_par_statut(self):
        """Filtrage detaille des commandes (ID, Client, Chef, Details, Date, Prix)."""
        self._nettoyer_console()
        print("--- FILTRER LES COMMANDES PAR STATUT ---")
        print("1. Acceptees | 2. En preparation | 3. Pretes | 4. Livrees | 5. Confirmees | 6. Annulees")
        choix_s = input("\nVotre choix : ")
        
        mapping = {
            '1': StatutCommande.ACCEPTE_CHEF, '2': StatutCommande.EN_PREPARATION,
            '3': StatutCommande.PRET_LIVRAISON, '4': StatutCommande.LIVRE,
            '5': StatutCommande.CONFIRME, '6': StatutCommande.ANNULE
        }

        if choix_s in mapping:
            statut_elu = mapping[choix_s]
            commandes = self._admin_service.filtrer_commandes_details(statut_elu)
            
            self._nettoyer_console()
            print(f"--- LISTE : {statut_elu.value} ---")
            
            if not commandes:
                print("\nAucun resultat pour ce statut.")
            else:
                # Formatage large pour inclure toutes les colonnes demandees
                line_width = 120
                print("-" * line_width)
                print(f"{'ID':<4} | {'CLIENT':<15} | {'CHEF':<15} | {'PRIX':<10} | {'DATE':<12} | {'DETAILS'}")
                print("-" * line_width)
                
                for c in commandes:
                    date_str = c['date_creation'].strftime("%d/%m/%Y")
                    prix_str = f"{c['montant_total']} DH"
                    print(f"{c['id']:<4} | {c['nom_client']:<15} | {c['nom_fournisseur']:<15} | {prix_str:<10} | {date_str:<12} | {c['details']}")
                
                print("-" * line_width)
            input("\nAppuyez sur Entree pour revenir...")

    def _gestion_categories(self):
        """Affiche et ajoute des categories culinaires."""
        self._nettoyer_console()
        print("--- GESTION DES CATEGORIES ---")
        cats = self._admin_service.obtenir_toutes_categories()
        print(f"{'ID':<5} | {'LIBELLE':<30}")
        print("-" * 35)
        for c in cats: print(f"{c['id']:<5} | {c['libelle']:<30}")
        
        nom = input("\nNom de la nouvelle categorie (ou 0 pour retour) : ")
        if nom != '0' and nom:
            if self._admin_service.gerer_categories("AJOUT", nom):
                input(f"\n[OK] Categorie '{nom}' ajoutee.")
            else:
                input("\n[!] Erreur (doublon possible).")

    def _consulter_statistiques(self):
        """Dashboard financier global."""
        self._nettoyer_console()
        print("="*45)
        print("       TABLEAU DE BORD STATISTIQUE")
        print("="*45)
        s = self._admin_service.obtenir_dashboard_stats()
        print(f"- Volume d'affaires global : {s['volume_daffaires']}")
        print(f"- Cuisiniers actifs (Chefs): {s['nombre_fournisseurs']}")
        print(f"- Clients inscrits          : {s['nombre_beneficiaires']}")
        print("-" * 45)
        input("\nAppuyez sur Entree pour revenir...")

    def _gestion_litiges(self):
        """Annulation et remboursement client."""
        self._nettoyer_console()
        print("--- GESTION DES LITIGES (SEQUESTRE) ---")
        commandes = self._admin_service.obtenir_commandes_pour_litige()
        
        if not commandes:
            input("\nAucune commande active susceptible de litige. Entree...")
            return

        print(f"{'ID':<5} | {'CLIENT':<7} | {'CHEF':<7} | {'TOTAL':<10} | {'STATUT'}")
        print("-" * 65)
        for c in commandes:
            print(f"{c['id']:<5} | {c['beneficiaire_id']:<7} | {c['supplier_id']:<7} | {c['montant_total']:<10} | {c['statut']}")
        
        try:
            id_cmd = int(input("\nID de la commande a rembourser (0 pour retour) : "))
            if id_cmd != 0 and self._admin_service.resoudre_litige_remboursement(id_cmd):
                input("\n[OK] Commande annulee et client rembourse.")
        except ValueError:
            input("\n[!] ID invalide.")