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

  /* Resolve IDs */
  SELECT VehicleID INTO vID FROM vehicles WHERE TRIM(Nickname)=TRIM(pVehicle) LIMIT 1;
  SELECT TariffID  INTO tID FROM tariffs  WHERE TRIM(Name)=TRIM(pTariff)   LIMIT 1;

  /* Get rate from VIEW (column name is normalized here), default to 0.15 */
  SELECT COALESCE(Rate, 0.15) INTO rate
  FROM tariff_list
  WHERE TRIM(Name)=TRIM(pTariff)
  LIMIT 1;

  /* Insert with computed cost; update same PK if it already exists */
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