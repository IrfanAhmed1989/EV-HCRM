USE ev_hcrm;
SHOW PROCEDURE STATUS
  WHERE Db='ev_hcrm'
    AND Name IN ('deleteVehicleByNickname','renameVehicle');
