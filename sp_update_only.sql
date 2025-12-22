DROP PROCEDURE IF EXISTS updateChargingSession;
DELIMITER $$
CREATE PROCEDURE updateChargingSession(
  IN pVehicle   VARCHAR(255),
  IN pStartDate DATE,
  IN pStartTime TIME,
  IN pEndDate   DATE,
  IN pEndTime   TIME,
  IN pKwh       DECIMAL(10,2)
)
BEGIN
  UPDATE charging_sessions cs
  JOIN vehicles v ON v.VehicleID = cs.VehicleID
  SET cs.EndDate = pEndDate,
      cs.EndTime = pEndTime,
      cs.kWh    = pKwh
  WHERE TRIM(v.Nickname) = TRIM(pVehicle)
    AND cs.StartDate = pStartDate
    AND cs.StartTime = pStartTime;
END$$
DELIMITER ;