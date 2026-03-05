# presentation/cli/menu_fournisseur.py

import os
from application.services.catalogue_service import CatalogueService
from application.services.commande_service import CommandeService
from core.entities.fournisseur import Fournisseur
from core.enums.statut_commande import StatutCommande

class MenuFournisseur:
    """
    Interface CLI pour les fournisseurs (Chefs).
    Gere le catalogue (CRUD), le flux de production et les finances.
    Responsable : Noureddine
    """

    def __init__(self, fournisseur: Fournisseur):
        self._fournisseur = fournisseur
        self._catalogue_service = CatalogueService()
        self._commande_service = CommandeService()
        self._en_cours = True

    def _nettoyer_console(self):
        """Efface l'ecran pour une navigation fluide."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher(self):
        """Boucle principale du tableau de bord Chef."""
        while self._en_cours:
            self._nettoyer_console()
            
            # APPEL UNIQUE : L'entite affiche ses options centralisees (p. 61)
            # Cela evite les doublons de menu et de "0. Deconnexion"
            self._fournisseur.afficher_tableau_de_bord()
            
            choix = input("\nVotre choix : ")

            if choix == '1':
                self._gerer_catalogue()
            elif choix == '2':
                self._suivre_commandes_actives()
            elif choix == '3':
                self._consulter_finances()
            elif choix == '4':
                self._soumettre_kyc_docs()
            elif choix == '5':
                self._voir_historique_complet() # NOM SYNCHRONISE ICI
            elif choix == '0':
                self._en_cours = False
            else:
                input("[!] Choix invalide. Appuyez sur Entree pour continuer...")

    # --- SECTION 1 : GESTION DU CATALOGUE (CRUD) ---

    def _gerer_catalogue(self):
        """Affiche la liste detaillee et propose les actions CRUD."""
        self._nettoyer_console()
        print("="*65)
        print("          GESTION DE MON CATALOGUE CULINAIRE")
        print("="*65)
        
        # Recuperation des plats avec le nom de la categorie via JOIN SQL
        plats = self._catalogue_service.obtenir_menu_fournisseur_detaille(self._fournisseur.id)
        
        if not plats:
            print("\nVotre catalogue est actuellement vide.")
        else:
            print(f"{'ID':<4} | {'TITRE':<18} | {'PRIX':<8} | {'CATEGORIE':<15}")
            print("-" * 65)
            for p in plats:
                statut_visuel = "[ON]" if p['est_disponible'] else "[OFF]"
                print(f"{p['id']:<4} | {p['titre']:<18} | {p['prix']:<8.2f} | {p['nom_cat']:<15} {statut_visuel}")
        
        print("\nActions : [A] Ajouter | [M] Modifier | [S] Supprimer | [R] Retour")
        choix = input("Votre choix : ").lower()

        if choix == 'a':
            self._formulaire_ajout_repas()
        elif choix == 'm':
            self._formulaire_modification_repas()
        elif choix == 's':
            self._formulaire_suppression_repas()

    def _formulaire_ajout_repas(self):
        """Affiche les categories creees par l'Admin avant l'ajout."""
        if not self._fournisseur.kyc_valide:
            input("\n[!] Erreur : Votre KYC doit etre valide pour publier. Entree..."); return

        self._nettoyer_console()
        print("--- AJOUTER UN NOUVEAU PLAT ---")
        cats = self._catalogue_service.obtenir_toutes_categories()
        print("\nCATEGORIES DISPONIBLES :")
        for c in cats: print(f"ID {c['id']} : {c['libelle']}")
        
        try:
            titre = input("\nNom du plat : ")
            prix = float(input("Prix (DH) : "))
            cat_id = int(input("ID de la categorie choisie : "))
            desc = input("Description : ")
            
            if self._catalogue_service.ajouter_repas_au_catalogue(self._fournisseur, titre, prix, cat_id, desc):
                input("\n[OK] Plat ajoute avec succes !")
        except ValueError:
            input("\n[!] Erreur : Saisie numerique incorrecte. Entree...")

    def _formulaire_modification_repas(self):
        """Modification d'un plat existant."""
        try:
            id_p = int(input("\nID du plat a modifier : "))
            titre = input("Nouveau nom : ")
            prix = float(input("Nouveau prix : "))
            desc = input("Nouvelle description : ")
            cat_id = int(input("Nouvel ID categorie : "))
            
            if self._catalogue_service.modifier_plat(id_p, titre, prix, desc, cat_id):
                input("\n[OK] Modifications enregistrees !")
            else:
                input("\n[!] Erreur : Plat introuvable.")
        except ValueError:
            input("\n[!] Erreur de saisie.")

    def _formulaire_suppression_repas(self):
        """Suppression physique d'un plat."""
        try:
            id_p = int(input("\nID du plat a supprimer : "))
            confirm = input(f"Etes-vous sur de supprimer le plat #{id_p} ? (O/N) : ").upper()
            if confirm == 'O':
                if self._catalogue_service.supprimer_plat(id_p):
                    input("\n[OK] Plat retire definitivement.")
                else:
                    input("\n[!] Erreur : Suppression impossible (deja commande).")
        except ValueError:
            input("\n[!] ID invalide.")

    # --- SECTION 2 : FLUX DE PRODUCTION (Workflow) ---

    def _suivre_commandes_actives(self):
        """Affiche les commandes en cours avec les coordonnees de Yasmine."""
        self._nettoyer_console()
        print("="*75)
        print("      VOS COMMANDES ACTIVES (A PREPARER / LIVRER)")
        print("="*75)
        
        commandes = self._commande_service._commande_repo.recuperer_actives_fournisseur_avec_client(self._fournisseur.id)

        if not commandes:
            input("\nAucune commande active pour le moment. Entree..."); return

        for c in commandes:
            details = self._commande_service._commande_repo.recuperer_lignes_format_texte(c['id'])
            print(f"\n[COMMANDE #{c['id']}] - Etat : {c['statut']}")
            print(f" > CLIENT   : {c['client_nom']} (Tel: {c['client_tel']})")
            print(f" > ADRESSE  : {c['adresse_livraison']}")
            print(f" > ARTICLES : {details}")
            print(f" > TOTAL    : {c['montant_total']} DH")
            print("-" * 50)

        try:
            id_upd = int(input("\nID de la commande a mettre a jour (0 pour retour) : "))
            if id_upd == 0: return

            print("\nNouveau statut :")
            print("1. Accepter | 2. En preparation | 3. Prete | 4. Livree")
            
            s_choix = input("Choix : ")
            mapping = {
                '1': StatutCommande.ACCEPTE_CHEF,
                '2': StatutCommande.EN_PREPARATION,
                '3': StatutCommande.PRET_LIVRAISON,
                '4': StatutCommande.LIVRE
            }

            if s_choix in mapping:
                self._commande_service.mettre_a_jour_flux_travail(id_upd, mapping[s_choix])
                input("\n[OK] Statut mis a jour !")
        except ValueError:
            input("\n[!] ID invalide.")

    # --- SECTION 3 : FINANCES ET HISTORIQUE ---

    def _consulter_finances(self):
        """Affiche le solde actuel."""
        self._nettoyer_console()
        print("="*40)
        print("       SOLDE DE MON PORTEFEUILLE")
        print("="*40)
        print(f"Argent disponible : {self._fournisseur.solde} DH")
        print("\nNote : L'argent est libere par le client")
        print("apres confirmation de reception (Séquestre).")
        input("\nAppuyez sur Entree...")

    def _voir_historique_complet(self): # NOM SYNCHRONISE ICI
        """Liste de toutes les commandes (Terminees, Annulees, etc.)."""
        self._nettoyer_console()
        print("="*65)
        print("      HISTORIQUE COMPLET DE MES VENTES")
        print("="*65)
        history = self._commande_service._commande_repo.recuperer_historique_fournisseur(self._fournisseur.id)
        
        if not history:
            input("\nAucun historique disponible. Entree..."); return

        for h in history:
            items = self._commande_service._commande_repo.recuperer_lignes_format_texte(h['id'])
            print(f"#{h['id']} | {h['date_creation']} | {h['montant_total']} DH | [{h['statut']}]")
            print(f"  > Articles : {items}")
            print("-" * 50)
        input("\nAppuyez sur Entree pour revenir au menu...")

    def _soumettre_kyc_docs(self):
        self._nettoyer_console()
        print("--- MISE A JOUR DOSSIER KYC ---")
        doc = input("Entrez le nom ou lien du document justificatif : ")
        if doc:
            self._fournisseur.soumettre_kyc([doc])
            input("\n[INFO] Documents envoyes a l'Admin. Entree...")