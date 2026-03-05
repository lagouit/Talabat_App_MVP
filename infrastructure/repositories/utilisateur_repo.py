# infrastructure/repositories/utilisateur_repo.py

from infrastructure.database.gestionnaire_bdd import GestionnaireBDD
from infrastructure.factories.fabrique_utilisateur import FabriqueUtilisateur
from core.enums.type_utilisateur import TypeUtilisateur
from mysql.connector import Error

class UtilisateurRepository:
    """
    Gere la persistance des Utilisateurs (Admin, Fournisseur, Beneficiaire).
    Gere l'heritage SQL et les mises a jour de profil.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Utilisation du Singleton pour la connexion (p. 211)
        self._db = GestionnaireBDD()

    # --- SECTION 1 : RECHERCHE (AUTHENTIFICATION & MODERATION) ---

    def trouver_par_email(self, email: str):
        """Recherche pour le Login."""
        return self._rechercher_unique("u.email = %s", (email,))

    def trouver_par_id(self, user_id: int):
        """Recherche pour la moderation ou recuperation profil."""
        return self._rechercher_unique("u.id = %s", (user_id,))

    def _rechercher_unique(self, clause_where: str, params: tuple):
        """Methode privee pour factoriser les requetes avec jointures SQL."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = f"""
            SELECT u.*, b.adresse_livraison, b.telephone, f.biographie, f.kyc_valide, f.solde_accumule
            FROM Utilisateurs u
            LEFT JOIN Beneficiaires b ON u.id = b.user_id
            LEFT JOIN Fournisseurs f ON u.id = f.user_id
            WHERE {clause_where}
        """
        try:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row:
                type_u = TypeUtilisateur.depuis_chaine(row['type_utilisateur'])
                # Reconstructon de l'objet via la Factory (p. 214)
                return FabriqueUtilisateur.creer_utilisateur(type_u, row)
            return None
        finally:
            cursor.close()

    # --- SECTION 2 : SAUVEGARDE ET MISE A JOUR ---

    def sauvegarder(self, utilisateur) -> bool:
        """Enregistre un nouvel utilisateur avec gestion de transaction SQL."""
        conn = self._db.connexion
        cursor = conn.cursor()
        try:
            # 1. Insertion table parente (Utilise le vrai mot de passe)
            sql_base = """
                INSERT INTO Utilisateurs (nom, email, mot_de_passe, type_utilisateur) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_base, (
                utilisateur.nom, 
                utilisateur.email, 
                utilisateur.mot_de_passe, 
                utilisateur.type_utilisateur.value
            ))
            user_id = cursor.lastrowid

            # 2. Insertion table enfant (Heritage p. 45)
            if utilisateur.type_utilisateur == TypeUtilisateur.BENEFICIAIRE:
                sql = "INSERT INTO Beneficiaires (user_id, adresse_livraison, telephone) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, utilisateur.adresse_livraison, utilisateur.telephone))
            
            elif utilisateur.type_utilisateur == TypeUtilisateur.FOURNISSEUR:
                sql = "INSERT INTO Fournisseurs (user_id, biographie) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, utilisateur.biographie))

            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print(f"[REPO] Erreur sauvegarde : {e}")
            return False
        finally:
            cursor.close()

    def mettre_a_jour_profil_client(self, user_id: int, adresse: str, tel: str) -> bool:
        """Permet a Yasmine de modifier ses informations de livraison."""
        cursor = self._db.connexion.cursor()
        sql = "UPDATE Beneficiaires SET adresse_livraison = %s, telephone = %s WHERE user_id = %s"
        try:
            cursor.execute(sql, (adresse, tel, user_id))
            self._db.connexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def mettre_a_jour_statut_kyc(self, fournisseur_id: int, statut: bool) -> bool:
        """Active ou bloque un compte cuisinier (Action Admin)."""
        cursor = self._db.connexion.cursor()
        sql = "UPDATE Fournisseurs SET kyc_valide = %s WHERE user_id = %s"
        try:
            cursor.execute(sql, (statut, fournisseur_id))
            self._db.connexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def mettre_a_jour_solde(self, fournisseur_id: int, nouveau_solde: float):
        """Met a jour les revenus reels de Noureddine apres liberation du sequestre."""
        cursor = self._db.connexion.cursor()
        sql = "UPDATE Fournisseurs SET solde_accumule = %s WHERE user_id = %s"
        try:
            cursor.execute(sql, (nouveau_solde, fournisseur_id))
            self._db.connexion.commit()
        finally:
            cursor.close()

    # --- SECTION 3 : LISTES DE SUPERVISION (ADMIN) ---

    def recuperer_fournisseurs_en_attente(self):
        """Liste pour la moderation KYC."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT u.id, u.nom, u.email 
            FROM Utilisateurs u 
            JOIN Fournisseurs f ON u.id = f.user_id 
            WHERE f.kyc_valide = 0
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def recuperer_tous_fournisseurs(self):
        """Liste complete des chefs pour l'annuaire Admin."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT u.id, u.nom, u.email, f.kyc_valide, f.solde_accumule 
            FROM Utilisateurs u 
            JOIN Fournisseurs f ON u.id = f.user_id
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def recuperer_tous_beneficiaires(self):
        """Liste complete des clients pour l'annuaire Admin."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT u.id, u.nom, u.email, b.telephone, b.adresse_livraison 
            FROM Utilisateurs u 
            JOIN Beneficiaires b ON u.id = b.user_id
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res

    def compter_par_type(self, type_u: TypeUtilisateur) -> int:
        """Statistiques pour le dashboard."""
        cursor = self._db.connexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Utilisateurs WHERE type_utilisateur = %s", (type_u.value,))
        res = cursor.fetchone()[0]
        cursor.close()
        return res