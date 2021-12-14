-- MySQL dump 10.13  Distrib 8.0.25, for macos10.15 (x86_64)
--
-- Host: localhost    Database: DEV_MFRI
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `Applications`
--

DROP TABLE IF EXISTS `Applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Applications` (
  `Id` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` char(32) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `Description` char(128) DEFAULT NULL,
  `ContactId` int unsigned DEFAULT NULL,
  `CGIName` char(129) DEFAULT NULL,
  `content_type_app_label` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=MyISAM AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Applications`
--

LOCK TABLES `Applications` WRITE;
/*!40000 ALTER TABLE `Applications` DISABLE KEYS */;
INSERT INTO `Applications` VALUES (1,'User Maintenance','User creation and maintenance.',2,'user_list.cgi',NULL),(2,'Reports Page','Reports and utilities',2,'reportsmenu.cgi',NULL),(3,'CPAT','Comprehensive Physical Agility Test Database.',2,'',NULL),(4,'Seminar Registration','Registration system for open enrollment seminars.',2,'',NULL),(5,'Course Maintenance','Create and maintain course descriptions.',2,'course','MCourses'),(6,'Schedule Maintenance','Schedule Courses and Seminars',2,'schedule_list.cgi',NULL),(7,'Seminar Maintenance','Schedule Seminars',2,'semsched_list.cgi',NULL),(8,'Location Maintenance','Create and maintain directions and maps to training sites.',2,'loc_list.cgi',NULL),(9,'Affiliation Agencies','Maintenance Utility for Affilications',2,'affiliations','MAffiliations'),(10,'Contact Maintenance','Create and maintain contacts.',2,'cn_list.cgi',NULL),(11,'App Maint','Add applications and screens to system.',2,'app_list.cgi',NULL),(12,'FOS Schedule Maintenance','Schedule FOS Coruses.',2,'schedule_list.cgi',NULL),(16,'Certification Maintenance','Certification Information',2,'cert_list.cgi',NULL),(17,'Schedule Wizard','Wizard to schedule courses',2,'schedwiz.cgi',NULL),(13,'LSS Request Manager','Manage LSS Resource Requests',2,'lssr_list.cgi',NULL),(14,'Old LSS Admin','Administer LSS Resource Requests',2,'lssr_admin.cgi',NULL),(18,'Log Number Manager','Log Number Manager Utility',2,'lognum_list.cgi',NULL),(19,'Course Session Manager','Manage Course Session Descriptions',2,'sesdesc_list.cgi',NULL),(15,'Student Registration','Student Registration Manager',2,'stureg_reg.cgi',NULL),(25,'MESSA Manager','Manage MESSA data to be sent to MIEMSS',2,'messalist.cgi',NULL),(20,'Pocket Cards','Pocket Cards Print Utility',2,'pcard_manage.cgi',NULL),(26,'MFRI Instructor List','MFRI Instructor List',2,'inst_list.cgi',NULL),(27,'Student Transcripts','MFRI Student List',2,'trans_search.cgi',NULL),(28,'MFRI Key List','MFRI Key List',2,'key_list.cgi',NULL),(29,'MFRI Prop List','MFRI Prop List',2,'prop_list.cgi',NULL),(30,'MFRI Skills List','MFRI Skills List',2,'skill_list.cgi',NULL),(31,'Registration-Transcript Link','Registration-Transcript Link',2,'translinkcourse_list.cgi',NULL),(32,'Current Student Registrations','List of currently registered MFRI students',2,'strc_list.cgi',NULL),(33,'MFRI Student Registrations List','MFRI Student Registrations List',2,'reg_list.cgi',NULL),(34,'Student Flags List','Student Flags List',2,'flags_list.cgi',NULL),(36,'Student Invoice Batches','MFRI Student Invoice List',2,'bookfeebatch_list.cgi',NULL),(35,'Student Invoice List','MFRI Student Invoice List',2,'bookfee_list.cgi',NULL),(37,'Faculty Time Entry','Faculty Time Entry System',2,'flist.cgi',NULL),(38,'Faculty Time Entry Form','Faculty Time Entry Form',2,'ftime.cgi',NULL),(39,'MFRI Holidays List','MFRI Holidays List',2,'hldy_list.cgi',NULL),(40,'Clients List','Clients List',2,'client_list.cgi',NULL),(41,'Program Evaluations Maintenance','Program Evaluations Maintenance',2,'stevm_list.cgi',NULL),(42,'Program Evaluations','Program Evaluations',2,'stev_search.cgi',NULL),(43,'Website Content Manager','Website Content Manager',2,'pagecontent_list.cgi',NULL),(44,'User App Preferences','User App Preferences',2,'upref_list.cgi',NULL),(45,'Help Viewer','Help Viewer',2,'userguide_list.cgi',NULL),(46,'Print Requests','Print Requests',2,'printrequest','MPrint'),(47,'Time and Travel System','Time Entry System',2,'mtes','MTES'),(48,'Student Medical Responses','Student Medical Responses',2,'SMEDReview','SMED'),(49,'Student Zone Maintenance','Student Zone Maintenance',2,'szone','SZONE'),(50,'Email Templates','Email Boilerplate',2,'memail','MEmailMan'),(51,'File Storage','File Storage',2,'memail','AppFiles'),(52,'Automated Email Distribution','Automated Email Distribution',2,'maed','MAED'),(53,'App Settings','App Settings',2,'appsettings','AppSettings'),(54,'MFSPQB Home','MFSPQB Standards and Certifications',2,'mfspqb','QBHome'),(55,'Office Directory Maintenance','Office Directory Maintenance',2,'offices','MOfficesContacts'),(58,'LSS WORCS','LSS Work Order Request Control System',2,'lss/workorder','LSSWorcs'),(59,'User Profile','User Profile and System Settings',2,'userprofile','AppsAdmin'),(56,'LSS Admin','LSS Maintenance',2,'lss','LSSHome'),(57,'LSS Asset Management','LSS Asset Management',2,'lss/asset','LSSAssets'),(60,'Training Officer Portal Admin','Training Officer Portal Administration',2,'mtop','MTrainingPortal'),(61,'Course Resources','Books, Exams and other course resources',2,'exams','MExams'),(62,'Control Panel','Office Control Panel',2,'controlpanel','MRegionPanel'),(63,'Session Manager','Session Manager',2,'session','MSchedSessions'),(64,'MICRB Portal','MICRB Portal Administration',2,'micrb','Micrb'),(65,'Contact Manager','Lightweight Contact Manager',2,'contacts','MContactMan');
/*!40000 ALTER TABLE `Applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AppsAdmin_userprofile`
--

DROP TABLE IF EXISTS `AppsAdmin_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AppsAdmin_userprofile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `WorkingOffice_id` int NOT NULL,
  `LegacyUserData_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `AppsAdmin_userprofile_2ac04628` (`WorkingOffice_id`),
  KEY `AppsAdmin_userprofile_3728dbd6` (`LegacyUserData_id`)
) ENGINE=MyISAM AUTO_INCREMENT=365 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AppsAdmin_userprofile`
--

LOCK TABLES `AppsAdmin_userprofile` WRITE;
/*!40000 ALTER TABLE `AppsAdmin_userprofile` DISABLE KEYS */;
INSERT INTO `AppsAdmin_userprofile` VALUES (1,1,13,2),(295,3,16,3);
/*!40000 ALTER TABLE `AppsAdmin_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AppLinks`
--

DROP TABLE IF EXISTS `AppLinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AppLinks` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Application` int DEFAULT NULL,
  `Link` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Arguments` varchar(255) DEFAULT NULL,
  `MenuLink` int DEFAULT NULL,
  `AppHomePage` int DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `RequiresCreate` int DEFAULT NULL,
  `RequiresModify` int DEFAULT NULL,
  `RequiresDelete` int DEFAULT NULL,
  `RequiresApprove` int DEFAULT NULL,
  `RequiresOverride` int DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AppLinks`
--

LOCK TABLES `AppLinks` WRITE;
/*!40000 ALTER TABLE `AppLinks` DISABLE KEYS */;
INSERT INTO `AppLinks` VALUES (1,1,'user_list.cgi','List Users','',1,1,'List Users',0,0,0,0,0),(2,1,'user_create.cgi','Create User','',1,0,'Add Users',1,0,0,0,0),(3,1,'user_edit.cgi','Edit User','',0,0,'Change User Details',0,1,0,0,0),(4,2,'reportspage.cgi','Instructors','',1,1,'Reports and utilities Home',0,0,0,0,0),(5,1,'user_search.cgi','Search Users','',1,0,'Search For Users',0,0,0,0,0),(6,1,'user_view.cgi','Show User Details','',0,0,'Show User Details',0,0,0,0,0),(7,1,'user_edit_apps.cgi','Application Permissions','',0,0,'Assign permissions to each application for this user',0,1,0,0,0),(8,3,'cpat_list.cgi','Show CPAT Candidate List','',1,1,'Show Candidates',0,0,0,0,0),(9,4,'semreg_list.cgi','Seminar Registration Home','',1,0,'Seminar Registration Management',0,0,0,0,0),(10,5,'course','List Courses','',1,1,'List Courses',0,0,0,0,0),(102,65,'contacts','Contact Manager','',1,1,'Lightweight Contact Manager',0,0,0,0,0),(13,6,'schedule_list.cgi','List Scheduled Courses','',1,1,'List scheduled courses.',0,0,0,0,0),(14,6,'schedule_create.cgi','Schedule a course','',1,0,'Schedule a course.',1,0,0,0,0),(15,6,'schedule_edit.cgi','Edit Schedule','',0,0,'Change a scheduled course.',0,1,0,0,0),(16,7,'semsched_list.cgi','List All Scheduled Seminars','',1,0,'List all scheduled seminars.',0,0,0,0,0),(17,7,'semsched_create.cgi','Schedule a seminar','',1,0,'Schedule a seminar.',1,0,0,0,0),(18,7,'semsched_edit.cgi','Edit Seminar Schedule','',0,0,'Change a scheduled seminar.',0,1,0,0,0),(19,7,'semsched_approve.cgi','Approve A Seminar','',0,0,'Approve a scheduled seminar.',0,1,0,1,0),(20,7,'semsched_list.cgi','Approved Seminars','formbutton=menu&NoStartDate=1&NoEndDate=1&ShowLogNumbers=0&ShowSeminarSectionFilter=ShowAll&ShowSeminarStatusFilter=ShowApproved',0,0,'Approved seminars.',0,1,0,1,0),(21,7,'semsched_list.cgi','Seminars Waiting For Approval','formbutton=menu&NoStartDate=1&NoEndDate=1&ShowLogNumbers=0&ShowSeminarSectionFilter=ShowAll&ShowSeminarStatusFilter=ShowWaiting',0,0,'Seminars waiting for approval.',0,1,0,1,0),(22,8,'loc_list.cgi','List Training Center Details','',1,1,'List Courses',0,0,0,0,0),(23,8,'loc_create.cgi','New Training Center Detail Record','',1,0,'Create a new course description',1,0,0,0,0),(24,8,'loc_edit.cgi','Edit Training Center Detail Record','',0,0,'Change a course description',0,1,0,0,0),(25,9,'affiliation','Affiliation Agencies','',1,1,'Show Affiliations',0,0,0,0,0),(97,60,'mtop','Training Officer Portal Admin','',1,1,'Training Officer Portal Administration',0,0,0,0,0),(28,10,'cn_list.cgi','Show Contact Details','',1,1,'Show Contacts',0,0,0,0,0),(29,10,'cn_edit.cgi','Add New Contact Detail Record','',1,0,'Create a new Contact record',1,0,0,0,0),(30,10,'cn_edit.cgi','Edit Contact Detail Record','',0,0,'Change a Contact record',0,1,0,0,0),(31,11,'app_list.cgi','List Applications','',1,1,'List Applications',0,0,0,0,0),(32,11,'app_create.cgi','Add New Application','',1,0,'Create a new Application description',1,0,0,0,0),(33,11,'app_edit.cgi','Edit Application','',0,0,'Change a Application description',0,1,0,0,0),(34,12,'schedule_list.cgi','List Scheduled Courses','Section=FOS&CourseTypes=2,4,6,7,8,9',1,1,'List scheduled courses.',0,0,0,0,0),(35,12,'schedule_create.cgi','Schedule a course','Section=FOS&CourseTypes=2,4,6,7,8,9',1,0,'Schedule a course.',1,0,0,0,0),(36,12,'schedule_edit.cgi','Edit Schedule','',0,0,'Change a scheduled course.',0,1,0,0,0),(37,3,'cpat_edit.cgi','Add New CPAT Candidate','',1,0,'Create a new Candidate record',1,0,0,0,0),(38,3,'cpat_edit.cgi','Change CPAT Candidate Record','',0,0,'Change a Candidate record',0,1,0,0,0),(39,16,'cert_list.cgi','List Certifications','',1,1,'List certifications.',0,0,0,0,0),(40,16,'cert_edit.cgi','New Certification','',1,0,'Create a new certification description.',1,0,0,0,0),(41,16,'cert_edit.cgi','Edit Certification','',0,0,'Change a certification description.',0,1,0,0,0),(42,17,'schedwiz.cgi','Schedule Wizard','',1,1,'Wizard to schedule courses.',0,0,0,0,0),(43,13,'lssr_list.cgi','Show LSS Request List','',1,1,'Show LSSR',0,0,0,0,0),(44,13,'lssr_edit.cgi','Create New LSS Request','',1,0,'Create a New LSSR Form',1,0,0,0,1),(45,13,'lssr_edit.cgi','Change an existing LSSR Form','',0,0,'Change a LSSR Form',0,1,0,0,1),(46,13,'lssr_edit.cgi','Create New LSSR Form','T=3',0,0,'Create a New LSSR Form',1,0,0,0,0),(47,13,'lssr_edit.cgi','Change LSSR Form','T=7&RID=$RID',0,0,'Change an Existing LSSR Form',0,1,0,0,0),(48,13,'lssr_edit.cgi','Review New LSSR Form','T=4&RID=$RID',0,0,'Review a New LSSR Form',0,1,0,1,0),(49,13,'lssr_edit.cgi','Approve New LSSR Form','T=5&RID=$RID',0,0,'Approve or Reject a New LSSR Form',0,1,0,1,0),(50,13,'lssr_edit.cgi','View LSSR Form','T=6&RID=$RID',0,0,'View an Existing LSSR Form',0,0,0,0,0),(51,14,'lssr_edit.cgi','Create New LSSR Form','T=3',0,0,'Create a New LSSR Form',1,0,0,0,0),(52,14,'lssr_edit.cgi','Change LSSR Form','A=$UID&T=7&RID=$RID',0,0,'Change an Existing LSSR Form',0,1,0,0,0),(53,14,'lssr_edit.cgi','Review New LSSR Form','A=$UID&T=4&RID=$RID',0,0,'Review a New LSSR Form',0,1,0,1,0),(54,14,'lssr_edit.cgi','Approve New LSSR Form','A=$UID&T=5&RID=$RID',0,0,'Approve or Reject a New LSSR Form',0,1,0,1,0),(55,14,'lssr_edit.cgi','View LSSR Form','A=$UID&T=6&RID=$RID',0,0,'View an Existing LSSR Form',0,0,0,0,0),(56,13,'lssr_calendar.cgi','LSS Calendar',NULL,1,0,'View LSS Calendar',0,0,0,0,0),(57,18,'lognum_list.cgi','Log Number Manager','',1,1,'Log Number Manager Utility.',0,0,0,0,0),(58,19,'sesdesc_list.cgi','List Course Sessions','',0,0,'List Course Sessions',0,0,0,0,0),(59,15,'stureg_reg.cgi','List Students','',1,0,'List students for courses.',0,0,0,0,0),(60,15,' stureg_edit.cgi','Change A Student Record','',0,0,'Change a student record.',0,1,0,0,0),(61,25,'messalist.cgi','List MESSA data','',1,1,'List MESSA data to be sent to MIEMSS',0,1,0,0,0),(62,20,'pcard_manage.cgi','Print Pocket Cards','',0,0,'Pocket Cards Print Utility',1,1,0,1,0),(63,26,'inst_list.cgi','MFRI Instructor List','',1,1,'MFRI Instructor List',0,0,0,0,0),(64,27,'trans_search.cgi','Find Students','',1,1,'Search for Student Records',0,0,0,0,0),(65,28,'key_list.cgi','MFRI Key List','',1,1,'MFRI Key List',0,0,0,0,0),(66,29,'prop_list.cgi','MFRI Prop List','',1,1,'MFRI Prop List',0,0,0,0,0),(67,30,'skill_list.cgi','MFRI Skills List','',1,1,'MFRI Skills List',0,0,0,0,0),(68,31,'translinkcourse_list.cgi','Registration-Transcript Link','',1,1,'Registration-Transcript Link',0,0,0,0,0),(69,32,'strc_list.cgi','List Current Students','',0,0,'Show currently registered MFRI students',0,0,0,0,0),(70,33,'reg_search.cgi','MFRI Student Registrations List','',1,1,'MFRI Student Registrations List',0,0,0,0,0),(71,34,'flags_list.cgi','Student Flags List','',1,1,'Student Flags List',0,0,0,0,0),(72,36,'bookfeebatch_list.cgi','Student Invoice Batches','',1,1,'MFRI Student Invoice Batches',0,0,0,0,0),(73,35,'bookfee_list.cgi','Student Invoice List','',0,1,'MFRI Student Invoice List',0,0,0,0,0),(74,37,'flist.cgi','Faculty Time Entry','',1,1,'Faculty Time Entry System',0,0,0,0,0),(75,38,'ftime.cgi','Faculty Time Entry Form','',1,1,'Faculty Time Entry Form',0,0,0,0,0),(76,39,'hldy_list.cgi','MFRI Holidays List','',1,1,'MFRI Holidays List',0,0,0,0,0),(77,40,'client_list.cgi','Clients List','',1,1,'Clients List',0,0,0,0,0),(78,41,'stevm_list.cgi','Program Evaluations Maintenance','',1,1,'Program Evaluations Maintenance',0,0,0,0,0),(79,42,'stev_search.cgi','Program Evaluations','',1,1,'Program Evaluations',0,0,0,0,0),(80,44,'upref_list.cgi','User App Preferences','',0,0,'User App Preferences',0,0,0,0,0),(81,45,'userguide_list.cgi','Help Viewer','',1,1,'Help Viewer',0,0,0,0,0),(82,46,'printrequest','Print Requests','',1,1,'Print Requests',0,0,0,0,0),(83,47,'mtes','Time and Travel System','',1,1,'Time Entry System',0,0,0,0,0),(84,48,'SMEDReview','Student Medical Responses','',1,1,'Student Medical Responses',0,0,0,0,0),(85,49,'szone','Student Zone Maintenance','',1,1,'Student Zone Maintenance',0,0,0,0,0),(86,50,'memail','Email Boilerplate','',1,1,'Email Boilerplate',0,0,0,0,0),(87,51,'files','File Storage','',1,1,'File Storage',0,0,0,0,0),(88,52,'maed','Automated Email Distribution','',1,1,'Automated Email Distribution',0,0,0,0,0),(89,53,'appsettings','App Settings','',1,1,'App Settings',0,0,0,0,0),(90,54,'mfspqb','MFSPQB Home','',1,1,'MFSPQB Standards and Certifications',0,0,0,0,0),(91,55,'offices','Office Directory Maintenance','',1,1,'Office Directory Maintenance',0,0,0,0,0),(92,57,'lss/asset','LSS Asset Management','',1,1,'LSS Asset Management',0,0,0,0,0),(93,58,'lss/workorder','LSS WORCS','',1,1,'LSS Work Order Request Control System',0,0,0,0,0),(94,59,'userprofile','User Profile','',0,0,'User Profile and System Settings',0,0,0,0,0),(95,56,'lss','LSS Admin','',1,1,'LSS Maintenance',0,0,0,0,0),(98,61,'exams','Course Resources','',1,1,'Books, Exams and other course resources',0,0,0,0,0),(99,62,'controlpanel','Control Panel','',1,1,'Office Control Panel',0,0,0,0,0),(100,63,'session','Session Manager','',0,0,'Session Manager',0,0,0,0,0),(101,64,'micrb','MICRB Portal','',1,1,'MICRB Portal Administration',0,0,0,0,0);
/*!40000 ALTER TABLE `AppLinks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `Id` int unsigned NOT NULL AUTO_INCREMENT,
  `UserName` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `FullName` varchar(128) DEFAULT NULL,
  `Password` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `Email` varchar(255) NOT NULL DEFAULT '',
  `Permissions` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `Applications` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `GroupId` int unsigned NOT NULL DEFAULT '0',
  `SectionID` int unsigned DEFAULT '4',
  `RegionID` int unsigned DEFAULT '8',
  `ContactID` int unsigned DEFAULT '3',
  `InstructorID` int unsigned DEFAULT '1',
  `LSSRManagerID` int unsigned DEFAULT '3',
  `LSSRLevelID` int unsigned DEFAULT '1',
  `IsActive` int DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `UserName` (`UserName`)
) ENGINE=MyISAM AUTO_INCREMENT=236 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'InitAdmin','Initial Admin','','itdev@mfri.org','11111111111111111111111111111111','11111111111111111111111111111111',1,6,8,74,1,3,1,0,'tsweeting','2021-11-10 20:45:51',NULL,'0000-00-00 00:00:00'),(2,'tsweeting','Thomas Sweeting','','tsweeting@mfri.org','11111111111111111111111111111111','11111111111111111111111111111111',1,2,2,77,5510,167,3,1,'tsweeting','2021-11-10 20:47:02',NULL,'0000-00-00 00:00:00'),(3,'staff','MFRI Staff','','info@mfri.org','','',8,6,7,5,1,3,1,1,'tsweeting','2021-11-10 20:45:51',NULL,'0000-00-00 00:00:00'),(4,'instructor','MFRI Instructor','','info@mfri.org','','',8,3,7,6,1,3,1,0,'tsweeting','2021-11-10 20:47:02',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SchedPreferences`
--

DROP TABLE IF EXISTS `SchedPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SchedPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `GlobalReadPermission` int DEFAULT '1',
  `GlobalWritePermission` int DEFAULT '0',
  `ActivityCenterReadPermission` int DEFAULT '1',
  `ActivityCenterWritePermission` int DEFAULT '1',
  `SectionReadPermission` int DEFAULT '1',
  `SectionWritePermission` int DEFAULT '1',
  `PrimaryApprover` int DEFAULT '0',
  `FundingApprover` int DEFAULT '0',
  `ScheduleApprover` int DEFAULT '0',
  `EquivalencyClassCreator` int DEFAULT '0',
  `ClassFolderSendPermission` int DEFAULT '0',
  `ClassFolderReceivePermission` int DEFAULT '0',
  `ClassFolderClosePermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=130 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SchedPreferences`
--

LOCK TABLES `SchedPreferences` WRITE;
/*!40000 ALTER TABLE `SchedPreferences` DISABLE KEYS */;
INSERT INTO `SchedPreferences` VALUES (1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,NULL,'2010-10-04 21:15:12',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `SchedPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentRegistrationPreferences`
--

DROP TABLE IF EXISTS `StudentRegistrationPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentRegistrationPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `GradesReadPermission` int DEFAULT '1',
  `GradesWritePermission` int DEFAULT '0',
  `AffiliationReadPermission` int DEFAULT '1',
  `AffiliationWritePermission` int DEFAULT '0',
  `RegistrationReadPermission` int DEFAULT '1',
  `RegistrationWritePermission` int DEFAULT '0',
  `ReportsPermission` int DEFAULT '0',
  `ImportPermission` int DEFAULT '0',
  `ExportPermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=127 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentRegistrationPreferences`
--

LOCK TABLES `StudentRegistrationPreferences` WRITE;
/*!40000 ALTER TABLE `StudentRegistrationPreferences` DISABLE KEYS */;
INSERT INTO `StudentRegistrationPreferences` VALUES (1,2,1,1,1,1,1,1,1,1,1,1,1,NULL,'2009-05-05 13:55:44',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `StudentRegistrationPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentRecordsPreferences`
--

DROP TABLE IF EXISTS `StudentRecordsPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentRecordsPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `IDReadPermission` int DEFAULT '1',
  `IDWritePermission` int DEFAULT '0',
  `PrivateReadPermission` int DEFAULT '0',
  `PrivateWritePermission` int DEFAULT '0',
  `ContactReadPermission` int DEFAULT '1',
  `ContactWritePermission` int DEFAULT '0',
  `AffiliationReadPermission` int DEFAULT '1',
  `AffiliationWritePermission` int DEFAULT '0',
  `FlagsReadPermission` int DEFAULT '1',
  `FlagsWritePermission` int DEFAULT '0',
  `ImportPermission` int DEFAULT '0',
  `ExportPermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=129 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentRecordsPreferences`
--

LOCK TABLES `StudentRecordsPreferences` WRITE;
/*!40000 ALTER TABLE `StudentRecordsPreferences` DISABLE KEYS */;
INSERT INTO `StudentRecordsPreferences` VALUES (1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,NULL,'2008-11-15 22:00:10',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `StudentRecordsPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InstPreferences`
--

DROP TABLE IF EXISTS `InstPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `InstPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `GlobalEditPermissions` int DEFAULT '0',
  `OfficeEditPermissions` varchar(22) DEFAULT '',
  `SendEmail` int DEFAULT '0',
  `ReadEmail` int DEFAULT '1',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `ReportsPermission` int DEFAULT '0',
  `IDReadPermission` int DEFAULT '1',
  `IDWritePermission` int DEFAULT '0',
  `PrivateReadPermission` int DEFAULT '0',
  `PrivateWritePermission` int DEFAULT '0',
  `ContactReadPermission` int DEFAULT '1',
  `ContactWritePermission` int DEFAULT '0',
  `MailingAddressReadPermission` int DEFAULT '1',
  `MailingAddressWritePermission` int DEFAULT '0',
  `EmploymentReadPermission` int DEFAULT '1',
  `EmploymentWritePermission` int DEFAULT '0',
  `HomeOfficeWritePermissions` int DEFAULT '0',
  `PayRateReadPermission` int DEFAULT '0',
  `PayRateWritePermission` int DEFAULT '0',
  `DriversLicensePrivateReadPermission` int DEFAULT '0',
  `DriversLicenseReadPermission` int DEFAULT '1',
  `InstructorDetailsReadPermission` int DEFAULT '1',
  `DriversLicensePrivateWritePermission` int DEFAULT '0',
  `SecurityReadPermission` int DEFAULT '0',
  `SecurityWritePermission` int DEFAULT '0',
  `DriversLicenseWritePermission` int DEFAULT '0',
  `InstructorDetailsWritePermission` int DEFAULT '0',
  `InstructorTeachingHoursReadPermission` int DEFAULT '1',
  `InstructorTeachingHoursWritePermission` int DEFAULT '0',
  `SkillsReadPermission` int DEFAULT '1',
  `SkillsWritePermission` int DEFAULT '0',
  `FacultyWritePermissions` int DEFAULT '0',
  `FacultyReadPermissions` int DEFAULT '0',
  `TeachingSpecialtyReadPermission` int DEFAULT '0',
  `TeachingSpecialtyWritePermission` int DEFAULT '0',
  `MedicalExamReadPermission` int DEFAULT '0',
  `MedicalExamWritePermission` int DEFAULT '0',
  `MedicalExamPrivateReadPermission` int DEFAULT '0',
  `MedicalExamPrivateWritePermission` int DEFAULT '0',
  `ExportPermission` int DEFAULT '0',
  `ExportAddressPermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=153 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InstPreferences`
--

LOCK TABLES `InstPreferences` WRITE;
/*!40000 ALTER TABLE `InstPreferences` DISABLE KEYS */;
INSERT INTO `InstPreferences` VALUES (1,2,1,' ',1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,NULL,'2020-11-30 02:47:13',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `InstPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Permissions`
--

DROP TABLE IF EXISTS `Permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Permissions` (
  `Id` int unsigned NOT NULL AUTO_INCREMENT,
  `UserId` int unsigned DEFAULT NULL,
  `AppID` int unsigned DEFAULT NULL,
  `ReadPermission` int DEFAULT NULL,
  `CreatePermission` int DEFAULT NULL,
  `ModifyPermission` int DEFAULT NULL,
  `DeletePermission` int DEFAULT NULL,
  `ApprovePermission` int DEFAULT NULL,
  `OverridePermission` int DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=38381 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Permissions`
--

LOCK TABLES `Permissions` WRITE;
/*!40000 ALTER TABLE `Permissions` DISABLE KEYS */;
INSERT INTO `Permissions` VALUES (29696,2,43,0,0,0,0,0,0),(29695,2,59,1,0,0,0,0,0),(29694,2,1,1,1,1,1,1,1),(29693,2,44,0,0,0,0,0,0),(3557,1,1,1,1,1,1,1,1),(3556,1,4,1,1,1,1,1,1),(29692,2,60,1,0,0,0,0,0),(29691,2,47,1,0,0,0,0,0),(29690,2,49,0,0,0,0,0,0),(29689,2,27,1,1,1,1,1,1),(29688,2,15,1,1,1,1,1,1),(29687,2,48,1,0,0,0,0,0),(29686,2,35,0,0,0,0,0,0),(29685,2,36,1,0,0,0,0,0),(29684,2,34,1,0,0,0,0,0),(29683,2,63,0,0,0,0,0,0),(29682,2,4,1,1,1,1,1,1),(29681,2,7,1,1,1,1,1,1),(29680,2,17,1,1,1,1,1,1),(29679,2,6,1,0,1,1,1,1),(3555,1,7,0,0,0,0,0,0),(3554,1,17,1,1,1,1,1,1),(3553,1,6,1,1,1,1,1,1),(3552,1,18,1,1,1,1,1,1),(3551,1,8,1,1,1,1,1,1),(3550,1,13,1,1,1,1,1,1),(3549,1,14,1,1,1,1,1,1),(3548,1,2,1,1,1,1,1,1),(3547,1,12,1,1,1,1,1,1),(3546,1,19,1,1,1,1,1,1),(3545,1,5,1,1,1,1,1,1),(3544,1,10,1,1,1,1,1,1),(3543,1,16,1,1,1,1,1,1),(3542,1,3,1,1,1,1,1,1),(3541,1,11,1,1,1,1,1,1),(3540,1,9,1,1,1,1,1,1),(29678,2,2,1,0,0,0,0,0),(29677,2,31,1,0,0,0,0,0),(29676,2,41,1,0,0,0,0,0),(29675,2,42,1,0,0,0,0,0),(29674,2,46,1,0,0,0,0,0),(29673,2,20,1,1,1,1,1,1),(29672,2,14,0,0,0,0,0,0),(29671,2,55,1,0,0,0,0,0),(29670,2,64,1,1,1,0,0,0),(29669,2,54,1,0,0,0,0,0),(29668,2,33,1,0,0,0,0,0),(29667,2,30,1,1,1,0,0,0),(29666,2,29,1,1,1,0,0,0),(29665,2,28,1,1,1,0,0,0),(29664,2,26,1,0,0,0,0,0),(29663,2,39,0,0,0,0,0,0),(29662,2,25,1,1,1,1,1,1),(29661,2,18,1,1,1,1,1,1),(29660,2,8,1,1,1,1,1,1),(29659,2,58,1,0,0,0,0,0),(29658,2,13,1,1,1,1,1,1),(29657,2,57,1,0,0,0,0,0),(29656,2,56,1,0,0,0,0,0),(29655,2,45,0,0,0,0,0,0),(29654,2,51,1,0,0,0,0,0),(29653,2,38,0,0,0,0,0,0),(29652,2,37,0,0,0,0,0,0),(29651,2,12,0,0,0,0,0,0),(29650,2,50,1,0,0,0,0,0),(17107,3,9,0,0,0,0,0,0),(17108,3,11,0,0,0,0,0,0),(17109,3,3,0,0,0,0,0,0),(17110,3,16,0,0,0,0,0,0),(17111,3,40,0,0,0,0,0,0),(17112,3,10,0,0,0,0,0,0),(17113,3,5,0,0,0,0,0,0),(17114,3,19,0,0,0,0,0,0),(17115,3,32,0,0,0,0,0,0),(17116,3,50,0,0,0,0,0,0),(17117,3,12,0,0,0,0,0,0),(17118,3,37,0,0,0,0,0,0),(17119,3,38,0,0,0,0,0,0),(17120,3,51,0,0,0,0,0,0),(17121,3,45,0,0,0,0,0,0),(17122,3,14,0,0,0,0,0,0),(17123,3,13,0,0,0,0,0,0),(17124,3,8,0,0,0,0,0,0),(17125,3,18,0,0,0,0,0,0),(17126,3,25,0,0,0,0,0,0),(17127,3,39,0,0,0,0,0,0),(17128,3,26,0,0,0,0,0,0),(17129,3,28,0,0,0,0,0,0),(17130,3,29,0,0,0,0,0,0),(17131,3,30,0,0,0,0,0,0),(17132,3,33,0,0,0,0,0,0),(17133,3,20,0,0,0,0,0,0),(17134,3,46,0,0,0,0,0,0),(17135,3,42,0,0,0,0,0,0),(17136,3,41,0,0,0,0,0,0),(17137,3,31,0,0,0,0,0,0),(17138,3,2,0,0,0,0,0,0),(17139,3,6,0,0,0,0,0,0),(17140,3,17,0,0,0,0,0,0),(17141,3,7,0,0,0,0,0,0),(17142,3,4,0,0,0,0,0,0),(17143,3,34,0,0,0,0,0,0),(17144,3,36,0,0,0,0,0,0),(17145,3,35,0,0,0,0,0,0),(17146,3,48,0,0,0,0,0,0),(17147,3,15,0,0,0,0,0,0),(17148,3,27,0,0,0,0,0,0),(17149,3,49,0,0,0,0,0,0),(17150,3,47,1,0,0,0,0,0),(17151,3,44,0,0,0,0,0,0),(17152,3,1,0,0,0,0,0,0),(17153,3,43,0,0,0,0,0,0),(29649,2,32,1,0,0,0,0,0),(29648,2,19,1,1,1,1,1,1),(29647,2,61,1,0,0,0,0,0),(29646,2,5,1,1,1,1,1,1),(29645,2,62,1,0,0,0,0,0),(29644,2,10,1,1,1,1,1,1),(29643,2,40,1,0,0,0,0,0),(29642,2,16,1,1,1,1,1,1),(29641,2,3,1,1,1,1,0,0),(29640,2,52,1,0,0,0,0,0),(29639,2,53,0,0,0,0,0,0),(29638,2,11,0,0,0,0,0,0),(29637,2,9,1,1,1,1,1,1),(34098,2,65,1,0,0,0,0,0);
/*!40000 ALTER TABLE `Permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Affiliations`
--

DROP TABLE IF EXISTS `Affiliations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Affiliations` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `MFRICode` varchar(32) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `abbreviation` varchar(20) DEFAULT NULL,
  `FireMarshalNumber` varchar(32) DEFAULT NULL,
  `miemss_number` varchar(32) DEFAULT NULL,
  `mfirs_number` varchar(5) DEFAULT NULL,
  `CountyID` int unsigned DEFAULT NULL,
  `CountyNumber` char(3) DEFAULT '',
  `CountyIDTemp` int DEFAULT '30',
  `County` varchar(255) DEFAULT NULL,
  `Address1` varchar(255) DEFAULT NULL,
  `Address2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `PostCode` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `MailingAddress1` varchar(255) DEFAULT NULL,
  `StreetAddress1` varchar(255) DEFAULT NULL,
  `MailingAddress2` varchar(255) DEFAULT NULL,
  `StreetAddress2` varchar(255) DEFAULT NULL,
  `MailingCity` varchar(255) DEFAULT NULL,
  `StreetCity` varchar(255) DEFAULT NULL,
  `MailingState` varchar(255) DEFAULT NULL,
  `StreetState` varchar(255) DEFAULT NULL,
  `MailingPostCode` varchar(255) DEFAULT NULL,
  `StreetPostCode` varchar(255) DEFAULT NULL,
  `MailingCountry` varchar(255) DEFAULT NULL,
  `StreetCountry` varchar(255) DEFAULT NULL,
  `PrimaryPhoneNumber` varchar(255) DEFAULT NULL,
  `SecondaryPhoneNumber` varchar(255) DEFAULT NULL,
  `FaxNumber` varchar(255) DEFAULT NULL,
  `EmailAddress` varchar(255) DEFAULT NULL,
  `is_atra` tinyint(1) DEFAULT '0',
  `has_delegation_of_authority` tinyint(1) DEFAULT '0',
  `atra_number` varchar(2) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `ContactID` int unsigned DEFAULT NULL,
  `show_as_registration_option` tinyint(1) DEFAULT '0',
  `is_md_emergency_service` tinyint(1) DEFAULT '1',
  `has_training_officer` tinyint(1) DEFAULT '1',
  `has_no_address` tinyint(1) DEFAULT '0',
  `has_error` tinyint(1) DEFAULT '0',
  `is_duplicate` tinyint(1) DEFAULT '0',
  `internal_note` longtext,
  `has_bls_approver` tinyint(1) NOT NULL DEFAULT '0',
  `has_als_approver` tinyint(1) NOT NULL DEFAULT '0',
  `has_pdi_approver` tinyint(1) NOT NULL DEFAULT '0',
  `has_other_approver` tinyint(1) NOT NULL DEFAULT '0',
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `CreatedBy` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `AffiliationMFRICode_index` (`MFRICode`),
  KEY `ID_index` (`ID`),
  KEY `MFRICode_index` (`MFRICode`)
) ENGINE=MyISAM AUTO_INCREMENT=785 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Affiliations`
--

LOCK TABLES `Affiliations` WRITE;
/*!40000 ALTER TABLE `Affiliations` DISABLE KEYS */;
INSERT INTO `Affiliations` VALUES (731,'','MFRI NERTC-Instructor','NERTC-I','900178','900178','',14,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PO Box 789','9250 Fairview Point Road','','','Edgewood','Edgewood','MD','MD','21040','21001-6032','','','888-317-2218','410-676-5409','410-676-5413','necontact@mfri.org',0,0,'',NULL,0,1,1,1,0,0,0,'',1,1,1,1,'2019-03-08 19:40:58','','2010-08-31 15:04:52',''),(768,'','MFRI NCRO-Instructor','NCRO-I',NULL,'900181','',8,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PO Box 196','1008 Twin Arch Road','','','Mt Airy','Mt Airy','MD','MD','21771-0196','21771','','','800-287-6374','301-829-2020','301-829-2021','nccontact@mfri.org',0,0,'',NULL,NULL,1,1,1,0,0,0,'',1,1,1,1,'2017-11-30 15:16:23','','2017-08-24 19:27:16',''),(769,'','MFRI WMRTC-Instructor','WMRTC-I',NULL,'900182','',1,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'PO Box 5153','13928 Hazmat Drive SW','','','Cumberland','Cumberland','MD','MD','21502-5153','21502','','','888-691-6143','301-729-0431','301-729-6146','wmcontact@mfri.org',0,0,'',NULL,NULL,1,1,1,0,0,0,'',0,0,1,0,'2017-10-25 17:55:24','','2017-08-24 19:32:17',''),(770,'','MFRI UESRTC-Instructor','UESRTC-I',NULL,'900183','',19,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','601 Safety Drive','','','','Centreville','','MD','','21617','','','888-692-0055','410-758-2112','410-758-3573','uescontact@mfri.org',0,0,'',NULL,NULL,1,1,1,0,0,0,'',0,0,1,0,'2017-10-11 17:13:27','','2017-08-24 19:36:18',''),(771,'','MFRI LESRTC-Instructor','LESRTC-I',NULL,'900184','',21,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','12148 John Wilson Lane','','','','Princess Anne','','MD','','21853-3648','','','888-691-8880','410-749-0313','410-651-3356','lescontact@mfri.org',0,0,'',NULL,NULL,1,1,1,0,0,0,'',0,0,1,0,'2017-10-11 19:27:35','','2017-08-24 19:40:57',''),(772,'','MFRI SMRTC-Instructor','SMRTC-I',NULL,'900185','',10,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','10375 Audie Lane','','','','La Plata','','MD','','20646-0813','','','888-691-4628','301-934-2600','301-944-4333','smcontact@mfri.org',0,0,'',NULL,NULL,1,1,1,0,0,0,'',1,0,1,1,'2020-07-20 16:33:12','','2017-08-24 19:44:42',''),(773,'','MFRI Headquarters-Instructors & Staff','HQ-I&S',NULL,'900186','',18,'',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Building 199','4500 Campus Drive','','','College Park','College Park','MD','MD','20742-6811','20742','','','800-275-6374','301-226-9900','301-314-0752','',0,0,'',NULL,NULL,1,1,1,0,0,0,'',1,1,1,1,'2018-11-09 15:01:20','','2017-08-24 19:53:28','');
/*!40000 ALTER TABLE `Affiliations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClientStatus`
--

DROP TABLE IF EXISTS `ClientStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ClientStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClientStatus`
--

LOCK TABLES `ClientStatus` WRITE;
/*!40000 ALTER TABLE `ClientStatus` DISABLE KEYS */;
INSERT INTO `ClientStatus` VALUES (1,'Current'),(2,'Retired');
/*!40000 ALTER TABLE `ClientStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClientTypes`
--

DROP TABLE IF EXISTS `ClientTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ClientTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClientTypes`
--

LOCK TABLES `ClientTypes` WRITE;
/*!40000 ALTER TABLE `ClientTypes` DISABLE KEYS */;
INSERT INTO `ClientTypes` VALUES (1,'Not Specified'),(2,'US Government'),(3,'DoD'),(4,'State Government'),(5,'Commercial'),(6,'Other'),(7,'Private'),(8,'CityGov');
/*!40000 ALTER TABLE `ClientTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MFRIClients`
--

DROP TABLE IF EXISTS `MFRIClients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MFRIClients` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Number` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `StreetAddress1` varchar(255) DEFAULT NULL,
  `StreetAddress2` varchar(255) DEFAULT NULL,
  `StreetCity` varchar(255) DEFAULT NULL,
  `StreetState` varchar(255) DEFAULT NULL,
  `StreetPostCode` varchar(255) DEFAULT NULL,
  `StreetCountry` varchar(255) DEFAULT NULL,
  `MailingAddress1` varchar(255) DEFAULT NULL,
  `MailingAddress2` varchar(255) DEFAULT NULL,
  `MailingCity` varchar(255) DEFAULT NULL,
  `MailingState` varchar(255) DEFAULT NULL,
  `MailingPostCode` varchar(255) DEFAULT NULL,
  `MailingCountry` varchar(255) DEFAULT NULL,
  `ContactName` varchar(255) DEFAULT NULL,
  `PrimaryPhoneNumber` varchar(255) DEFAULT NULL,
  `SecondaryPhoneNumber` varchar(255) DEFAULT NULL,
  `FaxNumber` varchar(255) DEFAULT NULL,
  `EmailAddress` varchar(255) DEFAULT NULL,
  `TypeID` int unsigned DEFAULT '1',
  `StatusID` int unsigned DEFAULT '1',
  `MFRICoordinatorID` int unsigned DEFAULT '1',
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=1607 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MFRIClients`
--

LOCK TABLES `MFRIClients` WRITE;
/*!40000 ALTER TABLE `MFRIClients` DISABLE KEYS */;
INSERT INTO `MFRIClients` VALUES (2,'MFRI','0000','MFRI',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,2,NULL,'2008-04-10 22:18:03',NULL,'0000-00-00 00:00:00'),(1442,'MFRI Simulation Center','2461','','4500 Paint Branch Parkway','','College Park','Maryland','20742','USA','','','','','','','Michael Kernan','301-226-9947','','','',1,1,1,1,'aburke','2011-02-25 14:46:09','aburke','2011-02-25 14:46:09'),(1,'None Specified','0000','No Client Specified',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,2,NULL,'2008-04-10 22:18:02',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `MFRIClients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TCodes`
--

DROP TABLE IF EXISTS `TCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TCodes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TCodes`
--

LOCK TABLES `TCodes` WRITE;
/*!40000 ALTER TABLE `TCodes` DISABLE KEYS */;
INSERT INTO `TCodes` VALUES (1,'FPS MFRI Student Fee (430196-3924)','1525'),(2,'SPS MFRI Student Fee (294553-0615)','1526'),(3,'MFRI Bookstore (294546-3928)','1527'),(4,'MFRI Book Fee (430196-3924)','1528');
/*!40000 ALTER TABLE `TCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseCategoryTypes`
--

DROP TABLE IF EXISTS `CourseCategoryTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseCategoryTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseCategoryTypes`
--

LOCK TABLES `CourseCategoryTypes` WRITE;
/*!40000 ALTER TABLE `CourseCategoryTypes` DISABLE KEYS */;
INSERT INTO `CourseCategoryTypes` VALUES (1,'Not Specified'),(2,'Course'),(3,'Seminar'),(4,'Other');
/*!40000 ALTER TABLE `CourseCategoryTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseTypes`
--

DROP TABLE IF EXISTS `CourseTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseTypes`
--

LOCK TABLES `CourseTypes` WRITE;
/*!40000 ALTER TABLE `CourseTypes` DISABLE KEYS */;
INSERT INTO `CourseTypes` VALUES (1,'Unknown'),(2,'Curriculum'),(3,'Industrial'),(4,'Seminar'),(5,'Company Drill'),(6,'Other');
/*!40000 ALTER TABLE `CourseTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseCategories`
--

DROP TABLE IF EXISTS `CourseCategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseCategories` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `TypeID` int unsigned DEFAULT '1',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseCategories`
--

LOCK TABLES `CourseCategories` WRITE;
/*!40000 ALTER TABLE `CourseCategories` DISABLE KEYS */;
INSERT INTO `CourseCategories` VALUES (1,'None','Not Given',1),(2,'EMS','Emergency Medical Services',2),(3,'FIRE','Fire Suppression',2),(4,'HM','Hazardous Materials',2),(5,'IND','Industrial',2),(6,'MGMT','Managment',2),(7,'RES','Rescue',2),(8,'EMSS','Emergency Medical Services',3),(9,'FIRS','Fire Suppression',3),(10,'HMS','Hazardous Materials',3),(11,'INDS','Industrial',3),(12,'MGTS','Managment',3),(13,'RESS','Rescue',3),(14,'SEM','Miscellaneous Seminar',3),(15,'PDI','Professional Development for Instructors',3),(16,'SIM','Simulation Center',3),(17,'CD','Company Drill',2),(18,'TTT','Train the Trainer',3),(19,'NFA','Train the Trainer',2);
/*!40000 ALTER TABLE `CourseCategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseFundingSources`
--

DROP TABLE IF EXISTS `CourseFundingSources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseFundingSources` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseFundingSources`
--

LOCK TABLES `CourseFundingSources` WRITE;
/*!40000 ALTER TABLE `CourseFundingSources` DISABLE KEYS */;
INSERT INTO `CourseFundingSources` VALUES (1,'Not Specified',''),(2,'Academy','A'),(3,'Equivalent Credit','E'),(4,'State Budget','S'),(5,'Eligible for Grants','G'),(6,'Revenue Generated Income','R');
/*!40000 ALTER TABLE `CourseFundingSources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseStatus`
--

DROP TABLE IF EXISTS `CourseStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  `is_current_edition` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseStatus`
--

LOCK TABLES `CourseStatus` WRITE;
/*!40000 ALTER TABLE `CourseStatus` DISABLE KEYS */;
INSERT INTO `CourseStatus` VALUES (1,'Unknown',0),(2,'Available for Schedule',1),(3,'No Longer Available',0),(4,'Legacy',0),(5,'Needs Review',0),(6,'Duplicate',0),(7,'Incomplete',0);
/*!40000 ALTER TABLE `CourseStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseSponsors`
--

DROP TABLE IF EXISTS `CourseSponsors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseSponsors` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseSponsors`
--

LOCK TABLES `CourseSponsors` WRITE;
/*!40000 ALTER TABLE `CourseSponsors` DISABLE KEYS */;
INSERT INTO `CourseSponsors` VALUES (1,'Unknown'),(2,'MFRI'),(3,'NFA'),(4,'VFIS'),(5,'Other');
/*!40000 ALTER TABLE `CourseSponsors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseDescriptions`
--

DROP TABLE IF EXISTS `CourseDescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseDescriptions` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Abbr` varchar(32) DEFAULT NULL,
  `CourseCode` varchar(32) DEFAULT NULL,
  `CategoryID` int unsigned DEFAULT '1',
  `Category` varchar(32) DEFAULT '',
  `Level` varchar(5) DEFAULT '',
  `Title` varchar(255) DEFAULT NULL,
  `ACECode` varchar(255) DEFAULT NULL,
  `NFACode` varchar(255) DEFAULT '',
  `CourseTypeID` int unsigned DEFAULT NULL,
  `TotalHours` decimal(8,2) DEFAULT '0.00',
  `bkTotalHours` int DEFAULT '0',
  `InstructionalHours` decimal(8,2) DEFAULT '0.00',
  `bkInstructionalHours` int DEFAULT '0',
  `ModuleCount` int DEFAULT '1',
  `InStateFee` decimal(8,2) DEFAULT '0.00',
  `OutStateFee` decimal(8,2) DEFAULT '0.00',
  `MinStudents` int DEFAULT '15',
  `MaxStudents` int DEFAULT '30',
  `CourseStatusID` int unsigned DEFAULT NULL,
  `CourseSectionID` int unsigned DEFAULT NULL,
  `Description` text,
  `ACEDescription` text,
  `Prerequisites` text,
  `FPProcedures` text,
  `SPProcedures` text,
  `RegistrationMessage` text,
  `RegistrationEmailText` text,
  `final_email_agency_text` longtext,
  `final_email_student_text` longtext,
  `TypeID` int unsigned DEFAULT '1',
  `AccountID` int unsigned DEFAULT '1',
  `SponsorID` int unsigned DEFAULT '1',
  `ActivityCentersID` int DEFAULT '1',
  `StatusID` int unsigned DEFAULT '1',
  `developer_name` varchar(765) DEFAULT NULL,
  `developer_email` varchar(765) DEFAULT NULL,
  `show_in_catalog` tinyint(1) DEFAULT '1',
  `has_sim_center_component` tinyint(1) NOT NULL DEFAULT '0',
  `has_online_component` tinyint(1) NOT NULL DEFAULT '0',
  `pay_override` decimal(4,2) DEFAULT NULL,
  `lms_identifier` varchar(6) NOT NULL DEFAULT 'N/A',
  `is_sps_only` tinyint(1) NOT NULL DEFAULT '0',
  `is_bls` tinyint(1) NOT NULL DEFAULT '0',
  `is_als` tinyint(1) NOT NULL DEFAULT '0',
  `is_pdi` tinyint(1) NOT NULL DEFAULT '0',
  `acknowledge_physical_requirements` tinyint(1) NOT NULL DEFAULT '0',
  `physical_requirements` longtext,
  `ShowOnTranscript` int unsigned DEFAULT '1',
  `NeedProgramEvaluations` int unsigned DEFAULT '1',
  `ResourceFee` decimal(8,2) DEFAULT '0.00',
  `NewBookFee` decimal(8,2) DEFAULT '0.00',
  `UsedBookFee` decimal(8,2) DEFAULT '0.00',
  `TCodeID` int unsigned DEFAULT '4',
  `Notes` text,
  `EditionDate` date DEFAULT '0000-00-00',
  `EditionName` varchar(255) DEFAULT '',
  `RequireMedicalClearance` int DEFAULT '0',
  `MedicalClearanceNote` varchar(255) DEFAULT '',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `session_count` int DEFAULT '0',
  `session_in_modules` varchar(765) DEFAULT '',
  `track_count` int DEFAULT '0',
  `session_length_hours` int DEFAULT '3',
  `has_session_zero` tinyint(1) NOT NULL DEFAULT '0',
  `use_session_registration` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `ID_index` (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2394 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseDescriptions`
--

LOCK TABLES `CourseDescriptions` WRITE;
/*!40000 ALTER TABLE `CourseDescriptions` DISABLE KEYS */;
INSERT INTO `CourseDescriptions` VALUES (52,'NBCO','NBCO',4,'HM','220','Domestic Preparedness Training Responder - Operations Course','','',12,0.00,0,3.00,3,1,0.00,0.00,15,25,1,1,'<u>Objective</u>:  To identify correct operations level defensive response actions in the event of a nuclear, biological or chemical (NBC) incident, correct protective equipment, relevant detection and identification equipment, and to understand emergency decontamination procedures.<br><br><u>Learning Outcome</u>:  Upon successful completion of this course, the student will be able to correctly identify the correct operations level responder actions, utilize a quick method to predict the boundaries of the downwind vapor hazard associated with the release of any agents, utilize the proper protective equipment and understand the limitations of various self-protection methods and know what types of identification and detection equipment are available.<br><br><u>Course Content</u>:  Major topics covered in the course include appropriate responder actions, conducting a downwind hazard analysis, limitation of the prediction, levels of personal protection, detection and identification equipment and its capabilities, emergency decontamination, levels of decontamination, and decontamination delta presented by various agents.<br><br><u>Methods of Instruction</u>:  Lecture, demonstration, classroom activities, the use of varied audio/visual materials and a class practical exercise.','','The prerequisite for this course is Domestic Preparedness Training Program - Awareness Course.','','','','',NULL,NULL,2,2,2,3,3,NULL,NULL,0,0,0,NULL,'N/A',0,0,0,0,0,'',1,1,0.00,0.00,0.00,4,'','2003-04-29','',0,'','','2015-10-29 17:49:01','','2003-04-30 01:22:55',0,'',0,3,0,0),(75,'FOTIR','FOTIR',6,'MGMT','201','Fire Officer I','','Y208',2,0.00,0,63.00,63,1,1035.00,1090.00,15,30,1,2,'<u>Objective</u>:  To provide entry-level training in company operations and administration at the first-line supervisory level.  <i>Versions 1 and 2</i>  <br><br><u>Learning Outcome</u>:  Upon successful completion of this course, the student will be able to effectively manage human resources, community/public relations, fire department organizations and administration, fire inspection, investigation and public education, emergency service delivery and safety as a company officer.  (<i>NFPA 1021: Standard for Fire Officer Professional Qualifications</i>).  A score of 70% or better is required on all examinations.  Students must also successfully complete the Preceptorship Program prior to session 20.  <i>Versions 1 and 2</i><br><br><u>Course Content</u>:  Major topics covered in the course are the role of the fire officer, the fire officer\'s responsibility in facing compliance and accountability, managing cultural diversity, safety and wellness, quality management within the organizational structure, community awareness, public relations, fire safety education, functional leadership, problem solving, performance appraisal, building construction, fire cause determination, effective communication skills, and the incident command system with strategy and tactics.  <i>Versions 1 and 2</i><br><br><u>Methods of Instruction</u>:  Lecture, discussion, classroom exercises, case studies, audio/visual material, learner presentations/reports, preceptorship program, quizzes, a final examination, and completion of required skills and preceptorship program.  <i>Versions 1 and 2</i>','<u>Credit Recommendation</u>:  The ACE/CREDIT recommendation for this course is in the vocational certificate category or lower division baccalaureate/associate degree category, 4 semester hours in Fire Science Technology, Emergency Medical Service Technology, Emergency Management, or Public Administration (11/94) (12/99) (10/04) (09/10).  <i>Versions 1 and 2</i>','The prerequisites for this course are MFRI Firefighter II<br><br><b><u>OR</u></b><br><br>MFSPQB, NBFSPQ, IFSAC or DOD/IFSAC Firefighter II certification. <br><br><i>It is suggested a minimum of one year experience as a Firefighter II be completed before enrolling in this program.</i>','<b>Certification:</b><br>Upon successful completion, this course partially satisfies the professional certification requirements for:<br><ul><li>Fire Officer I</li></ul>','','','',NULL,NULL,2,2,2,3,3,NULL,NULL,1,0,0,NULL,'N/A',0,0,0,0,0,NULL,1,1,9.95,56.53,43.23,4,'Book price updated 11/2/09 - 1 book - $39.00<br>Updated ACE and prerequisites 5/25/10.<br>FALL 2010 BOOK PRICE UPDATE - $51.43<br>Book Price Update 8/29/13 - $54.83/New; $38.70/Used<br>Book Price Update 5/12/14 - $56.53/New; $43.23/Used','2008-06-08','',0,'','klayton','2015-07-06 13:20:47','tsweeting','2003-04-30 18:48:18',0,'',0,3,0,0),(82,'HMO','HMO',4,'HM','102','Hazardous Materials Operations','MFRI-0036','Y404',2,0.00,0,24.00,24,1,0.00,0.00,15,30,1,2,'<u>Objective</u>:  To provide the student with the knowledge and skills to perform hazardous materials first response.  <i>Versions 1, 2, and 3</i><br> <br><u>Learning Outcome</u>:  Upon successful completion of this course, the student will be able to analyze a hazardous materials incident, plan an initial response, implement the response, and evaluate the progress of the actions taken.  A score of 70% or better is required on all examinations.  <i>Versions 1, 2, and 3</i><br> <br><u>Course Content</u>:  Major topics covered in the course include firefighter safety, regulations and standards, chemistry, recognition and identifications, the DOT guidebook, site management, container behavior, defensive control measures, personal protective equipment, and decontamination.  <i>Versions 1 and 2</i><br><br><i>Version 3</i>:  Major topics covered in the course include firefighter safety, regulations and standards, chemistry, recognition and identifications, the DOT guidebook, site management, container behavior, defensive control measures, personal protective equipment, decontamination and terrorist and other criminal activity.<br><br><u>Methods of Instruction</u>:  Lecture, discussion, classroom exercises, audio/visual material, practical exercises, quizzes, observations, written examination and a final examination.  <i>Versions 1 and 2</i><br><br><i>Version 3</i>:  Lecture, discussion, classroom exercises, audio/visual materials, practical exercises, and written examinations.','<u>Credit Recommendation</u>:  The ACE/CREDIT recommendation for this course is:<br><br><i>Version 1</i>: In the vocational certificate or lower division baccalaureate/associate degree category, 1 semester hour in EMS Technology, Fire Sciences or Emergency Management (9/96). <br><br><i>Version 2</i>: In the vocational certificate or lower division, baccalaureate/associate degree category, 1 semester hour in Fire Chemistry, Hazardous Materials Chemistry or Emergency Management (9/03).  <br><br><i>Version 3</i>: In the vocational certificate or the lower division baccalaureate/associate degree category, 1 semester hour in Fire Chemistry, Hazardous Materials Chemistry, Hazardous Materials Management, Emergency Management, or Fire Science (2/09).','The prerequisite for this course is Protective Envelope and Foam, Pre-Emergency Response Training, MFRI Firefighter I or equivalent.','<b>Certification:</b><br><ol type=&quot;1&quot;><li>Upon successful completion, this course satisfies the professional certification requirements for:<br><br><ul><li>Responder to Hazardous Materials/WMD Incidents - Awareness</ul></li><br><li>Upon successful completion, this course partially satisfies the professional certification requirements for:<br><br><ul><li>Responder to Hazardous Materials/WMD Incidents - Operations</li></ol>','','','',NULL,NULL,2,2,2,3,4,NULL,NULL,0,0,0,NULL,'N/A',0,0,0,0,0,NULL,1,1,0.00,84.96,64.97,4,'NFA Code:  Y404; HMEP eligible 10/15/14 KLL<br><br>Book Price Update 5/9/14 - $84.96/New; $64.97/Used','2003-04-30','',0,'','sbergin','2016-07-12 17:52:27','tsweeting','2003-04-30 18:52:54',0,'',0,3,0,0),(104,'PEAF','PEAF',3,'FIRE','102','Protective Envelope And Foam','','',2,0.00,0,9.00,9,1,0.00,0.00,15,30,1,2,'<u>Objective</u>:  To provide rescue and emergency care providers the skills necessary to mitigate a hazardous materials incident.<br><br><u>Learning Outcome</u>:  Upon successful completion of the course, students will be able to understand and apply the skills necessary to protect themselves in a hazardous materials situation and apply foam to hazardous materials based on standards found in NFPA 472: <i>Standard for Professional Competence of Responders to Hazardous Materials Incidents</i>.  Students must successfully complete a skills check-off.<br><br><u>Course Content</u>:  Major topics covered in the course include personal protective equipment, respiratory protection, self-contained breathing apparatus, handling hose lines, and foam application.<br><br><u>Methods of Instruction</u>:  Lecture, discussion, practical exercises, graded practical exercises, and written examinations.','','There are no prerequisites for this course.<br><br><u>Note</u>:  Students are required to provide their own SCBA and turnout gear at the start of the first session.','','','','',NULL,NULL,2,2,2,3,3,NULL,NULL,1,0,0,NULL,'N/A',0,0,0,0,0,NULL,1,1,0.00,48.88,0.00,4,'Winter 2008 - Book price updated 01/16/08<br>Fall 2009 - 5th edition, Essentials<br>Book price updated 04/24/08 - $37.46<br>Book price updated 02/20/09 - $38.21<br>Book price updated 5/11/10 - $40.13<br>FALL 2010 BOOK PRICE UPDATE - $45.48<br>Book Price Update 9/3/13 - $48.88/New; $34.50/Used','2003-04-30','',1,'','sbergin','2016-01-29 12:38:14','tsweeting','2003-04-30 19:08:55',0,'',0,3,0,0),(199,'EVOR','EVOR',3,'FIRE','131','Emergency Vehicle Operator Refresher','','',2,0.00,0,12.00,12,1,0.00,0.00,15,30,1,2,'<u>Objective</u>:  To provide the necessary knowledge and skills to enhance the ability of current drivers of emergency services vehicles.<br><br><u>Learning Outcome</u>:  Upon successful completion of this course, the student will be able to perform vehicle readiness inspections, discuss driver qualifications, vehicle dynamics, basic vehicle control, and a variety of driving tasks.<br><br><u>Course Content</u>:  Major topics covered in this course include laws and liabilities, driver\'s role and responsibilities, driver readiness, operating space, major vehicle components, inspection and maintenance, physical forces of motion, vehicle dynamics and basic control tasks, road characteristics and vehicle maneuvers, route planning and selection, driving range rules, vehicle inspections by students, and range activities at slow and moderate speeds.<br><br><u>Methods of Instruction</u>:  Lecture, discussion, classroom exercises, audio/visual material, and practical exercises and graded practical exercises.','','The prerequisites for this course are a current, valid Maryland Driver\'s License or equivalent<br><br><b><u>AND</u></b><br><br>A letter from the Fire Chief of the department giving the student permission to drive the department\'s apparatus in the course.','','','','','','',2,2,2,3,3,NULL,NULL,1,0,0,NULL,'N/A',0,0,0,0,0,'',1,1,0.00,0.00,0.00,4,'','2003-06-13','',0,'','','2013-09-18 13:28:51','','2003-06-13 15:26:34',0,'',0,3,0,0),(726,NULL,'CFPS',5,'IND','230','Certified Fire Protection Specialist Preparatory','','',NULL,0.00,0,16.00,16,1,250.00,250.00,15,30,NULL,NULL,'This two-day program is designed to provide the participant with the skills and knowledge to quickly access the 20th edition of the NFPA Fire Protection Handbook for preparation to take the Certified Fire Protection Specialist examination offered by the CFPS Board, a component of the National Fire Protection Association.  This program will focus on techniques for utilizing the student\'s own Fire Protection Handbook (open-book exam) to quickly determine answers and solutions to sample questions pertaining to fire protection from the various topics and categories identified in the text.<br><br><b>NOTE</b>: Students are responsible for bringing their own NFPA Fire Protection Handbook, 20th edition (Volumes I and II).','','','','','','',NULL,NULL,2,2,2,2,2,NULL,NULL,1,0,0,NULL,'N/A',0,0,0,0,0,NULL,1,1,0.00,0.00,0.00,2,'','2005-06-29','',0,'','rdesper','2014-08-29 18:27:10','rdesper','2005-06-29 18:51:25',0,'',0,3,0,0),(1404,'','',2,'EMS','123','Heartsaver Pediatric First Aid with Adult and Pediatric CPR','','',NULL,0.00,0,8.00,8,1,0.00,0.00,15,30,NULL,NULL,'This one day program is intended for employee training at companies, corporations, businesses, etc.  This program is designed to review medical emergencies and injuries, as well as an option to review environmental emergencies.  Some examples of emergencies reviewed in the course include breathing problems, choking, allergies, diabetes, stroke, seizures, heart attack, fainting, shock, and musculoskeletal injuries.  This program also includes Child CPR/AED and Infant CPR with a mask. Optional Adult CPR/AED and Asthma modules are included.  There will be skills testing during this program, and a written first aid quiz, and it will result in a two-year certification.','','','','','','',NULL,NULL,2,4,2,2,2,NULL,NULL,1,0,0,NULL,'N/A',1,0,0,0,0,'',1,1,0.00,0.00,0.00,4,'','2010-10-21','',0,'','','2013-12-13 16:31:48','','2010-10-21 17:59:18',0,'',0,3,0,0),(1485,NULL,'EMTB',2,'EMS','106','Emergency Medical Technician','','',NULL,0.00,0,165.00,0,9,0.00,0.00,15,35,NULL,NULL,'<u>Objective</u>:  To provide students with the necessary knowledge and skills to perform emergency medical care in a pre-hospital environment at the basic life support level.  <i>Versions 1 and 2</i><br><br><u>Learning Outcome</u>:  Upon successful completion of this course, the student will be able to recognize, assess, and manage medical and trauma signs and symptoms in patients of emergency situations, determine and use appropriate equipment for patient management and care, communicate and work with other emergency service personnel in the care, transport and transfer of patients and maintain patient and department records.  Each written module examination must be passed with a score of 70% or better.  Each practical module examination must be passed according to a checklist based on U.S. DOT requirements.  At the conclusion of the MFRI portion of the program, a written and practical certification examination will be administered by MIEMSS.  <i>Versions 1 and 2</i><br><br><u>Course Content</u>:  Major topics include legal aspects of emergency care, infection control, patient assessment, the respiratory system, oxygen adjuncts and delivery, CPR, AED, bleeding control and management of soft tissue injuries, musculoskeletal injuries and management, spinal immobilization, pediatric and obstetric emergencies, crisis intervention, multiple casualty and triage management, ambulance operations, and EMS systems.  <i>Versions 1 and 2</i><br><br><u>Methods of Instruction</u>:  Lecture, discussion, classroom exercises, case studies, audio/visual material, skills practical scenarios and modular written and practical examinations.  <i>Versions 1 and 2</i>','','There are no prerequisites for this course.<br><br><i>The student must complete the required internship in the local department prior to session 52 to be eligible to take the MIEMSS written and practical examinations</i>.','','MIEMSS Testing Fee for Practical','','',NULL,NULL,2,2,2,3,3,NULL,NULL,0,0,0,NULL,'N/A',0,0,0,0,0,NULL,1,1,0.00,75.00,45.00,4,'93.50 textbook price as of 8/26/13<br>Book Price Update 8/29/13 - $75.00/New (Price set by Director Edwards; $45.00/Used','2012-07-01','',0,'','sbergin','2015-08-18 19:48:02','klayton','2012-03-28 16:57:50',0,'',0,3,0,0),(1763,'','',7,'RES','210','Rescue Technician - Vehicle and Machinery Extrication','','',NULL,0.00,0,27.00,0,1,0.00,0.00,15,25,NULL,3,'<u>Course Objective</u>:  To provide students with the knowledge, skills and abilities necessary to extricate victims from common passenger vehicles, simple small machines, commercial or heavy vehicles and heavy machinery. <br><br><u>Course Description</u>: Major topics covered in this course include planning for a vehicle or machinery incident, performing on-going incident size-up, establishing scene safety zones, establishing fire protection, stabilizing vehicles or machines, isolating potentially harmful energy sources, determining access and egress points, creating access and egress openings, disentangling victims, removing packaged victims, and terminating vehicle or machinery rescue incidents. Methods of instruction include lecture, discussion and team-focused practical exercises. <br><br><u>Successful Completion</u>: Students must attend required classroom sessions, complete homework assignments, demonstrate proficiency in the practical skills evolutions and obtain a score of 70% or better on the final written and practical examinations.','','Personal Protective Equipment and SCBA (FIRE 099), Protective Envelope and Foam (FIRE 102), Pre-Emergency Response Training (FIRE 103), Firefighter I (FIRE 101), or equivalent.','<b>Certification:</b><br>Upon successful completion, this course partially satisfies the professional certification requirements for:<br><ul><li>Vehicle and Machinery Technical Rescuer I and II</li></ul>','','','','','Successful completion of this course may make you eligible for certification at the Vehicle Technical Rescuer I & II level.  If you have Firefighter I certification, have successfully completed EMR or a higher level EMS training class, and have either completed the MFRI Rescue Technician: Site Operations class or are certified to any Rescue Technician level you are eligible for certification.  The certification application can be found at https://zone.mfri.org/mfspqb/forms/certapp1006vtriii.pdf. Send the completed application with a check or money order made out to MFSPQB for $10 to the address on the application.',2,2,2,3,2,NULL,NULL,1,0,0,NULL,'N/A',0,0,0,0,0,'',1,1,0.00,50.58,38.68,4,'FALL 2010 BOOK PRICE UPDATE - $23.38<br>Book Price Update 8/29/13 - $48.88/New; $34.50/Used<br>Book Price Update 5/9/14 - $50.58/New; $38.68/Used','2014-04-01','',0,'','','2016-09-29 11:50:48','','2014-05-07 17:57:07',0,'',0,3,0,0),(1799,'','',17,'CD','100','Company Drill','','',NULL,0.00,0,3.00,0,1,0.00,0.00,10,100,NULL,2,'Company Drills are 3 hour training opportunities on any fire, EMS, haz-mat or rescue topic and are offered to all Maryland Emergency Services organizations.','','Company Drills must be scheduled through a regional office at least 30 days prior the date they want to hold the drill.','Local departments are offered two company drills per year at no charge.','','','','','',5,2,2,3,2,NULL,NULL,0,0,0,NULL,'N/A',0,1,1,0,0,'',1,0,0.00,0.00,0.00,1,'','2014-07-01','',0,'','','2014-09-16 11:54:11','','2014-09-11 12:19:59',0,'',0,3,0,0),(2295,'','FFI',3,'FIRE','101','Firefighter I (PILOT)','','',NULL,135.00,0,135.00,0,1,0.00,0.00,15,25,NULL,3,'<u>Course Objective</u>: To provide students with the knowledge, skills and abilities to safely and effectively perform basic firefighting operations as part of a firefighting team. Upon successful completion of this course, the student will be able to understand and apply the principles of fire behavior; building construction; water distribution systems; fixed fire protection systems; ventilation; hose streams; fire prevention; and inspections, ladders, and rescue techniques<br><br><u>Course Description</u>: Major topics covered in this course are the fire department organization, communications, the incident command system, ropes and knots, fire behavior, safety, fire prevention, personal protective equipment, fire extinguishers, respiratory protection, ventilation, hoselines, forcible entry, search and rescue procedures, and ladder and sprinkler systems.  Methods of instruction include lecture, discussion and team-focused practical exercises.  <br><br><u>Successful Completion</u>:   Students must attend required classroom sessions, complete all assigned online and classroom activities and homework assignments, demonstrate proficiency in the practical skills evolutions and obtain a score of 70% or better on the written and practical examinations.','','Medical Clearance.','<b>Certification</b>:  Upon successful completion, this course partially satisfies the professional certification requirements for:<br><ul><li>Fire Fighter I</li</ul>','','','','','',2,2,2,3,2,'','',1,0,1,NULL,'UMDCNV',0,0,0,0,0,'',1,1,0.00,52.50,34.50,4,'IFSTA Pilot with online component using UMD Canvas.','2020-01-02','',1,'','','2019-12-11 18:51:48','','2019-12-11 18:51:48',45,'',0,3,0,0);
/*!40000 ALTER TABLE `CourseDescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRApplicationLevel`
--

DROP TABLE IF EXISTS `MESSRApplicationLevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRApplicationLevel` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRApplicationLevel`
--

LOCK TABLES `MESSRApplicationLevel` WRITE;
/*!40000 ALTER TABLE `MESSRApplicationLevel` DISABLE KEYS */;
INSERT INTO `MESSRApplicationLevel` VALUES (1,'None'),(2,'FR'),(3,'EMT-B'),(4,'CRT/EMT-I'),(5,'EMT-P'),(6,'EMD');
/*!40000 ALTER TABLE `MESSRApplicationLevel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRApplicationTypes`
--

DROP TABLE IF EXISTS `MESSRApplicationTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRApplicationTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRApplicationTypes`
--

LOCK TABLES `MESSRApplicationTypes` WRITE;
/*!40000 ALTER TABLE `MESSRApplicationTypes` DISABLE KEYS */;
INSERT INTO `MESSRApplicationTypes` VALUES (1,'None'),(2,'Initial Certification'),(3,'Reciprocity'),(4,'Reinstatement'),(5,'Recertifciation'),(6,'Not Applicable');
/*!40000 ALTER TABLE `MESSRApplicationTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRCollegeLevelTypes`
--

DROP TABLE IF EXISTS `MESSRCollegeLevelTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRCollegeLevelTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRCollegeLevelTypes`
--

LOCK TABLES `MESSRCollegeLevelTypes` WRITE;
/*!40000 ALTER TABLE `MESSRCollegeLevelTypes` DISABLE KEYS */;
INSERT INTO `MESSRCollegeLevelTypes` VALUES (1,'None'),(2,'1'),(3,'2'),(4,'3'),(5,'4'),(6,'5'),(7,'6 or over');
/*!40000 ALTER TABLE `MESSRCollegeLevelTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRGenderTypes`
--

DROP TABLE IF EXISTS `MESSRGenderTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRGenderTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRGenderTypes`
--

LOCK TABLES `MESSRGenderTypes` WRITE;
/*!40000 ALTER TABLE `MESSRGenderTypes` DISABLE KEYS */;
INSERT INTO `MESSRGenderTypes` VALUES (1,'None'),(2,'Male'),(3,'Female');
/*!40000 ALTER TABLE `MESSRGenderTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRGradeLevelTypes`
--

DROP TABLE IF EXISTS `MESSRGradeLevelTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRGradeLevelTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRGradeLevelTypes`
--

LOCK TABLES `MESSRGradeLevelTypes` WRITE;
/*!40000 ALTER TABLE `MESSRGradeLevelTypes` DISABLE KEYS */;
INSERT INTO `MESSRGradeLevelTypes` VALUES (1,'None'),(2,'7 years or less'),(3,'8'),(4,'9'),(5,'10'),(6,'11'),(7,'12/G.E.D.'),(8,'13'),(9,'14'),(10,'15'),(11,'16'),(12,'17'),(13,'18 or over');
/*!40000 ALTER TABLE `MESSRGradeLevelTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRRaceTypes`
--

DROP TABLE IF EXISTS `MESSRRaceTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRRaceTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRRaceTypes`
--

LOCK TABLES `MESSRRaceTypes` WRITE;
/*!40000 ALTER TABLE `MESSRRaceTypes` DISABLE KEYS */;
INSERT INTO `MESSRRaceTypes` VALUES (1,'None'),(2,'White'),(3,'African American'),(4,'Asian'),(5,'Hispanic'),(6,'American Indian/Alaskan Native'),(7,'Other'),(8,'Native Hawaiian / other Pacific Islander');
/*!40000 ALTER TABLE `MESSRRaceTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRHoldStatus`
--

DROP TABLE IF EXISTS `MESSRHoldStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRHoldStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=80 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRHoldStatus`
--

LOCK TABLES `MESSRHoldStatus` WRITE;
/*!40000 ALTER TABLE `MESSRHoldStatus` DISABLE KEYS */;
INSERT INTO `MESSRHoldStatus` VALUES (1,'Received'),(2,'Pre-Registered'),(3,'Duplicate'),(4,'Rejected'),(5,'Withdrawn'),(6,'Registered'),(7,'Error'),(70,'Error'),(71,'Duplicate'),(72,'Back page scanned first'),(73,'Wrong Class'),(8,'Merged'),(74,'Walk In'),(9,'Placed In Class'),(75,'SSN Does Not Match Name'),(76,'Provider Number Does Not Match Name'),(77,'Missing SSN or Invalid'),(78,'Missing or Invalid Name'),(79,'Invalid Birth Date');
/*!40000 ALTER TABLE `MESSRHoldStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSROutcomeNumberTypes`
--

DROP TABLE IF EXISTS `MESSROutcomeNumberTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSROutcomeNumberTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSROutcomeNumberTypes`
--

LOCK TABLES `MESSROutcomeNumberTypes` WRITE;
/*!40000 ALTER TABLE `MESSROutcomeNumberTypes` DISABLE KEYS */;
INSERT INTO `MESSROutcomeNumberTypes` VALUES (1,'None'),(2,'Module'),(3,'Session');
/*!40000 ALTER TABLE `MESSROutcomeNumberTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSROutcomeTypes`
--

DROP TABLE IF EXISTS `MESSROutcomeTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSROutcomeTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSROutcomeTypes`
--

LOCK TABLES `MESSROutcomeTypes` WRITE;
/*!40000 ALTER TABLE `MESSROutcomeTypes` DISABLE KEYS */;
INSERT INTO `MESSROutcomeTypes` VALUES (1,'None'),(2,'Successfully Completed'),(3,'Withdrew'),(4,'Dropped'),(5,'Failed'),(6,'Incomplete'),(7,'Successfully Completed Retraining'),(8,'Transferred'),(9,'Failed Practical Exam'),(10,'Failed Midterm Exam');
/*!40000 ALTER TABLE `MESSROutcomeTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRSponsorTypes`
--

DROP TABLE IF EXISTS `MESSRSponsorTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRSponsorTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRSponsorTypes`
--

LOCK TABLES `MESSRSponsorTypes` WRITE;
/*!40000 ALTER TABLE `MESSRSponsorTypes` DISABLE KEYS */;
INSERT INTO `MESSRSponsorTypes` VALUES (1,'None'),(2,'Academy'),(3,'MFRI'),(4,'Private'),(5,'High School'),(6,'College'),(7,'Law Enforcement');
/*!40000 ALTER TABLE `MESSRSponsorTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRSuffixTypes`
--

DROP TABLE IF EXISTS `MESSRSuffixTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRSuffixTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRSuffixTypes`
--

LOCK TABLES `MESSRSuffixTypes` WRITE;
/*!40000 ALTER TABLE `MESSRSuffixTypes` DISABLE KEYS */;
INSERT INTO `MESSRSuffixTypes` VALUES (1,'None'),(2,'I'),(3,'II'),(4,'III'),(5,'IV'),(6,'Jr'),(7,'Sr'),(8,'V');
/*!40000 ALTER TABLE `MESSRSuffixTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRTitleTypes`
--

DROP TABLE IF EXISTS `MESSRTitleTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRTitleTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRTitleTypes`
--

LOCK TABLES `MESSRTitleTypes` WRITE;
/*!40000 ALTER TABLE `MESSRTitleTypes` DISABLE KEYS */;
INSERT INTO `MESSRTitleTypes` VALUES (1,'None'),(2,'Mr.'),(3,'Mrs.'),(4,'Ms.');
/*!40000 ALTER TABLE `MESSRTitleTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MESSRHold`
--

DROP TABLE IF EXISTS `MESSRHold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MESSRHold` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `FormVersion` int DEFAULT '0',
  `FormNumberBack` varchar(20) DEFAULT '',
  `FormNumberFront` varchar(20) DEFAULT '',
  `ScheduledCourseID` int unsigned DEFAULT '0',
  `ApplicationTypeID` int unsigned DEFAULT '1',
  `ApplicationLevelID` int unsigned DEFAULT '1',
  `CountyNumber` char(3) DEFAULT '',
  `LogNumber` varchar(255) DEFAULT NULL,
  `LogNumberCategory` varchar(255) DEFAULT '',
  `LogNumberLevel` varchar(255) DEFAULT '',
  `LogNumberFundingSource` varchar(255) DEFAULT '',
  `LogNumberSection` varchar(255) DEFAULT '',
  `LogNumberPrefix` varchar(128) DEFAULT '',
  `LogNumberOrdinal` varchar(128) DEFAULT '',
  `LogNumberFiscalYear` varchar(128) DEFAULT '',
  `SponsorID` int unsigned DEFAULT '1',
  `ClientNumber` varchar(16) DEFAULT '',
  `IDNumber` blob,
  `BIDNumber` blob,
  `StateProviderNumber` blob,
  `BStateProviderNumber` blob,
  `CompanyNumber` varchar(255) DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `LegalQuestion1` int DEFAULT NULL,
  `LegalQuestion2` int DEFAULT NULL,
  `LegalQuestion3` int DEFAULT NULL,
  `TitleID` int unsigned DEFAULT '1',
  `FirstName` varchar(255) DEFAULT '',
  `MiddleName` varchar(255) DEFAULT '',
  `LastName` varchar(255) DEFAULT '',
  `Suffix` varchar(255) DEFAULT '',
  `POBox` int DEFAULT '0',
  `RuralRoute` int DEFAULT '0',
  `StreetAddressNumber` varchar(32) DEFAULT '',
  `StreetAddress` varchar(255) DEFAULT '',
  `Apt` varchar(255) DEFAULT '',
  `City` varchar(255) DEFAULT '',
  `State` char(2) DEFAULT '',
  `PostCode` varchar(20) DEFAULT '',
  `HomePhone` varchar(32) DEFAULT '',
  `WorkPhone` varchar(32) DEFAULT '',
  `GenderID` int DEFAULT '1',
  `Hispanic` int DEFAULT '0',
  `RaceID` int unsigned DEFAULT '1',
  `GradeLevelID` int unsigned DEFAULT '1',
  `CollegeLevelID` int unsigned DEFAULT '1',
  `Outcome` int DEFAULT NULL,
  `OutcomeTypeID` int unsigned DEFAULT '1',
  `OutcomeNum` int DEFAULT NULL,
  `PracticalExamResuscitation` char(1) DEFAULT '',
  `PracticalExamResuscitationRetest` char(1) DEFAULT '',
  `PracticalExamMedical` char(1) DEFAULT '',
  `PracticalExamMedicalRetest` char(1) DEFAULT '',
  `PracticalExamTrauma` char(1) DEFAULT '',
  `PracticalExamTraumaRetest` char(1) DEFAULT '',
  `WrittenExamNumber` char(3) DEFAULT '',
  `OverAllScore` char(3) DEFAULT '',
  `FrontPage` datetime DEFAULT '0000-00-00 00:00:00',
  `BackPage` datetime DEFAULT '0000-00-00 00:00:00',
  `SynchedFront` datetime DEFAULT '0000-00-00 00:00:00',
  `SynchedBack` datetime DEFAULT '0000-00-00 00:00:00',
  `MergeID` int DEFAULT NULL,
  `StatusID` int DEFAULT NULL,
  `EvaluationResults` text,
  `ModularGrades` text,
  `PreRegID` int unsigned DEFAULT '0',
  `StudentRegID` int unsigned DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Priority` int DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=262536 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MESSRHold`
--

LOCK TABLES `MESSRHold` WRITE;
/*!40000 ALTER TABLE `MESSRHold` DISABLE KEYS */;
/*!40000 ALTER TABLE `MESSRHold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentMESSRData`
--

DROP TABLE IF EXISTS `StudentMESSRData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentMESSRData` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `FileName` varchar(255) DEFAULT '',
  `FrontPage05Format` int DEFAULT '1',
  `ScheduledCourseID` int unsigned DEFAULT NULL,
  `PageSidesScanned` int DEFAULT '0',
  `DataSentToMIEMSS` int DEFAULT '0',
  `DataRetrievedByMIEMSS` int DEFAULT '0',
  `RetrievedDate` datetime DEFAULT '0000-00-00 00:00:00',
  `NotificationSentToMIEMSS` int DEFAULT '0',
  `NotificationDate` datetime DEFAULT '0000-00-00 00:00:00',
  `MIEMSSUser` varchar(32) DEFAULT '',
  `SendDate` datetime DEFAULT NULL,
  `RecordCount` int DEFAULT '0',
  `PreRegCount` int DEFAULT '0',
  `StatusID` int unsigned DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=31627 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentMESSRData`
--

LOCK TABLES `StudentMESSRData` WRITE;
/*!40000 ALTER TABLE `StudentMESSRData` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentMESSRData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locations`
--

DROP TABLE IF EXISTS `Locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Locations` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `RegionID` int unsigned DEFAULT NULL,
  `County` varchar(255) DEFAULT NULL,
  `CountyID` int unsigned DEFAULT NULL,
  `Address1` varchar(255) DEFAULT NULL,
  `Address2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `PostCode` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `PrimaryPhoneNumber` varchar(255) DEFAULT NULL,
  `SecondaryPhoneNumber` varchar(255) DEFAULT NULL,
  `FaxNumber` varchar(255) DEFAULT NULL,
  `EmailAddress` varchar(255) DEFAULT NULL,
  `ContactID` int unsigned DEFAULT NULL,
  `MapLinkID` int unsigned DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=1010 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locations`
--

LOCK TABLES `Locations` WRITE;
/*!40000 ALTER TABLE `Locations` DISABLE KEYS */;
INSERT INTO `Locations` VALUES (1,'MFRI Headquarters',7,'Prince Georges',18,'4500 Campus Drive','','College Park','MD','20742','USA','301 226 9900','800 ASK MFRI','','info@mfri.org',0,0,NULL,'2018-08-06 20:07:38',NULL,'0000-00-00 00:00:00'),(2,'MFRI Southern Maryland Regional Training Center',6,'Charles',10,'10375 Audie Lane','','La Plata','MD','20646','USA','301.934.2600','888.691.4628','301.934.4333','smrtc@mfri.org',0,0,NULL,'2007-08-22 14:17:22',NULL,'0000-00-00 00:00:00'),(3,'MFRI Western Maryland Regional Training Center',1,'Washington',1,'13928 Hazmat Drive SW','','Cumberland','MD','21502','USA','888-691-6143','301-729-0431','301 729 6146','wmcontact@mfri.org',0,0,'tsweeting','2017-09-11 15:24:16','tsweeting','2003-04-23 23:45:37'),(4,'MFRI North Central Regional Training Center',2,'Frederick',8,'PO Box 1032','','Mt. Airy','MD','21771','USA','301 829 2020','800 287 6374','301 829 2021','',0,0,'tsweeting','2003-05-15 17:23:46','tsweeting','2003-04-23 23:46:54'),(5,'MFRI North East Regional Training Center',3,'Cecil',14,'PO Box 789','9250 Faiview Point Road','Edgewood','MD','21010','USA','410 676 5409','888 317 2218','410-676-5413','',0,0,'tsweeting','2016-03-22 17:30:49','tsweeting','2003-04-23 23:48:16'),(6,'MFRI Upper Eastern Shore Regional Training Center',4,'Queen Anne',19,'601 Safety Drive','','Centreville','MD','21617','USA','410 758 2112','888 692 0055','410 758  3573','',0,0,'tsweeting','2003-05-15 17:35:54','tsweeting','2003-04-23 23:49:45'),(7,'MFRI Lower Eastern Shore Regional Training Center',5,'Somerset',21,'12148 John Wilson Lane','','Princess Anne','MD','21853','USA','410 749 0313','888 691 8880','410 651 3356','',0,0,'tsweeting','2003-05-15 17:23:07','tsweeting','2003-04-23 23:51:03');
/*!40000 ALTER TABLE `Locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PhoneNumberTypes`
--

DROP TABLE IF EXISTS `PhoneNumberTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PhoneNumberTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PhoneNumberTypes`
--

LOCK TABLES `PhoneNumberTypes` WRITE;
/*!40000 ALTER TABLE `PhoneNumberTypes` DISABLE KEYS */;
INSERT INTO `PhoneNumberTypes` VALUES (1,'None'),(2,'Primary'),(3,'Secondary'),(4,'Fax'),(5,'Pager'),(6,'Work'),(7,'Home'),(8,'Mobile'),(9,'Other'),(10,'Toll Free'),(11,'Metro DC Local'),(12,'Office Primary'),(13,'Office Secondary'),(14,'Office Mobile');
/*!40000 ALTER TABLE `PhoneNumberTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MFRIRegions`
--

DROP TABLE IF EXISTS `MFRIRegions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MFRIRegions` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `RegionNumber` int unsigned DEFAULT NULL,
  `Name` varchar(80) DEFAULT NULL,
  `Abbreviation` varchar(10) DEFAULT NULL,
  `County` varchar(255) DEFAULT NULL,
  `StreetAddress1` varchar(255) DEFAULT NULL,
  `StreetAddress2` varchar(255) DEFAULT NULL,
  `PostalAddress1` varchar(255) DEFAULT NULL,
  `PostalStreetAddress2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `PostCode` varchar(255) DEFAULT NULL,
  `PrimaryPhoneNumber` varchar(255) DEFAULT NULL,
  `SecondaryPhoneNumber` varchar(255) DEFAULT NULL,
  `MetroPhoneNumber` varchar(255) DEFAULT NULL,
  `TollFreePhoneNumber` varchar(255) DEFAULT NULL,
  `FaxNumber` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `URL` varchar(255) DEFAULT '',
  `ContactID` int unsigned DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MFRIRegions`
--

LOCK TABLES `MFRIRegions` WRITE;
/*!40000 ALTER TABLE `MFRIRegions` DISABLE KEYS */;
INSERT INTO `MFRIRegions` VALUES (1,1,'Western Maryland','WMRTC','Washington','13928 Hazmat Dr. SW','','PO Box 5153','','Cresaptown','MD','21502-5153','301-729-0431','','','1-888-691-6143','301-729-6146','tdyche@mfri.org','www.mfri.org/Regions/r1wmro.html',155),(2,2,'North Central','NCRTC','Frederick','1003 Twin Arch Road','','PO Box 196','','Mt. Airy','MD','21771-0196','301-829-2020','','','1-800-287-6374','301-829-2021','alevy@mfri.org','www.mfri.org/Regions/r2ncro.html',42),(3,3,'North East','NERTC','Harford','Building 1074, Riley Road','Aberdeen Proving Grounds','PO Box 1032','','Aberdeen','MD','21001-6032','410-272-2288','','','1-888-317-2218','410-272-2289','aperrico@mfri.org','www.mfri.org/Regions/r3nero.html',221),(4,4,'Upper Eastern Shore','UESRTC','Queen Anne','601 Safety Drive','','601 Safety Drive','','Centreville','MD','21617','410-758-2112','','','1-888-692-0055','410-758-3573','jbeall@mfri.org','www.mfri.org/Regions/r4uero.html',88),(5,5,'Lower Eastern Shore','LESRTC','Somerset','12148 John Wilson Lane','','12148 John Wilson Lane','','Princess Anne','MD','21853-3648','410-749-0313','410-651-3331','','1-888-691-8880','410-651-3356','jward@mfri.org','www.mfri.org/Regions/r5lero.html',127),(6,6,'Southern Maryland','SMRTC','Charles','10375 Audie Lane','','PO Box 813','','La Plata','MD','20646-0813','301-934-2600','','301-870-2095','1-888-691-4628','301-934-4333','jbeall@mfri.org','www.mfri.org/Regions/r6smro.html',211),(7,0,'Headquarters','HQ','Prince Georges','4500 Paint Branch Parkway','','University of Maryland','Building 199','College Park','MD','20742','301-226-9900','','','1-800-275-6374','301-314-0686',NULL,'www.mfri.org/Regions/mfrihqcp.html',NULL),(8,0,'None','None',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'www.mfri.org/Regions/mfrihqcp.html',NULL),(9,0,'All','All',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'www.mfri.org/Regions/regionalinfo.html',NULL);
/*!40000 ALTER TABLE `MFRIRegions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CourseSection`
--

DROP TABLE IF EXISTS `CourseSection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CourseSection` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  `Abbreviation` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CourseSection`
--

LOCK TABLES `CourseSection` WRITE;
/*!40000 ALTER TABLE `CourseSection` DISABLE KEYS */;
INSERT INTO `CourseSection` VALUES (1,'Special Programs','SPS'),(2,'Field Operations','FO'),(3,'All','ALL'),(4,'Other','OTH'),(5,'Advanced Life Support','ALS'),(6,'Administrative Services','ADS'),(7,'Logistical Support','LSS'),(8,'Director\'s Office','DIR'),(9,'Institute Development','IDS'),(10,'Technology and Certification Section','TCS');
/*!40000 ALTER TABLE `CourseSection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `JurisdictionTypes`
--

DROP TABLE IF EXISTS `JurisdictionTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `JurisdictionTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `JurisdictionTypes`
--

LOCK TABLES `JurisdictionTypes` WRITE;
/*!40000 ALTER TABLE `JurisdictionTypes` DISABLE KEYS */;
INSERT INTO `JurisdictionTypes` VALUES (1,'City'),(2,'County'),(3,'State'),(4,'Federal'),(5,'National'),(6,'International'),(7,'Industry'),(8,'DoD'),(9,'Unknown');
/*!40000 ALTER TABLE `JurisdictionTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Jurisdictions`
--

DROP TABLE IF EXISTS `Jurisdictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Jurisdictions` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  `Number` varchar(10) DEFAULT '',
  `TypeID` int unsigned DEFAULT NULL,
  `special_type` tinyint(1) DEFAULT '0',
  `MfriRegionID` int unsigned DEFAULT '8',
  `mfri_office_id` int unsigned DEFAULT NULL,
  `SortOrder` int DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Jurisdictions`
--

LOCK TABLES `Jurisdictions` WRITE;
/*!40000 ALTER TABLE `Jurisdictions` DISABLE KEYS */;
INSERT INTO `Jurisdictions` VALUES (1,'Allegany','01',2,0,1,5,1),(2,'Annapolis','',1,0,4,8,2),(3,'Anne Arundel','02',2,0,4,8,1),(4,'Baltimore','33',1,0,3,7,2),(5,'Baltimore','03',2,0,3,7,1),(6,'Calvert','04',2,0,6,10,1),(7,'Caroline','05',2,0,4,8,1),(8,'Carroll','06',2,0,2,6,1),(9,'Cecil','07',2,0,3,7,1),(10,'Charles','08',2,0,6,10,1),(11,'Dorchester','09',2,0,5,9,1),(12,'Frederick','10',2,0,2,6,1),(13,'Garrett','11',2,0,1,5,1),(14,'Harford','12',2,0,3,7,1),(15,'Howard','13',2,0,2,6,1),(16,'Kent','14',2,0,4,8,1),(17,'Montgomery','15',2,0,2,6,1),(18,'Prince George\'s','16',2,0,6,10,1),(19,'Queen Anne\'s','17',2,0,4,8,1),(20,'St. Mary\'s','18',2,0,6,10,1),(21,'Somerset','19',2,0,5,9,1),(22,'Talbot','20',2,0,4,8,1),(23,'Washington','21',2,0,1,5,1),(24,'Wicomico','22',2,0,5,9,1),(25,'Worcester','23',2,0,5,9,1),(26,'Maryland State','',3,1,7,11,2),(27,'Not in Maryland','',2,1,8,2,2),(28,'US Government','',4,1,7,2,3),(29,'DoD','27',8,1,7,2,3),(30,'Unknown','',2,0,8,4,0),(31,'Commercial','00',7,1,7,2,3);
/*!40000 ALTER TABLE `Jurisdictions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MFRIOffices`
--

DROP TABLE IF EXISTS `MFRIOffices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MFRIOffices` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `RegionNumber` int unsigned DEFAULT NULL,
  `Name` varchar(80) DEFAULT NULL,
  `Abbreviation` varchar(10) DEFAULT NULL,
  `FRSNumber` varchar(255) DEFAULT NULL,
  `is_payroll_processor` tinyint(1) DEFAULT '0',
  `is_department` tinyint(1) DEFAULT '0',
  `is_registration_processor` tinyint(1) DEFAULT '0',
  `is_statewide` tinyint(1) NOT NULL DEFAULT '0',
  `sort_order` int unsigned DEFAULT '0',
  `internal_note` longtext NOT NULL,
  `public_note` longtext NOT NULL,
  `public_alert_text` longtext,
  `public_schedule_note` longtext,
  `public_schedule_alert_text` longtext,
  `default_send_alert_email_to_office_before_approval` tinyint(1) DEFAULT '0',
  `default_send_alert_email_to_office_after_approval` tinyint(1) DEFAULT '0',
  `StreetAddress1` varchar(255) DEFAULT NULL,
  `StreetAddress2` varchar(255) DEFAULT NULL,
  `StreetCity` varchar(255) DEFAULT NULL,
  `StreetState` varchar(255) DEFAULT 'MD',
  `StreetPostCode` varchar(20) DEFAULT NULL,
  `PostalAddress1` varchar(255) DEFAULT NULL,
  `PostalAddress2` varchar(255) DEFAULT NULL,
  `PostalCity` varchar(255) DEFAULT NULL,
  `PostalState` varchar(255) DEFAULT 'MD',
  `PostalPostCode` varchar(20) DEFAULT NULL,
  `PhoneNumber1TypeID` int unsigned DEFAULT '2',
  `PhoneNumber1` varchar(32) DEFAULT NULL,
  `PhoneNumber2TypeID` int unsigned DEFAULT '3',
  `PhoneNumber2` varchar(32) DEFAULT NULL,
  `PhoneNumber3TypeID` int unsigned DEFAULT '4',
  `PhoneNumber3` varchar(32) DEFAULT NULL,
  `PhoneNumber4TypeID` int unsigned DEFAULT '10',
  `PhoneNumber4` varchar(32) DEFAULT NULL,
  `PhoneNumber5TypeID` int unsigned DEFAULT '1',
  `PhoneNumber5` varchar(32) DEFAULT NULL,
  `PrimaryEmail` varchar(255) DEFAULT NULL,
  `SecondaryEmail` varchar(255) DEFAULT NULL,
  `ParentOfficeID` int unsigned DEFAULT '1',
  `LocationOfficeID` int unsigned DEFAULT '1',
  `OldCourSesectionID` int unsigned DEFAULT '4',
  `OldCourseRegionID` int unsigned DEFAULT '8',
  `PrimaryContactID` int unsigned DEFAULT '0',
  `SecondaryContactID` int unsigned DEFAULT '0',
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MFRIOffices`
--

LOCK TABLES `MFRIOffices` WRITE;
/*!40000 ALTER TABLE `MFRIOffices` DISABLE KEYS */;
INSERT INTO `MFRIOffices` VALUES (1,0,'Not Specified','NA','4301960',0,0,0,0,0,'','',NULL,NULL,NULL,0,1,NULL,NULL,NULL,'MD',NULL,NULL,NULL,NULL,'MD',NULL,2,NULL,3,NULL,4,NULL,10,NULL,1,NULL,NULL,NULL,1,1,4,8,0,0,1,NULL,'2021-09-28 21:45:35',NULL,'0000-00-00 00:00:00'),(2,0,'Special Programs','SPS','2945530',0,1,0,1,0,'','','','','',0,1,'','','','MD','','','','','MD','',2,'301-226-9940',3,'',4,'301-314-0692',10,'',1,'','specialprog@mfri.org','',3,4,1,7,0,0,NULL,NULL,'2021-09-30 19:17:03',NULL,'2020-08-28 02:57:49'),(3,0,'Operations','FO','4301960',0,1,0,0,0,'','','','','',0,1,'','','','MD','','','','','MD','',2,'301-226-9971',3,'',4,'301-314-0752',10,'',1,'','fieldops@mfri.org','',14,4,2,7,0,0,NULL,NULL,'2021-09-30 19:16:10',NULL,'2021-09-16 18:50:44'),(4,0,'Headquarters','HQ','4301960',0,0,0,0,0,'','',NULL,NULL,NULL,0,1,'University of Maryland','4500 Campus Drive','College Park','MD','20742','','','','MD','',2,'800-275-6374',10,'800-ASK-MFRI',3,'301-226-9900',4,'301-314-0686',1,'','info@mfri.org','',1,4,4,7,0,0,NULL,NULL,'2021-09-28 21:45:35',NULL,'2020-05-20 00:26:49'),(5,1,'Western Maryland','WMRTC','4301960',0,0,1,0,0,'','','','','',0,1,'13928 Hazmat Dr. SW','','Cresaptown','MD','21502','P.O. Box 5153','','Cresaptown','MD','21502-5153',2,'888-691-6143',3,'301-729-0431',4,'301-729-6146',10,'',1,'','wmcontact@mfri.org','',18,5,2,1,0,0,NULL,NULL,'2021-09-30 19:19:28',NULL,'2021-02-25 21:31:59'),(6,2,'North Central','NCRTC','4301960',0,0,1,0,0,'','','','Fall, 2021 Classes are currently a work in progress. Classes will be released to the schedule as host facilities confirm those with us. Course locations may be adjusted as necessary based on current COVID related restrictions','',0,1,'1008 Twin Arch Rd','','Mount Airy','MD','21771-0196','PO Box 196','','Mount Airy','MD','21771-0196',2,'800-287-6374',3,'301-829-2020',4,'301-829-2021',10,'',1,'','nccontact@mfri.org','',18,6,2,2,0,0,NULL,NULL,'2021-09-30 19:18:18',NULL,'2021-02-25 21:32:12'),(7,3,'North East','NERTC','4301960',0,0,1,0,0,'','','','','',0,1,'9258 Lauderick Creek Road','Aberdeen Proving Ground/Edgewood Area','Gunpowder','MD','21010','PO Box 789','','Edgewood','MD','21040',2,'888-317-2218',3,'410-676-5409',3,'410-676-5362',4,'410-676-5413',1,'','necontact@mfri.org','nertc@mfri.org',18,7,2,3,0,0,NULL,NULL,'2021-09-30 19:18:28',NULL,'2021-02-25 21:32:23'),(8,4,'Upper Eastern Shore','UESRTC','4301960',0,0,1,0,0,'','','','','',0,1,'601 Safety Drive','','Centreville','MD','21617','','','','MD','',2,'888-692-0055',3,'410-758-2112',4,'410-758-3573',10,'',1,'','uescontact@mfri.org','',18,8,2,4,0,0,NULL,NULL,'2021-09-30 19:19:15',NULL,'2021-09-13 14:41:59'),(9,5,'Lower Eastern Shore','LESRTC','4301960',0,0,1,0,0,'','','','','',0,1,'12148 John Wilson Lane','','Princess Anne','MD','21853-3648','','','','MD','',2,'888-691-8880',3,'410-749-0313',4,'410-651-3356',3,'410-651-3331',1,'','lescontact@mfri.org','',18,9,2,5,0,0,NULL,NULL,'2021-09-30 19:17:58',NULL,'2021-02-25 21:32:49'),(10,6,'Southern Maryland','SMRTC','4301960',0,0,1,0,0,'','','','','',0,1,'10375 Audie Lane','','LaPlata','MD','20646','','','','MD','',2,'888-691-4628',3,'301-934-2600',4,'301-934-4333',11,'301-870-2095',1,'','smcontact@mfri.org','smrtc@mfri.org',18,10,2,6,0,0,NULL,NULL,'2021-09-30 19:18:37',NULL,'2021-02-25 21:33:00'),(11,0,'Advanced Life Support','ALS','4301960',0,1,1,1,0,'','','','','',0,0,'','','','MD','','','','','MD','',2,'301-226-9917',3,'1-800-275-6374',4,'301-314-0752',10,'',1,'','als@mfri.org','',18,4,5,7,0,0,NULL,NULL,'2021-09-30 19:17:46',NULL,'2020-08-28 03:15:11'),(12,0,'Finance & Administration','ADS','4301960',0,1,0,0,0,'','',NULL,NULL,NULL,0,1,'','','','','','','','','','',2,'301-226-9900',3,'',4,'301-314-0686',1,'',1,'','adminsvc@mfri.org','',14,4,6,7,NULL,NULL,NULL,NULL,'2021-09-28 21:45:35',NULL,'2020-05-05 16:46:00'),(13,0,'Logistical Support Services','LSS','4301960',0,1,0,0,0,'','','','','',0,0,'','','','','','','','','','',2,'301-226-9985',3,'',4,'301-314-9876',1,'',1,'','logsupport@mfri.org','',14,4,7,7,NULL,NULL,NULL,'','2021-09-28 22:02:56',NULL,'2013-08-29 22:01:32'),(14,0,'Director\'s Office','DIR','4301960',0,1,0,0,0,'','',NULL,NULL,NULL,0,1,'','','','','','','','','','',2,'301-226-9960',3,'',4,'301-314-1497',1,'',1,'','director@mfri.org','',NULL,4,8,7,NULL,NULL,NULL,'','2021-09-28 21:45:35','','2013-09-10 13:24:26'),(15,0,'Planning','IDS','4301960',0,1,0,0,0,'','',NULL,NULL,NULL,0,1,'','','','','','','','','','',2,'301-226-9934',3,'',4,'301-314-0752',1,'',1,'','instdev@mfri.org','',14,4,9,7,NULL,NULL,NULL,NULL,'2021-09-28 21:45:35',NULL,'2020-05-05 16:45:06'),(16,0,'Technology and Certification Services','TCS','4301960',0,1,0,0,0,'','','','','',0,1,'','','','','','','','','','',2,'301-226-9900',3,'',4,'301-314-0686',3,'',3,'','','',18,4,2,7,NULL,NULL,NULL,NULL,'2021-09-30 19:19:03',NULL,'2013-08-29 21:59:34'),(17,0,'Quality Assurance & Quality Improvement','QAQI','',0,1,0,1,0,'','',NULL,NULL,NULL,0,1,'','','','','','','','','','',1,'',1,'',1,'',1,'',1,'','','',14,4,4,8,0,0,1,NULL,'2021-09-28 21:45:35',NULL,'2020-05-05 16:47:11'),(18,0,'State Programs','STP','',1,1,0,1,0,'','','','<h4>NOTICE</h4>\r\n<p>\r\nDue to the restrictions set as a result of the COVID 19 pandemic, all MFRI class sessions that are lectures will be conducted via Zoom through the University Canvas system. Courses that are entirely lecture programs will be conducted entirely via Zoom. However, students may be required to personally attend the first session at the advertised location for final registration requirements, orientation and to receive class materials. In addition any class that has written testing shall meet at the class location by direction of the instructor or appropriate MFRI office.\r\n</p>\r\n<p>\r\nIn addition, in all cases where classes will meet at the course location, students will be subject to wellness checks, social distancing and workgroups of 10 or less.\r\n</p>','',0,1,'','','','','','','','','','',1,'',1,'',1,'',1,'',1,'','','',3,4,4,8,0,0,1,NULL,'2021-09-30 19:16:29',NULL,'2021-09-16 18:51:02'),(19,NULL,'Simulation Center','sim','',0,1,0,1,0,'','',NULL,NULL,NULL,0,1,'','','','','','','','','','',12,'301-226-9900',9,'',9,'',9,'',9,'','','',14,4,4,8,0,0,1,NULL,'2021-09-28 21:45:35',NULL,'2020-06-18 19:21:32'),(20,NULL,'Maryland Instructor Certification Review Board','MICRB','',0,0,0,1,0,'','','','','',0,1,'','','','','','','','','','',7,'301-226-9962',1,'',1,'',1,'',1,'','micrb@mfri.org','',14,4,4,8,0,0,1,NULL,'2021-09-28 21:45:35',NULL,'2020-12-10 20:23:53');
/*!40000 ALTER TABLE `MFRIOffices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ScheduledCourseStatus`
--

DROP TABLE IF EXISTS `ScheduledCourseStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ScheduledCourseStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ScheduledCourseStatus`
--

LOCK TABLES `ScheduledCourseStatus` WRITE;
/*!40000 ALTER TABLE `ScheduledCourseStatus` DISABLE KEYS */;
INSERT INTO `ScheduledCourseStatus` VALUES (1,'Not Scheduled'),(2,'Course Requested'),(3,'Course Confirmed'),(4,'Closed'),(5,'Full'),(6,'Cancelled'),(7,'Duplicate'),(8,'Needs Review'),(9,'Error'),(10,'Provisional'),(11,'Manager Approval'),(12,'Not Approved Needs Correction'),(13,'Not Approved Cancelled'),(14,'Not Approved');
/*!40000 ALTER TABLE `ScheduledCourseStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LinkStatus`
--

DROP TABLE IF EXISTS `LinkStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LinkStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LinkStatus`
--

LOCK TABLES `LinkStatus` WRITE;
/*!40000 ALTER TABLE `LinkStatus` DISABLE KEYS */;
INSERT INTO `LinkStatus` VALUES (1,'Ok'),(2,'Broken'),(3,'Temporarily Removed'),(4,'Deleted');
/*!40000 ALTER TABLE `LinkStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LinkTypes`
--

DROP TABLE IF EXISTS `LinkTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LinkTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LinkTypes`
--

LOCK TABLES `LinkTypes` WRITE;
/*!40000 ALTER TABLE `LinkTypes` DISABLE KEYS */;
INSERT INTO `LinkTypes` VALUES (1,'Web Page'),(2,'Email Link'),(3,'HTML'),(4,'PDF'),(5,'Word Doc'),(6,'Excell File'),(7,'WordPerfect Doc'),(8,'Text File'),(9,'JPEG'),(10,'GIF'),(11,'TIFF'),(12,'Powerpoint'),(13,'PNG'),(14,'RTF');
/*!40000 ALTER TABLE `LinkTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Links`
--

DROP TABLE IF EXISTS `Links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Links` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  `URL` text NOT NULL,
  `LinkTypeID` int unsigned DEFAULT NULL,
  `LinkStatusID` int unsigned DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=1050 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Links`
--

LOCK TABLES `Links` WRITE;
/*!40000 ALTER TABLE `Links` DISABLE KEYS */;
INSERT INTO `Links` VALUES (1018,'Firefighter I (PILOT)','/seminarpdf/20200601FirefighterIPILOT.pdf',4,1,'tsweeting','2020-04-10 23:05:44','tsweeting','2020-04-10 23:05:44');
/*!40000 ALTER TABLE `Links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ScheduleTypes`
--

DROP TABLE IF EXISTS `ScheduleTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ScheduleTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  `is_available` tinyint(1) NOT NULL DEFAULT '1',
  `schedule_defaults` varchar(765) DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ScheduleTypes`
--

LOCK TABLES `ScheduleTypes` WRITE;
/*!40000 ALTER TABLE `ScheduleTypes` DISABLE KEYS */;
INSERT INTO `ScheduleTypes` VALUES (1,'Per Class',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [],}'),(2,'Day',1,'{\'sessions_per_week_days\': 2,\'sessions_per_weekend\': 2,\'use_consecutive_days\': True,\'is_all_day\': True,\'hours\': [{\'start_time\': \'08:00:00\',\'end_time\': \'15:00:00\',},],}'),(3,'Night',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [{\'start_time\': \'19:00:00\',\'end_time\': \'22:00:00\',},],}'),(4,'Seminar',0,''),(5,'Site Specific',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [],}'),(6,'Cadet',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 0,\'use_consecutive_days\': True,\'is_all_day\': True,\'hours\': [{\'start_time\': \'11:00:00\',\'end_time\': \'15:00:00\',},],}'),(7,'Reg. Restricted',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [],}'),(8,'Weekend',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': True,\'is_all_day\': True,\'hours\': [{\'start_time\': \'19:00:00\',\'end_time\': \'22:00:00\',},{\'start_time\': \'08:00:00\',\'end_time\': \'15:00:00\',},],}'),(9,'Academy',1,'{\'sessions_per_week_days\': 2,\'sessions_per_weekend\': 0,\'use_consecutive_days\': True,\'is_all_day\': True,\'hours\': [{\'start_time\': \'08:00:00\',\'end_time\': \'15:00:00\',},],}'),(10,'Equivalency',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [],}'),(11,'Online',1,'{\'sessions_per_week_days\': 1,\'sessions_per_weekend\': 2,\'use_consecutive_days\': False,\'is_all_day\': False,\'hours\': [],}');
/*!40000 ALTER TABLE `ScheduleTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UMDTerms`
--

DROP TABLE IF EXISTS `UMDTerms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UMDTerms` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UMDTerms`
--

LOCK TABLES `UMDTerms` WRITE;
/*!40000 ALTER TABLE `UMDTerms` DISABLE KEYS */;
INSERT INTO `UMDTerms` VALUES (1,'Spring','1'),(2,'Summer 1','5'),(4,'Fall','8');
/*!40000 ALTER TABLE `UMDTerms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ScheduledCourses`
--

DROP TABLE IF EXISTS `ScheduledCourses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ScheduledCourses` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `CourseID` int unsigned DEFAULT NULL,
  `LocationID` int unsigned DEFAULT NULL,
  `InstructorID` int unsigned DEFAULT NULL,
  `OldInstructorID` int unsigned DEFAULT '0',
  `LogNumber` varchar(255) DEFAULT NULL,
  `MIEMSSLogNumber` varchar(255) DEFAULT '',
  `FundingSourceCode` varchar(10) DEFAULT '',
  `SectionNumber` char(3) DEFAULT '000',
  `FiscalYear` varchar(4) DEFAULT '0000',
  `RegOpenDate` datetime DEFAULT NULL,
  `RegClosedDate` datetime DEFAULT NULL,
  `StartDate` datetime DEFAULT NULL,
  `EndDate` datetime DEFAULT NULL,
  `RecurringDays` varchar(20) DEFAULT NULL,
  `MinStudents` int DEFAULT NULL,
  `MaxStudents` int DEFAULT NULL,
  `UseWaitList` int DEFAULT NULL,
  `UseWebRegister` int DEFAULT NULL,
  `RegisteredCount` int DEFAULT NULL,
  `DroppedCount` int DEFAULT NULL,
  `OutStateFee` decimal(8,2) DEFAULT '0.00',
  `InStateFee` decimal(8,2) DEFAULT '0.00',
  `RegionID` int unsigned DEFAULT NULL,
  `SectionID` int unsigned DEFAULT NULL,
  `ActivityCenterID` int unsigned DEFAULT '1',
  `MFRIOfficeID` int unsigned DEFAULT '1',
  `LinkID` int unsigned DEFAULT NULL,
  `TypeID` int unsigned DEFAULT '1',
  `ShowOnTranscript` int DEFAULT '1',
  `TranscriptNote` text,
  `NeedProgramEvaluations` int unsigned DEFAULT '1',
  `ProgramEvaluationNote` text,
  `CourseIsSeminar` int DEFAULT '0',
  `StatusID` int unsigned DEFAULT NULL,
  `ProgramStatusID` int unsigned DEFAULT '1',
  `RegistrationStatusID` int unsigned DEFAULT '1',
  `HostAgencyID` int unsigned DEFAULT '6',
  `JurisdictionID` int unsigned DEFAULT '30',
  `HostReservations` int DEFAULT '0',
  `HostRegistrations` int DEFAULT '0',
  `UseHostAgencyPriority` int DEFAULT '0',
  `UseJurisdictionPriority` int DEFAULT '0',
  `UseRegionPriority` int DEFAULT '0',
  `UseInStatePriority` int DEFAULT '1',
  `UseCertExpirationPriority` int DEFAULT '0',
  `SentToTranscript` datetime DEFAULT '0000-00-00 00:00:00',
  `SavedInTranscript` datetime DEFAULT '0000-00-00 00:00:00',
  `MarkAsDeleted` int DEFAULT '0',
  `TaskID` int unsigned DEFAULT '1',
  `Notes` text,
  `AlertMsg` varchar(255) DEFAULT NULL,
  `SpecialAlert` varchar(255) DEFAULT NULL,
  `RegistrationNote` varchar(255) DEFAULT '',
  `registration_alert_text` longtext,
  `registration_header_text` longtext,
  `registration_special_instructions_text` longtext,
  `registration_footer_text` longtext,
  `ResourceFee` decimal(8,2) DEFAULT '0.00',
  `NewBookFee` decimal(8,2) DEFAULT '0.00',
  `UsedBookFee` decimal(8,2) DEFAULT '0.00',
  `TCodeID` int unsigned DEFAULT '4',
  `TermID` int unsigned DEFAULT '1',
  `ShortLogNumber` varchar(255) DEFAULT NULL,
  `OwnerID` int unsigned DEFAULT '1',
  `ClientID` int unsigned DEFAULT '1',
  `require_payment` tinyint(1) NOT NULL DEFAULT '0',
  `require_epins` tinyint(1) DEFAULT '0',
  `require_mfri_student_number` tinyint(1) DEFAULT '0',
  `require_ssn` tinyint(1) DEFAULT '1',
  `require_nfasid` tinyint(1) DEFAULT '0',
  `require_birth_date` tinyint(1) DEFAULT '1',
  `require_emt_expiration_date` tinyint(1) DEFAULT '0',
  `require_address` tinyint(1) DEFAULT '1',
  `require_affiliation` tinyint(1) DEFAULT '1',
  `require_email_address` tinyint(1) DEFAULT '1',
  `require_primary_phone` tinyint(1) DEFAULT '1',
  `require_cell_phone` tinyint(1) DEFAULT '0',
  `require_training_officer_approval` tinyint(1) DEFAULT '0',
  `require_mfri_office_approval` tinyint(1) DEFAULT '0',
  `send_alert_email_to_office_before_approval` tinyint(1) DEFAULT '0',
  `send_alert_email_to_office_after_approval` tinyint(1) DEFAULT '0',
  `allow_late_registration` tinyint(1) NOT NULL DEFAULT '0',
  `OldCoordinatorID` int unsigned DEFAULT '0',
  `ClassFolderSentDate` datetime DEFAULT '0000-00-00 00:00:00',
  `ClassFolderSentID` int unsigned DEFAULT '3',
  `ClassFolderReceivedDate` datetime DEFAULT '0000-00-00 00:00:00',
  `ClassFolderReceivedID` int unsigned DEFAULT '3',
  `ClassFolderClosedDate` datetime DEFAULT '0000-00-00 00:00:00',
  `ClassFolderClosedID` int unsigned DEFAULT '3',
  `ClassFolderNote` text,
  `RegistrationMessage` text,
  `RegistrationEmailText` text,
  `additional_course_prerequisite` varchar(765) DEFAULT '',
  `other_registration_release_agency_name` varchar(255) DEFAULT '',
  `umd_canvas_lms_course_identifier` varchar(255) DEFAULT '',
  `umd_canvas_lms_course_name` varchar(255) DEFAULT '',
  `lms_course_identifier` varchar(255) DEFAULT '',
  `lms_course_name` varchar(255) DEFAULT '',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `naemt_course_number` varchar(765) DEFAULT '',
  PRIMARY KEY (`ID`),
  KEY `ID_index` (`ID`),
  KEY `CID_index` (`CourseID`)
) ENGINE=MyISAM AUTO_INCREMENT=41033 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ScheduledCourses`
--

LOCK TABLES `ScheduledCourses` WRITE;
/*!40000 ALTER TABLE `ScheduledCourses` DISABLE KEYS */;
INSERT INTO `ScheduledCourses` VALUES (26040,1799,2,2,0,NULL,'--','S','117','2015','2015-04-28 00:00:00','2015-05-15 00:00:00','2015-05-17 13:00:00','2015-05-17 16:00:00',',,,,,,Su',15,25,1,0,21,0,0.00,0.00,6,2,3,10,0,8,1,'',0,'',0,3,1,1,51,18,0,0,1,1,1,1,0,NULL,NULL,0,1,'Live Fire Training','Live Fire Training','','',NULL,NULL,NULL,NULL,0.00,0.00,0.00,4,2,'117',4902,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,'2015-06-11 13:25:29',70,'2015-06-11 12:29:40',38,'2015-06-18 09:25:13',38,NULL,'','','','','','','','','klayton','2021-10-25 17:27:43','dstevens','2015-04-28 12:59:04',''),(26041,52,6,2,0,NULL,'--','S','001','2015','2015-04-28 00:00:00','2016-05-30 00:00:00','2016-05-31 08:00:00','2016-05-31 11:00:00',',Tu,,,,,',15,30,1,1,0,0,0.00,0.00,4,2,3,3,NULL,11,0,'',0,'',0,9,1,1,6,30,0,0,0,0,0,1,0,NULL,NULL,0,1,'This class was scheduled to conduct testing on the Training Officer Portal part of the new online registration system.  This course has not been or will be published!','','','','','','','',0.00,0.00,0.00,4,2,'001',1,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,NULL,3,NULL,3,NULL,3,NULL,'','','','','','','','','klayton','2017-06-28 17:17:55','sbergin','2015-04-28 14:00:54',''),(26042,1485,6,2,0,NULL,'--','S','093','2015','2015-04-28 00:00:00','2017-12-13 00:00:00','2017-12-12 08:00:00','2017-12-13 15:00:00',',,,,,Sa,Su',1,10,1,1,0,0,0.00,0.00,4,2,3,3,0,2,1,'',0,'',0,6,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'This class was scheduled to conduct testing on the Training Officer Portal part of the new online registration system.  This course has not been or will be published!','','','','','','','',0.00,75.00,45.00,4,2,'093',1,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,NULL,'','','','','','','','','bgannon','2021-10-25 17:27:43','sbergin','2015-04-28 16:30:35',''),(26043,2295,184,5510,0,NULL,'--','S','088','2015','2020-08-28 00:00:00','2021-09-01 00:00:00','2021-09-01 08:00:00','2021-10-01 15:00:00',',Tu,,,,,',5,100,1,1,6,0,1.00,1.00,2,2,3,6,1018,2,0,'',0,'',0,3,1,1,6,30,0,0,0,0,0,1,0,NULL,NULL,0,1,'This class was scheduled to conduct testing on the Training Officer Portal part of the new online registration system.  This course has not been or will be published!','Registration Note goes here.','Alert Message goes here.','','','','','',0.00,52.50,34.50,4,2,'088',1,1,0,0,0,1,1,1,0,1,1,1,1,0,1,0,0,1,1,0,'2017-08-24 15:17:54',191,NULL,3,NULL,3,NULL,'','text for registration email receipt.','','','','','09dc088d-78f8-4655-b325-fb6817dd31ad','FIRE-101-S088-2015','tsweeting','2021-10-26 00:15:24','sbergin','2015-04-28 16:31:40',''),(26044,82,6,2,0,NULL,'--','S','092','2015','2015-04-28 00:00:00','2015-05-16 00:00:00','2015-06-05 08:00:00','2015-06-13 15:00:00',',,,,,Sa,Su',15,25,1,1,0,0,0.00,0.00,4,2,3,3,0,8,1,'',0,'',0,6,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'This class was scheduled to conduct testing on the Training Officer Portal part of the new online registration system.  This course has not been or will be published!','','','','','','','',0.00,84.96,64.97,4,2,'092',1,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,'2015-07-14 13:50:27',38,NULL,'','','','','','','','','klayton','2015-07-14 17:50:27','sbergin','2015-04-28 16:33:34',''),(26045,75,1,2,0,NULL,'--','E','056','2015','2015-04-28 00:00:00','2015-04-29 00:00:00','2015-02-16 08:00:00','2015-02-16 16:00:00','M,,,,,,',10,25,1,1,1,0,1090.00,1035.00,7,1,2,2,0,10,1,'',0,'No evaluations required for Equivalency Examinations',0,3,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'','','','',NULL,NULL,NULL,NULL,9.95,56.53,43.23,2,1,'056',4793,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,NULL,'','','','','','','','','jhart','2021-10-25 17:27:43','rdesper','2015-04-28 17:09:25',''),(26046,1763,185,2,0,NULL,'--','A','051','2015','2015-03-29 00:00:00','2015-04-23 00:00:00','2015-05-12 08:00:00','2015-05-22 15:00:00','M,Tu,W,Th,F,,',15,25,1,0,9,0,0.00,0.00,2,2,3,6,0,9,1,'',1,'',0,3,1,1,6,30,0,0,0,0,0,1,0,NULL,NULL,0,1,'','','','',NULL,NULL,NULL,NULL,0.00,50.58,38.68,4,2,'051',5465,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,'2015-07-13 10:16:06',144,'2015-07-14 12:00:10',38,'2015-07-16 13:38:54',38,NULL,'','','','','','','','','ksnyder','2021-10-25 17:27:43','ksnyder','2015-04-29 13:53:56',''),(26047,726,742,2,0,'003-16','','R','003','2016','2015-04-29 00:00:00','0000-00-00 00:00:00','2015-07-20 08:00:00','2015-07-21 16:00:00','M,Tu,,,,,',10,25,1,1,0,0,250.00,250.00,7,1,2,2,0,5,1,'',1,'',0,3,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'','','','',NULL,NULL,NULL,NULL,0.00,0.00,0.00,2,3,'003',1,2,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,NULL,'','','','','','','','','jhart','2021-11-08 02:08:09','rlogan','2015-04-29 20:00:31',''),(26048,199,273,2,0,NULL,'--','S','005','2015','2015-04-30 00:00:00','2015-06-22 00:00:00','2015-06-24 19:00:00','2015-07-11 22:00:00',',,W,,,Sa,',15,25,1,0,19,0,0.00,0.00,6,2,3,10,0,3,1,'',1,'',0,3,1,1,263,20,0,0,1,1,1,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'','','','',NULL,NULL,NULL,NULL,0.00,0.00,0.00,4,2,'005',4902,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,'2015-08-03 09:45:00',70,'2015-08-04 14:46:34',38,'0000-00-00 00:00:00',3,NULL,'','','','','','','','','dcornell','2021-10-25 17:27:43','dstevens','2015-04-30 12:39:05',''),(26049,104,374,2,0,NULL,'--','A','061','2015','2015-04-08 00:00:00','2015-04-09 00:00:00','2015-04-29 19:00:00','2015-05-03 22:00:00',',,W,,,,Su',15,25,1,0,21,0,0.00,0.00,2,2,3,6,0,9,1,'',1,'',0,3,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'','','','',NULL,NULL,NULL,NULL,0.00,48.88,0.00,4,1,'061',5465,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,'2015-05-27 14:30:31',144,'2015-06-02 16:01:52',38,'2015-06-07 18:17:02',38,NULL,'','','','','','','','','ksnyder','2021-10-25 17:27:43','kbonanno','2015-04-30 14:03:48',''),(26050,1404,1,2,0,NULL,'--','R','001','2016','2015-04-30 00:00:00','2015-08-05 00:00:00','2015-08-25 08:00:00','2015-08-25 16:00:00',',Tu,,,,,',10,25,1,1,13,0,0.00,0.00,7,1,2,2,0,5,1,'',1,'',0,3,1,1,6,30,0,0,0,0,0,1,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',0,1,'','','','',NULL,NULL,NULL,NULL,0.00,0.00,0.00,2,4,'001',4951,2,0,0,0,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,'0000-00-00 00:00:00',3,NULL,'','','','','','','','','rdesper','2021-11-08 02:08:09','rlogan','2015-04-30 14:52:01','');
/*!40000 ALTER TABLE `ScheduledCourses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PublicSchedulesStatus`
--

DROP TABLE IF EXISTS `PublicSchedulesStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PublicSchedulesStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Value` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PublicSchedulesStatus`
--

LOCK TABLES `PublicSchedulesStatus` WRITE;
/*!40000 ALTER TABLE `PublicSchedulesStatus` DISABLE KEYS */;
INSERT INTO `PublicSchedulesStatus` VALUES (1,'Ok'),(2,'Deleted'),(3,'Error');
/*!40000 ALTER TABLE `PublicSchedulesStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PublicSchedules`
--

DROP TABLE IF EXISTS `PublicSchedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PublicSchedules` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ShortName` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT '',
  `code_name` varchar(255) DEFAULT '',
  `Name` varchar(128) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT '',
  `Description` varchar(255) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT '',
  `SectionID` int unsigned DEFAULT '2',
  `ApproverID` int DEFAULT '4',
  `ContactID` int unsigned DEFAULT '4',
  `StatusID` int DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PublicSchedules`
--

LOCK TABLES `PublicSchedules` WRITE;
/*!40000 ALTER TABLE `PublicSchedules` DISABLE KEYS */;
INSERT INTO `PublicSchedules` VALUES (1,'None','none','None','Unspecified',3,4,2,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(2,'MDFS','mdfs','Courses for Maryland Emergency Services Personnel.','Courses for Maryland Fire Service Personnel.',2,4,4,1,NULL,'2020-06-09 00:33:21',NULL,'0000-00-00 00:00:00'),(3,'ALS','als','Advanced Life Support','Advanced Life Support Courses.',2,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(4,'Seminars','seminars','Seminars','Seminars and courses taught in a seminar format.',3,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(5,'Online','online','Online Courses','Courses taught via the Internet.',2,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(6,'GovInd','govind','Government and Industrial','Courses for Goverment and Private Industry.',1,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(7,'DoD','dod','Department of Defense','Courses for US Department of Defense Personnel.',1,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(8,'Meaney','meaney','Meaney Center','Courses for the George Meaney Center.',1,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(9,'NDLS','ndls','National Disaster Life Support','Maryland regional National Disaster Life Support coalition.',2,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00'),(10,'PDI','pdi','Professional Development for Instructors','MFRI Professional Development for Instructors',3,4,4,1,NULL,'2020-01-15 03:17:10',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `PublicSchedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PublicScheduleLink`
--

DROP TABLE IF EXISTS `PublicScheduleLink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PublicScheduleLink` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `PublicScheduleID` int unsigned DEFAULT '1',
  `ScheduledCourseID` int unsigned DEFAULT '1',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=39382 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PublicScheduleLink`
--

LOCK TABLES `PublicScheduleLink` WRITE;
/*!40000 ALTER TABLE `PublicScheduleLink` DISABLE KEYS */;
INSERT INTO `PublicScheduleLink` VALUES (24671,1,26046),(24660,2,26040),(24665,1,26041),(24666,1,26042),(24668,1,26044),(24669,1,26045),(24672,1,26047),(24673,2,26048),(24674,1,26049),(24675,1,26050),(38272,1,26043);
/*!40000 ALTER TABLE `PublicScheduleLink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InstructorPayRateFactors`
--

DROP TABLE IF EXISTS `InstructorPayRateFactors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `InstructorPayRateFactors` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Value` decimal(8,2) DEFAULT '1.00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InstructorPayRateFactors`
--

LOCK TABLES `InstructorPayRateFactors` WRITE;
/*!40000 ALTER TABLE `InstructorPayRateFactors` DISABLE KEYS */;
INSERT INTO `InstructorPayRateFactors` VALUES (1,1.00),(2,1.25),(3,1.50);
/*!40000 ALTER TABLE `InstructorPayRateFactors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InstructorPayRates`
--

DROP TABLE IF EXISTS `InstructorPayRates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `InstructorPayRates` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Value` decimal(8,2) DEFAULT '0.00',
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InstructorPayRates`
--

LOCK TABLES `InstructorPayRates` WRITE;
/*!40000 ALTER TABLE `InstructorPayRates` DISABLE KEYS */;
INSERT INTO `InstructorPayRates` VALUES (1,0.00,'Not Specified'),(2,14.00,'Inactive'),(3,16.00,'Inactive - Beginning (expired 7/1/14)'),(4,18.00,'Inactive - Beginning (expired 7/1/17)'),(5,22.00,'Inactive - 400 Hours (expired 7/1/14)'),(6,26.00,'Inactive - Instructor Trainer (expired 7/1/14)'),(8,21.00,'Exception'),(9,22.00,'Exception'),(10,25.00,'Exception'),(11,27.00,'Exception'),(12,19.00,'Exception'),(13,23.00,'Exception'),(14,24.00,'Inactive - 400 Hours (expired 7/1/17)'),(15,25.00,'Inactive - 400 Hours & 25+ Years (expired 7/1/17)'),(16,26.00,'Exception'),(17,29.00,'Exception'),(18,20.00,'Inactive - 200 Hours & Certified (expired 7/1/17)'),(19,16.00,'Exception'),(20,30.00,'Exception'),(21,28.00,'Inactive - Instructor Trainier (expired 7/1/17)'),(22,31.00,'Exception'),(23,32.00,'Exception'),(24,33.00,'Exception'),(25,24.00,'Exception'),(26,24.00,'Inactive - ALS Base (expired 7/1/17)'),(27,25.00,'Inactive - ALS Base & 25+ Years (expired 7/1/17)'),(28,28.00,'Exception'),(29,20.00,'Exception'),(30,35.00,'Exception'),(31,20.00,'Beginning'),(32,22.00,'200 Hours & Certified'),(33,26.00,'400 Hours'),(34,26.00,'ALS Base'),(35,27.00,'400 Hours & 25 Years'),(36,27.00,'ALS & 25 Years'),(37,30.00,'Instructor Trainier'),(38,40.00,'Exception'),(39,37.00,'Exception'),(40,17.00,'Exception');
/*!40000 ALTER TABLE `InstructorPayRates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmploymentStatus`
--

DROP TABLE IF EXISTS `EmploymentStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmploymentStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmploymentStatus`
--

LOCK TABLES `EmploymentStatus` WRITE;
/*!40000 ALTER TABLE `EmploymentStatus` DISABLE KEYS */;
INSERT INTO `EmploymentStatus` VALUES (1,'Not Specified'),(2,'Inactive'),(3,'Hourly'),(4,'Salary'),(5,'Inactive'),(6,'Suspended'),(7,'Separated');
/*!40000 ALTER TABLE `EmploymentStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PositionCategories`
--

DROP TABLE IF EXISTS `PositionCategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PositionCategories` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PositionCategories`
--

LOCK TABLES `PositionCategories` WRITE;
/*!40000 ALTER TABLE `PositionCategories` DISABLE KEYS */;
INSERT INTO `PositionCategories` VALUES (1,'Not Specified'),(2,'Faculty'),(3,'Staff'),(4,'Field Instructor'),(5,'Faculty / Instructor'),(6,'Staff / Instructor'),(7,'Student'),(8,'Honorarium'),(9,'Other or Consultant');
/*!40000 ALTER TABLE `PositionCategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MfriInstructors`
--

DROP TABLE IF EXISTS `MfriInstructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MfriInstructors` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `TitleID` int unsigned DEFAULT '1',
  `FirstName` varchar(255) DEFAULT NULL,
  `MiddleName` varchar(255) DEFAULT NULL,
  `LastName` varchar(255) DEFAULT NULL,
  `Suffix` varchar(255) DEFAULT NULL,
  `public_first_name` varchar(255) DEFAULT NULL,
  `public_middle_name` varchar(255) DEFAULT NULL,
  `public_last_name` varchar(255) DEFAULT NULL,
  `public_suffix` varchar(255) DEFAULT NULL,
  `use_public_name` tinyint(1) NOT NULL DEFAULT '0',
  `NickName` varchar(255) DEFAULT NULL,
  `ShowNickName` int DEFAULT '0',
  `ShowName` int DEFAULT '1',
  `internal_name_note` varchar(765) DEFAULT '',
  `show_name_as_is` tinyint(1) NOT NULL DEFAULT '1',
  `no_bulletin_email` tinyint(1) NOT NULL DEFAULT '0',
  `no_marketing_email` tinyint(1) NOT NULL DEFAULT '0',
  `SSN` varchar(255) DEFAULT NULL,
  `UniversityIDNumber` blob,
  `BirthDate` date DEFAULT '0000-00-00',
  `MedicalExamRequired` int DEFAULT '0',
  `no_medical_exam_suspended` tinyint(1) NOT NULL DEFAULT '0',
  `StateProviderNumber` blob,
  `DriversLicenseNumber` blob,
  `DriversLicenseState` varchar(255) DEFAULT 'MD',
  `DriversLicenseCommercial` int DEFAULT '0',
  `DriversLicenseClass` varchar(255) DEFAULT '',
  `DriversLicenseEndorsement` varchar(255) DEFAULT '',
  `DriversLicenseRestriction` varchar(255) DEFAULT '',
  `DriversLicensePoints` blob,
  `DriversLicenseTypeID` varchar(255) DEFAULT NULL,
  `DriversLicenseExpirationDate` date DEFAULT '0000-00-00',
  `PassportNumber` varchar(255) DEFAULT NULL,
  `PassportExpirationDate` date DEFAULT '0000-00-00',
  `CountyID` int unsigned DEFAULT '30',
  `ShowCountyID` int DEFAULT '0',
  `Address1` varchar(255) DEFAULT NULL,
  `Address2` varchar(255) DEFAULT NULL,
  `ShowAddress` int DEFAULT '0',
  `City` varchar(255) DEFAULT NULL,
  `ShowCity` int DEFAULT '0',
  `State` varchar(255) DEFAULT NULL,
  `ShowState` int DEFAULT '0',
  `PostCode` varchar(32) DEFAULT NULL,
  `ShowPostCode` int DEFAULT '0',
  `Country` varchar(255) DEFAULT NULL,
  `ShowCountry` int DEFAULT '0',
  `PrimaryPhoneNumberTypeID` int unsigned DEFAULT '2',
  `PrimaryPhoneNumber` varchar(32) DEFAULT NULL,
  `ShowPrimaryPhoneNumber` int DEFAULT '0',
  `SecondaryPhoneNumberTypeID` int unsigned DEFAULT '3',
  `SecondaryPhoneNumber` varchar(32) DEFAULT NULL,
  `ShowSecondaryPhoneNumber` int DEFAULT '0',
  `Alternate1PhoneNumberTypeID` int unsigned DEFAULT '1',
  `Alternate1PhoneNumber` varchar(32) DEFAULT NULL,
  `ShowAlternate1PhoneNumber` int DEFAULT '0',
  `Alternate2PhoneNumberTypeID` int unsigned DEFAULT '1',
  `Alternate2PhoneNumber` varchar(32) DEFAULT NULL,
  `Alternate3PhoneNumberTypeID` int unsigned DEFAULT '1',
  `Alternate3PhoneNumber` varchar(32) DEFAULT NULL,
  `Alternate4PhoneNumberTypeID` int unsigned DEFAULT '1',
  `Alternate4PhoneNumber` varchar(32) DEFAULT NULL,
  `ShowAlternate4PhoneNumber` int DEFAULT '0',
  `ShowAlternate3PhoneNumber` int DEFAULT '0',
  `ShowAlternate2PhoneNumber` int DEFAULT '0',
  `mfri_primary_phone_number` varchar(96) DEFAULT NULL,
  `mfri_secondary_phone_number` varchar(96) DEFAULT NULL,
  `show_mfri_primary_phone_number` tinyint(1) NOT NULL DEFAULT '1',
  `show_mfri_secondary_phone_number` tinyint(1) NOT NULL DEFAULT '1',
  `mfri_email` varchar(765) DEFAULT '',
  `umd_directory` varchar(765) DEFAULT '',
  `umd_email` varchar(765) DEFAULT '',
  `PrimaryEmail` varchar(255) DEFAULT NULL,
  `ShowPrimaryEmail` int DEFAULT '0',
  `SecondaryEmail` varchar(255) DEFAULT NULL,
  `AlternateAddress1` varchar(255) DEFAULT NULL,
  `AlternateAddress2` varchar(255) DEFAULT NULL,
  `ShowAlternateAddress` int DEFAULT '0',
  `AlternateCity` varchar(255) DEFAULT NULL,
  `ShowAlternateCity` int DEFAULT '0',
  `AlternateState` varchar(255) DEFAULT NULL,
  `ShowAlternateState` int DEFAULT '0',
  `AlternatePostCode` varchar(32) DEFAULT NULL,
  `AlternateCountry` varchar(255) DEFAULT NULL,
  `ShowSecondaryEmail` int DEFAULT '0',
  `HomeOfficeID` int unsigned DEFAULT '1',
  `DirectSupervisorID` int unsigned DEFAULT '1',
  `ShowHomeOfficeID` int DEFAULT '1',
  `EmploymentStatusID` int unsigned DEFAULT '1',
  `PositionCategoryID` int unsigned DEFAULT '4',
  `IsInstructor` int DEFAULT '0',
  `HireDate` date DEFAULT '0000-00-00',
  `AdjustedServiceDate` date DEFAULT '0000-00-00',
  `SeparationDate` date DEFAULT '0000-00-00',
  `LastPhysicalExamID` int unsigned DEFAULT '0',
  `LastPhysicalExamDate` date DEFAULT '0000-00-00',
  `HourlyRate` decimal(8,2) DEFAULT '0.00',
  `HourlyRateID` int unsigned DEFAULT '1',
  `HourlyRateFactorID` int unsigned DEFAULT '1',
  `leave_balance` decimal(6,2) NOT NULL DEFAULT '0.00',
  `FacultyAnnualLeave` float DEFAULT '0',
  `FacultySickLeave` float DEFAULT '0',
  `FacultyPersonalLeave` float DEFAULT '0',
  `FacultyMilitaryLeave` float DEFAULT '0',
  `FacultyNonPaidLeave` float DEFAULT '0',
  `FacultyImmediateFamilySickLeave` float DEFAULT '0',
  `FacultyOfficialHolidayLeave` int DEFAULT '0',
  `EmploymentAcknowledgementDate` date DEFAULT '0000-00-00',
  `TotalInstructionalHours` int DEFAULT '0',
  `PDIHours` int DEFAULT '0',
  `PracticeTeaching1EvaluationDate` date DEFAULT '0000-00-00',
  `PracticeTeaching2EvaluationDate` date DEFAULT '0000-00-00',
  `InterimEvaluation1Date` date DEFAULT '0000-00-00',
  `InterimEvaluation2Date` date DEFAULT '0000-00-00',
  `RoutineEvaluationDate` date DEFAULT '0000-00-00',
  `InstructorTrainerDate` date DEFAULT '0000-00-00',
  `MICRBEvaluatorDate` date DEFAULT '0000-00-00',
  `MICRBCertificationDate` date DEFAULT '0000-00-00',
  `MicrbID` int unsigned DEFAULT '0',
  `umd_canvas_lms_user_name` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_account_password` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_account_identifier` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_name_created_date` date DEFAULT NULL,
  `lms_user_name` varchar(255) DEFAULT '',
  `lms_user_account_password` varchar(255) DEFAULT '',
  `lms_user_account_identifier` varchar(255) DEFAULT '',
  `lms_user_name_created_date` date DEFAULT NULL,
  `TotalOtherHours` int DEFAULT '0',
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6392 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MfriInstructors`
--

LOCK TABLES `MfriInstructors` WRITE;
/*!40000 ALTER TABLE `MfriInstructors` DISABLE KEYS */;
INSERT INTO `MfriInstructors` VALUES (5510,1,'Thomas','G','Sweeting','','','','','',0,'',0,1,'',1,0,0,NULL,_binary 'vZ}\�\�\\9�$�\�','1963-08-28',0,0,_binary '��\�<������(P�\�\�','','MD',0,'C','None','B','',NULL,'0000-00-00','7œ‚×îîˆ+n¹\'5J\Zhá','0000-00-00',18,1,'5803 Swarthmore Drive','',1,'Berwyn Heights',0,'MD',0,'20740',0,'USA',0,2,'3012269912',1,3,'',1,1,'',0,1,'',1,'',1,'',0,0,0,'301 226 9912','240 676 6083',1,0,'tsweeting@mfri.org','tgs','tgs@umd.edu','tsweeting@mfri.org',1,'','','',0,'',0,'',0,'','USA',1,13,17,1,3,4,1,'2000-01-04','0000-00-00','0000-00-00',0,'0000-00-00',0.00,32,1,1.15,0,0,0,0,0,0,0,'0000-00-00',276,0,'0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','2021-07-14',514,'','','',NULL,'tsweeting5510','Sweeting19630828','7349a865-363f-40be-8da3-c37aeaab72ea','2018-07-17',0,1,'tsweeting','2021-10-26 00:21:30','smoltz','2006-02-13 13:55:42'),(1,1,'MFRI','','Staff','',NULL,NULL,NULL,NULL,0,'',0,0,'',1,0,0,'!gÐÍ‡ŠúÀ­z„×',NULL,'0000-00-00',0,0,NULL,'','MD',0,'','','','',NULL,'0000-00-00',NULL,'0000-00-00',30,0,NULL,NULL,0,NULL,0,NULL,0,NULL,0,NULL,0,2,NULL,0,3,NULL,0,1,NULL,0,1,NULL,1,NULL,1,NULL,0,0,0,NULL,NULL,1,1,'','','',NULL,0,NULL,NULL,NULL,0,NULL,0,NULL,0,NULL,NULL,0,1,1,0,1,3,0,'0000-00-00','0000-00-00','0000-00-00',0,'0000-00-00',0.00,1,1,0.00,0,0,0,0,0,0,0,'0000-00-00',0,0,'0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00',0,'','','',NULL,'','','',NULL,0,2,'','2021-10-25 17:36:33',NULL,'0000-00-00 00:00:00'),(2,1,'MFRI','','Instructor','',NULL,NULL,NULL,NULL,0,'',0,0,'',1,0,0,'¯¶ºëMš˜–¥ø@ö',_binary '�\�A����̌\�ZbY\�\�','0000-00-00',0,0,NULL,'','MD',0,'','','','',NULL,'0000-00-00',NULL,'0000-00-00',30,0,NULL,NULL,0,NULL,0,NULL,0,NULL,0,NULL,0,2,NULL,0,3,NULL,0,1,NULL,0,1,NULL,1,NULL,1,NULL,0,0,0,NULL,NULL,1,1,'','','',NULL,0,NULL,NULL,NULL,0,NULL,0,NULL,0,NULL,NULL,0,1,1,0,1,4,1,'0000-00-00','0000-00-00','0000-00-00',0,'0000-00-00',0.00,1,1,0.00,0,0,0,0,0,0,0,'0000-00-00',0,0,'0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00',0,'','','',NULL,'','','',NULL,0,2,'','2021-10-26 00:21:22',NULL,'0000-00-00 00:00:00'),(3,1,'Academy',NULL,'Instructor',NULL,NULL,NULL,NULL,NULL,0,NULL,0,1,'',1,0,0,NULL,NULL,'0000-00-00',0,0,NULL,'','MD',0,'','','','',NULL,'0000-00-00',NULL,'0000-00-00',30,0,NULL,NULL,0,NULL,0,NULL,0,NULL,0,NULL,0,2,NULL,0,3,NULL,0,1,NULL,0,1,NULL,1,NULL,1,NULL,0,0,0,NULL,NULL,1,1,'','','',NULL,0,NULL,NULL,NULL,0,NULL,0,NULL,0,NULL,NULL,0,1,1,1,1,4,1,'0000-00-00','0000-00-00','0000-00-00',0,'0000-00-00',0.00,1,1,0.00,0,0,0,0,0,0,0,'0000-00-00',0,0,'0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00','0000-00-00',0,'','','',NULL,'','','',NULL,0,2,NULL,'2021-10-25 17:36:33',NULL,'0000-00-00 00:00:00'),(11,1,'Joseph','','Blog','','','','','',0,'fuzzy',1,1,'',1,0,0,NULL,_binary '�d!g����\�$�ͷ�','1969-07-20',0,0,_binary '��\�<������(P�\�\�','','MD',0,'','','','',NULL,NULL,'7œ‚×îîˆ+n¹\'5J\Zhá',NULL,18,1,'4500 Paint Branch Parkway','',1,'College Park',1,'MD',1,'20742',1,'USA',0,2,'301 226 9912',1,3,'',1,1,'',0,1,'',1,'',1,'',0,0,0,NULL,NULL,1,1,'itcoord@mfri.org','','','itcoord@mfri.org',1,'','','',0,'',0,'MD',0,'','USA',1,9,1,1,3,4,0,'2000-01-01',NULL,NULL,0,NULL,0.00,5,1,0.00,0,0,0,0,0,0,0,'2000-01-01',0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'','','',NULL,'','','',NULL,0,2,'tsweeting','2021-10-26 00:21:30','tsweeting','2012-08-02 15:35:30');
/*!40000 ALTER TABLE `MfriInstructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FlagPreferences`
--

DROP TABLE IF EXISTS `FlagPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FlagPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `ReadPermission` int DEFAULT '1',
  `WritePermission` int DEFAULT '0',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FlagPreferences`
--

LOCK TABLES `FlagPreferences` WRITE;
/*!40000 ALTER TABLE `FlagPreferences` DISABLE KEYS */;
INSERT INTO `FlagPreferences` VALUES (1,2,1,1,1,1,NULL,'2006-12-01 16:10:16',NULL,'0000-00-00 00:00:00'),(2,42,1,1,0,0,NULL,'2007-04-23 18:34:23',NULL,'0000-00-00 00:00:00'),(3,107,1,1,0,0,NULL,'2007-05-02 16:29:57',NULL,'0000-00-00 00:00:00'),(4,130,1,0,0,0,NULL,'2007-07-13 17:09:16',NULL,'0000-00-00 00:00:00'),(5,133,1,1,0,0,NULL,'2007-09-06 12:38:39',NULL,'0000-00-00 00:00:00'),(6,70,1,1,0,0,NULL,'2008-09-25 14:24:19',NULL,'0000-00-00 00:00:00'),(7,63,1,1,0,0,NULL,'2009-05-11 18:31:43',NULL,'0000-00-00 00:00:00'),(8,144,1,1,0,0,NULL,'2009-10-12 15:59:14',NULL,'0000-00-00 00:00:00'),(9,94,1,1,0,0,NULL,'2009-11-17 23:33:21',NULL,'0000-00-00 00:00:00'),(10,47,1,1,0,0,NULL,'2009-11-17 23:33:32',NULL,'0000-00-00 00:00:00'),(11,55,1,1,0,0,NULL,'2010-07-06 18:33:45',NULL,'0000-00-00 00:00:00'),(12,81,1,1,0,0,NULL,'2010-07-06 18:33:56',NULL,'0000-00-00 00:00:00'),(13,64,1,1,0,0,NULL,'2010-07-06 18:34:05',NULL,'0000-00-00 00:00:00'),(14,57,1,1,0,0,NULL,'2010-07-06 18:34:15',NULL,'0000-00-00 00:00:00'),(15,127,1,1,0,0,NULL,'2010-07-06 18:34:52',NULL,'0000-00-00 00:00:00'),(16,59,1,1,0,0,NULL,'2010-07-06 18:35:03',NULL,'0000-00-00 00:00:00'),(17,41,1,1,0,0,NULL,'2010-07-06 18:35:32',NULL,'0000-00-00 00:00:00'),(18,100,1,1,0,0,NULL,'2011-02-17 16:21:51',NULL,'0000-00-00 00:00:00'),(19,150,1,1,0,0,NULL,'2011-09-15 22:32:29',NULL,'0000-00-00 00:00:00'),(20,152,1,1,0,0,NULL,'2012-02-14 18:51:19',NULL,'0000-00-00 00:00:00'),(21,153,1,1,0,0,NULL,'2012-02-23 15:24:30',NULL,'0000-00-00 00:00:00'),(22,154,1,1,0,0,NULL,'2012-04-30 21:55:14',NULL,'0000-00-00 00:00:00'),(23,155,1,1,0,0,NULL,'2012-06-13 15:33:33',NULL,'0000-00-00 00:00:00'),(24,157,1,1,0,0,NULL,'2012-07-27 18:58:36',NULL,'0000-00-00 00:00:00'),(25,156,1,1,0,0,NULL,'2012-08-17 19:20:14',NULL,'0000-00-00 00:00:00'),(26,158,1,1,0,0,NULL,'2012-12-10 20:51:40',NULL,'0000-00-00 00:00:00'),(27,160,1,1,0,0,NULL,'2013-01-03 15:14:15',NULL,'0000-00-00 00:00:00'),(28,161,1,1,0,0,NULL,'2013-02-11 16:30:41',NULL,'0000-00-00 00:00:00'),(29,169,1,1,0,0,NULL,'2014-04-07 15:48:17',NULL,'0000-00-00 00:00:00'),(30,173,1,1,0,0,NULL,'2014-08-06 22:01:33',NULL,'0000-00-00 00:00:00'),(31,178,1,1,0,0,NULL,'2014-10-29 18:55:42',NULL,'0000-00-00 00:00:00'),(32,179,1,1,0,0,NULL,'2014-11-11 16:16:33',NULL,'0000-00-00 00:00:00'),(33,183,1,1,0,0,NULL,'2015-02-18 18:12:47',NULL,'0000-00-00 00:00:00'),(34,184,1,1,0,0,NULL,'2015-07-28 21:38:04',NULL,'0000-00-00 00:00:00'),(35,185,1,1,0,0,NULL,'2015-09-17 14:13:17',NULL,'0000-00-00 00:00:00'),(36,186,1,1,0,0,NULL,'2016-01-25 00:01:07',NULL,'0000-00-00 00:00:00'),(37,195,1,1,0,0,NULL,'2017-01-23 17:45:05',NULL,'0000-00-00 00:00:00'),(38,200,1,1,0,0,NULL,'2017-08-07 15:07:07',NULL,'0000-00-00 00:00:00'),(39,201,1,1,0,0,NULL,'2017-08-28 15:04:05',NULL,'0000-00-00 00:00:00'),(40,204,1,1,0,0,NULL,'2017-11-09 15:08:07',NULL,'0000-00-00 00:00:00'),(41,211,1,1,0,0,NULL,'2018-10-12 15:18:18',NULL,'0000-00-00 00:00:00'),(42,212,1,1,0,0,NULL,'2018-11-13 18:45:58',NULL,'0000-00-00 00:00:00'),(43,213,1,1,0,0,NULL,'2018-11-19 21:03:16',NULL,'0000-00-00 00:00:00'),(44,205,1,1,0,0,NULL,'2018-12-03 15:46:15',NULL,'0000-00-00 00:00:00'),(45,216,1,1,0,0,NULL,'2019-05-07 18:06:50',NULL,'0000-00-00 00:00:00'),(46,218,1,1,0,0,NULL,'2019-06-27 17:37:00',NULL,'0000-00-00 00:00:00'),(47,221,1,1,0,0,NULL,'2019-09-30 14:41:56',NULL,'0000-00-00 00:00:00'),(48,88,1,1,0,0,NULL,'2019-11-22 19:44:05',NULL,'0000-00-00 00:00:00'),(49,225,1,1,0,0,NULL,'2020-07-17 18:40:43',NULL,'0000-00-00 00:00:00'),(50,231,1,1,0,0,NULL,'2021-04-02 19:15:46',NULL,'0000-00-00 00:00:00'),(51,232,1,1,0,0,NULL,'2021-05-03 21:21:36',NULL,'0000-00-00 00:00:00'),(52,233,1,1,0,0,NULL,'2021-05-03 22:05:08',NULL,'0000-00-00 00:00:00'),(53,235,1,1,0,0,NULL,'2021-09-15 18:51:46',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `FlagPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FlagStatus`
--

DROP TABLE IF EXISTS `FlagStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FlagStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FlagStatus`
--

LOCK TABLES `FlagStatus` WRITE;
/*!40000 ALTER TABLE `FlagStatus` DISABLE KEYS */;
INSERT INTO `FlagStatus` VALUES (1,'Current'),(2,'Retired');
/*!40000 ALTER TABLE `FlagStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FlagTypes`
--

DROP TABLE IF EXISTS `FlagTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FlagTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FlagTypes`
--

LOCK TABLES `FlagTypes` WRITE;
/*!40000 ALTER TABLE `FlagTypes` DISABLE KEYS */;
INSERT INTO `FlagTypes` VALUES (1,'Not Specified'),(2,'No Show'),(3,'Discipline'),(4,'Incomplete'),(5,'Fee'),(6,'Attendance');
/*!40000 ALTER TABLE `FlagTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentRecordFlags`
--

DROP TABLE IF EXISTS `StudentRecordFlags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentRecordFlags` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT '',
  `Note` text,
  `TypeID` int unsigned DEFAULT '1',
  `StatusID` int unsigned DEFAULT '1',
  `initial_duration_months` int DEFAULT '6',
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentRecordFlags`
--

LOCK TABLES `StudentRecordFlags` WRITE;
/*!40000 ALTER TABLE `StudentRecordFlags` DISABLE KEYS */;
INSERT INTO `StudentRecordFlags` VALUES (1,'None','Not Specified',1,1,6,1,NULL,'2006-12-01 20:06:04',NULL,'0000-00-00 00:00:00'),(2,'Course No Show','Failed to appear for first day of course',2,1,6,1,'tsweeting','2012-09-18 15:20:29',NULL,'0000-00-00 00:00:00'),(3,'Owes Book Fee','Failed to return or pay for text book',5,1,0,1,'tsweeting','2016-10-18 21:13:26',NULL,'0000-00-00 00:00:00'),(4,'Suspended','Suspended from course registration or attendance',3,1,6,1,'tsweeting','2012-09-18 15:22:13',NULL,'0000-00-00 00:00:00'),(5,'Drop','Repeated drops',6,1,6,1,'tsweeting','2012-09-18 15:21:51','tsweeting','2007-04-13 23:56:01');
/*!40000 ALTER TABLE `StudentRecordFlags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFlagAssignments`
--

DROP TABLE IF EXISTS `StudentFlagAssignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFlagAssignments` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '1',
  `FlagID` int unsigned DEFAULT '1',
  `ExpirationDate` date DEFAULT '0000-00-00',
  `AssignmentDate` date DEFAULT '0000-00-00',
  `Note` text,
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10329 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFlagAssignments`
--

LOCK TABLES `StudentFlagAssignments` WRITE;
/*!40000 ALTER TABLE `StudentFlagAssignments` DISABLE KEYS */;
INSERT INTO `StudentFlagAssignments` VALUES (10245,103029,3,'0000-00-00','2021-08-10','',1,'tsweeting','2021-08-10 14:36:14','tsweeting','2021-08-10 14:36:14'),(10246,126554,3,'0000-00-00','2021-08-10','',1,'tsweeting','2021-08-10 14:37:26','tsweeting','2021-08-10 14:37:26');
/*!40000 ALTER TABLE `StudentFlagAssignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFlagStatus`
--

DROP TABLE IF EXISTS `StudentFlagStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFlagStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFlagStatus`
--

LOCK TABLES `StudentFlagStatus` WRITE;
/*!40000 ALTER TABLE `StudentFlagStatus` DISABLE KEYS */;
INSERT INTO `StudentFlagStatus` VALUES (1,'No Flags'),(2,'Flagged'),(3,'Suspended'),(4,'Contact Region'),(5,'Medical Clearance');
/*!40000 ALTER TABLE `StudentFlagStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentsBilled`
--

DROP TABLE IF EXISTS `StudentsBilled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentsBilled` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `LastName` varchar(255) DEFAULT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `MiddleName` varchar(255) DEFAULT NULL,
  `Suffix` varchar(255) DEFAULT NULL,
  `SSN` blob,
  `Address1` varchar(255) DEFAULT NULL,
  `Address2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `PostCode` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `RecordStatusID` int unsigned DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=18314 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentsBilled`
--

LOCK TABLES `StudentsBilled` WRITE;
/*!40000 ALTER TABLE `StudentsBilled` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentsBilled` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MFRIStudentNumberLookup`
--

DROP TABLE IF EXISTS `MFRIStudentNumberLookup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MFRIStudentNumberLookup` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `mfri_student_number` varchar(255) DEFAULT NULL,
  `ssn` blob,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=95951 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MFRIStudentNumberLookup`
--

LOCK TABLES `MFRIStudentNumberLookup` WRITE;
/*!40000 ALTER TABLE `MFRIStudentNumberLookup` DISABLE KEYS */;
INSERT INTO `MFRIStudentNumberLookup` VALUES (74887,'10777073',_binary '\����\�c��L�E','','2021-07-11 00:50:42','','2021-07-11 00:50:42'),(76788,'10796596',_binary 'Պ\�ț�ms�A�NA','','2021-07-11 00:54:31','','2021-07-11 00:54:31'),(77615,'10805244',_binary '\�\��CT\�SK\�L','','2021-07-11 00:56:12','','2021-07-11 00:56:12'),(79620,'10826217',_binary 'v(\�1�]tӴ��!H[s6','','2021-07-11 01:00:29','','2021-07-11 01:00:29'),(79621,'10826226',_binary '�tih\�,�\�ٮU��\�','','2021-07-11 01:00:29','','2021-07-11 01:00:29'),(80871,'10838947',_binary '��$gu��Bs;U','','2021-07-11 01:03:10','','2021-07-11 01:03:10'),(91641,'10950767',_binary 'z�\\zw�4wj\�BP^','','2021-07-11 01:27:51','','2021-07-11 01:27:51'),(94333,'10979901',_binary '\�\�\�\�Ԟm#\�&��','','2021-07-11 01:34:44','','2021-07-11 01:34:44'),(95180,'10988442',_binary 'X[%n�\�\�\�B�\�w','','2021-07-12 09:38:24','','2021-07-12 09:38:24'),(95477,'10950767',_binary '5T:�+_\�?Y��W�)','','2021-08-12 19:12:05','','2021-08-12 19:12:05');
/*!40000 ALTER TABLE `MFRIStudentNumberLookup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentRecords`
--

DROP TABLE IF EXISTS `StudentRecords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentRecords` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `TitleID` int unsigned DEFAULT '1',
  `LastName` varchar(255) DEFAULT '',
  `FirstName` varchar(255) DEFAULT '',
  `MiddleName` varchar(255) DEFAULT '',
  `Suffix` varchar(255) DEFAULT '',
  `show_name_as_is` tinyint(1) NOT NULL DEFAULT '0',
  `AffiliationID` int unsigned DEFAULT '6',
  `IDNumber` blob,
  `SSN` blob,
  `UniversityIDNumber` blob,
  `StateProviderNumber` blob,
  `nfa_sid_number` blob,
  `mfri_student_number` varchar(255) DEFAULT '',
  `old_mfri_student_number` varchar(255) DEFAULT '',
  `AffiliatedCompanyNumber` varchar(255) DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `GenderID` int unsigned DEFAULT NULL,
  `RaceID` int unsigned DEFAULT NULL,
  `hispanic` tinyint(1) DEFAULT '0',
  `GradeLevelID` int unsigned DEFAULT NULL,
  `CollegeLevelID` int unsigned DEFAULT NULL,
  `CountyID` int unsigned DEFAULT '30',
  `Address1` varchar(255) DEFAULT NULL,
  `Address2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `PostCode` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT '',
  `PrimaryPhoneNumber` varchar(255) DEFAULT NULL,
  `PrimaryPhoneNumberTypeID` varchar(255) DEFAULT '1',
  `SecondaryPhoneNumber` varchar(255) DEFAULT NULL,
  `SecondaryPhoneNumberTypeID` varchar(255) DEFAULT '1',
  `Email` varchar(255) DEFAULT NULL,
  `PrimaryEmail` varchar(255) DEFAULT NULL,
  `SecondaryEmail` varchar(255) DEFAULT NULL,
  `StatusID` int unsigned DEFAULT NULL,
  `Note` text,
  `ADAFlag` int DEFAULT '0',
  `NoShowFlag` int DEFAULT '0',
  `no_bulletin_email` tinyint(1) NOT NULL DEFAULT '0',
  `StudentStatusID` int unsigned DEFAULT '1',
  `RecordStatusID` int unsigned DEFAULT '1',
  `CertificationExpirationDate` date DEFAULT NULL,
  `umd_canvas_lms_user_name` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_account_password` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_account_identifier` varchar(255) DEFAULT '',
  `umd_canvas_lms_user_name_created_date` date DEFAULT NULL,
  `lms_user_name` varchar(255) DEFAULT '',
  `lms_user_account_password` varchar(255) DEFAULT '',
  `lms_user_account_identifier` varchar(255) DEFAULT '',
  `lms_user_name_created_date` date DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`),
  KEY `BirthDate_index` (`BirthDate`)
) ENGINE=MyISAM AUTO_INCREMENT=128517 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentRecords`
--

LOCK TABLES `StudentRecords` WRITE;
/*!40000 ALTER TABLE `StudentRecords` DISABLE KEYS */;
INSERT INTO `StudentRecords` VALUES (103029,1,'Schnoodle','Gerban','','',0,6,_binary '\�\�^\���\�Z\�\�(�-\�',_binary '\�\�^\���\�Z\�\�(�-\�',_binary '��\�<������(P�\�\�',_binary '��\�<������(P�\�\�',_binary '7��\�\�\�+n�\'5J\Zh\�','10777073','gschnoodle103029','','2003-03-01',NULL,NULL,0,NULL,NULL,30,'4500 Paint Branch Parkway','','College Park','md','20742','USA','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,'This is a note.',0,0,0,5,1,NULL,'','','',NULL,'gschnoodle103029','Schnoodle19780301','a1d7d0e0-93ad-4762-8a8c-dd576bb60588','2019-10-08','tgs','2021-10-25 21:20:32','tgs','2016-03-14 22:42:24'),(105293,1,'Schnoodle','Gerban','','',0,492,_binary 'v�}�\�=\rl��N:��i',_binary 'v�}�\�=\rl��N:��i',_binary '��\�<������(P�\�\�',NULL,_binary '7��\�\�\�+n�\'5J\Zh\�','10796596','gschnoodle105293','000000','2002-01-01',NULL,NULL,0,NULL,NULL,30,'4500 Campus Drive','','College Park','MD','20740','USA','','2','','3','itdev@mfri.org','itdev@mfri.org','',9,'',0,0,1,5,1,NULL,'','','',NULL,'gschnoodle105293','Schnoodle19700101','486ed2c5-a8a5-4646-9644-1750c97aa966','2018-07-17','tgs','2021-10-25 21:20:32','\'tsweeting\'','2016-09-30 21:10:29'),(106361,1,'Augusti','Lovisa','','',0,20,_binary 'zo쩒�\���|�N\�ڧ',_binary 'zo쩒�\���|�N\�ڧ',_binary '��\�<������(P�\�\�',_binary '\�^#\�\�\���k9�\�\�	d',_binary '7��\�\�\�+n�\'5J\Zh\�','10805244','laugusti106361','020007','2016-09-23',NULL,NULL,0,NULL,NULL,30,'4500 Paint Branch Parkway','','College Park','MD','20740','USA','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,'',0,0,0,5,1,'0000-00-00','','','',NULL,'laugusti106361','Augusti20160923','d25adbe0-7a0f-4171-afff-02d459a36a58','2019-10-08','tsweeting','2021-10-26 00:11:56','tsweeting','2016-09-23 18:53:55'),(109306,1,'Villegas','Micaela','','',0,492,_binary '\�FB�\�\�\�\��I�l�M',_binary '\�FB�\�\�\�\��I�l�M',NULL,_binary '�\�\�B,%�\�\�\�Z\�\�x�',NULL,'10826217','mvillegas109306','110060',NULL,NULL,NULL,0,NULL,NULL,13,'4500 Paint Branch Parkway','','College Park','MD','20740','USA','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',19,NULL,0,0,0,5,1,NULL,'','','',NULL,'mvillegas109306','Villegas20170710','49898fa3-5768-442a-8c1d-38e1c7f3f4af','2017-07-26','sbergin','2021-10-25 21:20:32','\'tsweeting\'','2017-04-08 21:01:20'),(109316,1,'Loef','Euphrosyne','','',0,20,_binary 'B{*\Z\n\�1\�:g�2�',_binary 'B{*\Z\n\�1\�:g�2�',NULL,_binary '{\�^42h\�\�H\�9\�4�S',NULL,'10826226','eloef109316','000000','2021-10-25',NULL,NULL,0,NULL,NULL,30,'4500 Paint Branch Parkway','','College Park','MD','20740','USA','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',9,'',0,0,1,5,1,NULL,'','','',NULL,'eloef109316','Loef20170710','22c519be-82a4-49c0-978e-484f39562d63','2017-07-26','tsweeting','2021-10-26 00:09:08','\'tsweeting\'','2017-06-30 20:03:45'),(110790,1,'Greasespot','Philip','FAINTCRY','III',0,492,_binary '��i�\�˸-�[\\',_binary '��i�\�˸-�[\\',NULL,NULL,NULL,'10838947','pgreasespot110790','000000','1960-01-01',NULL,NULL,0,NULL,NULL,30,'4500 Campus Drive','','College Park','MD','20740','USA','1231231233','2','','3','mfritest02@gmail.com','mfritest02@gmail.com','',9,'',0,0,1,5,1,NULL,'','','',NULL,'pgreasespot110790','Greasespot19600101','f92d9281-977d-4637-ba27-2452bb959763','2017-07-26','tsweeting','2021-10-26 00:13:19','\'tsweeting\'','2017-07-06 16:35:25'),(126554,1,'Schnoodle','Gerban','','',0,492,_binary '��󐩡O\�N��X\��',_binary '��󐩡O\�N��X\��',NULL,NULL,'','10979901','','','1988-12-01',1,1,0,NULL,NULL,30,'4500 Campus Drive','','College Park','MD','20740','US','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,NULL,0,0,0,1,1,NULL,'','','',NULL,'','','',NULL,'tsweeting','2021-10-26 00:11:56','tgs','2021-04-18 02:23:34'),(126555,1,'Schnoodle','Gerban','','',0,492,_binary '4\'N\�\�%%\�̚*�ָ',_binary '4\'N\�\�%%\�̚*�ָ',NULL,NULL,'','10950767','','','1982-12-01',1,1,0,NULL,NULL,30,'4500 Campus Drive','','College Park','MD','20740','US','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,'',0,0,0,1,1,NULL,'','','',NULL,'','','',NULL,'tsweeting','2021-10-26 00:11:56','tgs','2021-04-18 02:50:28'),(127469,1,'Villegas','Micaela','','',0,20,_binary 'ţ\�P\�~�CN�|\����',_binary 'ţ\�P\�~�CN�|\����',NULL,_binary '�\�\�B,%�\�\�\�Z\�\�x�','','10988442','','',NULL,1,1,0,NULL,NULL,30,'4500 Paint Branch Parkway','','College Park','MD','20740','USA','1231231233','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,'',0,0,0,1,1,NULL,'','','',NULL,'','','',NULL,'tsweeting','2021-10-26 00:11:56','tgs','2021-07-12 09:38:12'),(128319,1,'Schnoodle','Gerban','','',0,6,_binary '4\'N\�\�%%\�̚*�ָ',_binary '4\'N\�\�%%\�̚*�ָ',NULL,NULL,'','10950767','','','1980-12-01',1,1,0,NULL,NULL,30,'','','Berwyn Heights','MD','20740','US','','2','','3','itdev@mfri.org','itdev@mfri.org','',NULL,'',0,0,0,1,1,NULL,'','','',NULL,'','','',NULL,'dsklodowski','2021-10-25 21:20:32','dsklodowski','2021-09-28 11:56:23');
/*!40000 ALTER TABLE `StudentRecords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RegistrationPriorityRules`
--

DROP TABLE IF EXISTS `RegistrationPriorityRules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RegistrationPriorityRules` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT '',
  `UserSelectable` int DEFAULT '0',
  `UseForCourse` varchar(255) DEFAULT '',
  `PriorityIncrement` int DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RegistrationPriorityRules`
--

LOCK TABLES `RegistrationPriorityRules` WRITE;
/*!40000 ALTER TABLE `RegistrationPriorityRules` DISABLE KEYS */;
INSERT INTO `RegistrationPriorityRules` VALUES (1,'Host Agency',1,'',3),(2,'Jurisdiction',1,'',1),(3,'In State',1,'',1),(4,'EMTB Expiration in 6 Months',0,'EMS-203',2),(5,'Student Flagged',0,'',-3),(6,'Region',1,'',1),(7,'Late Registration',0,'',-8);
/*!40000 ALTER TABLE `RegistrationPriorityRules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PreRegistrationStatus`
--

DROP TABLE IF EXISTS `PreRegistrationStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PreRegistrationStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `SortOrder` int DEFAULT '0',
  `Name` varchar(255) DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PreRegistrationStatus`
--

LOCK TABLES `PreRegistrationStatus` WRITE;
/*!40000 ALTER TABLE `PreRegistrationStatus` DISABLE KEYS */;
INSERT INTO `PreRegistrationStatus` VALUES (1,3,'Not Specified'),(2,2,'Pre-Registered'),(3,5,'Rejected'),(5,6,'No Show'),(6,4,'Pending'),(7,1,'Seated');
/*!40000 ALTER TABLE `PreRegistrationStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PreRegistrations`
--

DROP TABLE IF EXISTS `PreRegistrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PreRegistrations` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `StudentID` int unsigned NOT NULL DEFAULT '0',
  `ScheduledCourseID` int unsigned DEFAULT '0',
  `ApplicationTypeID` int unsigned DEFAULT '1',
  `LogNumber` varchar(255) DEFAULT NULL,
  `SponsorID` int unsigned DEFAULT '1',
  `IDNumber` blob,
  `SSN` blob,
  `BIDNumber` varchar(255) DEFAULT NULL,
  `StateProviderNumber` blob,
  `mfri_student_number` varchar(255) DEFAULT '',
  `nfa_sid_number` blob,
  `BProviderNumber` varchar(255) DEFAULT NULL,
  `AffiliatedCompanyNumber` varchar(255) DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `LegalQuestion1` int DEFAULT NULL,
  `LegalQuestion2` int DEFAULT NULL,
  `LegalQuestion3` int DEFAULT NULL,
  `TitleID` int unsigned DEFAULT '1',
  `FirstName` varchar(255) DEFAULT '',
  `MiddleName` varchar(255) DEFAULT '',
  `LastName` varchar(255) DEFAULT '',
  `Suffix` varchar(255) DEFAULT '',
  `Address1` varchar(255) DEFAULT '',
  `Address2` varchar(255) DEFAULT '',
  `Apt` varchar(255) DEFAULT '',
  `City` varchar(255) DEFAULT '',
  `State` char(2) DEFAULT '',
  `PostCode` varchar(20) DEFAULT '',
  `Country` varchar(255) DEFAULT '',
  `CountyID` int unsigned DEFAULT '30',
  `PrimaryPhoneNumber` varchar(32) DEFAULT '',
  `SecondaryPhoneNumber` varchar(32) DEFAULT '',
  `Email` varchar(255) DEFAULT '',
  `GenderID` int DEFAULT '1',
  `RaceID` int unsigned DEFAULT '1',
  `GradeLevelID` int unsigned DEFAULT '1',
  `CollegeLevelID` int unsigned DEFAULT '1',
  `Outcome` int DEFAULT NULL,
  `OutcomeTypeID` int unsigned DEFAULT '1',
  `OutcomeNum` int DEFAULT NULL,
  `PracticalExamMedical` int DEFAULT NULL,
  `PracticalExamMedicalRetest` int DEFAULT NULL,
  `PracticalExamTrauma` int DEFAULT NULL,
  `PracticalExamTraumaRetest` int DEFAULT NULL,
  `WrittenExamNumber` varchar(5) DEFAULT NULL,
  `FrontPage` datetime DEFAULT '0000-00-00 00:00:00',
  `BackPage` datetime DEFAULT '0000-00-00 00:00:00',
  `SynchedFront` datetime DEFAULT '0000-00-00 00:00:00',
  `SynchedBack` datetime DEFAULT '0000-00-00 00:00:00',
  `StatusID` int DEFAULT '0',
  `OldStatusID` int unsigned DEFAULT '1',
  `NoShowFlag` int DEFAULT '0',
  `StudentRegID` int unsigned DEFAULT '0',
  `is_web_reg` tinyint(1) NOT NULL DEFAULT '0',
  `is_late_registration` tinyint(1) NOT NULL DEFAULT '0',
  `owes_course_fee` tinyint(1) NOT NULL DEFAULT '0',
  `registration_approved_by` varchar(255) DEFAULT '',
  `registration_approved_by_username` varchar(255) DEFAULT '',
  `registration_approved_on` datetime DEFAULT NULL,
  `book_fee_acknowledged` tinyint(1) NOT NULL DEFAULT '0',
  `book_fee_agency_pay` tinyint(1) NOT NULL DEFAULT '0',
  `Priority` int DEFAULT '0',
  `AffiliationID` int unsigned DEFAULT '0',
  `MESSRDataReceived` int DEFAULT NULL,
  `CertificationExpirationDate` date DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=344822 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PreRegistrations`
--

LOCK TABLES `PreRegistrations` WRITE;
/*!40000 ALTER TABLE `PreRegistrations` DISABLE KEYS */;
INSERT INTO `PreRegistrations` VALUES (204451,0,24265,1,'EMS-204-S009-2015',1,NULL,_binary 'kF9�&�\�2�/s\n\�\�',NULL,_binary '4\�\�\�\�z��MLD[�\�','',NULL,NULL,'160000',NULL,NULL,NULL,NULL,1,'Gord','','Slusher','','4500 Paint Branch Parkway','','','College Park','MD','20740','',30,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',2,1,0,0,0,0,0,'','',NULL,0,0,1,335,0,'0000-00-00','mbilger','2021-10-25 21:20:03','mbilger','2015-04-28 18:49:56'),(222164,109316,26043,1,'FIRE-101-S088-2015',1,NULL,_binary 'B{*\Z\n\�1\�:g�2�',NULL,_binary '��\�<������(P�\�\�','',_binary '��\�<������(P�\�\�',NULL,'020007','2021-10-25',NULL,NULL,NULL,1,'Euphrosyne','','Loef','','4500 Paint Branch Parkway','',NULL,'College Park','MD','20740','',30,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508756,1,0,0,'Steve Race','AVFD01','2016-06-06 16:19:29',0,0,1,20,0,'0000-00-00','tsweeting','2021-10-26 00:13:39','tsweeting','2015-04-28 19:13:43'),(222165,106361,26043,1,'FIRE-101-S088-2015',1,NULL,_binary 'zo쩒�\���|�N\�ڧ',NULL,_binary '\�^#\�\�\���k9�\�\�	d','',NULL,NULL,'020007',NULL,NULL,NULL,NULL,1,'Lovisa','','Augusti','','4500 Paint Branch Parkway','','','College Park','MD','20740','USA',30,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508757,1,0,0,'Steve Race','AVFD01','2016-06-06 16:19:23',0,0,1,20,0,'0000-00-00','tsweeting','2021-10-26 00:13:39','tsweeting','2015-04-28 19:13:43'),(337787,127469,26043,1,'FIRE-101-S088-2015',1,NULL,_binary 'ţ\�P\�~�CN�|\����',NULL,_binary '�\�\�B,%�\�\�\�Z\�\�x�','10988442','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Micaela','','Villegas','','4500 Paint Branch Parkway','','','College Park','MD','20740','USA',3,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508760,1,0,0,'Steve Race','AVFD01','2016-06-06 16:16:50',0,0,1,20,NULL,NULL,'tgs','2021-10-26 00:13:40','tgs','2021-07-12 09:43:41'),(228951,110790,26043,1,NULL,1,NULL,_binary '��i�\�˸-�[\\',NULL,_binary '��\�<������(P�\�\�','',_binary '��\�<������(P�\�\�',NULL,NULL,'1960-01-01',NULL,NULL,NULL,1,'Philip','','Greasespot','','','',NULL,'','','','',30,'','','',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508761,0,0,0,'','',NULL,0,0,0,492,NULL,'0000-00-00','tsweeting','2021-10-26 00:13:40','tsweeting','2017-06-30 19:47:03'),(331982,126554,26043,1,'FIRE-101-S088-2015',1,NULL,_binary '��󐩡O\�N��X\��',NULL,_binary '��\�<������(P�\�\�','','',NULL,NULL,'1988-12-01',NULL,NULL,NULL,NULL,'Gerban','','Schnoodle','','4500 Campus Drive','','','College Park','MD','20740','US',13,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508758,0,0,0,NULL,NULL,NULL,0,0,1,492,NULL,NULL,'tgs','2021-10-26 00:13:39','tgs','2021-04-18 02:23:34'),(331983,126555,26043,1,'FIRE-101-S088-2015',1,NULL,_binary '4\'N\�\�%%\�̚*�ָ',NULL,NULL,'','',NULL,NULL,'1982-12-01',NULL,NULL,NULL,NULL,'Gerban','','Schnoodle','','4500 Campus Drive',NULL,'','College Park','MD','20740','US',13,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,508759,1,1,0,'Thomas G Sweeting','tgs','2021-04-17 22:49:26',1,0,1,492,NULL,NULL,'tgs','2021-10-26 00:13:39','tgs','2021-04-18 02:50:28'),(343465,128319,39949,1,'MGMT-202-S003-2022',1,NULL,_binary '4\'N\�\�%%\�̚*�ָ',NULL,NULL,'10950767','',NULL,NULL,'1980-12-01',NULL,NULL,NULL,NULL,'Gerban','','Schnoodle','','4500 Campus Drive',NULL,'','Berwyn Heights','MD','20740','US',13,'3012269912','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',2,1,0,NULL,1,0,0,'Chuck Gizzy','afd01','2021-09-27 17:32:22',1,0,2,492,NULL,NULL,'dsklodowski','2021-10-25 21:20:03','dsklodowski','2021-09-28 11:56:24'),(343233,109316,26386,1,'FIRE-101-S090-2015',1,NULL,_binary 'B{*\Z\n\�1\�:g�2�',NULL,_binary '{\�^42h\�\�H\�9\�4�S','','',NULL,NULL,NULL,NULL,NULL,NULL,1,'Euphrosyne','','LOEF','','4500 Paint Branch Parkway','','','College Park','MD','20740','',30,'1231231233','','mfritest01@yahoo.com',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,506846,0,0,0,NULL,NULL,NULL,0,0,1,492,NULL,NULL,'sbergin','2021-10-25 21:20:03','sbergin','2021-09-22 14:42:16'),(343234,105293,26386,1,'FIRE-101-S090-2015',1,NULL,_binary 'v�}�\�=\rl��N:��i',NULL,NULL,'','',NULL,NULL,'2010-01-01',NULL,NULL,NULL,1,'Gerban','','Schnoodle','','4500 Campus Drive','','','College Park','MD','20740','',30,'','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,506847,0,0,0,NULL,NULL,NULL,0,0,1,492,NULL,NULL,'sbergin','2021-10-25 21:20:03','sbergin','2021-09-22 14:42:16'),(343232,110790,26386,1,'FIRE-101-S090-2015',1,NULL,_binary '~8΀b\�\�D\�y�R�',NULL,NULL,'','',NULL,NULL,'1960-01-01',NULL,NULL,NULL,1,'Philip','FAINTCRY','Greasespot','III','4500 Campus Drive','','','College Park','MD','20740','',30,'1231231233','','mfritest02@gmail.com',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,506848,0,0,0,NULL,NULL,NULL,0,0,1,492,NULL,NULL,'sbergin','2021-10-25 21:20:03','sbergin','2021-09-22 14:42:16'),(343236,109306,26386,1,'FIRE-101-S090-2015',1,NULL,_binary '\�FB�\�\�\�\��I�l�M',NULL,_binary '�\�\�B,%�\�\�\�Z\�\�x�','','',NULL,NULL,NULL,NULL,NULL,NULL,1,'Micaela','','Villegas','','4500 Paint Branch Parkway','','','College Park','MD','20740','',13,'1231231233','','itdev@mfri.org',1,1,1,1,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',7,1,0,506849,0,0,0,NULL,NULL,NULL,0,0,1,492,NULL,NULL,'sbergin','2021-10-25 21:20:03','sbergin','2021-09-22 14:42:16');
/*!40000 ALTER TABLE `PreRegistrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFeeBatchesTypes`
--

DROP TABLE IF EXISTS `StudentFeeBatchesTypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFeeBatchesTypes` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFeeBatchesTypes`
--

LOCK TABLES `StudentFeeBatchesTypes` WRITE;
/*!40000 ALTER TABLE `StudentFeeBatchesTypes` DISABLE KEYS */;
INSERT INTO `StudentFeeBatchesTypes` VALUES (1,'Charges'),(2,'Address Information');
/*!40000 ALTER TABLE `StudentFeeBatchesTypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFeeErrors`
--

DROP TABLE IF EXISTS `StudentFeeErrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFeeErrors` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Value` varchar(255) DEFAULT NULL,
  `Level` int DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFeeErrors`
--

LOCK TABLES `StudentFeeErrors` WRITE;
/*!40000 ALTER TABLE `StudentFeeErrors` DISABLE KEYS */;
INSERT INTO `StudentFeeErrors` VALUES (1,'No Errors','',0),(2,'SSN','Error',2),(3,'Resource Fee','Error',2),(4,'Credit Amount','Error',2),(5,'Name','Error',2),(6,' Address 1','Error',2),(7,'Address 2','Error',2),(8,'No Street Address Given','Error',2),(9,'City','Error',2),(10,'State','Error',2),(11,'Zip Code','Error',2),(12,'Country','Warning',1),(13,'Primary Phone Number','Warning',1),(14,'Secondary Phone Number','Warning',1);
/*!40000 ALTER TABLE `StudentFeeErrors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFeesStatus`
--

DROP TABLE IF EXISTS `StudentFeesStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFeesStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFeesStatus`
--

LOCK TABLES `StudentFeesStatus` WRITE;
/*!40000 ALTER TABLE `StudentFeesStatus` DISABLE KEYS */;
INSERT INTO `StudentFeesStatus` VALUES (1,'New'),(2,'Sent to Accounting Office'),(3,'Sent to Bursar'),(4,'Paid'),(5,'Removed'),(6,'Locked by Accounts Payable'),(7,'Addresses Sent to Bursar');
/*!40000 ALTER TABLE `StudentFeesStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFeeBatches`
--

DROP TABLE IF EXISTS `StudentFeeBatches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFeeBatches` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ScheduledCourseID` int unsigned DEFAULT '0',
  `Description` varchar(255) DEFAULT NULL,
  `StatusID` int unsigned DEFAULT '1',
  `TypeID` int unsigned DEFAULT '1',
  `DateSentToAccounting` datetime DEFAULT '0000-00-00 00:00:00',
  `DateLockedByAccounting` datetime DEFAULT '0000-00-00 00:00:00',
  `DateSentToBursar` datetime DEFAULT '0000-00-00 00:00:00',
  `DatePidnSentToBursar` datetime DEFAULT '0000-00-00 00:00:00',
  `RecordStatusID` int unsigned DEFAULT '1',
  `ErrorID` int unsigned DEFAULT '1',
  `MaxAmountDue` decimal(8,2) DEFAULT '0.00',
  `TCodeID` int unsigned DEFAULT '4',
  `TermID` int unsigned DEFAULT '1',
  `ItemReference` varchar(255) DEFAULT NULL,
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`),
  KEY `STATID_index` (`StatusID`),
  KEY `SCHEDID_index` (`ScheduledCourseID`)
) ENGINE=MyISAM AUTO_INCREMENT=9166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFeeBatches`
--

LOCK TABLES `StudentFeeBatches` WRITE;
/*!40000 ALTER TABLE `StudentFeeBatches` DISABLE KEYS */;
/*!40000 ALTER TABLE `StudentFeeBatches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentFeesPreferences`
--

DROP TABLE IF EXISTS `StudentFeesPreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentFeesPreferences` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `UserID` int unsigned DEFAULT '0',
  `ReadPermission` int DEFAULT '1',
  `WritePermission` int DEFAULT '0',
  `AccountingReadPermission` int DEFAULT '1',
  `AccountingWritePermission` int DEFAULT '0',
  `SendToBursarPermission` int DEFAULT '0',
  `AdminReadPermission` int DEFAULT '0',
  `AdminWritePermission` int DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentFeesPreferences`
--

LOCK TABLES `StudentFeesPreferences` WRITE;
/*!40000 ALTER TABLE `StudentFeesPreferences` DISABLE KEYS */;
INSERT INTO `StudentFeesPreferences` VALUES (1,2,1,1,1,1,1,1,1,NULL,'2007-08-02 17:41:04',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `StudentFeesPreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentMethod`
--

DROP TABLE IF EXISTS `PaymentMethod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentMethod` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `PaymentTypeID` int unsigned DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  `ExpiryDate` datetime DEFAULT NULL,
  `StatusID` int unsigned DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentMethod`
--

LOCK TABLES `PaymentMethod` WRITE;
/*!40000 ALTER TABLE `PaymentMethod` DISABLE KEYS */;
INSERT INTO `PaymentMethod` VALUES (1,11,'None',NULL,NULL,5);
/*!40000 ALTER TABLE `PaymentMethod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentMethodStatus`
--

DROP TABLE IF EXISTS `PaymentMethodStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentMethodStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentMethodStatus`
--

LOCK TABLES `PaymentMethodStatus` WRITE;
/*!40000 ALTER TABLE `PaymentMethodStatus` DISABLE KEYS */;
INSERT INTO `PaymentMethodStatus` VALUES (1,'Good'),(2,'Bad'),(3,'Expired'),(4,'Error'),(5,'None');
/*!40000 ALTER TABLE `PaymentMethodStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentStatus`
--

DROP TABLE IF EXISTS `PaymentStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentStatus`
--

LOCK TABLES `PaymentStatus` WRITE;
/*!40000 ALTER TABLE `PaymentStatus` DISABLE KEYS */;
INSERT INTO `PaymentStatus` VALUES (1,'Pending'),(2,'Paid'),(3,'Cleared'),(4,'Error'),(5,'30 Days Past Due'),(6,'60 Days Past Due'),(7,'90 Days Past Due'),(8,'90+ Days Past Due'),(9,'None Pending');
/*!40000 ALTER TABLE `PaymentStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentType`
--

DROP TABLE IF EXISTS `PaymentType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentType` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentType`
--

LOCK TABLES `PaymentType` WRITE;
/*!40000 ALTER TABLE `PaymentType` DISABLE KEYS */;
INSERT INTO `PaymentType` VALUES (1,'Visa'),(2,'MasterCard'),(3,'American Express'),(4,'Diners Club'),(5,'Other'),(6,'Scholarship'),(7,'Cash'),(8,'Check'),(9,'Purchase Order'),(10,'No Charge'),(11,'None');
/*!40000 ALTER TABLE `PaymentType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RegistrationStatus`
--

DROP TABLE IF EXISTS `RegistrationStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RegistrationStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `SortOrder` int DEFAULT '0',
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RegistrationStatus`
--

LOCK TABLES `RegistrationStatus` WRITE;
/*!40000 ALTER TABLE `RegistrationStatus` DISABLE KEYS */;
INSERT INTO `RegistrationStatus` VALUES (1,2,'Pending'),(2,1,'New'),(3,6,'Registered'),(4,4,'Rejected'),(5,3,'Wait List'),(6,5,'Pre-Registered'),(7,9,'Dropped'),(8,7,'Unknown'),(9,7,'Completed Successfully'),(10,10,'Failed Midterm Exam'),(11,24,'Incomplete - Instructor Evaluation'),(12,23,'Incomplete - Other Course Requirement'),(13,22,'Incomplete - Attendance'),(14,20,'Incomplete - Work Schedule Conflict'),(15,19,'Incomplete - Department Activities Conflict'),(16,18,'Incomplete - Illness'),(17,17,'Incomplete - Attended Only To Start Class'),(18,16,'Incomplete - Other (See Note)'),(19,9,'Failed'),(20,21,'Incomplete - Home Activities Conflict'),(21,15,'Incomplete'),(22,8,'No Show'),(23,0,'Failed Practical Exam');
/*!40000 ALTER TABLE `RegistrationStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentGradeOptions`
--

DROP TABLE IF EXISTS `StudentGradeOptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentGradeOptions` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(32) DEFAULT NULL,
  `RecordStatusID` int unsigned DEFAULT '1',
  `is_passing` tinyint(1) DEFAULT '1',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentGradeOptions`
--

LOCK TABLES `StudentGradeOptions` WRITE;
/*!40000 ALTER TABLE `StudentGradeOptions` DISABLE KEYS */;
INSERT INTO `StudentGradeOptions` VALUES (1,'Unknown',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(2,'Passed',1,1,NULL,'2005-08-06 18:22:58',NULL,'0000-00-00 00:00:00'),(3,'Withdraw',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(4,'Drop',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(5,'Failed',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(6,'Incomplete',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(7,'Passed Retraining',1,1,NULL,'2005-08-06 18:22:58',NULL,'0000-00-00 00:00:00'),(8,'Discipline',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(9,'Cancelled',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(10,'3 Hours',1,1,NULL,'2006-11-01 20:09:45',NULL,'0000-00-00 00:00:00'),(11,'6 Hours',1,1,NULL,'2006-11-01 20:09:45',NULL,'0000-00-00 00:00:00'),(12,'Failed Practical',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(13,'Failed Midterm',1,0,NULL,'2016-04-18 21:01:46',NULL,'0000-00-00 00:00:00'),(14,'1.5 Hours',1,1,NULL,'2013-12-04 23:19:06',NULL,'0000-00-00 00:00:00'),(15,'9 Hours',1,1,NULL,'2014-04-09 14:38:07',NULL,'0000-00-00 00:00:00'),(16,'12 Hours',1,1,NULL,'2014-04-09 14:38:12',NULL,'0000-00-00 00:00:00'),(17,'5 Hours',1,1,NULL,'2014-04-10 15:42:06',NULL,'0000-00-00 00:00:00'),(18,'4 Hours',1,1,NULL,'2014-06-13 14:48:58',NULL,'0000-00-00 00:00:00'),(19,'4.5 Hours',1,1,NULL,'2015-04-28 17:50:58',NULL,'0000-00-00 00:00:00'),(20,'.75 Hours',1,1,NULL,'2016-04-08 14:31:33',NULL,'0000-00-00 00:00:00'),(21,'2 Hours',1,1,NULL,'2020-06-05 18:36:09',NULL,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `StudentGradeOptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentRegistration`
--

DROP TABLE IF EXISTS `StudentRegistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudentRegistration` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `StudentID` int unsigned DEFAULT '0',
  `UpdatedStudentRecordID` int DEFAULT '0',
  `ContactID` int unsigned DEFAULT '0',
  `SchedCourseID` int unsigned DEFAULT '0',
  `RegistrationStatusID` int unsigned DEFAULT '8',
  `RegistrationStatusNote` varchar(255) DEFAULT NULL,
  `PaymentDue` decimal(8,2) DEFAULT '0.00',
  `PaymentMethodID` int unsigned DEFAULT '1',
  `PaymentStatusID` int unsigned DEFAULT '9',
  `ResourceFee` decimal(8,2) DEFAULT '0.00',
  `HasBook` int DEFAULT '0',
  `has_resource` tinyint(1) DEFAULT '0',
  `PidnBatchID` int unsigned DEFAULT '0',
  `PidnSent` int DEFAULT '0',
  `UsedBook` int DEFAULT '0',
  `CreditAmount` decimal(8,2) DEFAULT '0.00',
  `InvoiceErrorID` int unsigned DEFAULT '1',
  `InvoiceErrorList` varchar(255) DEFAULT NULL,
  `InvoiceErrorLevel` int DEFAULT '0',
  `CreditBatchID` int unsigned DEFAULT '0',
  `InvoiceBatchID` int unsigned DEFAULT '0',
  `AffiliationID` int unsigned DEFAULT '6',
  `Grade` varchar(20) DEFAULT 'None',
  `GradeID` int unsigned DEFAULT '1',
  `GradeNote` varchar(80) DEFAULT '',
  `PercentageScore` varchar(10) DEFAULT '0%',
  `WebRegHoldID` int unsigned DEFAULT '0',
  `PreRegNumber` int DEFAULT '0',
  `PreRegPriority` int DEFAULT '0',
  `PreRegID` int unsigned DEFAULT '0',
  `MESSRHoldID` int unsigned DEFAULT '0',
  `MESSRDataReceived` int unsigned DEFAULT '0',
  `SentToTranscript` datetime DEFAULT '0000-00-00 00:00:00',
  `SavedInTranscript` datetime DEFAULT '0000-00-00 00:00:00',
  `StatusID` int unsigned DEFAULT '8',
  `StatusNote` varchar(255) DEFAULT '',
  `Note` varchar(255) DEFAULT '',
  `exam_results` longtext NOT NULL,
  `last_exam_mastery_report` longtext NOT NULL,
  `ok_to_email_grades` tinyint(1) NOT NULL DEFAULT '1',
  `application_type_id` int DEFAULT NULL,
  `application_level_id` int DEFAULT NULL,
  `evoc_vehicle_type_id` int DEFAULT NULL,
  `umd_canvas_lms_enrollment_identifier` varchar(255) DEFAULT '',
  `umd_canvas_lms_enrollment_date` date DEFAULT NULL,
  `lms_enrollment_identifier` varchar(255) DEFAULT '',
  `lms_enrollment_date` date DEFAULT NULL,
  `is_web_reg` tinyint(1) NOT NULL DEFAULT '0',
  `owes_course_fee` tinyint(1) NOT NULL DEFAULT '0',
  `registration_approved_by` varchar(255) DEFAULT '',
  `registration_approved_by_username` varchar(255) DEFAULT '',
  `registration_approved_on` datetime DEFAULT NULL,
  `book_fee_acknowledged` tinyint(1) NOT NULL DEFAULT '0',
  `book_fee_agency_pay` tinyint(1) NOT NULL DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`),
  KEY `SID_index` (`StudentID`),
  KEY `SCHEDID_index` (`SchedCourseID`),
  KEY `PBID_index` (`PidnBatchID`),
  KEY `CAID_index` (`CreditBatchID`),
  KEY `IBID_index` (`InvoiceBatchID`)
) ENGINE=MyISAM AUTO_INCREMENT=508762 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentRegistration`
--

LOCK TABLES `StudentRegistration` WRITE;
/*!40000 ALTER TABLE `StudentRegistration` DISABLE KEYS */;
INSERT INTO `StudentRegistration` VALUES (105293,53670,NULL,NULL,12659,6,NULL,0.00,1,9,0.00,0,0,NULL,0,0,0.00,1,NULL,0,NULL,NULL,457,'Passed',2,'','90',NULL,0,0,NULL,79018,1,'2009-02-03 08:56:54','2009-02-14 12:14:45',9,'','','','',1,2,1,NULL,'',NULL,'',NULL,0,0,'','',NULL,0,0,'klayton','2016-11-03 00:16:30','kclose','2009-01-16 19:48:39'),(109306,54954,NULL,NULL,12576,6,NULL,0.00,1,9,0.00,0,0,NULL,0,0,0.00,1,NULL,0,NULL,NULL,276,'Passed',2,'','72',NULL,0,0,NULL,82705,1,'2009-03-12 11:15:14','2009-03-16 12:30:04',9,'','','','',1,5,3,NULL,'',NULL,'',NULL,0,0,'','',NULL,0,0,'klayton','2016-11-03 00:16:30','kclose','2009-02-19 19:53:44'),(109316,54959,NULL,NULL,12796,6,NULL,0.00,1,9,0.00,0,0,NULL,0,0,0.00,1,NULL,0,NULL,NULL,62,'Passed',2,'','72',NULL,0,0,NULL,82715,1,'2009-06-24 12:32:10','2009-07-06 17:56:22',9,'','','','',1,1,1,NULL,'',NULL,'',NULL,0,0,'','',NULL,0,0,'klayton','2016-11-03 00:16:30','bgannon','2009-02-19 20:09:28'),(110790,55472,NULL,NULL,12706,6,NULL,0.00,1,9,0.00,0,0,NULL,0,0,0.00,1,NULL,0,NULL,NULL,355,'Passed',2,'','74',NULL,0,0,NULL,83764,1,'2009-05-07 08:38:36','2009-05-19 15:39:53',9,'','','','',1,6,1,NULL,'',NULL,'',NULL,0,0,'','',NULL,0,0,'klayton','2016-11-03 00:16:30','pcusic','2009-03-03 13:42:07'),(508761,110790,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,492,'Unknown',1,'','',0,0,0,228951,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,0,0,'','',NULL,0,0,'tsweeting','2021-10-26 00:13:40','tsweeting','2021-10-26 00:13:40'),(508760,127469,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,20,'Unknown',1,'','',0,0,1,337787,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,1,0,'Steve Race','AVFD01','2016-06-06 16:16:50',0,0,'tsweeting','2021-10-26 00:13:40','tsweeting','2021-10-26 00:13:40'),(508759,126555,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,492,'Unknown',1,'','',0,0,1,331983,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,1,0,'Thomas G Sweeting','tgs','2021-04-17 22:49:26',1,0,'tsweeting','2021-10-26 00:13:39','tsweeting','2021-10-26 00:13:39'),(508758,126554,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,492,'Unknown',1,'','',0,0,1,331982,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,0,0,NULL,NULL,NULL,0,0,'tsweeting','2021-10-26 00:13:39','tsweeting','2021-10-26 00:13:39'),(508757,106361,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,20,'Unknown',1,'','',0,0,1,222165,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,1,0,'Steve Race','AVFD01','2016-06-06 16:19:23',0,0,'tsweeting','2021-10-26 00:13:39','tsweeting','2021-10-26 00:13:39'),(508756,109316,0,0,26043,2,NULL,0.00,1,9,0.00,0,0,0,0,0,0.00,1,NULL,0,0,0,20,'Unknown',1,'','',0,0,1,222164,0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'','','','',1,NULL,NULL,NULL,'',NULL,'',NULL,1,0,'Steve Race','AVFD01','2016-06-06 16:19:29',0,0,'tsweeting','2021-10-26 00:13:39','tsweeting','2021-10-26 00:13:39');
/*!40000 ALTER TABLE `StudentRegistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WebRegHoldStatus`
--

DROP TABLE IF EXISTS `WebRegHoldStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `WebRegHoldStatus` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WebRegHoldStatus`
--

LOCK TABLES `WebRegHoldStatus` WRITE;
/*!40000 ALTER TABLE `WebRegHoldStatus` DISABLE KEYS */;
INSERT INTO `WebRegHoldStatus` VALUES (1,'Received'),(2,'Deleted'),(3,'Rejected'),(4,'Accepted'),(5,'Duplicate'),(6,'Error');
/*!40000 ALTER TABLE `WebRegHoldStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WebRegHold`
--

DROP TABLE IF EXISTS `WebRegHold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `WebRegHold` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `ScheduledCourseID` int unsigned DEFAULT '0',
  `Fee` decimal(8,2) DEFAULT '0.00',
  `InStateRate` int DEFAULT '1',
  `Priority` int DEFAULT '0',
  `AffiliationID` int unsigned DEFAULT '6',
  `Affiliation` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT '',
  `first_name` varchar(255) DEFAULT '',
  `middle_name` varchar(255) DEFAULT '',
  `last_name` varchar(255) DEFAULT '',
  `suffix` varchar(255) DEFAULT '',
  `IDNumber` blob,
  `StateProviderNumber` blob,
  `mfri_student_number` varchar(255) DEFAULT '',
  `nfa_sid_number` blob,
  `birth_date` date DEFAULT '0000-00-00',
  `emt_expiration_date` date DEFAULT '0000-00-00',
  `Address1` varchar(255) DEFAULT '',
  `Address2` varchar(255) DEFAULT '',
  `City` varchar(255) DEFAULT '',
  `State` varchar(255) DEFAULT '',
  `PostCode` varchar(32) DEFAULT '',
  `Country` varchar(255) DEFAULT '',
  `PrimaryPhoneNumber` varchar(32) DEFAULT '',
  `SecondaryPhoneNumber` varchar(32) DEFAULT '',
  `MobilePhoneNumber` varchar(32) DEFAULT '',
  `Email` varchar(255) DEFAULT '',
  `StatusID` int unsigned DEFAULT '4',
  `is_late_registration` tinyint(1) NOT NULL DEFAULT '0',
  `owes_course_fee` tinyint(1) NOT NULL DEFAULT '0',
  `book_fee_acknowledged` tinyint(1) NOT NULL DEFAULT '0',
  `is_approved` tinyint(1) DEFAULT '0',
  `has_been_reviewed` tinyint(1) DEFAULT '0',
  `approved_on` datetime DEFAULT '0000-00-00 00:00:00',
  `approved_by` varchar(255) DEFAULT NULL,
  `approved_by_username` varchar(80) DEFAULT NULL,
  `book_fee_agency_pay` tinyint(1) NOT NULL DEFAULT '0',
  `training_officer_note` longtext,
  `student_note` longtext,
  `registrar_note` longtext,
  `StudentRegID` int unsigned DEFAULT '0',
  `LastChangeBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `LastChange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CreatedBy` varchar(32) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `Created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=196272 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WebRegHold`
--

LOCK TABLES `WebRegHold` WRITE;
/*!40000 ALTER TABLE `WebRegHold` DISABLE KEYS */;
INSERT INTO `WebRegHold` VALUES (171360,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:55:41'),(171361,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:59:14'),(167956,38656,250.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',_binary 'T\�*��VaI#�lZ\�2=�','',_binary '~�\"��2K�S\�\�rq$\�z','2010-10-01',NULL,'4500 Campus Drive','','College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,1,'2020-10-01 16:38:16','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2020-10-01 20:37:59'),(171373,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:26:10'),(171372,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:25:08'),(171370,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:22:56'),(171369,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:22:55'),(171368,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:22:20'),(171367,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:22:19'),(171363,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:06:23'),(171362,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 20:00:57'),(171358,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:51:44'),(171352,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:32:23'),(171355,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:47:11'),(171356,26043,1.00,1,0,6,'MFRI Test','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1986-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-12 19:48:08'),(171428,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:21:35'),(171429,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:23:33'),(171430,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:27:43'),(171431,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:32:59'),(171432,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:42:00'),(171433,26043,1.00,1,0,6,'MFRI Test 821','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:44:26'),(171434,26043,1.00,1,0,6,'MFRI Test 850','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 01:50:55'),(171439,26043,1.00,1,0,6,'MFRI Test 850','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1992-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-13 03:23:32'),(171555,26043,1.00,1,0,6,'MFRI Test 912','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1991-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-15 02:12:55'),(171556,26043,1.00,1,0,6,'MFRI Test 915','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1991-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-15 02:13:52'),(171710,26043,1.00,1,0,6,'MFRI Test 500','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�d`b��.����P\"�\�',NULL,'',_binary '\�%\�HCxϐ\�\�r\�x ','1975-11-01',NULL,'4500 Campus Drive',NULL,'college park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-16 22:04:40'),(171711,26043,1.00,1,0,6,'MFRI Test 500','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�d`b��.����P\"�\�',NULL,'',_binary '\�%\�HCxϐ\�\�r\�x ','1975-11-01',NULL,'4500 Campus Drive',NULL,'college park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,1,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-16 22:20:04'),(171712,26043,1.00,1,0,6,'MFRI Test 500','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�d`b��.����P\"�\�',NULL,'',_binary '\�%\�HCxϐ\�\�r\�x ','1975-11-01',NULL,'4500 Campus Drive',NULL,'college park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,1,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-16 22:26:38'),(171713,26043,1.00,1,0,6,'MFRI Test 500','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�d`b��.����P\"�\�',NULL,'',_binary '\�%\�HCxϐ\�\�r\�x ','1975-11-01',NULL,'4500 Campus Drive',NULL,'college park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,1,0,0,0,NULL,'','',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-11-16 22:37:17'),(171722,26043,1.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1987-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,1,0,1,'2020-11-16 18:55:16','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2020-11-16 23:54:00'),(171820,26043,1.00,1,0,6,'MFRI Test 1157','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1985-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,1,'2020-11-17 22:58:05','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2020-11-17 16:58:03'),(171900,26043,1.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','2004-11-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,1,0,1,'2020-11-17 23:06:23','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2020-11-18 04:00:27'),(175133,26043,1.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',_binary '��\�<������(P�\�\�','',_binary '~�\"��2K�S\�\�rq$\�z','1982-12-01','0000-00-00','4500 Campus Drive','','College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,1,0,1,1,1,'2021-04-17 22:49:26','Thomas G Sweeting','tgs',0,'','','',NULL,'','2021-10-25 21:20:38','','2020-12-28 02:22:41'),(180665,39672,0.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'',_binary '~�\"��2K�S\�\�rq$\�z','1990-12-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','1231231233','','','itdev@mfri.org',1,0,0,0,0,1,'2021-03-02 15:50:44','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2021-03-02 20:50:30'),(194474,40258,0.00,1,0,763,'Commercial Ambulance Service','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�\�	Qp�p�J\�\�yK�',_binary '\�\�\�\�{6��\�\\�]�q�','',_binary '>{B��w�NW\�\�ї','1994-12-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','3012269912','','','itdev@mfri.org',1,0,0,0,0,1,'2021-09-16 10:55:55','Thomas G Sweeting','tgs',0,'','','Administratively not approved.',NULL,'','2021-10-25 21:20:38','','2021-09-16 14:54:42'),(194475,40258,0.00,1,0,784,'Unaffiliated','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '�\�	Qp�p�J\�\�yK�',_binary '\�\�\�\�{6��\�\\�]�q�','',_binary '>{B��w�NW\�\�ї','1994-12-01',NULL,'4500 Campus Drive',NULL,'College Park','MD','20740','US','3012269912','','','itdev@mfri.org',1,0,0,0,0,1,'2021-09-16 11:07:46','Jason Shorter','Unaffiliated_260005_01',0,'','','',NULL,'','2021-10-25 21:20:38','','2021-09-16 14:59:55'),(194956,39949,0.00,1,0,492,'Grantsville Volunteer Fire Department, Inc.','Gerban  Schnoodle','Gerban','','Schnoodle','',_binary '4\'N\�\�%%\�̚*�ָ',NULL,'10950767',_binary '~�\"��2K�S\�\�rq$\�z','1980-12-01',NULL,'4500 Campus Drive',NULL,'Berwyn Heights','MD','20740','US','3012269912','','','itdev@mfri.org',4,0,0,1,1,1,'2021-09-28 18:25:38','Chuck Gizzy','afd01',0,'','','',NULL,'','2021-10-25 21:20:38','','2021-09-27 21:27:18');
/*!40000 ALTER TABLE `WebRegHold` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-10 16:25:53
