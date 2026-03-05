# infrastructure/factories/fabrique_utilisateur.py

from core.enums.type_utilisateur import TypeUtilisateur
from core.entities.beneficiaire import Beneficiaire
from core.entities.fournisseur import Fournisseur
from core.entities.administrateur import Administrateur

class FabriqueUtilisateur:
    """
    Classe implementant le DESIGN PATTERN: FACTORY (p. 214 du cours).
    Responsable de l'instanciation des objets selon les donnees MySQL.
    """

    @staticmethod
    def creer_utilisateur(type_u: TypeUtilisateur, data: dict):
        """
        Transforme un dictionnaire (ligne SQL) en objet Python.
        """
        # 1. Extraction des champs communs
        id_user = data.get('id', 0)
        nom = data.get('nom', "")
        email = data.get('email', "")
        mdp = data.get('mot_de_passe', "")

        try:
            # 2. Branchement vers la classe correspondante
            if type_u == TypeUtilisateur.BENEFICIAIRE:
                return Beneficiaire(
                    id_user=id_user,
                    nom=nom,
                    email=email,
                    mot_de_passe=mdp,
                    adresse_livraison=data.get('adresse_livraison', ""),
                    telephone=data.get('telephone', "")
                )

            elif type_u == TypeUtilisateur.FOURNISSEUR:
                # On recupere kyc_valide et solde depuis MySQL
                # On convertit en bool/float car MySQL renvoie parfois des types bruts
                kyc = bool(data.get('kyc_valide', False))
                solde_db = float(data.get('solde_accumule', 0.0))
                
                return Fournisseur(
                    id_user=id_user,
                    nom=nom,
                    email=email,
                    mot_de_passe=mdp,
                    biographie=data.get('biographie', ""),
                    kyc_valide=kyc,
                    solde=solde_db
                )

            elif type_u == TypeUtilisateur.ADMIN:
                return Administrateur(
                    id_user=id_user,
                    nom=nom,
                    email=email,
                    mot_de_passe=mdp,
                    matricule=data.get('matricule', "ADM-999")
                )
            
            else:
                raise ValueError(f"Type utilisateur '{type_u}' non reconnu.")

        except Exception as e:
            print(f"[FACTORY] Erreur lors de la creation de l'objet : {e}")
            return None