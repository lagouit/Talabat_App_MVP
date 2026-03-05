# tests/test_infrastructure.py
from infrastructure.database.gestionnaire_bdd import GestionnaireBDD
from infrastructure.factories.fabrique_utilisateur import FabriqueUtilisateur
from core.enums.type_utilisateur import TypeUtilisateur
from core.entities.fournisseur import Fournisseur

def test_singleton_bdd():
    """Vérifie que le Singleton garantit une instance unique (p. 211)."""
    db1 = GestionnaireBDD()
    db2 = GestionnaireBDD()
    assert db1 is db2

def test_factory_fournisseur():
    """Vérifie que la Factory crée la bonne sous-classe (p. 214)."""
    data = {"id": 1, "nom": "Noureddine", "email": "n@chef.ma", "mot_de_passe": "123"}
    user = FabriqueUtilisateur.creer_utilisateur(TypeUtilisateur.FOURNISSEUR, data)
    assert isinstance(user, Fournisseur)
    assert user.type_utilisateur == TypeUtilisateur.FOURNISSEUR