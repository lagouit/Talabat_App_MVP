# core/entities/commande.py

from datetime import datetime
from typing import List
from core.entities.repas import Repas
from core.enums.statut_commande import StatutCommande

class LigneCommande:
    """
    Classe représentant une ligne spécifique dans une commande.
    Relation : COMPOSITION FORTE avec Commande (p. 40).
    """
    def __init__(self, repas: Repas, quantite: int):
        self._repas = repas
        self._quantite = quantite
        # RÈGLE MÉTIER : On fixe le prix au moment de l'achat 
        # pour protéger la commande si le fournisseur change ses prix plus tard.
        self._prix_unitaire_fixe = repas.prix

    @property
    def sous_total(self) -> float:
        return self._prix_unitaire_fixe * self._quantite

    def __str__(self) -> str:
        return f"{self._repas.titre} x{self._quantite} ({self._prix_unitaire_fixe} DH/u)"


class Commande:
    """
    Classe représentant une Commande sur Talabat.
    Gère le cycle de vie et le calcul du montant total.
    """

    def __init__(self, id_commande: int, beneficiaire_id: int, fournisseur_id: int):
        self._id = id_commande
        self._beneficiaire_id = beneficiaire_id
        self._fournisseur_id = fournisseur_id
        self._date_creation = datetime.now()
        self._statut = StatutCommande.ATTENTE_PAIEMENT
        
        # Initialisation de la collection pour la Composition (p. 40)
        self._lignes: List[LigneCommande] = []

    # --- ENCAPSULATION ---

    @property
    def id(self) -> int:
        return self._id

    @property
    def statut(self) -> StatutCommande:
        return self._statut

    @property
    def montant_total(self) -> float:
        """Calcule dynamiquement le total de la commande (Somme des lignes)."""
        return sum(ligne.sous_total for ligne in self._lignes)

    # --- MÉTHODES MÉTIER ---

    def ajouter_produit(self, repas: Repas, quantite: int) -> None:
        """
        Implémentation de la COMPOSITION FORTE :
        L'objet LigneCommande est instancié à l'INTÉRIEUR de Commande.
        """
        if quantite <= 0:
            raise ValueError("La quantité doit être supérieure à 0.")
        
        if not repas.est_disponible:
            raise ValueError(f"Le repas '{repas.titre}' n'est plus disponible.")

        # Création de l'objet composé
        nouvelle_ligne = LigneCommande(repas, quantite)
        self._lignes.append(nouvelle_ligne)

    def changer_statut(self, nouveau_statut: StatutCommande) -> None:
        """
        Gère la transition des états (Workflow de Noureddine et Yasmine).
        Ex: On ne peut pas livrer si ce n'est pas payé.
        """
        self._statut = nouveau_statut
        print(f"[LOG] Commande #{self._id} passée au statut : {self._statut.value}")

    def obtenir_recapitulatif(self) -> str:
        """Génère une facture textuelle pour la console (CLI)."""
        lignes_str = "\n".join([f"  - {str(l)}" for l in self._lignes])
        date_fmt = self._date_creation.strftime("%d/%m/%Y %H:%M")
        
        return (
            f"==================================\n"
            f"COMMANDE #{self._id} - {date_fmt}\n"
            f"Statut : {self._statut.value}\n"
            f"----------------------------------\n"
            f"{lignes_str}\n"
            f"----------------------------------\n"
            f"TOTAL À PAYER : {self.montant_total} DH\n"
            f"=================================="
        )