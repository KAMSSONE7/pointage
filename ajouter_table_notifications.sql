-- Ajout de la table Notifications pour gérer les notifications des utilisateurs
USE donnee_app;

CREATE TABLE IF NOT EXISTS Notifications (
    Id_notification INT PRIMARY KEY AUTO_INCREMENT,
    Id_utilisateur VARCHAR(20) NOT NULL,
    Type_utilisateur ENUM('etudiant', 'enseignant', 'administration') NOT NULL,
    Titre VARCHAR(100) NOT NULL,
    Message TEXT NOT NULL,
    Type_notification ENUM('info', 'avertissement', 'urgence', 'confirmation') DEFAULT 'info',
    Date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Date_lecture TIMESTAMP NULL,
    Lu TINYINT(1) DEFAULT 0,
    Lien VARCHAR(255) NULL,
    Priorite ENUM('basse', 'moyenne', 'haute') DEFAULT 'moyenne',
    INDEX idx_utilisateur (Id_utilisateur, Type_utilisateur),
    INDEX idx_date_creation (Date_creation),
    INDEX idx_lu (Lu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Ajout de quelques notifications de test
INSERT INTO Notifications (Id_utilisateur, Type_utilisateur, Titre, Message, Type_notification, Priorite)
VALUES 
('0141973436', 'etudiant', 'Bienvenue sur la plateforme', 'Votre compte a été créé avec succès !', 'info', 'basse'),
('0141973436', 'etudiant', 'Présence enregistrée', 'Votre présence a été enregistrée avec succès pour le cours de Base de données.', 'confirmation', 'moyenne'),
('0141973436', 'etudiant', 'Rappel de cours', 'Vous avez un cours de Réseaux demain à 10h30.', 'avertissement', 'moyenne');
