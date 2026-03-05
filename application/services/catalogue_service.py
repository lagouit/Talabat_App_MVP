# application/services/catalogue_service.py

from typing import List, Dict, Any, Optional
from core.entities.repas import Repas
from core.entities.fournisseur import Fournisseur
from infrastructure.repositories.repas_repo import RepasRepository

class CatalogueService:
    """
    Service gerant la logique du catalogue culinaire.
    Coordonne les actions entre les Repositories et les Menus CLI.
    Responsable : Equipe Talabat
    """

    def __init__(self):
        # Inversion de dependance : on utilise le repository pour la persistance
        self._repas_repo = RepasRepository()

    # --- SECTION 1 : GESTION DES CATEGORIES ---

    def obtenir_toutes_categories(self) -> List[Dict[str, Any]]:
        """Recupere la liste des categories (Marocain, Italien, etc.)."""
        return self._repas_repo.recuperer_toutes_categories()

    # --- SECTION 2 : LOGIQUE POUR NOUREDDINE (Fournisseur) ---

    def ajouter_repas_au_catalogue(self, fournisseur: Fournisseur, titre: str, 
                                   prix: float, id_categorie: int, 
                                   description: str = "") -> bool:
        """
        Action : Noureddine ajoute un plat.
        REGLE METIER : Le chef doit etre valide par l'Admin pour publier.
        """
        if not fournisseur.kyc_valide:
            print(f"\n[!] Blocage : {fournisseur.nom}, votre compte doit etre valide par l'Admin.")
            return False

        try:
            # Creation de l'objet metier
            nouveau_repas = Repas(
                id_repas=0, 
                titre=titre, 
                prix=prix, 
                fournisseur_id=fournisseur.id,
                categorie_id=id_categorie,
                description=description
            )
            # Sauvegarde SQL
            return self._repas_repo.ajouter(nouveau_repas)
        except ValueError as e:
            print(f"[ERREUR METIER] {e}")
            return False

    def obtenir_menu_fournisseur_detaille(self, supplier_id: int) -> List[Dict[str, Any]]:
        """Retourne les plats du chef avec les noms de categories."""
        return self._repas_repo.recuperer_par_fournisseur_detaille(supplier_id)

    def modifier_plat(self, id_p: int, titre: str, prix: float, desc: str, cat_id: int) -> bool:
        """Met a jour les informations d'un plat."""
        return self._repas_repo.mettre_a_jour(id_p, titre, prix, desc, cat_id)

    def supprimer_plat(self, id_p: int) -> bool:
        """Retire un plat du catalogue."""
        return self._repas_repo.supprimer(id_p)

    def gerer_stock_repas(self, repas_id: int, disponible: bool) -> bool:
        """Change la visibilite d'un plat dans le catalogue public."""
        return self._repas_repo.modifier_disponibilite(repas_id, disponible)

    # --- SECTION 3 : LOGIQUE POUR YASMINE (Client) ---

    def obtenir_catalogue_public_detaille(self, id_cat: int = None) -> List[Dict[str, Any]]:
        """
        Recupere le catalogue avec les infos de confiance (Nom chef + Bio).
        Applique un filtre si id_cat est fourni.
        """
        return self._repas_repo.recuperer_catalogue_avec_chef(id_cat)

    def trouver_plat_par_id(self, id_p: int) -> Optional[Repas]:
        """Retourne un objet Repas complet pour la creation d'une commande."""
        return self._repas_repo.trouver_par_id(id_p)