INSERT INTO player_match_kpis VALUES (1,1,1,1,3.5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (2,1,1,2,3,4.5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (3,1,1,3,5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (4,1,1,4,3.5,3,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (5,1,1,5,3.5,5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (6,1,1,1,3.5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (7,1,1,2,4.5,3,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (8,1,1,3,5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (9,1,1,4,3.5,3,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (10,1,1,5,3.5,5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (11,1,1,1,3.5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (12,1,1,2,3,4.5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (13,1,1,3,5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (14,1,1,4,3.5,3,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (15,1,1,5,3.5,5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (16,1,1,1,3.5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (17,1,1,2,4.5,5,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (18,1,1,3,5,4,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (19,1,1,4,3.5,3,CURRENT_TIMESTAMP);
INSERT INTO player_match_kpis VALUES (20,1,1,5,3.5,5,CURRENT_TIMESTAMP);

INSERT INTO kpi VALUES (1,1,'Transition','Transition description',4);
INSERT INTO kpi VALUES (2,1,'Playing 1-5 Out','Playing 1-5 Out description',4.5);
INSERT INTO kpi VALUES (3,1,'Playing 2-4 Out','Playing 2-4 Out description',4.5);
INSERT INTO kpi VALUES (4,1,'Side Out Of Bounds 1-Away','Side Out Of Bounds description',4.5);
INSERT INTO kpi VALUES (5,1,'Base 1-Up','Base 1-Up description',5);

INSERT INTO kpi_category VALUES (1,'Offence','Description of Offence');
INSERT INTO kpi_category VALUES (2,'Defence','Description of Defence');
INSERT INTO kpi_category VALUES (3,'Team Culture - On Court','Description of Team Culture - On Court');
INSERT INTO kpi_category VALUES (4,'Team Culture - Off Court','Description of Team Culture - Off Court');

INSERT INTO sport VALUES (1,'AFL','afl','Australian Rules Football',TRUE,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO sport VALUES (2,'Basketball','basketball','Basketball',TRUE,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);

INSERT INTO league VALUES (1,'Victorian Junior Basketball League','VJBL');

INSERT INTO season VALUES (1,1,'VJBL Summer Season','20-NOV-2026','28-FEB-2027',TRUE);

INSERT INTO club VALUES (1,2,'Hawthorn Magic Basketball Club','120–122 Camberwell Road, Hawthorn East VIC','+61 437 773 678','https://basketballhawthorn.com.au/');
INSERT INTO club VALUES (2,2,'Camberwell Dragons Basketball Club','606 High Street, Kew, VIC 3101','+61 3 4444 5555','https://camberwellbasketball.com');
INSERT INTO club VALUES (3,2,'Kew Basketball Club','606 High Street, Kew, VIC 3101','+61 3 4444 5555','https://camberwellbasketball.com');

INSERT INTO team VALUES (1,1,'Hawthorn Magic U14 Boys',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO team VALUES (2,1,'Hawthorn Magic U16 Boys',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO team VALUES (3,1,'Hawthorn Magic U18 Boys',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO team VALUES (4,2,'Camberwell Dragons U14 Boys',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO team VALUES (5,3,'Kew Comets U14 Boys',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);

INSERT INTO match VALUES (1,1,1,4,'2026-11-17 14:30:00','271C Belmore Rd, Balwyn North VIC 3104',30,20);
INSERT INTO match VALUES (2,1,1,5,'2026-11-24 10:00:00','271C Belmore Rd, Balwyn North VIC 3104',22,40);

INSERT INTO athlete VALUES (1,1,'Aaron','Anderson','1-JAN-2008',15,'centre', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (2,1,'Billy','Brown','2-JAN-2008',2,'forward', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (3,1,'Charlie','Curtis','20-APR-2008',23,'forward', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (4,1,'Dirk','Diggler','4-APR-2008',6,'back', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (5,1,'Seb','Marsic','5-MAY-2008',2,'back', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (6,2,'Fred','Fanning','11-JAN-2008',1,'centre', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (7,2,'Graeham','Goble','12-JAN-2008',2,'forward', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (8,2,'Harry','Highpants','13-APR-2008',3,'forward', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (9,2,'Ian','Irwin','14-APR-2008',4,'back', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
INSERT INTO athlete VALUES (10,2,'John','Johnson','15-MAY-2008',5,'back', TRUE, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);
