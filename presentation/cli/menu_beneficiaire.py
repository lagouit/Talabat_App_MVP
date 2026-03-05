# presentation/cli/menu_beneficiaire.py

import os
from application.services.catalogue_service import CatalogueService
from application.services.commande_service import CommandeService
from core.entities.beneficiaire import Beneficiaire
from core.enums.statut_commande import StatutCommande

class MenuBeneficiaire:
    """
    Interface CLI pour les clients (Beneficiaires).
    Gere la recherche enrichie, le panier, l'historique et le profil.
    Responsable : Yasmine
    """

    def __init__(self, beneficiaire: Beneficiaire):
        self._beneficiaire = beneficiaire
        self._catalogue_service = CatalogueService()
        self._commande_service = CommandeService()
        self._panier = [] # Liste locale : [{'repas': Repas, 'quantite': int}]
        self._en_cours = True

    def _nettoyer_console(self):
        """Efface l'ecran pour une navigation fluide."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher(self):
        """Boucle principale de l'espace Client."""
        while self._en_cours:
            self._nettoyer_console()
            
            # APPEL UNIQUE : L'entite affiche ses options centralisees (p. 61)
            # Evite les doublons de menu et de "0. Deconnexion"
            self._beneficiaire.afficher_tableau_de_bord()
            
            choix = input("\nVotre choix : ")

            if choix == '1':
                self._explorer_catalogue_enrichi()
            elif choix == '2':
                self._afficher_panier()
            elif choix == '3':
                self._voir_historique_detaille()
            elif choix == '4':
                self._confirmer_reception_finale()
            elif choix == '5':
                self._modifier_coordonnees()
            elif choix == '0':
                self._en_cours = False
            else:
                input("[!] Choix invalide. Appuyez sur Entree...")

    # --- SECTION 1 : RECHERCHE ET CATALOGUE ---

    def _explorer_catalogue_enrichi(self):
        """Recherche par categorie et affichage des infos chefs + bio."""
        self._nettoyer_console()
        print("--- EXPLORATION DU CATALOGUE ---")
        print("1. Voir tout le catalogue")
        print("2. Filtrer par categorie")
        print("0. Retour")
        
        choix_rech = input("\nVotre choix : ")
        id_cat = None

        if choix_rech == '2':
            # Affichage de la liste des categories
            categories = self._catalogue_service.obtenir_toutes_categories()
            if not categories:
                print("\nAucune categorie creee par l'Admin.")
            else:
                print("\n--- CATEGORIES DISPONIBLES ---")
                for c in categories:
                    print(f"ID {c['id']} : {c['libelle']}")
                try:
                    id_cat = int(input("\nID de la categorie choisie : "))
                except ValueError:
                    input("\n[!] ID invalide. Affichage global...")

        # Recuperation des donnees (JOIN SQL : Nom Chef, Bio et Categorie)
        repas_liste = self._catalogue_service.obtenir_catalogue_public_detaille(id_cat)
        
        self._nettoyer_console()
        print("="*110)
        print(f"{'ID':<3} | {'PLAT':<18} | {'PRIX':<8} | {'CHEF':<12} | {'BIO DU CUISINIER'}")
        print("="*110)
        
        if not repas_liste:
            print("Aucun plat ne correspond a votre recherche.")
        else:
            for r in repas_liste:
                # On tronque la bio si elle est trop longue pour l'affichage
                bio = r['bio_chef'] if r['bio_chef'] else "Pas de description."
                print(f"{r['id']:<3} | {r['titre']:<18} | {float(r['prix']):<8.2f} | {r['nom_chef']:<12} | {bio[:50]}...")
        
        print("-" * 110)
        
        id_achat = input("\nID du plat pour ajouter au panier (ou Entree pour quitter) : ")
        if id_achat:
            try:
                id_p = int(id_achat)
                plat_elu_dict = next((r for r in repas_liste if r['id'] == id_p), None)
                if plat_elu_dict:
                    qte = int(input(f"Quantite pour '{plat_elu_dict['titre']}' : "))
                    if qte > 0:
                        # On reconstruit un objet Repas propre pour le panier
                        from core.entities.repas import Repas
                        obj_repas = Repas(plat_elu_dict['id'], plat_elu_dict['titre'], 
                                        float(plat_elu_dict['prix']), plat_elu_dict['fournisseur_id'], 0)
                        self._panier.append({'repas': obj_repas, 'quantite': qte})
                        input(f"\n[OK] {obj_repas.titre} ajoute au panier !")
                    else:
                        input("\n[!] Quantite invalide.")
                else:
                    input("\n[!] ID introuvable.")
            except ValueError:
                input("\n[!] Erreur de saisie.")

    # --- SECTION 2 : PANIER ET PAIEMENT ---

    def _afficher_panier(self):
        """Gestion du panier et déclenchement du paiement sequestre."""
        self._nettoyer_console()
        print("="*45)
        print("           MON PANIER ACTUEL")
        print("="*45)
        
        if not self._panier:
            input("\nVotre panier est vide. Entree pour retour...")
            return

        total = 0.0
        for i, item in enumerate(self._panier):
            st = float(item['repas'].prix) * item['quantite']
            total += st
            print(f"{i+1}. {item['repas'].titre} x{item['quantite']} = {st:.2f} DH")
        
        print("-" * 45)
        print(f"TOTAL A PAYER : {total:.2f} DH")
        print("\n1. Valider et Payer (Argent bloque en sequestre)")
        print("2. Vider le panier")
        print("0. Retour")
        
        choix = input("\nChoix : ")
        if choix == '1':
            # On utilise le fournisseur du premier plat
            chef_id = self._panier[0]['repas'].fournisseur_id
            if self._commande_service.initialiser_commande(self._beneficiaire.id, chef_id, self._panier):
                self._panier = []
                input("\n[SUCCES] Commande payee ! Fonds bloques par Talabat en sequestre.")
            else:
                input("\n[ERREUR] Echec lors de la transaction.")
        elif choix == '2':
            self._panier = []
            input("\nPanier vide.")

    # --- SECTION 3 : HISTORIQUE ET CONFIRMATION ---

    def _voir_historique_detaille(self):
        """Affiche les commandes avec le detail des noms de plats (Composition)."""
        self._nettoyer_console()
        print("--- HISTORIQUE DETAILLE DE MES COMMANDES ---")
        commandes = self._commande_service.obtenir_historique_detaille_client(self._beneficiaire.id)
        
        if not commandes:
            input("\nAucune commande enregistree. Entree...")
            return

        for c in commandes:
            print(f"\n[CMD #{c['id']}] Date: {c['date_creation']} | Statut: {c['statut']}")
            print(f" > Articles : {c['articles']}") # Affiche "Pizza x2, Tagine x1"
            print(f" > Total    : {float(c['montant_total']):.2f} DH")
            print("-" * 50)
        
        input("\nAppuyez sur Entree pour revenir...")

    def _confirmer_reception_finale(self):
        """Action cruciale : Libere l'argent du sequestre pour payer le chef."""
        self._nettoyer_console()
        print("--- COMMANDES LIVREES (ATTENTE CONFIRMATION) ---")
        a_valider = self._commande_service.obtenir_commandes_en_attente_confirmation(self._beneficiaire.id)
        
        if not a_valider:
            input("\nAucune commande a confirmer. (Le chef doit d'abord livrer). Entree..."); return

        print(f"{'ID':<5} | {'CHEF':<18} | {'TOTAL':<10} | {'DATE'}")
        print("-" * 55)
        for c in a_valider:
            print(f"{c['id']:<5} | {c['nom_fournisseur']:<18} | {float(c['montant_total']):<10.2f} | {c['date_creation'].strftime('%d/%m/%Y')}")

        try:
            id_cmd = int(input("\nEntrez l'ID de la commande recue (0 pour retour) : "))
            if id_cmd == 0: return
            
            cmd = next((c for c in a_valider if c['id'] == id_cmd), None)
            if cmd:
                confirm = input(f"\nConfirmez-vous la reception de chez {cmd['nom_fournisseur']} ? (OUI/NON) : ").upper()
                if confirm == 'OUI':
                    if self._commande_service.finaliser_reception_et_payer_chef(id_cmd, cmd['supplier_id'], float(cmd['montant_total'])):
                        print("\n[MERCI] Argent transfere au chef. Evaluez votre experience :")
                        note = int(input("Note (1 a 5) : "))
                        comm = input("Votre avis : ")
                        input(f"\n[OK] Merci pour votre evaluation ! Entree...")
            else:
                input("\n[!] ID incorrect ou commande non eligible.")
        except ValueError:
            input("\n[!] Saisie invalide.")

    # --- SECTION 4 : PROFIL ---

    def _modifier_coordonnees(self):
        """Modification de l'adresse et du telephone avec persistance MySQL."""
        self._nettoyer_console()
        print("--- MISE A JOUR DU PROFIL ---")
        print(f"Adresse actuelle : {self._beneficiaire.adresse_livraison}")
        print(f"Telephone actuel : {self._beneficiaire.telephone}")
        
        n_adr = input("\nNouvelle adresse (Entree pour garder) : ").strip() or self._beneficiaire.adresse_livraison
        n_tel = input("Nouveau telephone (Entree pour garder) : ").strip() or self._beneficiaire.telephone
        
        try:
            # 1. Mise a jour objet (Validation Domaine p. 28)
            self._beneficiaire.adresse_livraison = n_adr
            self._beneficiaire.telephone = n_tel
            
            # 2. Sauvegarde base de donnees (Infrastructure)
            if self._commande_service._user_repo.mettre_a_jour_profil_client(self._beneficiaire.id, n_adr, n_tel):
                input("\n[SUCCES] Profil mis a jour avec succes !")
        except ValueError as e:
            input(f"\n[ERREUR] {e}")