-- MySQL dump 10.13  Distrib 9.5.0, for macos15.7 (arm64)
--
-- Host: localhost    Database: ev_hcrm
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `ev_hcrm`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ev_hcrm` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `ev_hcrm`;

--
-- Table structure for table `charging_sessions`
--

DROP TABLE IF EXISTS `charging_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `charging_sessions` (
  `VehicleID` int NOT NULL,
  `TariffID` int NOT NULL,
  `StartDate` date NOT NULL,
  `StartTime` time NOT NULL,
  `EndDate` date NOT NULL,
  `EndTime` time NOT NULL,
  `kWh` decimal(6,2) NOT NULL,
  `Cost` decimal(7,2) NOT NULL,
  PRIMARY KEY (`VehicleID`,`StartDate`,`StartTime`),
  KEY `fk_cs_tariff` (`TariffID`),
  KEY `idx_cs_startdate` (`StartDate`),
  CONSTRAINT `fk_cs_tariff` FOREIGN KEY (`TariffID`) REFERENCES `tariffs` (`TariffID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cs_vehicle` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `charging_sessions`
--

LOCK TABLES `charging_sessions` WRITE;
/*!40000 ALTER TABLE `charging_sessions` DISABLE KEYS */;
INSERT INTO `charging_sessions` VALUES (1,1,'2025-12-01','18:05:00','2025-12-01','20:10:00',18.20,2.73),(1,1,'2025-12-02','19:10:00','2025-12-02','21:00:00',14.70,2.21),(1,1,'2025-12-03','20:15:00','2025-12-03','22:05:00',16.10,2.42),(1,1,'2025-12-04','18:40:00','2025-12-04','20:25:00',12.90,1.94),(1,1,'2025-12-05','19:30:00','2025-12-05','21:15:00',17.30,2.60),(1,1,'2025-12-06','18:00:00','2025-12-06','20:00:00',15.00,2.25),(1,1,'2025-12-07','20:10:00','2025-12-07','22:20:00',21.40,3.21),(1,1,'2025-12-08','18:55:00','2025-12-08','20:45:00',13.60,2.04),(1,1,'2025-12-09','19:05:00','2025-12-09','21:00:00',15.90,2.39),(1,1,'2025-12-10','18:25:00','2025-12-10','20:05:00',12.50,1.88),(1,1,'2025-12-11','19:45:00','2025-12-11','21:30:00',18.60,2.79),(1,1,'2025-12-12','20:00:00','2025-12-12','22:00:00',22.20,3.33),(1,1,'2025-12-13','18:15:00','2025-12-13','20:15:00',14.40,2.16),(1,1,'2025-12-14','19:20:00','2025-12-14','21:10:00',16.80,2.52),(1,1,'2025-12-15','18:35:00','2025-12-15','20:30:00',13.10,1.97),(1,1,'2025-12-16','20:05:00','2025-12-16','22:10:00',19.70,2.96),(2,2,'2025-12-01','18:00:00','2025-12-01','20:00:00',12.00,1.80),(2,2,'2025-12-02','19:00:00','2025-12-02','21:00:00',13.50,2.03),(2,2,'2025-12-03','20:00:00','2025-12-03','22:00:00',15.20,2.28),(2,2,'2025-12-04','18:30:00','2025-12-04','20:30:00',11.40,1.71),(2,2,'2025-12-05','19:20:00','2025-12-05','21:20:00',16.90,2.54),(2,2,'2025-12-06','20:10:00','2025-12-06','22:10:00',18.30,2.75),(2,2,'2025-12-07','18:45:00','2025-12-07','20:45:00',10.80,1.62),(2,2,'2025-12-08','19:35:00','2025-12-08','21:35:00',14.60,2.19),(2,2,'2025-12-09','20:25:00','2025-12-09','22:25:00',17.10,2.57),(2,2,'2025-12-10','18:10:00','2025-12-10','20:10:00',12.70,1.91),(2,2,'2025-12-11','19:50:00','2025-12-11','21:50:00',19.90,2.99),(2,2,'2025-12-12','20:15:00','2025-12-12','22:15:00',21.00,3.15),(2,2,'2025-12-13','18:25:00','2025-12-13','20:25:00',11.60,1.74),(2,2,'2025-12-14','19:05:00','2025-12-14','21:05:00',13.80,2.07),(2,2,'2025-12-15','20:00:00','2025-12-15','22:00:00',16.20,2.43),(2,2,'2025-12-16','18:55:00','2025-12-16','20:55:00',12.40,1.86);
/*!40000 ALTER TABLE `charging_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drivers`
--

DROP TABLE IF EXISTS `drivers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drivers` (
  `DriverID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(50) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `IsPrimary` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`DriverID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drivers`
--

LOCK TABLES `drivers` WRITE;
/*!40000 ALTER TABLE `drivers` DISABLE KEYS */;
INSERT INTO `drivers` VALUES (1,'Alice','Green','alice@example.com',1),(2,'Bob','Smith','bob@example.com',0);
/*!40000 ALTER TABLE `drivers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `monthly_statements`
--

DROP TABLE IF EXISTS `monthly_statements`;
/*!50001 DROP VIEW IF EXISTS `monthly_statements`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `monthly_statements` AS SELECT 
 1 AS `First_Name`,
 1 AS `Last_Name`,
 1 AS `Nickname`,
 1 AS `BillingMonth`,
 1 AS `TotalSessions`,
 1 AS `Total_kWh`,
 1 AS `TotalCost`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `session_details`
--

DROP TABLE IF EXISTS `session_details`;
/*!50001 DROP VIEW IF EXISTS `session_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `session_details` AS SELECT 
 1 AS `DriverFirstName`,
 1 AS `DriverLastName`,
 1 AS `Vehicle`,
 1 AS `Tariff`,
 1 AS `Start`,
 1 AS `End`,
 1 AS `kWh`,
 1 AS `Cost`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `tariff_list`
--

DROP TABLE IF EXISTS `tariff_list`;
/*!50001 DROP VIEW IF EXISTS `tariff_list`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `tariff_list` AS SELECT 
 1 AS `Name`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `tariffs`
--

DROP TABLE IF EXISTS `tariffs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tariffs` (
  `TariffID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `TimeOfUse` enum('Flat','PeakOffPeak') NOT NULL,
  `Rate_Per_kWh` decimal(5,2) DEFAULT NULL,
  `PeakRate` decimal(5,2) DEFAULT NULL,
  `OffPeakRate` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`TariffID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tariffs`
--

LOCK TABLES `tariffs` WRITE;
/*!40000 ALTER TABLE `tariffs` DISABLE KEYS */;
INSERT INTO `tariffs` VALUES (1,'Flat Rate','Flat',0.15,NULL,NULL),(2,'TOU','PeakOffPeak',NULL,0.20,0.10);
/*!40000 ALTER TABLE `tariffs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vehicle_list`
--

DROP TABLE IF EXISTS `vehicle_list`;
/*!50001 DROP VIEW IF EXISTS `vehicle_list`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vehicle_list` AS SELECT 
 1 AS `Nickname`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicles` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `DriverID` int NOT NULL,
  `VIN` char(17) NOT NULL,
  `Nickname` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`VehicleID`),
  UNIQUE KEY `VIN` (`VIN`),
  KEY `fk_vehicle_driver` (`DriverID`),
  CONSTRAINT `fk_vehicle_driver` FOREIGN KEY (`DriverID`) REFERENCES `drivers` (`DriverID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
INSERT INTO `vehicles` VALUES (1,1,'1HGCM82633A004352','Tesla Model 3'),(2,2,'1HGCM82633A004353','Chevy Bolt');
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'ev_hcrm'
--

--
-- Dumping routines for database 'ev_hcrm'
--
/*!50003 DROP PROCEDURE IF EXISTS `addChargingSession` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `addChargingSession`(
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `deleteChargingSession` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `deleteChargingSession`(
  IN inVehicleNickname VARCHAR(40),
  IN inStartDate       DATE,
  IN inStartTime       TIME
)
BEGIN
  DECLARE vID INT;
  SELECT VehicleID INTO vID FROM vehicles WHERE Nickname = inVehicleNickname LIMIT 1;
  DELETE FROM charging_sessions
  WHERE VehicleID = vID AND StartDate = inStartDate AND StartTime = inStartTime;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `deleteDriverByEmail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `deleteDriverByEmail`(IN inEmail VARCHAR(100))
BEGIN
  DELETE FROM drivers WHERE Email = inEmail;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `deleteVehicleByNickname` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `deleteVehicleByNickname`(IN inNickname VARCHAR(40))
BEGIN
  DELETE FROM vehicles WHERE Nickname = inNickname;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `getChargingSessions` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `getChargingSessions`()
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `renameVehicle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `renameVehicle`(IN oldNickname VARCHAR(40), IN newNickname VARCHAR(40))
BEGIN
   UPDATE vehicles SET Nickname = newNickname WHERE Nickname = oldNickname;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `updateChargingSession` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `updateChargingSession`(
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `ev_hcrm`
--

USE `ev_hcrm`;

--
-- Final view structure for view `monthly_statements`
--

/*!50001 DROP VIEW IF EXISTS `monthly_statements`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `monthly_statements` AS select `d`.`First_Name` AS `First_Name`,`d`.`Last_Name` AS `Last_Name`,`v`.`Nickname` AS `Nickname`,date_format(`cs`.`StartDate`,'%Y-%m') AS `BillingMonth`,count(0) AS `TotalSessions`,sum(`cs`.`kWh`) AS `Total_kWh`,sum(`cs`.`Cost`) AS `TotalCost` from ((`charging_sessions` `cs` join `vehicles` `v` on((`cs`.`VehicleID` = `v`.`VehicleID`))) join `drivers` `d` on((`v`.`DriverID` = `d`.`DriverID`))) group by `BillingMonth`,`v`.`VehicleID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `session_details`
--

/*!50001 DROP VIEW IF EXISTS `session_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `session_details` AS select `d`.`First_Name` AS `DriverFirstName`,`d`.`Last_Name` AS `DriverLastName`,`v`.`Nickname` AS `Vehicle`,`t`.`Name` AS `Tariff`,concat(`cs`.`StartDate`,' ',`cs`.`StartTime`) AS `Start`,concat(`cs`.`EndDate`,' ',`cs`.`EndTime`) AS `End`,round(`cs`.`kWh`,2) AS `kWh`,round(`cs`.`Cost`,2) AS `Cost` from (((`charging_sessions` `cs` join `vehicles` `v` on((`cs`.`VehicleID` = `v`.`VehicleID`))) join `drivers` `d` on((`v`.`DriverID` = `d`.`DriverID`))) join `tariffs` `t` on((`cs`.`TariffID` = `t`.`TariffID`))) order by `cs`.`StartDate`,`cs`.`StartTime` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `tariff_list`
--

/*!50001 DROP VIEW IF EXISTS `tariff_list`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `tariff_list` AS select `tariffs`.`Name` AS `Name` from `tariffs` order by `tariffs`.`Name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vehicle_list`
--

/*!50001 DROP VIEW IF EXISTS `vehicle_list`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vehicle_list` AS select `vehicles`.`Nickname` AS `Nickname` from `vehicles` order by `vehicles`.`Nickname` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-20 18:26:33
