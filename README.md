# Talabat App - MVP ??

## ?? Pr�sentation du Projet
Talabat est une plateforme de mise en relation pour la restauration artisanale � domicile. Ce projet vise � "ub�riser" le secteur du fait-maison en connectant des **Cuisiniers Artisans (Fournisseurs)** et des **Clients (B�n�ficiaires)**.

Ce projet a �t� r�alis� dans le cadre de la formation **JOBINTECH (DXC Rabat)**.

### ?? �quipe de D�veloppement
*   **Yasmine ELANBRI** : Pilotage du p�rim�tre B�n�ficiaire (Panier, Commandes, S�questre).
*   **Noureddine LAGOUIT** : Pilotage du p�rim�tre Fournisseur (KYC, Catalogue CRUD, Revenus).

---

## ??? Sp�cifications Techniques
L'application respecte les standards de l'industrie enseign�s par le **Pr. Abdelhay HAQIQ** :

*   **Architecture Multi-couches (N-Tier)** : 
    1.  **Core (Domaine)** : Logique m�tier pure (Entit�s, Enums).
    2.  **Infrastructure** : Persistance (MySQL Repositories) et Design Patterns.
    3.  **Application (Services)** : Orchestration des flux de donn�es.
    4.  **Pr�sentation (CLI)** : Interface utilisateur en ligne de commande.
*   **Design Patterns Obligatoires** :
    *   **Singleton** : Instance unique de connexion � MySQL (`GestionnaireBDD`).
    *   **Factory** : D�couplage de la cr�ation des objets (`FabriqueUtilisateur`, `FabriqueNotification`).
*   **Principes SOLID** : Forte coh�sion, faible couplage, et encapsulation stricte.

---

## ?? Installation et Configuration

### Pr�-requis
*   Python 3.10+
*   Serveur MySQL (WAMP, XAMPP ou MySQL Installer)

### �tapes
1. **Cloner le projet** :
   ```bash
   git clone https://github.com/lagouit/Talabat_App_MVP.git
   cd Talabat_App_MVP
