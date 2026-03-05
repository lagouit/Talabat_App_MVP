# tests/test_entities.py
import pytest
from core.entities.repas import Repas
from core.entities.commande import Commande
from core.entities.beneficiaire import Beneficiaire

def test_repas_validation_prix():
    """Vérifie que l'encapsulation empêche un prix négatif (p. 28)."""
    with pytest.raises(ValueError):
        Repas(1, "Couscous", -10.0, 1, 1)

def test_calcul_total_commande():
    """Vérifie le calcul dynamique du montant total (Composition p. 40)."""
    cmd = Commande(1, beneficiaire_id=10, fournisseur_id=20)
    r1 = Repas(1, "Tagine", 80.0, 20, 1)
    r2 = Repas(2, "Thé", 15.0, 20, 1)
    
    cmd.ajouter_produit(r1, 2) # 160 DH
    cmd.ajouter_produit(r2, 1) # 15 DH
    
    assert cmd.montant_total == 175.0

def test_heritage_utilisateur():
    """Vérifie que le Bénéficiaire est bien une instance d'Utilisateur (p. 45)."""
    client = Beneficiaire(1, "Yasmine", "y@dxc.ma", "pass")
    from core.entities.utilisateur import Utilisateur
    assert isinstance(client, Utilisateur)