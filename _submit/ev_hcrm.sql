-- EV-HCRM Final Project Database (Part 2)
-- Author: Irfan Ahmed
-- Date: 2025-12-04
-- Contents: schema (4 tables), foreign keys with ON UPDATE/DELETE CASCADE, composite PK (no integer id), seed data (>=30 rows), index, view with aggregates, stored procedures (get/add/update/delete).


DROP DATABASE IF EXISTS ev_hcrm;
CREATE DATABASE ev_hcrm;
USE ev_hcrm;

-- =========================
-- Tables
-- =========================

-- Drivers
CREATE TABLE drivers (
  DriverID INT AUTO_INCREMENT PRIMARY KEY,
  First_Name VARCHAR(50) NOT NULL,
  Last_Name  VARCHAR(50) NOT NULL,
  Email      VARCHAR(100) UNIQUE NOT NULL,
  IsPrimary  TINYINT(1) NOT NULL DEFAULT 0
);

-- Vehicles
CREATE TABLE vehicles (
  VehicleID INT AUTO_INCREMENT PRIMARY KEY,
  DriverID  INT NOT NULL,
  VIN       CHAR(17) UNIQUE NOT NULL,
  Nickname  VARCHAR(40),
  CONSTRAINT fk_vehicle_driver
    FOREIGN KEY (DriverID) REFERENCES drivers(DriverID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Tariffs
CREATE TABLE tariffs (
  TariffID      INT AUTO_INCREMENT PRIMARY KEY,
  Name          VARCHAR(50) NOT NULL,
  TimeOfUse     ENUM('Flat','PeakOffPeak') NOT NULL,
  Rate_Per_kWh  DECIMAL(5,2),
  PeakRate      DECIMAL(5,2),
  OffPeakRate   DECIMAL(5,2)
);

-- Charging Sessions
-- Requirement: composite PK (no separate integer id)
CREATE TABLE charging_sessions (
  VehicleID  INT NOT NULL,
  TariffID   INT NOT NULL,
  StartDate  DATE NOT NULL,
  StartTime  TIME NOT NULL,
  EndDate    DATE NOT NULL,
  EndTime    TIME NOT NULL,
  kWh        DECIMAL(6,2) NOT NULL,
  Cost       DECIMAL(7,2) NOT NULL,
  CONSTRAINT pk_charging_sessions PRIMARY KEY (VehicleID, StartDate, StartTime),
  CONSTRAINT fk_cs_vehicle
    FOREIGN KEY (VehicleID) REFERENCES vehicles(VehicleID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_cs_tariff
    FOREIGN KEY (TariffID) REFERENCES tariffs(TariffID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Helpful index for month queries
CREATE INDEX idx_cs_startdate ON charging_sessions(StartDate);

-- =========================
-- Seed Data
-- =========================
INSERT INTO drivers (First_Name, Last_Name, Email, IsPrimary)
VALUES ('Alice','Green','alice@example.com',1),
       ('Bob','Smith','bob@example.com',0);

INSERT INTO vehicles (DriverID, VIN, Nickname)
VALUES (1,'1HGCM82633A004352','Tesla Model 3'),
       (2,'1HGCM82633A004353','Chevy Bolt');

INSERT INTO tariffs (Name, TimeOfUse, Rate_Per_kWh, PeakRate, OffPeakRate)
VALUES ('Flat Rate','Flat',0.15,NULL,NULL),
       ('TOU','PeakOffPeak',NULL,0.20,0.10);

-- Generate at least 30 rows for December 2025
-- We mix flat and TOU sessions across both vehicles
INSERT INTO charging_sessions (VehicleID, TariffID, StartDate, StartTime, EndDate, EndTime, kWh, Cost)
VALUES
-- First 16 sessions (Vehicle 1, Flat Rate)
(1, 1, '2025-12-01','18:05:00','2025-12-01','20:10:00',18.2, 18.2*0.15),
(1, 1, '2025-12-02','19:10:00','2025-12-02','21:00:00',14.7, 14.7*0.15),
(1, 1, '2025-12-03','20:15:00','2025-12-03','22:05:00',16.1, 16.1*0.15),
(1, 1, '2025-12-04','18:40:00','2025-12-04','20:25:00',12.9, 12.9*0.15),
(1, 1, '2025-12-05','19:30:00','2025-12-05','21:15:00',17.3, 17.3*0.15),
(1, 1, '2025-12-06','18:00:00','2025-12-06','20:00:00',15.0, 15.0*0.15),
(1, 1, '2025-12-07','20:10:00','2025-12-07','22:20:00',21.4, 21.4*0.15),
(1, 1, '2025-12-08','18:55:00','2025-12-08','20:45:00',13.6, 13.6*0.15),
(1, 1, '2025-12-09','19:05:00','2025-12-09','21:00:00',15.9, 15.9*0.15),
(1, 1, '2025-12-10','18:25:00','2025-12-10','20:05:00',12.5, 12.5*0.15),
(1, 1, '2025-12-11','19:45:00','2025-12-11','21:30:00',18.6, 18.6*0.15),
(1, 1, '2025-12-12','20:00:00','2025-12-12','22:00:00',22.2, 22.2*0.15),
(1, 1, '2025-12-13','18:15:00','2025-12-13','20:15:00',14.4, 14.4*0.15),
(1, 1, '2025-12-14','19:20:00','2025-12-14','21:10:00',16.8, 16.8*0.15),
(1, 1, '2025-12-15','18:35:00','2025-12-15','20:30:00',13.1, 13.1*0.15),
(1, 1, '2025-12-16','20:05:00','2025-12-16','22:10:00',19.7, 19.7*0.15),

-- Next 16 sessions (Vehicle 2, TOU; 50% peak, 50% off-peak)
(2, 2, '2025-12-01','18:00:00','2025-12-01','20:00:00',12.0, (12.0/2)*0.20 + (12.0/2)*0.10),
(2, 2, '2025-12-02','19:00:00','2025-12-02','21:00:00',13.5, (13.5/2)*0.20 + (13.5/2)*0.10),
(2, 2, '2025-12-03','20:00:00','2025-12-03','22:00:00',15.2, (15.2/2)*0.20 + (15.2/2)*0.10),
(2, 2, '2025-12-04','18:30:00','2025-12-04','20:30:00',11.4, (11.4/2)*0.20 + (11.4/2)*0.10),
(2, 2, '2025-12-05','19:20:00','2025-12-05','21:20:00',16.9, (16.9/2)*0.20 + (16.9/2)*0.10),
(2, 2, '2025-12-06','20:10:00','2025-12-06','22:10:00',18.3, (18.3/2)*0.20 + (18.3/2)*0.10),
(2, 2, '2025-12-07','18:45:00','2025-12-07','20:45:00',10.8, (10.8/2)*0.20 + (10.8/2)*0.10),
(2, 2, '2025-12-08','19:35:00','2025-12-08','21:35:00',14.6, (14.6/2)*0.20 + (14.6/2)*0.10),
(2, 2, '2025-12-09','20:25:00','2025-12-09','22:25:00',17.1, (17.1/2)*0.20 + (17.1/2)*0.10),
(2, 2, '2025-12-10','18:10:00','2025-12-10','20:10:00',12.7, (12.7/2)*0.20 + (12.7/2)*0.10),
(2, 2, '2025-12-11','19:50:00','2025-12-11','21:50:00',19.9, (19.9/2)*0.20 + (19.9/2)*0.10),
(2, 2, '2025-12-12','20:15:00','2025-12-12','22:15:00',21.0, (21.0/2)*0.20 + (21.0/2)*0.10),
(2, 2, '2025-12-13','18:25:00','2025-12-13','20:25:00',11.6, (11.6/2)*0.20 + (11.6/2)*0.10),
(2, 2, '2025-12-14','19:05:00','2025-12-14','21:05:00',13.8, (13.8/2)*0.20 + (13.8/2)*0.10),
(2, 2, '2025-12-15','20:00:00','2025-12-15','22:00:00',16.2, (16.2/2)*0.20 + (16.2/2)*0.10),
(2, 2, '2025-12-16','18:55:00','2025-12-16','20:55:00',12.4, (12.4/2)*0.20 + (12.4/2)*0.10);

-- =========================
-- View(s)
-- =========================
CREATE OR REPLACE VIEW monthly_statements AS
SELECT
  d.First_Name,
  d.Last_Name,
  v.Nickname,
  DATE_FORMAT(cs.StartDate, '%Y-%m') AS BillingMonth,
  COUNT(*) AS TotalSessions,
  SUM(cs.kWh) AS Total_kWh,
  SUM(cs.Cost) AS TotalCost
FROM charging_sessions cs
JOIN vehicles v ON cs.VehicleID = v.VehicleID
JOIN drivers  d ON v.DriverID   = d.DriverID
GROUP BY BillingMonth, v.VehicleID;

-- =========================
-- Stored Procedures
-- =========================
DELIMITER //

CREATE PROCEDURE getChargingSessions()
BEGIN
  SELECT
    v.Nickname AS Vehicle,
    d.First_Name, d.Last_Name,
    CONCAT(cs.StartDate, ' ', cs.StartTime) AS Start,
    CONCAT(cs.EndDate, ' ', cs.EndTime)     AS End,
    cs.kWh,
    cs.Cost,
    t.Name AS Tariff
  FROM charging_sessions cs
  JOIN vehicles v ON cs.VehicleID = v.VehicleID
  JOIN drivers  d ON v.DriverID   = d.DriverID
  JOIN tariffs  t ON cs.TariffID  = t.TariffID
  ORDER BY cs.StartDate, cs.StartTime;
END //

CREATE PROCEDURE addChargingSession(
  IN vehicleNickname VARCHAR(40),
  IN tariffName      VARCHAR(50),
  IN startDate       DATE, IN startTime TIME,
  IN endDate         DATE, IN endTime   TIME,
  IN inKWh           DECIMAL(6,2)
)
BEGIN
  DECLARE vID INT; DECLARE tID INT; DECLARE cost DECIMAL(7,2);
  SELECT VehicleID INTO vID FROM vehicles WHERE Nickname = vehicleNickname LIMIT 1;
  SELECT TariffID  INTO tID FROM tariffs  WHERE Name     = tariffName      LIMIT 1;

  IF (SELECT TimeOfUse FROM tariffs WHERE TariffID = tID) = 'Flat' THEN
    SET cost = inKWh * (SELECT Rate_Per_kWh FROM tariffs WHERE TariffID = tID);
  ELSE
    -- Simplified TOU: 50% peak, 50% off-peak
    SET cost = (inKWh/2) * (SELECT PeakRate    FROM tariffs WHERE TariffID = tID)
             + (inKWh/2) * (SELECT OffPeakRate FROM tariffs WHERE TariffID = tID);
  END IF;

  INSERT INTO charging_sessions (VehicleID, TariffID, StartDate, StartTime, EndDate, EndTime, kWh, Cost)
  VALUES (vID, tID, startDate, startTime, endDate, endTime, inKWh, cost);
END //

CREATE PROCEDURE updateChargingSession(
  IN inVehicleNickname VARCHAR(40),
  IN inStartDate       DATE, IN inStartTime TIME,
  IN newEndDate        DATE, IN newEndTime  TIME,
  IN newKWh            DECIMAL(6,2)
)
BEGIN
  DECLARE vID INT; DECLARE tID INT; DECLARE cost DECIMAL(7,2);

  SELECT VehicleID INTO vID FROM vehicles WHERE Nickname = inVehicleNickname LIMIT 1;
  SELECT TariffID  INTO tID FROM charging_sessions WHERE VehicleID = vID AND StartDate = inStartDate AND StartTime = inStartTime;

  IF (SELECT TimeOfUse FROM tariffs WHERE TariffID = tID) = 'Flat' THEN
    SET cost = newKWh * (SELECT Rate_Per_kWh FROM tariffs WHERE TariffID = tID);
  ELSE
    SET cost = (newKWh/2) * (SELECT PeakRate    FROM tariffs WHERE TariffID = tID)
             + (newKWh/2) * (SELECT OffPeakRate FROM tariffs WHERE TariffID = tID);
  END IF;

  UPDATE charging_sessions
  SET EndDate = newEndDate,
      EndTime = newEndTime,
      kWh     = newKWh,
      Cost    = cost
  WHERE VehicleID = vID AND StartDate = inStartDate AND StartTime = inStartTime;
END //

CREATE PROCEDURE deleteChargingSession(
  IN inVehicleNickname VARCHAR(40),
  IN inStartDate       DATE,
  IN inStartTime       TIME
)
BEGIN
  DECLARE vID INT;
  SELECT VehicleID INTO vID FROM vehicles WHERE Nickname = inVehicleNickname LIMIT 1;
  DELETE FROM charging_sessions
  WHERE VehicleID = vID AND StartDate = inStartDate AND StartTime = inStartTime;
END //

DELIMITER ;
