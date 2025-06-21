-- Ajout de la table Messages pour gérer les notifications
ALTER TABLE Presence_ens ADD COLUMN Valide TINYINT(1) DEFAULT 0;

CREATE TABLE Messages (
    Id_message INT PRIMARY KEY AUTO_INCREMENT,
    Id_ens VARCHAR(20) NOT NULL,
    Contenu TEXT NOT NULL,
    Date_message TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Lu TINYINT(1) DEFAULT 0,
    FOREIGN KEY (Id_ens) REFERENCES Enseignant(Id_ens)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
