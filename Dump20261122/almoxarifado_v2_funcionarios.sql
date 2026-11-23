-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: almoxarifado_v2
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionarios` (
  `id` int NOT NULL,
  `nome` varchar(120) NOT NULL,
  `setor` varchar(120) NOT NULL,
  `pode_retirar` tinyint(1) NOT NULL DEFAULT '1',
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `data_cadastro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `ck_funcionario_nome` CHECK ((char_length(trim(`nome`)) > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionarios`
--

LOCK TABLES `funcionarios` WRITE;
/*!40000 ALTER TABLE `funcionarios` DISABLE KEYS */;
INSERT INTO `funcionarios` VALUES (1,'Ana Silva','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(2,'Carlos Souza','Almoxarifado',1,1,'2026-11-22 17:56:47'),(3,'Maria Santos','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(4,'João Pereira','Financeiro',1,1,'2026-11-22 17:56:47'),(5,'Beatriz Costa','Logística',1,1,'2026-11-22 17:56:47'),(6,'Funcionario Teste 006','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(7,'Funcionario Teste 007','Almoxarifado',1,1,'2026-11-22 17:56:47'),(8,'Funcionario Teste 008','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(9,'Funcionario Teste 009','Financeiro',1,1,'2026-11-22 17:56:47'),(10,'Funcionario Teste 010','Logística',1,1,'2026-11-22 17:56:47'),(11,'Funcionario Teste 011','Administrativo',1,1,'2026-11-22 17:56:47'),(12,'Funcionario Teste 012','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(13,'Funcionario Teste 013','Almoxarifado',1,1,'2026-11-22 17:56:47'),(14,'Funcionario Teste 014','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(15,'Funcionario Teste 015','Financeiro',1,1,'2026-11-22 17:56:47'),(16,'Funcionario Teste 016','Logística',1,1,'2026-11-22 17:56:47'),(17,'Funcionario Teste 017','Administrativo',1,1,'2026-11-22 17:56:47'),(18,'Funcionario Teste 018','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(19,'Funcionario Teste 019','Almoxarifado',1,1,'2026-11-22 17:56:47'),(20,'Funcionario Teste 020','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(21,'Funcionario Teste 021','Financeiro',1,1,'2026-11-22 17:56:47'),(22,'Funcionario Teste 022','Logística',1,1,'2026-11-22 17:56:47'),(23,'Funcionario Teste 023','Administrativo',1,1,'2026-11-22 17:56:47'),(24,'Funcionario Teste 024','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(25,'Funcionario Teste 025','Almoxarifado',1,1,'2026-11-22 17:56:47'),(26,'Funcionario Teste 026','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(27,'Funcionario Teste 027','Financeiro',1,1,'2026-11-22 17:56:47'),(28,'Funcionario Teste 028','Logística',1,1,'2026-11-22 17:56:47'),(29,'Funcionario Teste 029','Administrativo',1,1,'2026-11-22 17:56:47'),(30,'Funcionario Teste 030','Tecnologia da Informação',1,1,'2026-11-22 17:56:47'),(31,'Funcionario Teste 031','Almoxarifado',1,1,'2026-11-22 17:56:47'),(32,'Funcionario Teste 032','Recursos Humanos',1,1,'2026-11-22 17:56:47'),(33,'Funcionario Teste 033','Financeiro',1,1,'2026-11-22 17:56:47'),(34,'Funcionario Teste 034','Logística',1,1,'2026-11-22 17:56:47'),(35,'Funcionario Teste 035','Administrativo',1,1,'2026-11-22 17:56:47'),(36,'Funcionario Teste 036','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(37,'Funcionario Teste 037','Almoxarifado',1,1,'2026-11-22 17:56:48'),(38,'Funcionario Teste 038','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(39,'Funcionario Teste 039','Financeiro',1,1,'2026-11-22 17:56:48'),(40,'Funcionario Teste 040','Logística',1,1,'2026-11-22 17:56:48'),(41,'Funcionario Teste 041','Administrativo',1,1,'2026-11-22 17:56:48'),(42,'Funcionario Teste 042','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(43,'Funcionario Teste 043','Almoxarifado',1,1,'2026-11-22 17:56:48'),(44,'Funcionario Teste 044','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(45,'Funcionario Teste 045','Financeiro',1,1,'2026-11-22 17:56:48'),(46,'Funcionario Teste 046','Logística',1,1,'2026-11-22 17:56:48'),(47,'Funcionario Teste 047','Administrativo',1,1,'2026-11-22 17:56:48'),(48,'Funcionario Teste 048','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(49,'Funcionario Teste 049','Almoxarifado',1,1,'2026-11-22 17:56:48'),(50,'Funcionario Teste 050','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(51,'Funcionario Teste 051','Financeiro',1,1,'2026-11-22 17:56:48'),(52,'Funcionario Teste 052','Logística',1,1,'2026-11-22 17:56:48'),(53,'Funcionario Teste 053','Administrativo',1,1,'2026-11-22 17:56:48'),(54,'Funcionario Teste 054','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(55,'Funcionario Teste 055','Almoxarifado',1,1,'2026-11-22 17:56:48'),(56,'Funcionario Teste 056','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(57,'Funcionario Teste 057','Financeiro',1,1,'2026-11-22 17:56:48'),(58,'Funcionario Teste 058','Logística',1,1,'2026-11-22 17:56:48'),(59,'Funcionario Teste 059','Administrativo',1,1,'2026-11-22 17:56:48'),(60,'Funcionario Teste 060','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(61,'Funcionario Teste 061','Almoxarifado',1,1,'2026-11-22 17:56:48'),(62,'Funcionario Teste 062','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(63,'Funcionario Teste 063','Financeiro',1,1,'2026-11-22 17:56:48'),(64,'Funcionario Teste 064','Logística',1,1,'2026-11-22 17:56:48'),(65,'Funcionario Teste 065','Administrativo',1,1,'2026-11-22 17:56:48'),(66,'Funcionario Teste 066','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(67,'Funcionario Teste 067','Almoxarifado',1,1,'2026-11-22 17:56:48'),(68,'Funcionario Teste 068','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(69,'Funcionario Teste 069','Financeiro',1,1,'2026-11-22 17:56:48'),(70,'Funcionario Teste 070','Logística',1,1,'2026-11-22 17:56:48'),(71,'Funcionario Teste 071','Administrativo',1,1,'2026-11-22 17:56:48'),(72,'Funcionario Teste 072','Tecnologia da Informação',1,1,'2026-11-22 17:56:48'),(73,'Funcionario Teste 073','Almoxarifado',1,1,'2026-11-22 17:56:48'),(74,'Funcionario Teste 074','Recursos Humanos',1,1,'2026-11-22 17:56:48'),(75,'Funcionario Teste 075','Financeiro',1,1,'2026-11-22 17:56:49'),(76,'Funcionario Teste 076','Logística',1,1,'2026-11-22 17:56:49'),(77,'Funcionario Teste 077','Administrativo',1,1,'2026-11-22 17:56:49'),(78,'Funcionario Teste 078','Tecnologia da Informação',1,1,'2026-11-22 17:56:49'),(79,'Funcionario Teste 079','Almoxarifado',1,1,'2026-11-22 17:56:49'),(80,'Funcionario Teste 080','Recursos Humanos',1,1,'2026-11-22 17:56:49'),(81,'Funcionario Teste 081','Financeiro',1,1,'2026-11-22 17:56:49'),(82,'Funcionario Teste 082','Logística',1,1,'2026-11-22 17:56:49'),(83,'Funcionario Teste 083','Administrativo',1,1,'2026-11-22 17:56:49'),(84,'Funcionario Teste 084','Tecnologia da Informação',1,1,'2026-11-22 17:56:49'),(85,'Funcionario Teste 085','Almoxarifado',1,1,'2026-11-22 17:56:49'),(86,'Funcionario Teste 086','Recursos Humanos',1,1,'2026-11-22 17:56:49'),(87,'Funcionario Teste 087','Financeiro',1,1,'2026-11-22 17:56:49'),(88,'Funcionario Teste 088','Logística',1,1,'2026-11-22 17:56:49'),(89,'Funcionario Teste 089','Administrativo',1,1,'2026-11-22 17:56:49'),(90,'Funcionario Teste 090','Tecnologia da Informação',1,1,'2026-11-22 17:56:49'),(91,'Funcionario Teste 091','Almoxarifado',1,1,'2026-11-22 17:56:49'),(92,'Funcionario Teste 092','Recursos Humanos',1,1,'2026-11-22 17:56:49'),(93,'Funcionario Teste 093','Financeiro',1,1,'2026-11-22 17:56:49'),(94,'Funcionario Teste 094','Logística',1,1,'2026-11-22 17:56:49'),(95,'Funcionario Teste 095','Administrativo',1,1,'2026-11-22 17:56:49'),(96,'Funcionario Teste 096','Tecnologia da Informação',1,1,'2026-11-22 17:56:49'),(97,'Funcionario Teste 097','Almoxarifado',1,1,'2026-11-22 17:56:49'),(98,'Funcionario Teste 098','Recursos Humanos',1,1,'2026-11-22 17:56:49'),(99,'Funcionario Teste 099','Financeiro',1,1,'2026-11-22 17:56:49'),(100,'Funcionario Teste 100','Logística',1,1,'2026-11-22 17:56:49');
/*!40000 ALTER TABLE `funcionarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-22 18:58:58
