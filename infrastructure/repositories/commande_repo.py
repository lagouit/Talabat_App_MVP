# infrastructure/repositories/commande_repo.py

from infrastructure.database.gestionnaire_bdd import GestionnaireBDD
from core.entities.commande import Commande, LigneCommande
from core.enums.statut_commande import StatutCommande
from mysql.connector import Error
from typing import List, Dict, Any

class CommandeRepository:
    """
    Gere la persistance des Commandes, Lignes et Sequestres dans MySQL.
    Incorpore les jointures SQL pour les informations de contact et les stats.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Utilisation du Singleton (p. 211 du cours)
        self._db = GestionnaireBDD()

    # --- SECTION 1 : CREATION ET TRANSACTION (Yasmine) ---

    def sauvegarder_nouvelle_commande(self, commande: Commande, transaction_id: str) -> bool:
        """Enregistre Commande + Lignes + Sequestre dans une transaction atomique."""
        conn = self._db.connexion
        cursor = conn.cursor()
        try:
            # 1. Insertion Commande
            sql_cmd = "INSERT INTO Commandes (beneficiaire_id, supplier_id, montant_total, statut) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_cmd, (commande._beneficiaire_id, commande._fournisseur_id, commande.montant_total, commande.statut.name))
            commande_id = cursor.lastrowid

            # 2. Insertion Lignes (Composition p. 40)
            sql_line = "INSERT INTO LignesCommande (commande_id, repas_id, quantite, prix_unitaire_fixe) VALUES (%s, %s, %s, %s)"
            for ligne in commande._lignes:
                cursor.execute(sql_line, (commande_id, ligne._repas.id, ligne._quantite, ligne._prix_unitaire_fixe))

            # 3. Insertion Sequestre (est_bloque = 1)
            sql_seq = "INSERT INTO PaiementsSequestre (commande_id, transaction_id, montant, est_bloque) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_seq, (commande_id, transaction_id, commande.montant_total, True))

            conn.commit()
            return True
        except Error as e:
            conn.rollback()
            print(f"[REPO] Erreur transactionnelle : {e}")
            return False
        finally:
            cursor.close()

    # --- SECTION 2 : WORKFLOW ET SEQUESTRE (Workflow binome) ---

    def mettre_a_jour_statut(self, commande_id: int, nouveau_statut: StatutCommande) -> bool:
        """Modifie l'etat de la commande (ex: LIVRE, CONFIRME)."""
        cursor = self._db.connexion.cursor()
        try:
            cursor.execute("UPDATE Commandes SET statut = %s WHERE id = %s", (nouveau_statut.name, commande_id))
            self._db.connexion.commit()
            return True
        except Error:
            return False
        finally:
            cursor.close()

    def liberer_fonds_sequestre(self, commande_id: int) -> bool:
        """Passe le paiement de bloque a libre dans MySQL (Action Yasmine)."""
        cursor = self._db.connexion.cursor()
        try:
            cursor.execute("UPDATE PaiementsSequestre SET est_bloque = 0 WHERE commande_id = %s", (commande_id,))
            self._db.connexion.commit()
            return True
        except Error:
            return False
        finally:
            cursor.close()

    # --- SECTION 3 : VUES NOUREDDINE (Cuisinier) ---

    def recuperer_actives_fournisseur_avec_client(self, supplier_id: int) -> List[Dict[str, Any]]:
        """Recupere les commandes en cours avec Nom, Tel et Adresse du client."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT c.id, c.montant_total, c.statut, c.date_creation,
                   u.nom as client_nom, b.telephone as client_tel, b.adresse_livraison
            FROM Commandes c
            JOIN Utilisateurs u ON c.beneficiaire_id = u.id
            JOIN Beneficiaires b ON c.beneficiaire_id = b.user_id
            WHERE c.supplier_id = %s AND c.statut NOT IN ('CONFIRME', 'ANNULE')
            ORDER BY c.date_creation ASC
        """
        cursor.execute(sql, (supplier_id,))
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total']) # Securite type
        cursor.close()
        return rows

    def recuperer_historique_fournisseur(self, supplier_id: int):
        cursor = self._db.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Commandes WHERE supplier_id = %s ORDER BY date_creation DESC", (supplier_id,))
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total'])
        cursor.close()
        return rows

    # --- SECTION 4 : VUES YASMINE (Client) ---

    def recuperer_commandes_beneficiaire(self, beneficiary_id: int):
        cursor = self._db.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Commandes WHERE beneficiaire_id = %s ORDER BY date_creation DESC", (beneficiary_id,))
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total'])
        cursor.close()
        return rows

    def recuperer_commandes_a_confirmer_par_client(self, client_id: int) -> List[Dict[str, Any]]:
        """Liste les commandes LIVREES pour que Yasmine valide le paiement."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT c.id, u.nom as nom_fournisseur, c.montant_total, c.date_creation, c.supplier_id
            FROM Commandes c
            JOIN Utilisateurs u ON c.supplier_id = u.id
            WHERE c.beneficiaire_id = %s AND c.statut = 'LIVRE'
        """
        cursor.execute(sql, (client_id,))
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total'])
        cursor.close()
        return rows

    # --- SECTION 5 : VUES ADMIN (Stats et Details) ---

    def calculer_volume_total(self) -> float:
        """Somme de toutes les ventes (FIX : Cast float pour eviter erreur Decimal)."""
        cursor = self._db.connexion.cursor()
        sql = "SELECT SUM(montant_total) FROM Commandes WHERE statut NOT IN ('ATTENTE_PAIEMENT', 'ANNULE')"
        cursor.execute(sql)
        res = cursor.fetchone()
        cursor.close()
        if res and res[0] is not None:
            return float(res[0])
        return 0.0

    def recuperer_tout_par_statut_detaille(self, statut_name: str) -> List[Dict[str, Any]]:
        """Vue Admin avec noms Client et Chef via JOIN SQL."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT c.id, u_b.nom as nom_client, u_s.nom as nom_fournisseur, 
                   c.montant_total, c.date_creation, c.statut
            FROM Commandes c
            JOIN Utilisateurs u_b ON c.beneficiaire_id = u_b.id
            JOIN Utilisateurs u_s ON c.supplier_id = u_s.id
            WHERE c.statut = %s ORDER BY c.date_creation DESC
        """
        cursor.execute(sql, (statut_name,))
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total'])
        cursor.close()
        return rows

    def recuperer_lignes_format_texte(self, commande_id: int) -> str:
        """Transforme les articles d'une commande en chaine (ex: Tagine x2)."""
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = """
            SELECT r.titre, lc.quantite 
            FROM LignesCommande lc
            JOIN Repas r ON lc.repas_id = r.id
            WHERE lc.commande_id = %s
        """
        cursor.execute(sql, (commande_id,))
        lignes = cursor.fetchall()
        cursor.close()
        return ", ".join([f"{l['titre']} (x{l['quantite']})" for l in lignes])

    def recuperer_commandes_pour_litige(self):
        cursor = self._db.connexion.cursor(dictionary=True)
        sql = "SELECT * FROM Commandes WHERE statut NOT IN ('CONFIRME', 'ANNULE', 'ATTENTE_PAIEMENT')"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for r in rows: r['montant_total'] = float(r['montant_total'])
        cursor.close()
        return rows