# presentation/cli/menu_principal.py

import os
import sys
from application.services.auth_service import AuthService
from core.enums.type_utilisateur import TypeUtilisateur
from presentation.cli.menu_beneficiaire import MenuBeneficiaire
from presentation.cli.menu_fournisseur import MenuFournisseur
from presentation.cli.menu_admin import MenuAdmin

class MenuPrincipal:
    """
    Interface en ligne de commande (CLI) principale de l'application Talabat.
    Responsable de l'accueil, de l'inscription et de l'authentification.
    """

    def __init__(self):
        self._auth_service = AuthService()
        self._en_cours = True

    def _nettoyer_console(self):
        """Efface le texte de la console selon le système d'exploitation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _afficher_banniere(self):
        print("="*45)
        print("       TALABAT - RESTAURATION ARTISANALE")
        print("      Formation JobInTech - Projet MVP")
        print("="*45)

    def run(self):
        """Boucle principale du menu d'accueil."""
        while self._en_cours:
            self._nettoyer_console()
            self._afficher_banniere()
            print("1. Se connecter")
            print("2. Créer un compte Client (Bénéficiaire)")
            print("3. Devenir Cuisinier (Fournisseur)")
            print("q. Quitter l'application")
            print("-" * 45)
            
            choix = input("Votre choix : ").lower()

            if choix == '1':
                self._menu_connexion()
            elif choix == '2':
                self._menu_inscription(TypeUtilisateur.BENEFICIAIRE)
            elif choix == '3':
                self._menu_inscription(TypeUtilisateur.FOURNISSEUR)
            elif choix == 'q':
                print("\n[SYSTÈME] Merci d'avoir utilisé Talabat. À bientôt !")
                self._en_cours = False
            else:
                input("\n[!] Choix invalide. Appuyez sur Entrée...")

    def _menu_connexion(self):
        """Gère la saisie des identifiants et la redirection par rôle."""
        self._nettoyer_console()
        print("--- CONNEXION ---")
        email = input("Email : ")
        mdp = input("Mot de passe : ")

        user = self._auth_service.se_connecter(email, mdp)

        if user:
            input(f"\n[SUCCÈS] Connexion réussie. Bienvenue {user.nom} !")
            self._rediriger_vers_espace_role(user)
        else:
            input("\n[ERREUR] Identifiants incorrects. Appuyez sur Entrée...")

    def _menu_inscription(self, type_u: TypeUtilisateur):
        """Collecte les informations et délègue l'inscription au service."""
        self._nettoyer_console()
        print(f"--- INSCRIPTION ({type_u.value}) ---")
        
        infos = {
            "nom": input("Nom complet : "),
            "email": input("Email : "),
            "mot_de_passe": input("Mot de passe : ")
        }

        # Champs spécifiques selon le rôle (p. 45 - Héritage)
        if type_u == TypeUtilisateur.BENEFICIAIRE:
            infos["adresse_livraison"] = input("Adresse de livraison : ")
            infos["telephone"] = input("Téléphone (06...) : ")
        
        elif type_u == TypeUtilisateur.FOURNISSEUR:
            infos["biographie"] = input("Parlez-nous de votre cuisine (Bio) : ")

        if self._auth_service.sinscrire(type_u, infos):
            input("\n[SUCCÈS] Compte créé ! Vous pouvez maintenant vous connecter.")
        else:
            input("\n[ERREUR] L'inscription a échoué. L'email est peut-être déjà utilisé.")

    def _rediriger_vers_espace_role(self, user):
        """
        Délègue l'affichage au menu spécifique selon le rôle.
        C'est une forme de polymorphisme dans la couche présentation.
        """
        if user.type_utilisateur == TypeUtilisateur.BENEFICIAIRE:
            MenuBeneficiaire(user).afficher()
        elif user.type_utilisateur == TypeUtilisateur.FOURNISSEUR:
            MenuFournisseur(user).afficher()
        elif user.type_utilisateur == TypeUtilisateur.ADMIN:
            MenuAdmin(user).afficher()
        
        # Une fois déconnecté de l'espace rôle, on revient ici
        self._auth_service.se_deconnecter()

if __name__ == "__main__":
    app = MenuPrincipal()
    app.run()