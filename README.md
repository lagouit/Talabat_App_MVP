# Talabat App - MVP ??

## ?? Présentation du Projet
Talabat est une plateforme de mise en relation pour la restauration artisanale à domicile. Ce projet vise à "ubériser" le secteur du fait-maison en connectant des **Cuisiniers Artisans (Fournisseurs)** et des **Clients (Bénéficiaires)**.

Ce projet a été réalisé dans le cadre de la formation **JOBINTECH (DXC Rabat)**.

### ?? Équipe de Développement
*   **Yasmine ELANBRI** : Pilotage du périmètre Bénéficiaire (Panier, Commandes, Séquestre).
*   **Noureddine LAGOUIT** : Pilotage du périmètre Fournisseur (KYC, Catalogue CRUD, Revenus).

---

## ??? Spécifications Techniques
L'application respecte les standards de l'industrie enseignés par le **Pr. Abdelhay HAQIQ** :

*   **Architecture Multi-couches (N-Tier)** : 
    1.  **Core (Domaine)** : Logique métier pure (Entités, Enums).
    2.  **Infrastructure** : Persistance (MySQL Repositories) et Design Patterns.
    3.  **Application (Services)** : Orchestration des flux de données.
    4.  **Présentation (CLI)** : Interface utilisateur en ligne de commande.
*   **Design Patterns Obligatoires** :
    *   **Singleton** : Instance unique de connexion à MySQL (`GestionnaireBDD`).
    *   **Factory** : Découplage de la création des objets (`FabriqueUtilisateur`, `FabriqueNotification`).
*   **Principes SOLID** : Forte cohésion, faible couplage, et encapsulation stricte.

---

## ?? Installation et Configuration

### Pré-requis
*   Python 3.10+
*   Serveur MySQL (WAMP, XAMPP ou MySQL Installer)

### Étapes
1. **Cloner le projet** :
   ```bash
   git clone https://github.com/lagouit/Talabat_App_MVP.git
   cd Talabat_App_MVP