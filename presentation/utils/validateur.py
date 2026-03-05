# presentation/utils/validateur.py

import re

class Validateur:
    """
    Classe utilitaire regroupant les validations par expressions régulières (Regex).
    Garantit l'intégrité des entrées utilisateur au niveau de la couche Présentation.
    """

    @staticmethod
    def valider_email(email: str) -> bool:
        """
        Vérifie si le format de l'email est valide.
        Ex: utilisateur@domaine.com
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email):
            return True
        print("[!] Format d'email invalide (ex: nom@mail.com).")
        return False

    @staticmethod
    def valider_telephone(tel: str) -> bool:
        """
        Vérifie si le numéro est un format mobile marocain valide.
        Doit commencer par 05, 06 ou 07 et contenir 10 chiffres.
        """
        pattern = r'^(05|06|07)\d{8}$'
        if re.match(pattern, tel):
            return True
        print("[!] Numéro invalide. Format attendu : 10 chiffres commençant par 05, 06 ou 07.")
        return False

    @staticmethod
    def est_vide(texte: str, nom_champ: str) -> bool:
        """Vérifie si une saisie est vide ou ne contient que des espaces."""
        if not texte or texte.strip() == "":
            print(f"[!] Le champ '{nom_champ}' ne peut pas être vide.")
            return True
        return False

    @staticmethod
    def valider_prix_saisie(prix_str: str) -> bool:
        """Vérifie si la saisie pour un prix est bien un nombre positif."""
        try:
            prix = float(prix_str)
            if prix > 0:
                return True
            print("[!] Le prix doit être supérieur à 0.")
            return False
        except ValueError:
            print("[!] Veuillez saisir un montant numérique valide (ex: 45.50).")
            return False
