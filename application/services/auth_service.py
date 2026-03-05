# application/services/auth_service.py

from typing import Optional, Dict, Any
from core.entities.utilisateur import Utilisateur
from core.enums.type_utilisateur import TypeUtilisateur
from infrastructure.repositories.utilisateur_repo import UtilisateurRepository
from infrastructure.factories.fabrique_utilisateur import FabriqueUtilisateur

class AuthService:
    """
    Service gérant l'Authentification et l'Inscription (Cas d'utilisation).
    Respecte le principe de Single Responsibility (SRP) : ne gère que la sécurité.
    """

    def __init__(self):
        self._repo = UtilisateurRepository()
        self._utilisateur_actuel: Optional[Utilisateur] = None

    @property
    def utilisateur_actuel(self) -> Optional[Utilisateur]:
        """Retourne l'utilisateur actuellement connecté au système."""
        return self._utilisateur_actuel

    def sinscrire(self, type_u: TypeUtilisateur, infos: Dict[str, Any]) -> bool:
        """
        Logique métier pour l'inscription d'un nouvel utilisateur.
        1. Vérifie si l'email existe déjà.
        2. Utilise la Factory pour créer l'objet.
        3. Sauvegarde via le Repository.
        """
        # Vérification d'unicité (Règle métier)
        if self._repo.trouver_par_email(infos.get('email')):
            print("[AUTH] Erreur : Cet email est déjà utilisé.")
            return False

        # Utilisation du PATRON FACTORY (p. 214)
        nouvel_utilisateur = FabriqueUtilisateur.creer_utilisateur(type_u, infos)
        
        if nouvel_utilisateur:
            return self._repo.sauvegarder(nouvel_utilisateur)
        return False

    def se_connecter(self, email: str, mot_de_passe: str) -> Optional[Utilisateur]:
        """
        Logique métier pour la connexion.
        Vérifie les identifiants et initialise la session.
        """
        user = self._repo.trouver_par_email(email)

        if user and user.verifier_mot_de_passe(mot_de_passe):
            self._utilisateur_actuel = user
            print(f"[AUTH] Bienvenue, {user.nom} ({user.type_utilisateur.value})")
            return user
        
        print("[AUTH] Échec de connexion : Email ou mot de passe incorrect.")
        return None

    def se_deconnecter(self) -> None:
        """Ferme la session utilisateur actuelle."""
        if self._utilisateur_actuel:
            print(f"[AUTH] Déconnexion de {self._utilisateur_actuel.nom}.")
            self._utilisateur_actuel = None

    def est_authentifie(self) -> bool:
        """Vérifie si une session est active."""
        return self._utilisateur_actuel is not None

