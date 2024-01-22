-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: db-mysql-lon1-67456-do-user-15430802-0.c.db.ondigitalocean.com:25060
-- Generation Time: Jan 22, 2024 at 10:09 PM
-- Server version: 8.0.30
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bot_discord`
--
CREATE DATABASE IF NOT EXISTS `bot_discord` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `bot_discord`;

-- --------------------------------------------------------

--
-- Table structure for table `MESSAGE`
--

CREATE TABLE `MESSAGE` (
  `ID_MESSAGE` bigint NOT NULL,
  `CONTENT` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `DATE` datetime NOT NULL,
  `ID_USER` bigint NOT NULL,
  `ID_SERVER` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `SERVER`
--

CREATE TABLE `SERVER` (
  `ID_SERVER` bigint NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `ICON_URL` varchar(255) DEFAULT NULL,
  `NB_USER` int NOT NULL,
  `JOIN_DATE` date NOT NULL,
  `CAN_JOIN_VOC` tinyint(1) NOT NULL,
  `STATUS` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `SPAM`
--

CREATE TABLE `SPAM` (
  `ID_SPAM` bigint NOT NULL,
  `NB_REP` int NOT NULL,
  `CONTENT` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `DATE` datetime NOT NULL,
  `ID_USER` bigint NOT NULL,
  `ID_SERVER` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `USER`
--

CREATE TABLE `USER` (
  `ID_USER` bigint NOT NULL,
  `NAME` varchar(32) NOT NULL,
  `NAME_GLOBAL` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `PP_URL` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `USER_SERVER`
--

CREATE TABLE `USER_SERVER` (
  `ID_USER` bigint NOT NULL,
  `ID_SERVER` bigint NOT NULL,
  `NAME_SERVER` varchar(32) NOT NULL,
  `PP_URL_SERVER` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `VOCAL_SESSION`
--

CREATE TABLE `VOCAL_SESSION` (
  `ID_VOC` int NOT NULL,
  `JOIN` int NOT NULL,
  `QUIT` int DEFAULT NULL,
  `ID_USER` bigint NOT NULL,
  `ID_SERVER` bigint NOT NULL,
  `TIME_VOC` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `MESSAGE`
--
ALTER TABLE `MESSAGE`
  ADD PRIMARY KEY (`ID_MESSAGE`),
  ADD KEY `MESS_ID_SERVER_idx` (`ID_SERVER`),
  ADD KEY `MESS_ID_USER_idx` (`ID_USER`);

--
-- Indexes for table `SERVER`
--
ALTER TABLE `SERVER`
  ADD PRIMARY KEY (`ID_SERVER`);

--
-- Indexes for table `SPAM`
--
ALTER TABLE `SPAM`
  ADD PRIMARY KEY (`ID_SPAM`),
  ADD KEY `SPAM_ID_USER_idx` (`ID_USER`),
  ADD KEY `SPAM_ID_SERVER_idx` (`ID_SERVER`);

--
-- Indexes for table `USER`
--
ALTER TABLE `USER`
  ADD PRIMARY KEY (`ID_USER`);

--
-- Indexes for table `USER_SERVER`
--
ALTER TABLE `USER_SERVER`
  ADD PRIMARY KEY (`ID_USER`,`ID_SERVER`),
  ADD KEY `USR_SERV_ID_SERVER_idx` (`ID_SERVER`);

--
-- Indexes for table `VOCAL_SESSION`
--
ALTER TABLE `VOCAL_SESSION`
  ADD PRIMARY KEY (`ID_VOC`),
  ADD KEY `VOC_SESSION_ID_USER_idx` (`ID_USER`),
  ADD KEY `VOC_SESSION_ID_SERVER_idx` (`ID_SERVER`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `VOCAL_SESSION`
--
ALTER TABLE `VOCAL_SESSION`
  MODIFY `ID_VOC` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `MESSAGE`
--
ALTER TABLE `MESSAGE`
  ADD CONSTRAINT `MESS_ID_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `MESS_ID_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);

--
-- Constraints for table `SPAM`
--
ALTER TABLE `SPAM`
  ADD CONSTRAINT `SPAM_ID_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `SPAM_ID_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);

--
-- Constraints for table `USER_SERVER`
--
ALTER TABLE `USER_SERVER`
  ADD CONSTRAINT `USR_SERV_ID_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `USR_SERV_ID_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);

--
-- Constraints for table `VOCAL_SESSION`
--
ALTER TABLE `VOCAL_SESSION`
  ADD CONSTRAINT `VOC_SESSION_ID_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `VOC_SESSION_ID_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
