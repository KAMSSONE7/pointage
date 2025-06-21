SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';
SET @old_autocommit=@@autocommit;

DROP SCHEMA IF EXISTS donnee_app;
CREATE SCHEMA donnee_app;
USE donnee_app;

-- structure de la table Salle
CREATE TABLE Salle (
    Id_salle INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Libelle VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la table Groupe_td
CREATE TABLE Groupe_td (
    Id_gpe_td INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Libelle VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la table Cours
CREATE TABLE Cours (
    Id_cours INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Libelle VARCHAR(50),
    Vol_hor INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Emploi_du_temps
CREATE TABLE Emploi_du_temps (
    Id_emp INT PRIMARY KEY AUTO_INCREMENT,
    Id_cours INT NOT NULL,
    Id_salle INT NOT NULL,
    Date_cours DATE,
    jours ENUM ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi') NOT NULL,
    heure_deb TIME NOT NULL,
    heure_fin TIME NOT NULL,
    FOREIGN KEY (Id_salle) REFERENCES Salle(Id_salle),
    FOREIGN KEY (Id_cours) REFERENCES Cours(Id_cours)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Administration
CREATE TABLE Administration (
    Id_adm VARCHAR(20) NOT NULL PRIMARY KEY,
    Nom VARCHAR(50) NOT NULL,
    Prenoms VARCHAR(50),
    Email VARCHAR(50) DEFAULT NULL,
    Numero VARCHAR(20) NOT NULL,
    Adresse VARCHAR(20) DEFAULT NULL,
    Mot_de_passe VARCHAR(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Enseignant
CREATE TABLE Enseignant (
    Id_ens VARCHAR(20) NOT NULL PRIMARY KEY,
    Id_cours INT NOT NULL,
    Nom VARCHAR(50) NOT NULL,
    Prenoms VARCHAR(50),
    Email VARCHAR(50) DEFAULT NULL,
    Numero VARCHAR(20) NOT NULL,
    Adresse VARCHAR(20) DEFAULT NULL,
    Mot_de_passe VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (Id_cours) REFERENCES Cours(Id_cours)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Etudiant
CREATE TABLE Etudiant (
    IP VARCHAR(20) NOT NULL PRIMARY KEY,
    Numero_carte_etu VARCHAR(20) DEFAULT NULL,
    Id_gpe_td INT NOT NULL,
    Nom VARCHAR(50) NOT NULL,
    Prenoms VARCHAR(50),
    Niveau VARCHAR(10),
    Email VARCHAR(50) DEFAULT NULL,
    Numero VARCHAR(20) NOT NULL,
    Adresse VARCHAR(20) DEFAULT NULL,
    Mot_de_passe VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (Id_gpe_td) REFERENCES Groupe_td(Id_gpe_td)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Presence_ens
CREATE TABLE Presence_ens (
    Id_pres INT PRIMARY KEY AUTO_INCREMENT,
    Id_ens VARCHAR(20) NOT NULL,
    Id_Salle INT NOT NULL,
    Date_presence TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Heure_debut TIME NOT NULL,
    Heure_fin TIME NOT NULL,
    FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens),
    FOREIGN KEY (Id_Salle) REFERENCES Salle(Id_Salle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la Presence_etu
CREATE TABLE Presence_etu (
    Id_pres INT PRIMARY KEY AUTO_INCREMENT,
    IP VARCHAR(20) NOT NULL,
    Date_presence TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Heure_debut TIME NOT NULL,
    Heure_fin TIME NOT NULL,
    FOREIGN KEY (IP) REFERENCES Etudiant(IP)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- structure de la table utilisateurs
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    profession VARCHAR(30) NOT NULL,
    mot_passe VARCHAR(255) NOT NULL,
    UNIQUE KEY (numero, mot_passe)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- insertion des salles de cours
SET AUTOCOMMIT=0;
INSERT INTO Salle (Libelle) VALUES
('Salle Info2'),
('Amphi A'),
('Amphi B'),
('Salle Info1'),
('DESS'),
('AMPHI IRMA');
COMMIT;

-- insertion des groupes de TD
SET AUTOCOMMIT=0;
INSERT INTO Groupe_td (Libelle) VALUES
('G1'),('G2'),('G3'),('G4'),('G5'), ('SI'),('Mecanique');
COMMIT;

-- insertion des cours
SET AUTOCOMMIT=0;
INSERT INTO Cours (Id_cours, Libelle, Vol_hor) VALUES
(1, 'Base de donnee', 30),
(2, 'Reseaux', 45),
(3, 'Merise', 40),
(4, 'Genie logiciel', 35),
(5, 'AGL', 25),
(6, 'Algo Avance', 20),
(7, 'RO', 30),
(8, 'Maintenance info', 30),
(9, 'Theorie des langages', 40);
COMMIT;

-- insertion des étudiants
SET AUTOCOMMIT=0;
INSERT INTO Etudiant (IP, Numero_carte_etu, Id_gpe_td, Nom, Prenoms, Niveau, Email, Numero, Adresse) VALUES 
('YEOH0612860001', NULL, 5, 'YEOUE', 'HIE BONIFACE', 'LICENCE 3', 'yeouehieboniface@gmail.com', '0709778606','YOPOUGON'),
('AKAN1109960001', 'CI0116304516', 5, 'AKA-DE', 'NAOMI YEI MARIE-CYRIELLE', 'LICENCE 3', 'naomiaka6@gmail.com', '0787182700', 'Koumassi'),
('KACA1805000001', 'CI0121391510', 5, 'KACOU', 'AHATCHE ARISTIDE JUNIOR', 'LICENCE 3', 'kacoujunior98@gmail.com', '0788192480','YOPOUGON'),
('DEMY1404030001', 'CI0122413387', 5, 'DEMBELE', 'YACOUBA', 'LICENCE 3', 'dyacouba767@gmail.com', '0103258832' ,'koumassi'),
('DIOH1606040001', 'CIO123429157', 5, 'DIOMANDE', 'HAMED MELOUA', 'LICENCE 3', 'HDIOMANDE924@GMAIL.COM', '0707779756', 'KOUMASSI'),
('KEIM1611990001', 'CI0120381984', 5, 'KEITA', 'MOHAMED ALEXANDRE', 'LICENCE 3', 'ndnm95@gmail.com', '0748601166', 'ABOBO'),
('ANOA1710790001', 'CI0100126104', 5, 'ANON AMONCOU', 'DIOM SEBASTIEN', 'LICENCE 3', 'leconcret@gmail.com', '0707623118', 'YOPOUGON'),
('DAOK0812000002', 'CI0121396277', 5, 'DAO', 'KARIM', 'LICENCE 3', 'kamssone7@gmail.com', '0101625160', 'TREICHVILLE'),
('KADA2508020001', 'CI0123429656', 5, 'KADJO', 'ALLOUAN MOISE BIENVENUE', 'LICENCE 3', 'kallouan25@gmail.com', '0502081881', 'ANGRE'),
('GNES2805030001', 'CI0122413970', 5, 'GNETO', 'SCHIPHRA GRACE', 'LICENCE 3', 'gnetoschiphra@gmail.com', '0141973436', 'ABOBO');
COMMIT;

-- insertion des administrateurs
SET AUTOCOMMIT=0;
INSERT INTO Administration (Id_adm, Nom, Prenoms, Email, Numero, Adresse) VALUES
('ADM001', 'Kone', 'Awa', 'awa.kone@gmail.com', '0101010101' ,'Abidjan'),
('ADM002', 'Coulibaly', 'Moussa', 'moussa.coulibaly@gmail.com', '0102030405', 'Bouaké'),
('ADM003', 'Toure', 'Fanta', 'fanta.toure@gmail.com', '0103050607', 'Daloa'),
('ADM004', 'Ouattara', 'Alpha', 'alpha.ouattara@gmail.com', '0106070809', 'Korhogo'),
('ADM005', 'Yao', 'Ama', 'ama.yao@gmail.com', '0108091011', 'San Pedro'),
('ADM006', 'Koffi', 'Jean', 'jean.koffi@gmail.com', '0110111213', 'Man'),
('ADM007', 'Ettien', 'Marie', 'marie.ettien@gmail.com', '0112131415', 'Gagnoa'),
('ADM008', 'Akissi', 'Dan', 'dan.akissi@gmail.com', '0114151617', 'Soubré'),
('ADM009', 'Bamba', 'Issa', 'issa.bamba@gmail.com', '0116171819', 'Abengourou'),
('ADM010', 'Zoumana', 'Fatou', 'fatou.zoumana@gmail.com', '0118192022', 'Yamoussoukro');
COMMIT;

-- insertion des enseignants
SET AUTOCOMMIT=0;
INSERT INTO Enseignant (Id_ens, Id_cours, Nom, Prenoms, Email, Numero, Adresse) VALUES
('ENS001', 1, 'Diabate', 'Abdoulaye', 'abdoulaye.diabate@gmail.com', '0701010101', 'Abidjan'),
('ENS002', 2, 'Bakayoko', 'Alima', 'alima.bakayoko@gmail.com', '0702030405', 'Bouaké'),
('ENS003', 3, 'N\'Dri', 'Kouadio', 'kouadio.ndri@gmail.com', '0703050607', 'Daloa'),
('ENS004', 4, 'Sangare', 'Fatima', 'fatima.sangare@gmail.com', '0706070809', 'Korhogo'),
('ENS005', 5, 'Kouakou', 'Joseph', 'joseph.kouakou@gmail.com', '0102030405', 'Abidjan'),
('ENS006', 6, 'Traore', 'Moussa', 'moussa.traore@gmail.com', '0708091011', 'San-Pédro'),
('ENS007', 7, 'Konan', 'Issa', 'issa.konan@gmail.com', '0712131415', 'Yamoussoukro'),
('ENS008', 8, 'Coulibaly', 'Aminata', 'aminata.coulibaly@gmail.com', '0715161718', 'Man'),
('ENS009', 9, 'Koffi', 'Jean', 'jean.koffi@gmail.com', '0718192021', 'Abidjan');
COMMIT;

-- insertion de l'emploi du temps (jusqu'en juillet 2025)
SET AUTOCOMMIT=0;
INSERT INTO Emploi_du_temps (Id_cours, Id_salle, Date_cours, jours, heure_deb, heure_fin) VALUES
(1, 1, '2025-06-01', 'Lundi', '08:00:00', '10:00:00'),
(2, 2, '2025-06-02', 'Mardi', '10:30:00', '12:30:00'),
(3, 3, '2025-06-03', 'Mercredi', '14:00:00', '16:00:00'),
(4, 4, '2025-06-04', 'Jeudi', '08:00:00', '10:00:00'),
(5, 1, '2025-06-05', 'Vendredi', '11:00:00', '13:00:00'),
(6, 1, '2025-06-06', 'Samedi', '09:00:00', '11:00:00'),
(7, 2, '2025-06-07', 'Lundi', '13:30:00', '15:30:00'),
(8, 3, '2025-06-08', 'Mardi', '15:00:00', '17:00:00'),
(9, 1, '2025-06-09', 'Mercredi', '16:00:00', '18:00:00'),
(4, 4, '2025-06-10', 'Jeudi', '08:00:00', '10:00:00'),
(5, 1, '2025-06-11', 'Vendredi', '11:00:00', '13:00:00'),
(6, 1, '2025-06-12', 'Samedi', '09:00:00', '11:00:00'),
(7, 2, '2025-06-13', 'Lundi', '13:30:00', '15:30:00'),
(8, 3, '2025-06-14', 'Mardi', '15:00:00', '17:00:00'),
(9, 1, '2025-06-15', 'Mercredi', '16:00:00', '18:00:00'),
(4, 4, '2025-06-16', 'Jeudi', '08:00:00', '10:00:00'),
(5, 1, '2025-06-17', 'Vendredi', '11:00:00', '13:00:00'),
(6, 1, '2025-06-18', 'Samedi', '09:00:00', '11:00:00'),
(7, 2, '2025-06-19', 'Lundi', '13:30:00', '15:30:00'),
(8, 3, '2025-06-20', 'Mardi', '15:00:00', '17:00:00'),
(9, 1, '2025-06-21', 'Mercredi', '16:00:00', '18:00:00'),
(4, 4, '2025-06-22', 'Jeudi', '08:00:00', '10:00:00'),
(1, 2, '2025-06-23', 'Lundi', '08:00:00', '10:00:00'),
(2, 3, '2025-06-24', 'Mardi', '10:30:00', '12:30:00'),
(3, 1, '2025-06-25', 'Mercredi', '14:00:00', '16:00:00'),
(4, 4, '2025-06-26', 'Jeudi', '08:00:00', '10:00:00'),
(5, 2, '2025-06-27', 'Vendredi', '11:00:00', '13:00:00'),
(6, 3, '2025-06-28', 'Samedi', '09:00:00', '11:00:00'),
(7, 1, '2025-07-01', 'Mardi', '08:00:00', '10:00:00'),
(8, 2, '2025-07-02', 'Mercredi', '10:30:00', '12:30:00'),
(9, 3, '2025-07-03', 'Jeudi', '14:00:00', '16:00:00'),
(1, 4, '2025-07-04', 'Vendredi', '08:00:00', '10:00:00'),
(2, 1, '2025-07-05', 'Samedi', '11:00:00', '13:00:00'),
(3, 2, '2025-07-07', 'Lundi', '09:00:00', '11:00:00'),
(4, 3, '2025-07-08', 'Mardi', '13:30:00', '15:30:00'),
(5, 4, '2025-07-09', 'Mercredi', '15:00:00', '17:00:00'),
(6, 1, '2025-07-10', 'Jeudi', '16:00:00', '18:00:00'),
(7, 2, '2025-07-11', 'Vendredi', '08:00:00', '10:00:00'),
(8, 3, '2025-07-12', 'Samedi', '11:00:00', '13:00:00'),
(9, 4, '2025-07-14', 'Lundi', '09:00:00', '11:00:00'),
(1, 1, '2025-07-15', 'Mardi', '13:30:00', '15:30:00'),
(2, 2, '2025-07-16', 'Mercredi', '15:00:00', '17:00:00'),
(3, 3, '2025-07-17', 'Jeudi', '16:00:00', '18:00:00'),
(4, 4, '2025-07-18', 'Vendredi', '08:00:00', '10:00:00'),
(5, 1, '2025-07-19', 'Samedi', '11:00:00', '13:00:00'),
(6, 2, '2025-07-21', 'Lundi', '09:00:00', '11:00:00'),
(7, 3, '2025-07-22', 'Mardi', '13:30:00', '15:30:00'),
(8, 4, '2025-07-23', 'Mercredi', '15:00:00', '17:00:00'),
(9, 1, '2025-07-24', 'Jeudi', '16:00:00', '18:00:00'),
(1, 2, '2025-07-25', 'Vendredi', '08:00:00', '10:00:00'),
(2, 3, '2025-07-26', 'Samedi', '11:00:00', '13:00:00'),
(3, 4, '2025-07-28', 'Lundi', '09:00:00', '11:00:00'),
(4, 1, '2025-07-29', 'Mardi', '13:30:00', '15:30:00'),
(5, 2, '2025-07-30', 'Mercredi', '15:00:00', '17:00:00'),
(6, 3, '2025-07-31', 'Jeudi', '16:00:00', '18:00:00');
COMMIT;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;