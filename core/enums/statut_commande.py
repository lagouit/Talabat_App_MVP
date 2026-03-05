# core/enums/statut_commande.py

from enum import Enum

class StatutCommande(Enum):
    """
    Énumération représentant les différents états du cycle de vie d'une commande.
    Permet de sécuriser les transitions d'état dans CommandeService.
    """
    
    # Étape initiale
    ATTENTE_PAIEMENT = "En attente de paiement"
    
    # Étape du séquestre (Argent bloqué par le système)
    PAYE_SEQUESTRE = "Payée (Fonds bloqués)"
    
    # Workflow du Fournisseur (Noureddine)
    ACCEPTE_CHEF = "Acceptée par le chef"
    EN_PREPARATION = "En cours de préparation"
    PRET_LIVRAISON = "Prête pour livraison"
    
    # Workflow du Bénéficiaire (Yasmine)
    LIVRE = "Livrée (Attente confirmation)"
    
    # Étape finale (Libération des fonds)
    CONFIRME = "Réception confirmée (Terminée)"
    
    # Cas exceptionnel
    ANNULE = "Annulée"

    @classmethod
    def obtenir_tous_les_libelles(cls):
        """Retourne la liste des descriptions lisibles."""
        return [statut.value for statut in cls]

    def __str__(self):
        return self.value