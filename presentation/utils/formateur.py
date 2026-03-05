# presentation/utils/formateur.py

from datetime import datetime
from typing import Union

class Formateur:
    """
    Classe utilitaire pour le formatage des données dans l'interface CLI.
    Regroupe des méthodes statiques pour assurer une identité visuelle cohérente.
    """

    @staticmethod
    def formater_prix(montant: Union[float, int]) -> str:
        """Affiche un montant avec 2 décimales et le symbole DH."""
        return f"{float(montant):>8.2f} DH"

    @staticmethod
    def formater_date(dt: datetime) -> str:
        """Convertit un objet datetime en format lisible (JJ/MM/AAAA à HH:MM)."""
        if not dt:
            return "Date inconnue"
        return dt.strftime("%d/%m/%Y à %H:%M")

    @staticmethod
    def titre_section(titre: str, caractere: str = "=") -> None:
        """Affiche un titre de menu centré et décoré."""
        largeur = 50
        print(f"\n{caractere}" * largeur)
        print(f"{titre.upper().center(largeur)}")
        print(f"{caractere}" * largeur)

    @staticmethod
    def separateur(largeur: int = 50) -> None:
        """Affiche une ligne de séparation simple."""
        print("-" * largeur)

    @staticmethod
    def formater_statut(statut: str) -> str:
        """Ajoute des décorations visuelles selon l'état de la commande."""
        m_statut = statut.upper()
        if "PAYE" in m_statut:
            return f" [🔒 {statut}] "  # Symbole cadenas pour le séquestre
        elif "LIVRE" in m_statut:
            return f" [🚚 {statut}] "
        elif "CONFIRME" in m_statut:
            return f" [✅ {statut}] "
        elif "ANNULE" in m_statut:
            return f" [❌ {statut}] "
        return f" [{statut}] "
