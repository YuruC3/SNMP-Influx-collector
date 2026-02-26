-- Set correct timezone 
SET GLOBAL time_zone = 'Europe/Stockholm';

SET NAMES utf8;
SET time_zone = '+01:00';
-- SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- DELIMITER ;;

-- DROP EVENT IF EXISTS `Prune_old_entries_staging_sensr`;;

-- CREATE EVENT `Prune_old_entries_staging_sensr` 
-- ON SCHEDULE EVERY 1 DAY STARTS '2024-07-17 22:00:00' 
-- ON COMPLETION 
-- NOT PRESERVE 
-- DISABLE ON SLAVE DO 
-- DELETE FROM staging_sensr 
-- WHERE time_stamp < NOW() - INTERVAL 2 MONTH;;

-- DELIMITER ;

SET NAMES utf8mb4;



-- New universal table type
CREATE TABLE newUniversalSensorTable (
    id MEDIUMINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    hostname TEXT(30),
    powerDrawPSU1 TINYINT(100),
    powerDrawPSU2 TINYINT(100) NULL,
    voltagePSU1 TINYINT(100),
    voltagePSU2 TINYINT(100) NULL,
    inletTemp FLOAT,
    exhaustTemp FLOAT,
    uptime INT NULL,
    pressure FLOAT NULL,
    altitude FLOAT NULL

);

