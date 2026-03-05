# core/entities/repas.py

from typing import Optional

class Repas:
    """
    Classe representant un plat/repas propose par un Fournisseur.
    C'est une entite de base du Domaine.
    Responsable : Noureddine
    """

    def __init__(self, id_repas: int, titre: str, prix: float, fournisseur_id: int, 
                 categorie_id: int, description: str = "", est_disponible: bool = True):
        self._id = id_repas
        self._fournisseur_id = fournisseur_id
        self._categorie_id = categorie_id
        self._description = description
        
        # --- CRUCIAL : On utilise les setters pour declencher la validation (p. 28) ---
        self.titre = titre           # Appelle @titre.setter
        self.prix = prix             # Appelle @prix.setter (C'est ici que le test passera)
        self.est_disponible = est_disponible # Appelle @est_disponible.setter

    # --- ENCAPSULATION (Getters/Setters avec @property) ---

    @property
    def id(self) -> int:
        return self._id

    @property
    def titre(self) -> str:
        return self._titre

    @titre.setter
    def titre(self, valeur: str):
        if not valeur or not valeur.strip():
            raise ValueError("Le titre du repas ne peut pas etre vide.")
        self._titre = valeur

    @property
    def prix(self) -> float:
        return self._prix

    @prix.setter
    def prix(self, valeur: float):
        # REGLE METIER : Un prix doit toujours etre positif
        if valeur <= 0:
            raise ValueError("Le prix doit etre un montant positif (en DH).")
        self._prix = valeur

    @property
    def est_disponible(self) -> bool:
        return self._est_disponible

    @est_disponible.setter
    def est_disponible(self, statut: bool):
        self._est_disponible = statut

    @property
    def fournisseur_id(self) -> int:
        return self._fournisseur_id

    @property
    def categorie_id(self) -> int:
        return self._categorie_id

    @property
    def description(self) -> str:
        return self._description

    # --- METHODES METIER ---

    def modifier_prix(self, nouveau_prix: float) -> None:
        """Permet a Noureddine de mettre a jour son tarif."""
        self.prix = nouveau_prix  # Utilise le setter pour la validation
        print(f"[CATALOGUE] Le prix de '{self._titre}' a ete mis a jour : {self._prix} DH")

    def basculer_disponibilite(self) -> None:
        """Active ou desactive le repas dans le catalogue en un clic."""
        self._est_disponible = not self._est_disponible
        etat = "disponible" if self._est_disponible else "indisponible"
        print(f"[CATALOGUE] Le repas '{self._titre}' est desormais {etat}.")

    def __str__(self) -> str:
        """Affichage formate pour le catalogue (CLI)."""
        dispo = "[O]" if self._est_disponible else "[X]"
        return f"{dispo} {self._id}: {self._titre} - {self._prix} DH"

    def __repr__(self) -> str:
        return f"Repas(id={self._id}, titre='{self._titre}', prix={self._prix})"