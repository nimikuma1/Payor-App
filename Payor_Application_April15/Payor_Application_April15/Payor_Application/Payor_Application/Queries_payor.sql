-- SQLite
CREATE TABLE priorauth (
    memberID TEXT,
    memberName TEXT,
    ICDCode TEXT,
    procedureCode TEXT,
    priorauthStatus TEXT
);

ALTER TABLE priorauth
ADD COLUMN memberID INTEGER PRIMARY KEY;

DROP TABLE priorauth;

CREATE TABLE Priorauth (
    memberID INTEGER PRIMARY KEY,
    memberName VARCHAR(100),
    payor VARCHAR(100),
    ICDCode VARCHAR(20),
    procedureCode VARCHAR(20),
    priorAuthStatus VARCHAR(20)
);


select * from Priorauth;

select count(*)from Priorauth;

DELETE from Priorauth where memberID in (1,2,3,4,5,6)

DELETE from Priorauth where memberID in (1,2,3)

select * from Priorauth