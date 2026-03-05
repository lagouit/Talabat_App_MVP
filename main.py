# ============================================================
# PROJET : Talabat_App_MVP
# RÔLE : Point d'entrée principal (Main Entry Point)
# ÉQUIPE : Yasmine ELANBRI & Noureddine LAGOUIT
# FORMATION : JOBINTECH - Développement Logiciel DXC
# ============================================================

import sys
from presentation.cli.menu_principal import MenuPrincipal
from infrastructure.database.gestionnaire_bdd import GestionnaireBDD

def demarrer_application():
    """
    Initialise les composants critiques et lance l'interface utilisateur.
    Gère le cycle de vie global de l'application.
    """
    print("[SYSTEME] Initialisation de Talabat App...")
    
    # 1. Initialisation du Singleton de la Base de Données
    # On force une première connexion pour vérifier que MySQL est actif
    db_manager = GestionnaireBDD()
    
    if db_manager.connexion is None:
        print("[ERREUR CRITIQUE] Impossible de se connecter à la base de données.")
        print("[CONSEIL] Vérifiez que MySQL est lancé et que le fichier .env est correct.")
        sys.exit(1)

    # 2. Instanciation du Menu Principal (Couche Présentation)
    app = MenuPrincipal()

    try:
        # 3. Lancement de la boucle principale
        app.run()
    
    except KeyboardInterrupt:
        # Gère le CTRL+C proprement
        print("\n\n[SYSTEME] Fermeture forcée par l'utilisateur.")
    
    except Exception as e:
        print(f"\n[ERREUR FATALE] Une erreur inattendue est survenue : {e}")
    
    finally:
        # 4. Nettoyage et fermeture des ressources (Singleton)
        print("[SYSTEME] Libération des ressources...")
        db_manager.fermer_connexion()
        print("[SYSTEME] Application fermée avec succès. Au revoir !")

if __name__ == "__main__":
    demarrer_application()
