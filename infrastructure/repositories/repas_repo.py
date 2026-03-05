# infrastructure/repositories/repas_repo.py

from infrastructure.database.gestionnaire_bdd import GestionnaireBDD
from core.entities.repas import Repas
from mysql.connector import Error
from typing import List, Optional, Dict, Any

class RepasRepository:
    """
    Gere la persistance des Repas et des Categories dans MySQL.
    Force la conversion des types DECIMAL en FLOAT pour eviter les crashs.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Utilisation du Singleton (p. 211 du cours)
        self._db = GestionnaireBDD()

    # --- SECTION 1 : CRUD REPAS (Noureddine) ---

    def ajouter(self, repas: Repas) -> bool:
        """Enregistre un nouveau plat."""
        cursor = self._db.connexion.cursor()
        sql = """
            INSERT INTO Repas (fournisseur_id, categorie_id, titre, description, prix, est_disponible)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                repas.fournisseur_id,
                repas.categorie_id,
                repas.titre,
                repas.description,
                repas.prix,
                repas.est_disponible
            ))
            self._db.connexion.commit()
            return True
        except Error as e:
            print(f"[REPO] Erreur ajout repas : {e}")
            return False
        finally:
            cursor.close()

    def recuperer_par_fournisseur_detaille(self, supplier_id: int) -> List[Dict[str, Any]]:
        """Recupere les plats d'un chef avec le libelle de la categorie."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT r.*, c.libelle as nom_cat 
            FROM Repas r
            JOIN Categories c ON r.categorie_id = c.id
            WHERE r.fournisseur_id = %s
        """
        try:
            cursor.execute(sql, (supplier_id,))
            rows = cursor.fetchall()
            # Conversion de securite pour les calculs Python
            for row in rows:
                row['prix'] = float(row['prix'])
            return rows
        finally:
            cursor.close()

    def mettre_a_jour(self, r_id: int, titre: str, prix: float, desc: str, cat_id: int) -> bool:
        """Modifie les informations d'un plat."""
        cursor = self._db.connexion.cursor()
        sql = "UPDATE Repas SET titre=%s, prix=%s, description=%s, categorie_id=%s WHERE id=%s"
        try:
            cursor.execute(sql, (titre, prix, desc, cat_id, r_id))
            self._db.connexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def supprimer(self, repas_id: int) -> bool:
        """Supprime un plat du catalogue."""
        cursor = self._db.connexion.cursor()
        try:
            cursor.execute("DELETE FROM Repas WHERE id = %s", (repas_id,))
            self._db.connexion.commit()
            return cursor.rowcount > 0
        except Error:
            return False
        finally:
            cursor.close()

    def modifier_disponibilite(self, repas_id: int, statut: bool) -> bool:
        cursor = self._db.connexion.cursor()
        try:
            cursor.execute("UPDATE Repas SET est_disponible = %s WHERE id = %s", (statut, repas_id))
            self._db.connexion.commit()
            return True
        finally:
            cursor.close()

    # --- SECTION 2 : CATALOGUE ENRICHI (Yasmine) ---

    def recuperer_catalogue_avec_chef(self, categorie_id: int = None) -> List[Dict[str, Any]]:
        """
        Recupere les plats avec Nom du chef, Bio et Categorie.
        FIX : Convertit le type DECIMAL de MySQL en FLOAT Python.
        """
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT r.id, r.titre, r.prix, r.description, r.fournisseur_id,
                   u.nom as nom_chef, f.biographie as bio_chef, c.libelle as nom_cat
            FROM Repas r
            JOIN Utilisateurs u ON r.fournisseur_id = u.id
            JOIN Fournisseurs f ON r.fournisseur_id = f.user_id
            JOIN Categories c ON r.categorie_id = c.id
            WHERE r.est_disponible = 1
        """
        try:
            if categorie_id:
                sql += " AND r.categorie_id = %s"
                cursor.execute(sql, (categorie_id,))
            else:
                cursor.execute(sql)
            
            rows = cursor.fetchall()
            # CRUCIAL : Conversion pour eviter l'erreur 'float + Decimal'
            for row in rows:
                row['prix'] = float(row['prix'])
            return rows
        finally:
            cursor.close()

    # --- SECTION 3 : GESTION DES CATEGORIES (Admin) ---

    def recuperer_toutes_categories(self) -> List[Dict[str, Any]]:
        cursor = self._db.connexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Categories ORDER BY libelle")
            return cursor.fetchall()
        finally:
            cursor.close()

    def ajouter_categorie(self, libelle: str) -> bool:
        cursor = self._db.connexion.cursor()
        try:
            cursor.execute("INSERT INTO Categories (libelle) VALUES (%s)", (libelle,))
            self._db.connexion.commit()
            return True
        except Error:
            return False
        finally:
            cursor.close()

    # --- HELPER : MAPPING ---

    def trouver_par_id(self, repas_id: int) -> Optional[Repas]:
        cursor = self._db.connexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Repas WHERE id = %s", (repas_id,))
            row = cursor.fetchone()
            return self._mapper_en_objet(row) if row else None
        finally:
            cursor.close()

    def _mapper_en_objet(self, row: dict) -> Repas:
        """Helper pour transformer une ligne SQL en objet avec prix en float."""
        return Repas(
            id_repas=row['id'],
            titre=row['titre'],
            prix=float(row['prix']), # Securite de type
            fournisseur_id=row['fournisseur_id'],
            categorie_id=row['categorie_id'],
            description=row['description'],
            est_disponible=bool(row['est_disponible'])
        )