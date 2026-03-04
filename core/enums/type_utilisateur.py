# core/enums/type_utilisateur.py

from enum import Enum

class TypeUtilisateur(Enum):
    """
    Énumération définissant les rôles critiques au sein de la plateforme Talabat.
    Assure la cohérence entre la base de données MySQL et la logique Python.
    """
    
    ADMIN = "ADMIN"
    FOURNISSEUR = "FOURNISSEUR"
    BENEFICIAIRE = "BENEFICIAIRE"

    @classmethod
    def depuis_chaine(cls, label: str):
        """
        Permet de convertir une chaîne (ex: issue de la BDD) en membre de l'Enum.
        Utile pour la FabriqueUtilisateur.
        """
        try:
            return cls[label.upper()]
        except KeyError:
            raise ValueError(f"Rôle utilisateur '{label}' non reconnu par le système.")

    def __str__(self):
        return self.value