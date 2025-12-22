
USE ev_hcrm;
DELIMITER //
DROP PROCEDURE IF EXISTS deleteVehicleByNickname;
CREATE PROCEDURE deleteVehicleByNickname(IN inNickname VARCHAR(40))
BEGIN
  DELETE FROM vehicles WHERE Nickname = inNickname;
END //
DROP PROCEDURE IF EXISTS renameVehicle;
CREATE PROCEDURE renameVehicle(IN oldNickname VARCHAR(40), IN newNickname VARCHAR(40))
BEGIN
  UPDATE vehicles SET Nickname = newNickname WHERE Nickname = oldNickname;
END //
DEL
USE ev_hcrm;
DELIMITER //
// Delete a vehicle by nickname (cascade removes its sessions)
CREATE PROCEDURE deleteVehicleByNickname(IN inNickname VARCHAR(40))
BEGIN
  DELETE FROM vehicles WHERE Nickname = inNickname;
END //

// Rename a vehicle nickname (demonstrates parent update)
CREATE PROCEDURE renameVehicle(IN oldNickname VARCHAR(40), IN newNickname VARCHAR(40))
BEGIN
  UPDATE vehicles SET Nickname = newNickname WHERE Nickname = oldNickname;
END //
DELIMITER ;
