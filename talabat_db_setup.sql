-- ============================================================
-- NOM DU PROJET : Talabat_App_MVP
-- EQUIPE : Yasmine ELANBRI & Noureddine LAGOUIT
-- FORMATION : JOBINTECH - Développement Logiciel DXC
-- SCRIPT : Initialisation de la base de données MySQL
-- ============================================================

-- 1. Création de la base de données
CREATE DATABASE IF NOT EXISTS talabat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE talabat_db;

-- 2. Désactivation des contraintes pour le nettoyage (en cas de ré-exécution)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Evaluations;
DROP TABLE IF EXISTS PaiementsSequestre;
DROP TABLE IF EXISTS LignesCommande;
DROP TABLE IF EXISTS Commandes;
DROP TABLE IF EXISTS Repas;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS DocumentsKYC;
DROP TABLE IF EXISTS Fournisseurs;
DROP TABLE IF EXISTS Beneficiaires;
DROP TABLE IF EXISTS Utilisateurs;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- COUCHE : GESTION DES UTILISATEURS (Héritage)
-- ============================================================

CREATE TABLE Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    type_utilisateur ENUM('ADMIN', 'FOURNISSEUR', 'BENEFICIAIRE') NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE Beneficiaires (
    user_id INT PRIMARY KEY,
    adresse_livraison TEXT,
    telephone VARCHAR(20),
    CONSTRAINT fk_benef_user FOREIGN KEY (user_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Fournisseurs (
    user_id INT PRIMARY KEY,
    biographie TEXT,
    kyc_valide BOOLEAN DEFAULT FALSE,
    solde_accumule DECIMAL(10, 2) DEFAULT 0.00,
    CONSTRAINT fk_fourn_user FOREIGN KEY (user_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE DocumentsKYC (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fournisseur_id INT NOT NULL,
    type_doc VARCHAR(50) NOT NULL,
    chemin_fichier VARCHAR(255),
    est_valide BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (fournisseur_id) REFERENCES Fournisseurs(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- COUCHE : OFFRE CULINAIRE
-- ============================================================

CREATE TABLE Categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libelle VARCHAR(50) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Repas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fournisseur_id INT NOT NULL,
    categorie_id INT NOT NULL,
    titre VARCHAR(100) NOT NULL,
    description TEXT,
    prix DECIMAL(10, 2) NOT NULL,
    est_disponible BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (fournisseur_id) REFERENCES Fournisseurs(user_id) ON DELETE CASCADE,
    FOREIGN KEY (categorie_id) REFERENCES Categories(id)
) ENGINE=InnoDB;

-- ============================================================
-- COUCHE : VENTES ET PAIEMENTS (Séquestre)
-- ============================================================

CREATE TABLE Commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    beneficiaire_id INT NOT NULL,
    supplier_id INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    montant_total DECIMAL(10, 2) NOT NULL,
    statut VARCHAR(50) DEFAULT 'ATTENTE_PAIEMENT',
    FOREIGN KEY (beneficiaire_id) REFERENCES Beneficiaires(user_id),
    FOREIGN KEY (supplier_id) REFERENCES Fournisseurs(user_id)
) ENGINE=InnoDB;

CREATE TABLE LignesCommande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    repas_id INT NOT NULL,
    quantite INT NOT NULL DEFAULT 1,
    prix_unitaire_fixe DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_ligne_cmd FOREIGN KEY (commande_id) REFERENCES Commandes(id) ON DELETE CASCADE,
    FOREIGN KEY (repas_id) REFERENCES Repas(id)
) ENGINE=InnoDB;

CREATE TABLE PaiementsSequestre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT UNIQUE NOT NULL,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    est_bloque BOOLEAN DEFAULT TRUE, -- TRUE = Argent bloqué par Talabat
    date_paiement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (commande_id) REFERENCES Commandes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- COUCHE : CONFIANCE ET DATA
-- ============================================================

CREATE TABLE Evaluations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT UNIQUE NOT NULL,
    note INT NOT NULL,
    commentaire TEXT,
    date_avis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (commande_id) REFERENCES Commandes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- DATA INITIALE (Pour vos tests)
-- ============================================================

INSERT INTO Categories (libelle) VALUES ('Marocain'), ('Africain'), ('Végétarien'), ('Desserts');

-- Compte Admin par défaut
INSERT INTO Utilisateurs (nom, email, mot_de_passe, type_utilisateur) 
VALUES ('Equipe Talabat', 'admin@talabat.ma', 'dxc2026', 'ADMIN');