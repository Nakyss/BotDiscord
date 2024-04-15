-- Table structure for table `LAST_SPAM`
CREATE TABLE `LAST_SPAM` (
  `ID_SPAM`     bigint  NOT NULL,
  `ID_CHANNEL`  bigint  NOT NULL,
  `ID_MESSAGE`  bigint  NOT NULL,
  CONSTRAINT PK_LAST_SPAM PRIMARY KEY (`ID_MESSAGE`)
);


-- Table structure for table `MESSAGE`
CREATE TABLE `MESSAGE` (
  `ID_MESSAGE`      bigint    NOT NULL,
  `LENGTH`          smallint  NULL,
  `NB_ATTACHMEMTS`  tinyint   NULL,
  `DATE`            datetime  NOT NULL,
  `ID_USER`         bigint    NOT NULL,
  `ID_SERVER`       bigint    NOT NULL,
  CONSTRAINT PK_MESSAGE PRIMARY KEY (`ID_MESSAGE`)
);


-- Table structure for table `SERVER`
CREATE TABLE `SERVER` (
  `ID_SERVER`     bigint          NOT NULL,
  `NAME`          varchar(32)     NOT NULL,
  `ICON_URL`      varchar(255)    NULL,
  `NB_USER`       int             NOT NULL,
  `JOIN_DATE`     date            NOT NULL,
  `CAN_JOIN_VOC`  tinyint(1)      NOT NULL,
  `STATUS`        tinyint(1)      NOT NULL,
  CONSTRAINT PK_SERVER PRIMARY KEY (`ID_SERVER`)
);


-- Table structure for table `SPAM`
CREATE TABLE `SPAM` (
  `ID_SPAM`     bigint          NOT NULL,
  `NB_REP`      int             NOT NULL,
  `CONTENT`     varchar(2000)   NOT NULL,
  `DATE`        datetime        NOT NULL,
  `ID_USER`     bigint          NOT NULL,
  `ID_SERVER`   bigint          NOT NULL,
  CONSTRAINT PK_SPAM PRIMARY KEY (`ID_SPAM`)
);


-- Table structure for table `USER`
CREATE TABLE `USER` (
  `ID_USER`       bigint        NOT NULL,
  `NAME`          varchar(32)   NOT NULL,
  `NAME_GLOBAL`   varchar(32)   NOT NULL,
  `PP_URL`        varchar(255)  NOT NULL,
  CONSTRAINT PK_USER PRIMARY KEY (`ID_USER`)
);


-- Table structure for table `USER_SERVER`
CREATE TABLE `USER_SERVER` (
  `ID_USER`         bigint        NOT NULL,
  `ID_SERVER`       bigint        NOT NULL,
  `NAME_SERVER`     varchar(32)   NOT NULL,
  `PP_URL_SERVER`   varchar(255)  NOT NULL,
  CONSTRAINT PK_USER_SERVER PRIMARY KEY (`ID_USER`,`ID_SERVER`)
);


-- Table structure for table `VOCAL_SESSION`
CREATE TABLE `VOCAL_SESSION` (
  `ID_VOC`      int     NOT NULL AUTO_INCREMENT,
  `JOIN`        int     NOT NULL,
  `QUIT`        int     NULL,
  `ID_USER`     bigint  NOT NULL,
  `ID_SERVER`   bigint  NOT NULL,
  `TIME_VOC`    int     NULL,
  CONSTRAINT PK_VOCAL_SESSION PRIMARY KEY (`ID_VOC`)
);



-- Indexes for table `LAST_SPAM`
ALTER TABLE `LAST_SPAM`
  ADD CONSTRAINT `FK_LAST_SPAM_TO_SPAM` FOREIGN KEY (`ID_SPAM`) REFERENCES `SPAM` (`ID_SPAM`);


-- Indexes for table `MESSAGE`
ALTER TABLE `MESSAGE`
  ADD CONSTRAINT `FK_MESSAGE_TO_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `FK_MESSAGE_TO_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);


-- Indexes for table `SPAM`
ALTER TABLE `SPAM`
  ADD CONSTRAINT `FK_SPAM_TO_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `FK_SPAM_TO_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);


-- Indexes for table `USER_SERVER`
ALTER TABLE `USER_SERVER`
  ADD CONSTRAINT `FK_USER_SERVER_TO_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `FK_USER_SERVER_TO_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);


-- Indexes for table `VOCAL_SESSION`
ALTER TABLE `VOCAL_SESSION`
  ADD CONSTRAINT `FK_VOCAL_SESSION_TO_SERVER` FOREIGN KEY (`ID_SERVER`) REFERENCES `SERVER` (`ID_SERVER`),
  ADD CONSTRAINT `FK_VOCAL_SESSION_TO_USER` FOREIGN KEY (`ID_USER`) REFERENCES `USER` (`ID_USER`);

