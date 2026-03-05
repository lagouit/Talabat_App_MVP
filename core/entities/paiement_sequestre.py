# core/entities/paiement_sequestre.py

from datetime import datetime

class PaiementSequestre:
    """
    Classe gérant la logique du Séquestre (Escrow).
    Garantit que les fonds sont bloqués jusqu'à la confirmation de livraison.
    Relation : 1-1 avec la classe Commande.
    """

    def __init__(self, transaction_id: str, montant: float, commande_id: int):
        self._transaction_id = transaction_id
        self._montant = montant
        self._commande_id = commande_id
        self._date_paiement = datetime.now()
        
        # État du séquestre (Encapsulation - p. 22)
        self.__est_bloque = True 
        self.__est_rembourse = False
        self.__date_liberation = None

    # --- ENCAPSULATION (@property - p. 28) ---

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def montant(self) -> float:
        return self._montant

    @property
    def est_bloque(self) -> bool:
        """Indique si l'argent est encore en séquestre."""
        return self.__est_bloque

    @property
    def est_rembourse(self) -> bool:
        return self.__est_rembourse

    # --- MÉTHODES MÉTIER (Cœur du système Talabat) ---

    def bloquer_fonds(self) -> None:
        """Initialise le blocage des fonds lors du paiement par le Bénéficiaire."""
        self.__est_bloque = True
        print(f"[SÉQUESTRE] Transaction {self._transaction_id} : {self._montant} DH bloqués pour la commande #{self._commande_id}.")

    def liberer_fonds(self) -> bool:
        """
        Débloque l'argent pour le verser au Fournisseur.
        Appelée quand Yasmine confirme la réception (p. 61 - Polymorphisme).
        """
        if not self.__est_bloque:
            print("[SÉQUESTRE] Erreur : Les fonds ont déjà été libérés ou remboursés.")
            return False
        
        if self.__est_rembourse:
            print("[SÉQUESTRE] Erreur : Impossible de libérer des fonds déjà remboursés.")
            return False

        self.__est_bloque = False
        self.__date_liberation = datetime.now()
        print(f"[SÉQUESTRE] SUCCÈS : {self._montant} DH ont été transférés au fournisseur.")
        return True

    def rembourser(self) -> bool:
        """
        Rend l'argent au Bénéficiaire en cas d'annulation ou de litige.
        Utilisée par l'Administrateur (p. 21 - Visibilité).
        """
        if not self.__est_bloque:
            print("[SÉQUESTRE] Erreur : Les fonds ne sont plus en séquestre (déjà versés).")
            return False

        self.__est_bloque = False
        self.__est_rembourse = True
        print(f"[SÉQUESTRE] REMBOURSEMENT : {self._montant} DH retournés au client pour la transaction {self._transaction_id}.")
        return True

    def obtenir_etat_paiement(self) -> str:
        """Retourne un résumé textuel du statut financier."""
        if self.__est_rembourse:
            return "Statut : Remboursé au client"
        elif self.__est_bloque:
            return "Statut : Fonds bloqués (Séquestre)"
        else:
            return f"Statut : Fonds libérés le {self.__date_liberation.strftime('%d/%m/%Y')}"

    def __str__(self) -> str:
        return f"Paiement #{self._transaction_id} | Montant: {self._montant} DH | Bloqué: {self.__est_bloque}"