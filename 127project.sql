
DROP DATABASE IF EXISTS `127project`;
CREATE DATABASE IF NOT EXISTS `127project` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `127project`;

-- CREATE TABLE FOR MEMBER
CREATE OR REPLACE TABLE member (
    student_number VARCHAR(10) PRIMARY KEY,
    password VARCHAR(15) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(20),
    last_name VARCHAR(20) NOT NULL,
    degree_program VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    batch_year VARCHAR(4) NOT NULL
);

-- CREATE TABLE FOR ORGANIZATION
CREATE OR REPLACE TABLE organization (
    organization_id INT PRIMARY KEY,
    organization_name VARCHAR(50) NOT NULL,
    academic_year VARCHAR(9), -- 'YYYY-YYYY' format
    semester ENUM('1st Semester', '2nd Semester', 'Midyear')
);

-- CREATE TABLE FOR MEMBERSHIP
CREATE OR REPLACE TABLE membership (
    student_number VARCHAR(10),
    organization_id INT,
    academic_year VARCHAR(9),
    semester ENUM('1st Semester', '2nd Semester', 'Midyear'),
    membership_status VARCHAR(20),
    member_role VARCHAR(30),
    committee VARCHAR(30),
    PRIMARY KEY (student_number, organization_id, academic_year, semester),
    FOREIGN KEY (student_number) REFERENCES member(student_number),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
);

-- CREATE TABLE FOR FEE
CREATE OR REPLACE TABLE fee (
    fee_reference_number VARCHAR(10) PRIMARY KEY,
    student_number VARCHAR(10),
    organization_id INT,
    semester ENUM('1st Semester', '2nd Semester', 'Midyear'),
    due_date DATE,
    amount_due DECIMAL(10, 2),
    FOREIGN KEY (student_number) REFERENCES member(student_number),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
);

-- CREATE TABLE FOR PAYMENT
CREATE OR REPLACE TABLE payment (
    payment_reference_number VARCHAR(10) PRIMARY KEY,
    student_number VARCHAR(10),
    organization_id INT,
    paid_date DATE,
    amount_paid DECIMAL(10, 2),
    fee_reference_number VARCHAR(10),
    FOREIGN KEY (student_number) REFERENCES member(student_number),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
    FOREIGN KEY (fee_reference_number) REFERENCES fee(fee_reference_number)
);


INSERT INTO member VALUES
('2023-10396', 'pass123', 'John Benedict', 'G.', 'Calimlim', 'Computer Science', 'male', '2023'),
('2023-00001', 'pass123', 'Alice', 'M.', 'Santos', 'BS Mathematics', 'Female', '2023'),
('2023-00002', 'pass123', 'Bob', 'J.', 'Reyes', 'BS Applied Math', 'Male', '2023'),
('2023-00003', 'pass123', 'Carla', NULL, 'Dela Cruz', 'BS Math', 'Female', '2023'),
('2023-00004', 'pass123', 'Daniel', 'F.', 'Tan', 'BS Applied Math', 'Male', '2022'),
('2023-00005', 'pass123', 'Elena', NULL, 'Morales', 'BS Math', 'Female', '2021'),
('2023-00006', 'pass123', 'Francis', 'B.', 'Lopez', 'BS Math', 'Male', '2023'),
('2023-00007', 'pass123', 'Grace', NULL, 'Lim', 'BS Applied Math', 'Female', '2022'),
('2023-00008', 'pass123', 'Henry', 'C.', 'Yu', 'BS Math', 'Male', '2021'),
('2023-00009', 'pass123', 'Ivy', NULL, 'Castro', 'BS Mathematics', 'Female', '2023'),
('2023-00010', 'pass123', 'Jake', 'E.', 'Gomez', 'BS Math', 'Male', '2022');

INSERT INTO organization VALUES
(17, 'Mathematical Sciences Society', '2024-2025', '1st Semester'),
(18, 'Actuarial Sciences Society', '2024-2025', '1st Semester'),
(19, 'Math Clubhouse', '2024-2025', '1st Semester'),
(20, 'Young Software Engineers Society', '2024-2025', '1st Semester'),
(21, 'Philobioscientia Society', '2024-2025', '1st Semester'),
(22, 'Sophia Philosophical Society', '2024-2025', '1st Semester'),
(23, 'Math Enthusiasts Circle', '2024-2025', '1st Semester'),
(90, 'Lisieux Music Ministry', '2024-2025', '1st Semester');

INSERT INTO membership VALUES
('2023-10396', 17, '2023-2024', '1st Semester', 'active', 'Member', 'Records'),
('2023-10396', 90, '2023-2024', '1st Semester', 'active', 'Member', 'Formation'),
('2023-00001', 17, '2024-2025', '1st Semester', 'active', 'President', 'Executive'),
('2023-00002', 17, '2024-2025', '1st Semester', 'active', 'Vice President', 'Executive'),
('2023-00003', 18, '2024-2025', '1st Semester', 'active', 'Member', 'Finance'),
('2023-00004', 19, '2024-2025', '1st Semester', 'inactive', 'Member', 'Events'),
('2023-00005', 20, '2024-2025', '1st Semester', 'active', 'Member', 'Logistics'),
('2023-00006', 21, '2024-2025', '1st Semester', 'active', 'Member', 'Finance'),
('2023-00007', 22, '2024-2025', '1st Semester', 'active', 'Member', 'Membership'),
('2023-00008', 23, '2024-2025', '1st Semester', 'active', 'Member', 'Outreach'),
('2023-00009', 17, '2024-2025', '1st Semester', 'active', 'Member', 'Documentation'),
('2023-00010', 18, '2024-2025', '1st Semester', 'inactive', 'Member', 'Events');

INSERT INTO fee VALUES
('FEE0000001', '2023-00001', 17, '1st Semester', '2024-09-01', 200.00),
('FEE0000002', '2023-00002', 17, '1st Semester', '2024-09-01', 200.00),
('FEE0000003', '2023-00003', 18, '1st Semester', '2024-09-05', 250.00),
('FEE0000004', '2023-00004', 19, '1st Semester', '2024-09-10', 150.00),
('FEE0000005', '2023-00005', 20, '1st Semester', '2024-09-03', 180.00),
('FEE0000006', '2023-00006', 21, '1st Semester', '2024-09-02', 220.00),
('FEE0000007', '2023-00007', 22, '1st Semester', '2024-09-01', 190.00),
('FEE0000008', '2023-00008', 23, '1st Semester', '2024-09-06', 200.00),
('FEE0000009', '2023-00009', 17, '1st Semester', '2024-09-01', 200.00),
('FEE0000010', '2023-00010', 18, '1st Semester', '2024-09-01', 250.00);

INSERT INTO payment VALUES
('PAY0000001', '2023-00001', 17, '2024-08-30', 200.00, 'FEE0000001'),
('PAY0000002', '2023-00002', 17, '2024-08-31', 200.00, 'FEE0000002'),
('PAY0000003', '2023-00003', 18, '2024-09-01', 250.00, 'FEE0000003'),
('PAY0000004', '2023-00004', 19, '2024-09-02', 150.00, 'FEE0000004'),
('PAY0000005', '2023-00005', 20, '2024-09-01', 180.00, 'FEE0000005'),
('PAY0000006', '2023-00006', 21, '2024-09-01', 220.00, 'FEE0000006'),
('PAY0000007', '2023-00007', 22, '2024-09-01', 190.00, 'FEE0000007'),
('PAY0000008', '2023-00008', 23, '2024-09-06', 200.00, 'FEE0000008'),
('PAY0000009', '2023-00009', 17, '2024-09-01', 200.00, 'FEE0000009'),
('PAY0000010', '2023-00010', 18, '2024-09-01', 250.00, 'FEE0000010');

INSERT INTO member VALUES
('2023-00011', 'pass456', 'Karen', NULL, 'Abad', 'BS Mathematics', 'Female', '2022'),
('2023-00012', 'pass456', 'Leo', 'R.', 'Bautista', 'BS Applied Math', 'Male', '2021'),
('2023-00013', 'pass456', 'Mia', NULL, 'Chan', 'BS Math', 'Female', '2022'),
('2023-00014', 'pass456', 'Noah', 'D.', 'Dizon', 'BS Math', 'Male', '2023'),
('2023-00015', 'pass456', 'Olive', NULL, 'Escobar', 'BS Math', 'Female', '2021'),
('2023-00016', 'pass456', 'Paulo', 'S.', 'Fernandez', 'BS Math', 'Male', '2022'),
('2023-00017', 'pass456', 'Queenie', NULL, 'Garcia', 'BS Applied Math', 'Female', '2023'),
('2023-00018', 'pass456', 'Ramon', 'J.', 'Herrera', 'BS Math', 'Male', '2022'),
('2023-00019', 'pass456', 'Samantha', NULL, 'Ignacio', 'BS Mathematics', 'Female', '2023'),
('2023-00020', 'pass456', 'Thomas', 'L.', 'Jimenez', 'BS Math', 'Male', '2021');

INSERT INTO membership VALUES
('2023-00011', 18, '2024-2025', '1st Semester', 'active', 'President', 'Executive'),
('2023-00012', 19, '2024-2025', '1st Semester', 'active', 'Vice President', 'Executive'),
('2023-00013', 20, '2024-2025', '1st Semester', 'active', 'Secretary', 'Executive'),
('2023-00014', 21, '2024-2025', '1st Semester', 'active', 'Treasurer', 'Executive'),
('2023-00015', 22, '2024-2025', '1st Semester', 'active', 'Auditor', 'Executive'),
('2023-00016', 23, '2024-2025', '1st Semester', 'active', 'PRO', 'Executive'),
('2023-00017', 17, '2024-2025', '1st Semester', 'active', 'Committee Head', 'Executive'),
('2023-00018', 18, '2024-2025', '1st Semester', 'active', 'Committee Head', 'Executive'),
('2023-00019', 19, '2024-2025', '1st Semester', 'active', 'Assistant Secretary', 'Executive'),
('2023-00020', 20, '2024-2025', '1st Semester', 'active', 'Committee Head', 'Executive');

INSERT INTO organization VALUES
(24, 'Alliance of Computer Science Students', '2024-2025', '1st Semester');

INSERT INTO member VALUES
('2023-00021', 'cs123', 'Ulysses', NULL, 'Kwan', 'BS Computer Science', 'male', '2022'),
('2023-00022', 'cs123', 'Veronica', 'A.', 'Luna', 'BS Computer Science', 'female', '2021'),
('2023-00023', 'cs123', 'Winston', 'B.', 'Mendoza', 'BS Computer Science', 'male', '2022'),
('2023-00024', 'cs123', 'Xenia', NULL, 'Navarro', 'BS Computer Science', 'female', '2023'),
('2023-00025', 'cs123', 'Yuri', 'C.', 'Ortega', 'BS Computer Science', 'male', '2023');

INSERT INTO membership VALUES
('2023-00021', 24, '2024-2025', '1st Semester', 'active', 'President', 'Executive'),
('2023-00022', 24, '2024-2025', '1st Semester', 'active', 'Vice President', 'Executive'),
('2023-00023', 24, '2024-2025', '1st Semester', 'inactive', 'Secretary', 'Executive'),
('2023-00024', 24, '2024-2025', '1st Semester', 'inactive', 'Treasurer', 'Executive'),
('2023-00025', 24, '2024-2025', '1st Semester', 'active', 'PRO', 'Executive');

INSERT INTO member (
  student_number, password, first_name, middle_name, last_name, degree_program, gender, batch_year
) VALUES
('2020-11223', 'pass11223', 'Alicia', 'D.', 'Rivera', 'BS Computer Science', 'female', '2020'),
('2020-22334', 'pass22334', 'Kenji', 'F.', 'Lopez', 'BS Computer Science', 'male', '2020'),
('2019-33445', 'pass33445', 'Isabela', 'M.', 'Gomez', 'BS Computer Science', 'Female', '2019');


INSERT INTO membership (
  student_number, organization_id, academic_year, semester, membership_status, member_role, committee
) VALUES
('2020-11223', 17, '2023-2024', '2nd Semester', 'alumni', 'Member', 'Records'),
('2020-22334', 17, '2023-2024', '2nd Semester', 'alumni', 'Member', 'Outreach'),
('2019-33445', 17, '2022-2023', '2nd Semester', 'alumni', 'Member', 'Publications');


INSERT INTO member (student_number, password, first_name, middle_name, last_name, degree_program, gender, batch_year) VALUES
('2023-12000', 'pass1234', 'Juan', 'Dela', 'Cruz', 'BS Computer Science', 'male', '2023'),
('2023-12001', 'hello567', 'Maria', NULL, 'Lopez', 'BA Communication', 'female', '2023'),
('2023-12002', 'pw2022', 'Carlos', 'S.', 'Reyes', 'BS Statistics', 'male', '2023'),
('2024-13456', 'hellocmsc', 'Marion', 'P.', 'Fontableu', 'BS Computer Science', 'male', '2024');

INSERT INTO organization (organization_id, organization_name, academic_year, semester) VALUES
(30, 'Junior Programmers Guild', '2024-2025', '1st Semester'),
(31, 'Media Arts Society', '2024-2025', '1st Semester'),
(32, 'Environmental Warriors', '2023-2024', '2nd Semester');

INSERT INTO membership (student_number, organization_id, academic_year, semester, membership_status, member_role, committee) VALUES
('2023-12000', 30, '2024-2025', '1st Semester', 'active', 'President', 'Executive'),
('2023-12001', 31, '2024-2025', '1st Semester', 'inactive', 'Member', 'Outreach'),
('2023-12002', 31, '2023-2024', '2nd Semester', 'active', 'Treasurer', 'Executive'),
('2023-12000', 32, '2023-2024', '2nd Semester', 'active', 'Secretary', 'Executive'),
('2023-12000', 17, '2024-2025', '1st Semester', 'inactive', 'Vice President', 'Executive'),
('2023-12002', 17, '2023-2024', '2nd Semester', 'active', 'President', 'Executive'),
('2024-13456', 17, '2023-2024', '2nd Semester', 'inactive', 'Treasurer', 'Executive');

INSERT INTO fee (fee_reference_number, student_number, organization_id, semester, due_date, amount_due) VALUES
('F012', '2023-12000', 30, '1st Semester', '2024-09-15', 500.00),
('F015', '2023-12001', 31, '1st Semester', '2024-09-20', 300.00),
('F018', '2023-12002', 31, '2nd Semester', '2024-02-10', 400.00);

INSERT INTO payment (payment_reference_number, student_number, organization_id, paid_date, amount_paid, fee_reference_number) VALUES
('P012', '2023-12000', 30, '2024-09-10', 500.00, 'F012'),
('P014', '2023-12002', 31, '2024-02-08', 400.00, 'F018');

INSERT INTO fee VALUES
('FEE0000011', '2023-00011', 18, '1st Semester', '2024-09-01', 250.00),
('FEE0000012', '2023-00012', 19, '1st Semester', '2024-09-02', 180.00),
('FEE0000013', '2023-00013', 20, '1st Semester', '2024-09-03', 190.00),
('FEE0000014', '2023-00014', 21, '1st Semester', '2024-09-04', 220.00),
('FEE0000015', '2023-00015', 22, '1st Semester', '2024-09-05', 200.00),
('FEE0000016', '2023-00016', 23, '1st Semester', '2024-09-06', 230.00),
('FEE0000017', '2023-00017', 17, '1st Semester', '2024-09-07', 210.00),
('FEE0000018', '2023-00018', 18, '1st Semester', '2024-09-08', 250.00),
('FEE0000019', '2023-00019', 19, '1st Semester', '2024-09-09', 200.00),
('FEE0000020', '2023-00020', 20, '1st Semester', '2024-09-10', 180.00);

INSERT INTO payment VALUES
('PAY0000011', '2023-00011', 18, '2024-08-31', 250.00, 'FEE0000011'),
('PAY0000012', '2023-00012', 19, '2024-09-01', 180.00, 'FEE0000012'),
('PAY0000013', '2023-00013', 20, '2024-09-02', 190.00, 'FEE0000013'),
('PAY0000014', '2023-00014', 21, '2024-09-03', 220.00, 'FEE0000014'),
('PAY0000015', '2023-00015', 22, '2024-09-04', 200.00, 'FEE0000015'),
('PAY0000016', '2023-00016', 23, '2024-09-05', 230.00, 'FEE0000016'),
('PAY0000017', '2023-00017', 17, '2024-09-06', 210.00, 'FEE0000017'),
('PAY0000018', '2023-00018', 18, '2024-09-07', 250.00, 'FEE0000018'),
('PAY0000019', '2023-00019', 19, '2024-09-08', 200.00, 'FEE0000019'),
('PAY0000020', '2023-00020', 20, '2024-09-09', 180.00, 'FEE0000020');

INSERT INTO member VALUES
('2023-12003', 'qwe123', 'Carlos', 'Z.', 'Del Rosario', 'BS Mathematics', 'male', '2023'),
('2023-12004', 'asd456', 'Diana', NULL, 'Flores', 'BS Applied Math', 'female', '2022'),
('2023-12005', 'zxc789', 'Edward', 'G.', 'Gonzales', 'BS Math', 'male', '2021');

INSERT INTO organization VALUES
(25, 'Data Science Guild', '2024-2025', '1st Semester'),
(26, 'Society of Math Majors', '2024-2025', '1st Semester');

INSERT INTO membership VALUES
('2023-12003', 25, '2024-2025', '1st Semester', 'active', 'Member', 'Analytics'),
('2023-12004', 26, '2024-2025', '1st Semester', 'active', 'Member', 'Research'),
('2023-12005', 25, '2024-2025', '1st Semester', 'inactive', 'Member', 'Events');

INSERT INTO fee VALUES
('FEE0000411', '2023-12003', 25, '1st Semester', '2024-09-02', 210.00),
('FEE0000412', '2023-12004', 26, '1st Semester', '2024-09-05', 200.00),
('FEE0000413', '2023-12005', 25, '1st Semester', '2024-09-08', 190.00);

INSERT INTO payment VALUES
('PAY0000411', '2023-12003', 25, '2024-09-01', 210.00, 'FEE0000411'),
('PAY0000412', '2023-12004', 26, '2024-09-05', 200.00, 'FEE0000412'),
('PAY0000413', '2023-12005', 25, '2024-09-08', 190.00, 'FEE0000413');


INSERT INTO member VALUES
('1981-01500', 'pass01500', 'Bianca', 'R.', 'Reyes', 'BS Math', 'female', '1981'),
('1982-02501', 'pass02501', 'Carlos', 'G.', 'Lopez', 'BS Math', 'male', '1982'),
('1983-03502', 'pass03502', 'Diana', 'L.', 'Torres', 'BS Math', 'female', '1983'),
('1984-04503', 'pass04503', 'Edward', NULL, 'Lim', 'BS Math', 'male', '1984'),
('1985-05504', 'pass05504', 'Fatima', 'J.', 'Gonzales', 'BS Math', 'female', '1985'),
('1986-06505', 'pass06505', 'George', 'M.', 'Tan', 'BS Math', 'male', '1986'),
('1987-07506', 'pass07506', 'Hannah', 'S.', 'Cruz', 'BS Math', 'female', '1987'),
('1988-08507', 'pass08507', 'Ian', 'K.', 'Ng', 'BS Math', 'male', '1988'),
('1989-09508', 'pass09508', 'Julia', 'F.', 'Ocampo', 'BS Math', 'female', '1989'),
('1990-10509', 'pass10509', 'Kevin', 'T.', 'Rivera', 'BS Math', 'male', '1990'),
('1991-11510', 'pass11510', 'Lara', 'V.', 'Salazar', 'BS Math', 'female', '1991'),
('1992-12511', 'pass12511', 'Martin', NULL, 'De Guzman', 'BS Math', 'male', '1992'),
('1993-13512', 'pass13512', 'Nina', 'A.', 'Santos', 'BS Math', 'female', '1993'),
('1994-14513', 'pass14513', 'Oscar', 'E.', 'Toribio', 'BS Math', 'male', '1994'),
('1995-15514', 'pass15514', 'Patricia', 'N.', 'Delos Reyes', 'BS Math', 'female', '1995'),
('1996-16515', 'pass16515', 'Quentin', 'C.', 'Yap', 'BS Math', 'male', '1996'),
('1997-17516', 'pass17516', 'Rina', 'D.', 'Velasco', 'BS Math', 'female', '1997'),
('1998-18517', 'pass18517', 'Samuel', 'J.', 'Co', 'BS Math', 'male', '1998'),
('1999-19518', 'pass19518', 'Tina', 'M.', 'Navarro', 'BS Math', 'female', '1999'),
('2000-20519', 'pass20519', 'Ulysses', 'P.', 'Manalo', 'BS Math', 'male', '2000'),
('2001-21520', 'pass21520', 'Vanessa', 'Q.', 'David', 'BS Math', 'female', '2001'),
('2002-22521', 'pass22521', 'Walter', NULL, 'Chua', 'BS Math', 'male', '2002'),
('2003-23522', 'pass23522', 'Xandra', 'B.', 'Fabian', 'BS Math', 'female', '2003'),
('2004-24523', 'pass24523', 'Yves', 'R.', 'Go', 'BS Math', 'male', '2004'),
('2005-25524', 'pass25524', 'Zenaida', 'H.', 'Ilagan', 'BS Math', 'female', '2005'),
('2006-26525', 'pass26525', 'Adrian', 'S.', 'Liu', 'BS Math', 'male', '2006'),
('2007-27526', 'pass27526', 'Beatrice', 'U.', 'Rosales', 'BS Math', 'female', '2007'),
('2008-28527', 'pass28527', 'Cyrus', 'D.', 'Tanaka', 'BS Math', 'male', '2008'),
('2009-29528', 'pass29528', 'Danica', 'W.', 'Santiago', 'BS Math', 'female', '2009'),
('2010-30529', 'pass30529', 'Emil', 'Y.', 'Reyes', 'BS Math', 'male', '2010'),
('2011-31530', 'pass31530', 'Fiona', 'Z.', 'Uy', 'BS Math', 'female', '2011'),
('2012-32531', 'pass32531', 'Gabriel', NULL, 'Dizon', 'BS Math', 'male', '2012'),
('2013-33532', 'pass33532', 'Hillary', 'B.', 'Padilla', 'BS Math', 'female', '2013'),
('2014-34533', 'pass34533', 'Ian', 'D.', 'Lopez', 'BS Math', 'male', '2014'),
('2015-35534', 'pass35534', 'Joyce', 'G.', 'Alvarez', 'BS Math', 'female', '2015'),
('2016-36535', 'pass36535', 'Karl', 'F.', 'Gomez', 'BS Math', 'male', '2016'),
('2017-37536', 'pass37536', 'Liza', 'J.', 'Bautista', 'BS Math', 'female', '2017'),
('2018-38537', 'pass38537', 'Miguel', 'K.', 'Chan', 'BS Math', 'male', '2018'),
('2019-39538', 'pass39538', 'Nadine', 'L.', 'Estrada', 'BS Math', 'female', '2019'),
('2020-40539', 'pass40539', 'Omar', 'M.', 'Francisco', 'BS Math', 'male', '2020'),
('2021-41540', 'pass41540', 'Paula', 'O.', 'Garcia', 'BS Math', 'female', '2021'),
('2022-42541', 'pass42541', 'Quincy', 'N.', 'Hernandez', 'BS Math', 'male', '2022');

INSERT INTO membership VALUES
('1984-04503', 17, '1987-1988', '1st Semester', 'alumni', 'President', NULL),
('1985-05504', 17, '1988-1989', '1st Semester', 'alumni', 'President', NULL),
('1986-06505', 17, '1989-1990', '1st Semester', 'alumni', 'President', NULL),
('1987-07506', 17, '1990-1991', '1st Semester', 'alumni', 'President', NULL),
('1988-08507', 17, '1991-1992', '1st Semester', 'alumni', 'President', NULL),
('1989-09508', 17, '1992-1993', '1st Semester', 'alumni', 'President', NULL),
('1990-10509', 17, '1993-1994', '1st Semester', 'alumni', 'President', NULL),
('1991-11510', 17, '1994-1995', '1st Semester', 'alumni', 'President', NULL),
('1992-12511', 17, '1995-1996', '1st Semester', 'alumni', 'President', NULL),
('1993-13512', 17, '1996-1997', '1st Semester', 'alumni', 'President', NULL),
('1994-14513', 17, '1997-1998', '1st Semester', 'alumni', 'President', NULL),
('1995-15514', 17, '1998-1999', '1st Semester', 'alumni', 'President', NULL),
('1996-16515', 17, '1999-2000', '1st Semester', 'alumni', 'President', NULL),
('1997-17516', 17, '2000-2001', '1st Semester', 'alumni', 'President', NULL),
('1998-18517', 17, '2001-2002', '1st Semester', 'alumni', 'President', NULL),
('1999-19518', 17, '2002-2003', '1st Semester', 'alumni', 'President', NULL),
('2000-20519', 17, '2003-2004', '1st Semester', 'alumni', 'President', NULL),
('2001-21520', 17, '2004-2005', '1st Semester', 'alumni', 'President', NULL),
('2002-22521', 17, '2005-2006', '1st Semester', 'alumni', 'President', NULL),
('2003-23522', 17, '2006-2007', '1st Semester', 'alumni', 'President', NULL),
('2004-24523', 17, '2007-2008', '1st Semester', 'alumni', 'President', NULL),
('2005-25524', 17, '2008-2009', '1st Semester', 'alumni', 'President', NULL),
('2006-26525', 17, '2009-2010', '1st Semester', 'alumni', 'President', NULL),
('2007-27526', 17, '2010-2011', '1st Semester', 'alumni', 'President', NULL),
('2008-28527', 17, '2011-2012', '1st Semester', 'alumni', 'President', NULL),
('2009-29528', 17, '2012-2013', '1st Semester', 'alumni', 'President', NULL),
('2010-30529', 17, '2013-2014', '1st Semester', 'alumni', 'President', NULL),
('2011-31530', 17, '2014-2015', '1st Semester', 'alumni', 'President', NULL),
('2012-32531', 17, '2015-2016', '1st Semester', 'alumni', 'President', NULL),
('2013-33532', 17, '2016-2017', '1st Semester', 'alumni', 'President', NULL),
('2014-34533', 17, '2017-2018', '1st Semester', 'alumni', 'President', NULL),
('2015-35534', 17, '2018-2019', '1st Semester', 'alumni', 'President', NULL),
('2016-36535', 17, '2019-2020', '1st Semester', 'alumni', 'President', NULL),
('2017-37536', 17, '2020-2021', '1st Semester', 'alumni', 'President', NULL),
('2018-38537', 17, '2021-2022', '1st Semester', 'alumni', 'President', NULL),
('2019-39538', 17, '2022-2023', '1st Semester', 'alumni', 'President', NULL);

INSERT INTO fee VALUES
('FX156700', '2023-00001', 17, '1st Semester', '2024-08-15', 300.00), -- Fully Paid on time
('FX156701', '2023-00002', 17, '1st Semester', '2024-08-15', 300.00), -- Paid late
('FX156702', '2023-00003', 18, '1st Semester', '2024-08-15', 250.00), -- Unpaid
('FX156703', '2023-00005', 20, '1st Semester', '2024-08-15', 200.00), -- Fully Paid on time
('FX156704', '2023-00006', 21, '1st Semester', '2024-08-15', 275.00), -- Unpaid
('FX156705', '2023-00007', 22, '1st Semester', '2024-08-15', 150.00), -- Paid late
('FX156706', '2023-00008', 23, '1st Semester', '2024-08-15', 225.00), -- Fully Paid on time
('FX156707', '2023-10396', 17, '1st Semester', '2024-08-15', 300.00), -- Paid late
('FX156708', '2023-00004', 19, '1st Semester', '2024-08-15', 180.00), -- Unpaid (inactive member)
('FX156709', '2023-00010', 18, '1st Semester', '2024-08-15', 250.00); -- Fully Paid on time (inactive member)

INSERT INTO payment VALUES
('PX156700', '2023-00001', 17, '2024-08-10', 300.00, 'FX156700'),   -- Paid on time (before or on due date)
('PX156701', '2023-00002', 17, '2024-09-01', 300.00, 'FX156701'),   -- Paid late
('PX156703', '2023-00005', 20, '2024-08-12', 200.00, 'FX156703'),   -- Paid on time
('PX156705', '2023-00007', 22, '2024-08-25', 150.00, 'FX156705'),   -- Paid late
('PX156706', '2023-00008', 23, '2024-08-14', 225.00, 'FX156706'),   -- Paid on time
('PX156707', '2023-10396', 17, '2024-08-30', 300.00, 'FX156707'),   -- Paid late
('PX156709', '2023-00010', 18, '2024-08-15', 250.00, 'FX156709');   -- Paid on time (inactive member)
