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
  DECLARE tou ENUM('Flat','PeakOffPeak');
  DECLARE rate DECIMAL(10,4);

  /* Resolve IDs and TOU */
  SELECT VehicleID INTO vID
    FROM vehicles
    WHERE TRIM(Nickname)=TRIM(pVehicle)
    LIMIT 1;

  SELECT TariffID, TimeOfUse INTO tID, tou
    FROM tariffs
    WHERE TRIM(Name)=TRIM(pTariff)
    LIMIT 1;

  /* Compute rate */
  IF tou = 'Flat' THEN
    SELECT COALESCE(Rate_Per_kWh, 0.15) INTO rate
    FROM tariffs
    WHERE TariffID = tID;
  ELSE
    /* PeakOffPeak: simple heuristic — 07:00–21:59 is peak */
    IF HOUR(pStartTime) BETWEEN 7 AND 21 THEN
      SELECT COALESCE(PeakRate, COALESCE(Rate_Per_kWh, 0.15)) INTO rate
      FROM tariffs
      WHERE TariffID = tID;
    ELSE
      SELECT COALESCE(OffPeakRate, COALESCE(Rate_Per_kWh, 0.15)) INTO rate
      FROM tariffs
      WHERE TariffID = tID;
    END IF;
  END IF;

  /* Insert/update with computed cost */
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