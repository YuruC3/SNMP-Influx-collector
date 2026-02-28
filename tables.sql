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
CREATE TABLE idracHOSTNAMECHANGEME (
    id MEDIUMINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    hostname TEXT(30),
    powerDrawPSU1 FLOAT,
    powerDrawPSU2 FLOAT NULL,
    voltagePSU1 TINYINT(100),
    voltagePSU2 TINYINT(100) NULL,
    inletTemp FLOAT,
    exhaustTemp FLOAT,
    cpu1Temp FLOAT,
    cpu2Temp FLOAT NULL,
    uptimeH INT ,
    uptimeD FLOAT NULL

);

CREATE TABLE fansHOSTNAMEHERE (
    id MEDIUMINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    hostname TEXT(30),
    FANxxxRPM INT

);



CREATE TABLE ciscoHOSTNAMEHERE (
    id MEDIUMINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    hostname TEXT(30),
    something INT

);