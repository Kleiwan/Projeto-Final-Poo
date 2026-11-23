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
-- Table structure for table `materiais`
--

DROP TABLE IF EXISTS `materiais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiais` (
  `codigo` varchar(50) NOT NULL,
  `nome` varchar(120) NOT NULL,
  `categoria` varchar(80) NOT NULL DEFAULT 'Geral',
  `unidade_medida` varchar(20) NOT NULL DEFAULT 'unidade',
  `estoque_inicial` decimal(10,2) NOT NULL DEFAULT '0.00',
  `quantidade` decimal(10,2) NOT NULL DEFAULT '0.00',
  `estoque_minimo` decimal(10,2) NOT NULL DEFAULT '0.00',
  `bloqueado` tinyint(1) NOT NULL DEFAULT '0',
  `motivo_bloqueio` varchar(255) NOT NULL DEFAULT '',
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`codigo`),
  CONSTRAINT `ck_material_estoque` CHECK ((`quantidade` >= 0)),
  CONSTRAINT `ck_material_inicial` CHECK ((`estoque_inicial` >= 0)),
  CONSTRAINT `ck_material_minimo` CHECK ((`estoque_minimo` >= 0)),
  CONSTRAINT `ck_material_nome` CHECK ((char_length(trim(`nome`)) > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiais`
--

LOCK TABLES `materiais` WRITE;
/*!40000 ALTER TABLE `materiais` DISABLE KEYS */;
INSERT INTO `materiais` VALUES ('MAT-001','Papel A4 (Resma)','Papelaria','resma',500.00,500.00,50.00,0,'',1),('MAT-002','Caneta Esferográfica Azul','Escritório','unidade',300.00,300.00,30.00,0,'',1),('MAT-003','Grampeador de Mesa','Escritório','unidade',45.00,45.00,5.00,0,'',1),('MAT-004','Pasta Suspensa Kraft','Arquivo','unidade',200.00,200.00,20.00,0,'',1),('MAT-005','Tesoura de Escritório','Escritório','unidade',60.00,60.00,6.00,0,'',1),('MAT-006','Material de Escritório 006','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-007','Material de Escritório 007','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-008','Material de Escritório 008','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-009','Material de Escritório 009','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-010','Material de Escritório 010','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-011','Material de Escritório 011','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-012','Material de Escritório 012','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-013','Material de Escritório 013','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-014','Material de Escritório 014','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-015','Material de Escritório 015','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-016','Material de Escritório 016','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-017','Material de Escritório 017','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-018','Material de Escritório 018','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-019','Material de Escritório 019','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-020','Material de Escritório 020','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-021','Material de Escritório 021','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-022','Material de Escritório 022','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-023','Material de Escritório 023','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-024','Material de Escritório 024','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-025','Material de Escritório 025','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-026','Material de Escritório 026','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-027','Material de Escritório 027','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-028','Material de Escritório 028','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-029','Material de Escritório 029','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-030','Material de Escritório 030','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-031','Material de Escritório 031','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-032','Material de Escritório 032','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-033','Material de Escritório 033','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-034','Material de Escritório 034','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-035','Material de Escritório 035','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-036','Material de Escritório 036','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-037','Material de Escritório 037','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-038','Material de Escritório 038','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-039','Material de Escritório 039','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-040','Material de Escritório 040','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-041','Material de Escritório 041','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-042','Material de Escritório 042','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-043','Material de Escritório 043','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-044','Material de Escritório 044','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-045','Material de Escritório 045','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-046','Material de Escritório 046','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-047','Material de Escritório 047','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-048','Material de Escritório 048','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-049','Material de Escritório 049','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-050','Material de Escritório 050','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-051','Material de Escritório 051','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-052','Material de Escritório 052','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-053','Material de Escritório 053','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-054','Material de Escritório 054','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-055','Material de Escritório 055','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-056','Material de Escritório 056','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-057','Material de Escritório 057','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-058','Material de Escritório 058','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-059','Material de Escritório 059','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-060','Material de Escritório 060','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-061','Material de Escritório 061','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-062','Material de Escritório 062','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-063','Material de Escritório 063','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-064','Material de Escritório 064','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-065','Material de Escritório 065','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-066','Material de Escritório 066','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-067','Material de Escritório 067','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-068','Material de Escritório 068','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-069','Material de Escritório 069','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-070','Material de Escritório 070','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-071','Material de Escritório 071','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-072','Material de Escritório 072','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-073','Material de Escritório 073','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-074','Material de Escritório 074','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-075','Material de Escritório 075','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-076','Material de Escritório 076','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-077','Material de Escritório 077','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-078','Material de Escritório 078','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-079','Material de Escritório 079','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-080','Material de Escritório 080','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-081','Material de Escritório 081','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-082','Material de Escritório 082','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-083','Material de Escritório 083','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-084','Material de Escritório 084','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-085','Material de Escritório 085','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-086','Material de Escritório 086','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-087','Material de Escritório 087','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-088','Material de Escritório 088','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-089','Material de Escritório 089','Escritório','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-090','Material de Escritório 090','Limpeza','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-091','Material de Escritório 091','Informática','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-092','Material de Escritório 092','Papelaria','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-093','Material de Escritório 093','Escritório','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-094','Material de Escritório 094','Limpeza','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-095','Material de Escritório 095','Informática','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-096','Material de Escritório 096','Papelaria','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-097','Material de Escritório 097','Escritório','caixa',1000.00,1000.00,25.00,0,'',1),('MAT-098','Material de Escritório 098','Limpeza','pacote',1000.00,1000.00,25.00,0,'',1),('MAT-099','Material de Escritório 099','Informática','unidade',1000.00,1000.00,25.00,0,'',1),('MAT-100','Material de Escritório 100','Papelaria','caixa',1000.00,1000.00,25.00,0,'',1);
/*!40000 ALTER TABLE `materiais` ENABLE KEYS */;
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
