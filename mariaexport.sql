-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.6.23-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for major6
DROP DATABASE IF EXISTS `major6`;
CREATE DATABASE IF NOT EXISTS `major6` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `major6`;

-- Dumping structure for table major6.registration
DROP TABLE IF EXISTS `registration`;
CREATE TABLE IF NOT EXISTS `registration` (
  `enrollment` varchar(15) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(300) NOT NULL,
  `course` varchar(30) NOT NULL,
  `role` varchar(30) NOT NULL,
  PRIMARY KEY (`enrollment`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table major6.registration: ~3 rows (approximately)
DELETE FROM `registration`;
INSERT INTO `registration` (`enrollment`, `name`, `email`, `password`, `course`, `role`) VALUES
	('adm-2026', 'Nitin Kumar', 'nitinkumar23@gmail.com', 'scrypt:32768:8:1$FGoi7yQZQPU0iAsS$951b05b850871002a56778b15f20464b331d30444c934c5a72e0e6a001a392b4b0bf47b01b3064d0c15e6c931d116811cea1c23b6db53fd78caa16c4ad07a4a0', 'admin', 'admin'),
	('sai-12345', 'Aatish Rana', 'nitin2334@gmail.com', 'scrypt:32768:8:1$LTezV1Vc6gDq8JOh$b01d7d7339b11b631ac130fa56140d2f8de7bb1511f8047a04f85de455c972df9eb94546523ba482ea04e509f05668ac3eff3b17805db8020207b6745c69d22c', 'BCA', 'student'),
	('sai-9090', 'Adnan Amir', 'adnanamir34@gmail.com', 'scrypt:32768:8:1$Mmcrtxu431jE6zzA$e04ce134c6b5ff9eab281d57cfdfe5993de01d884b1d53e4f2fd9f72afdbd2d9f85581c25ee6baebb8e139c50d936de818123a41099346c0d622ec25c213da8a', 'CS', 'teacher');

-- Dumping structure for table major6.result
DROP TABLE IF EXISTS `result`;
CREATE TABLE IF NOT EXISTS `result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enrollment` varchar(45) DEFAULT NULL,
  `semester` int(11) DEFAULT NULL,
  `subject` varchar(45) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL,
  `batch` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `enrollment` (`enrollment`),
  CONSTRAINT `result_ibfk_1` FOREIGN KEY (`enrollment`) REFERENCES `registration` (`enrollment`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table major6.result: ~4 rows (approximately)
DELETE FROM `result`;
INSERT INTO `result` (`id`, `enrollment`, `semester`, `subject`, `marks`, `batch`) VALUES
	(1, 'sai-12345', 1, 'C Programming', 34, '2023'),
	(2, 'sai-12345', 1, 'Mathematics', 45, '2023'),
	(3, 'sai-12345', 1, 'English', 56, '2023'),
	(4, 'sai-12345', 1, 'Computer Fundamentals', 34, '2023');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
