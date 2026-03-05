# tests/test_services.py
from core.entities.fournisseur import Fournisseur
from core.entities.paiement_sequestre import PaiementSequestre

def test_logique_sequestre():
    """Teste le cycle de vie du paiement (Sécurité financière)."""
    p = PaiementSequestre("TRX-123", 200.0, commande_id=1)
    
    # 1. Au début, l'argent est bloqué
    assert p.est_bloque is True
    
    # 2. Libération des fonds
    p.liberer_fonds()
    assert p.est_bloque is False
    
    # 3. Vérification qu'on ne peut pas libérer deux fois
    assert p.liberer_fonds() is False

def test_solde_fournisseur_apres_revenu():
    """Vérifie que le solde de Noureddine augmente correctement."""
    chef = Fournisseur(1, "Noureddine", "n@mail.com", "pass")
    initial_solde = chef.solde
    chef.ajouter_revenu(150.0)
    assert chef.solde == initial_solde + 150.0