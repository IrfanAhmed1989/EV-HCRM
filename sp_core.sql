DROP PROCEDURE IF EXISTS addChargingSession;
DELIMITER $$
CREATE PROCEDURE addChargingSession(
  IN pVehicle   VARCHAR(255),
  IN pTariff    VARCHAR(255),
  IN pStartDate DATE,
  IN pStartTime TIME,
  IN pEndDate   DATE,
  IN pEndTime   TIME,
  IN pKwh       DECIMAL(10,2)
)
BEGIN
  DECLARE vID INT;
  DECLARE tID INT;
  DECLARE rate DECIMAL(10,4);

  SELECT VehicleID INTO vID
    FROM vehicles
    WHERE TRIM(Nickname)=TRIM(pVehicle)
    LIMIT 1;

  SELECT TariffID, Rate INTO tID, rate
    FROM tariffs
    WHERE TRIM(Name)=TRIM(pTariff)
    LIMIT 1;

  /* Insert or update same PK (VehicleID, StartDate, StartTime) */
  INSERT INTO charging_sessions
    (VehicleID, TariffID, StartDate, StartTime, EndDate, EndTime, kWh, Cost)
  VALUES
    (vID, tID, pStartDate, pStartTime, pEndDate, pEndTime, pKwh, pKwh * rate)
  ON DUPLICATE KEY UPDATE
    EndDate = VALUES(EndDate),
    EndTime = VALUES(EndTime),
    kWh     = VALUES(kWh),
    Cost    = VALUES(Cost);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS getChargingSessions;
DELIMITER $$
CREATE PROCEDURE getChargingSessions()
BEGIN
  SELECT * FROM charging_sessions ORDER BY StartDate, StartTime;
END$$
DELIMITER ;
