CREATE DATABASE IF NOT EXISTS  UNIVAP;
USE UNIVAP;

CREATE TABLE professores(
registro INT PRIMARY KEY,
nomeprof VARCHAR(50),
telefoneprof VARCHAR(30),
idadeprof INT,
salarioprof FLOAT
);

CREATE TABLE disciplinas(
codigodisc int primary key,
nomedisc VARCHAR(50)
);

CREATE TABLE disciplinasxprofessores (
codigodisciplinacurso VARCHAR(10) PRIMARY KEY,
coddisciplina int,
codprofessor int,
FOREIGN KEY (codprofessor) REFERENCES professores(registro),
FOREIGN KEY (coddisciplina) REFERENCES disciplinas(codigodisc),
curso int,
cargahoraria int,
anoletivo int
);

INSERT INTO disciplinas (codigodisc,nomedisc) values (100, "POOI");
INSERT INTO disciplinas (codigodisc,nomedisc) values (200, "POOII");
INSERT INTO disciplinas (codigodisc,nomedisc) values (300, "POOIII");
INSERT INTO disciplinas (codigodisc,nomedisc) values (400, "POOIV");

INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values (1,"A","999",20,100);
INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values (2,"B","998",30,200);
INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values (3,"C","997",40,300);
INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values (4,"D","996",50,400);
INSERT INTO professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values (5,"E","999",60,100);

INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("1000",100,1,1,20,2021);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("2000",100,1,2,20,2021);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("3000",200,2,1,40,2021);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("4000",300,3,2,50,2022);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("5000",200,2,3,40,2021);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("6000",100,1,4,20,2022);
INSERT INTO disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("7000",400,4,1,80,2021);

SELECT * FROM PROFESSORES;
CREATE OR REPLACE VIEW vw_disciplinas_professores AS
SELECT 
    d.codigodisc AS CodigoDisciplina,
    d.nomedisc AS NomeDisciplina,
    p.registro AS CodigoProfessor,
    p.nomeprof AS NomeProfessor,
    p.telefoneprof AS Telefone,
    p.idadeprof AS Idade,
    p.salarioprof AS Salario,
    dxp.curso AS Curso,
    dxp.cargahoraria AS CargaHoraria,
    dxp.anoletivo AS AnoLetivo
FROM disciplinasxprofessores dxp
JOIN disciplinas d ON dxp.coddisciplina = d.codigodisc
JOIN professores p ON dxp.codprofessor = p.registro
ORDER BY d.codigodisc, p.registro;
SELECT * FROM vw_disciplinas_professores;
