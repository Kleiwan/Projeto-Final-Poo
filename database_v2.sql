-- ==============================================================
-- ALMOXARIFADO - BANCO DE DADOS VERSÃO 2
-- MySQL 8.0+ | Executar no MySQL Workbench
-- Massa de teste: 3.000 registros no total:
-- 100 funcionarios + 100 materiais + 2.400 retiradas + 400 entradas.
-- Os 5 funcionários, 5 materiais e 5 retiradas do dump anterior
-- foram preservados como os primeiros registros.
-- ==============================================================

CREATE DATABASE IF NOT EXISTS almoxarifado_v2
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE almoxarifado_v2;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS entradas;
DROP TABLE IF EXISTS retiradas;
DROP TABLE IF EXISTS materiais;
DROP TABLE IF EXISTS funcionarios;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE funcionarios (
    id INT NOT NULL,
    nome VARCHAR(120) NOT NULL,
    setor VARCHAR(120) NOT NULL,
    pode_retirar BOOLEAN NOT NULL DEFAULT TRUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT ck_funcionario_nome CHECK (CHAR_LENGTH(TRIM(nome)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE materiais (
    codigo VARCHAR(50) NOT NULL,
    nome VARCHAR(120) NOT NULL,
    categoria VARCHAR(80) NOT NULL DEFAULT 'Geral',
    unidade_medida VARCHAR(20) NOT NULL DEFAULT 'unidade',
    estoque_inicial DECIMAL(10,2) NOT NULL DEFAULT 0,
    quantidade DECIMAL(10,2) NOT NULL DEFAULT 0,
    estoque_minimo DECIMAL(10,2) NOT NULL DEFAULT 0,
    bloqueado BOOLEAN NOT NULL DEFAULT FALSE,
    motivo_bloqueio VARCHAR(255) NOT NULL DEFAULT '',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (codigo),
    CONSTRAINT ck_material_estoque CHECK (quantidade >= 0),
    CONSTRAINT ck_material_inicial CHECK (estoque_inicial >= 0),
    CONSTRAINT ck_material_minimo CHECK (estoque_minimo >= 0),
    CONSTRAINT ck_material_nome CHECK (CHAR_LENGTH(TRIM(nome)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE retiradas (
    id BIGINT NOT NULL AUTO_INCREMENT,
    funcionario_id INT NOT NULL,
    material_codigo VARCHAR(50) NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    momento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao VARCHAR(255) NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    INDEX ix_retirada_funcionario (funcionario_id),
    INDEX ix_retirada_material (material_codigo),
    INDEX ix_retirada_momento (momento),
    CONSTRAINT ck_retirada_quantidade CHECK (quantidade > 0),
    CONSTRAINT fk_retirada_funcionario FOREIGN KEY (funcionario_id)
      REFERENCES funcionarios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_retirada_material FOREIGN KEY (material_codigo)
      REFERENCES materiais(codigo) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE entradas (
    id BIGINT NOT NULL AUTO_INCREMENT,
    funcionario_id INT NOT NULL,
    material_codigo VARCHAR(50) NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    momento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao VARCHAR(255) NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    INDEX ix_entrada_funcionario (funcionario_id),
    INDEX ix_entrada_material (material_codigo),
    INDEX ix_entrada_momento (momento),
    CONSTRAINT ck_entrada_quantidade CHECK (quantidade > 0),
    CONSTRAINT fk_entrada_funcionario FOREIGN KEY (funcionario_id)
      REFERENCES funcionarios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_entrada_material FOREIGN KEY (material_codigo)
      REFERENCES materiais(codigo) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------------
-- Dados originais do primeiro dump: 5 funcionários e 5 materiais.
-- --------------------------------------------------------------
INSERT INTO funcionarios (id,nome,setor) VALUES
(1,'Ana Silva','Tecnologia da Informação'),
(2,'Carlos Souza','Almoxarifado'),
(3,'Maria Santos','Recursos Humanos'),
(4,'João Pereira','Financeiro'),
(5,'Beatriz Costa','Logística');

INSERT INTO materiais
(codigo,nome,categoria,unidade_medida,estoque_inicial,quantidade,estoque_minimo)
VALUES
('MAT-001','Papel A4 (Resma)','Papelaria','resma',500.00,500.00,50.00),
('MAT-002','Caneta Esferográfica Azul','Escritório','unidade',300.00,300.00,30.00),
('MAT-003','Grampeador de Mesa','Escritório','unidade',45.00,45.00,5.00),
('MAT-004','Pasta Suspensa Kraft','Arquivo','unidade',200.00,200.00,20.00),
('MAT-005','Tesoura de Escritório','Escritório','unidade',60.00,60.00,6.00);

INSERT INTO retiradas
(id,funcionario_id,material_codigo,quantidade,momento,observacao) VALUES
(1,1,'MAT-001',2.00,'2026-02-01 08:30:00','Registro preservado do dump anterior'),
(2,2,'MAT-002',1.00,'2026-02-01 09:15:00','Registro preservado do dump anterior'),
(3,3,'MAT-003',1.00,'2026-02-02 10:00:00','Registro preservado do dump anterior'),
(4,4,'MAT-004',5.00,'2026-02-03 11:20:00','Registro preservado do dump anterior'),
(5,5,'MAT-005',2.00,'2026-02-04 14:00:00','Registro preservado do dump anterior');

-- --------------------------------------------------------------
-- Complementação da massa: funcionários 6 a 100 e materiais 6 a 100.
-- --------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE gerar_massa_almoxarifado()
BEGIN
    DECLARE i INT DEFAULT 6;
    DECLARE n INT DEFAULT 1;
    DECLARE id_func INT;
    DECLARE cod_material VARCHAR(50);
    DECLARE qtd DECIMAL(10,2);

    WHILE i <= 100 DO
        INSERT INTO funcionarios (id,nome,setor)
        VALUES (
            i,
            CONCAT('Funcionario Teste ', LPAD(i,3,'0')),
            CASE MOD(i,6)
                WHEN 0 THEN 'Tecnologia da Informação'
                WHEN 1 THEN 'Almoxarifado'
                WHEN 2 THEN 'Recursos Humanos'
                WHEN 3 THEN 'Financeiro'
                WHEN 4 THEN 'Logística'
                ELSE 'Administrativo'
            END
        );
        SET i = i + 1;
    END WHILE;

    SET i = 6;
    WHILE i <= 100 DO
        SET cod_material = CONCAT('MAT-',LPAD(i,3,'0'));
        SET qtd = 1000.00;
        INSERT INTO materiais
        (codigo,nome,categoria,unidade_medida,estoque_inicial,quantidade,estoque_minimo)
        VALUES (
            cod_material,
            CONCAT('Material de Escritório ',LPAD(i,3,'0')),
            CASE MOD(i,4)
                WHEN 0 THEN 'Papelaria'
                WHEN 1 THEN 'Escritório'
                WHEN 2 THEN 'Limpeza'
                ELSE 'Informática'
            END,
            CASE MOD(i,3) WHEN 0 THEN 'unidade' WHEN 1 THEN 'caixa' ELSE 'pacote' END,
            qtd,qtd,25.00
        );
        SET i = i + 1;
    END WHILE;

    -- 2.395 retiradas adicionais (5 antigas + 2.395 = 2.400).
    SET n = 1;
    WHILE n <= 2395 DO
        SET id_func = MOD(n - 1,100) + 1;
        SET cod_material = CONCAT('MAT-',LPAD(MOD((n - 1) * 37,100) + 1,3,'0'));
        SET qtd = 1 + MOD(n,2);
        INSERT INTO retiradas
        (funcionario_id,material_codigo,quantidade,momento,observacao)
        VALUES (
            id_func,cod_material,qtd,
            DATE_ADD('2026-01-01 08:00:00', INTERVAL n HOUR),
            'Movimentação fictícia para teste'
        );
        SET n = n + 1;
    END WHILE;

    -- 400 entradas para representar reposições e formar histórico de estoque.
    SET n = 1;
    WHILE n <= 400 DO
        SET id_func = MOD(n - 1,100) + 1;
        SET cod_material = CONCAT('MAT-',LPAD(MOD((n - 1) * 13,100) + 1,3,'0'));
        SET qtd = 10 + MOD(n,11);
        INSERT INTO entradas
        (funcionario_id,material_codigo,quantidade,momento,observacao)
        VALUES (
            id_func,cod_material,qtd,
            DATE_ADD('2026-01-01 09:00:00', INTERVAL n DAY),
            'Reposição fictícia para teste'
        );
        SET n = n + 1;
    END WHILE;
END$$

DELIMITER ;

CALL gerar_massa_almoxarifado();
DROP PROCEDURE gerar_massa_almoxarifado;

-- Saldo atual = estoque inicial + entradas - retiradas.
UPDATE materiais m
SET m.quantidade =
    m.estoque_inicial
    + COALESCE((SELECT SUM(e.quantidade) FROM entradas e WHERE e.material_codigo=m.codigo),0)
    - COALESCE((SELECT SUM(r.quantidade) FROM retiradas r WHERE r.material_codigo=m.codigo),0);

-- ==============================================================
-- CONSULTAS / RELATÓRIOS PARA DEMONSTRAR O BANCO
-- ==============================================================

-- 1. Conferência da quantidade de registros (deve totalizar 3.000).
SELECT 'funcionarios' AS tabela, COUNT(*) AS total FROM funcionarios
UNION ALL SELECT 'materiais', COUNT(*) FROM materiais
UNION ALL SELECT 'retiradas', COUNT(*) FROM retiradas
UNION ALL SELECT 'entradas', COUNT(*) FROM entradas
UNION ALL SELECT 'TOTAL', (
    (SELECT COUNT(*) FROM funcionarios) +
    (SELECT COUNT(*) FROM materiais) +
    (SELECT COUNT(*) FROM retiradas) +
    (SELECT COUNT(*) FROM entradas)
);

-- 2. Materiais abaixo do estoque mínimo.
SELECT codigo,nome,quantidade,estoque_minimo
FROM materiais
WHERE quantidade <= estoque_minimo
ORDER BY quantidade;

-- 3. Materiais mais retirados.
SELECT m.codigo,m.nome,SUM(r.quantidade) AS total_retirado
FROM materiais m
JOIN retiradas r ON r.material_codigo=m.codigo
GROUP BY m.codigo,m.nome
ORDER BY total_retirado DESC
LIMIT 10;

-- 4. Funcionários com maior volume de retiradas.
SELECT f.id,f.nome,COUNT(r.id) AS numero_retiradas,SUM(r.quantidade) AS quantidade_total
FROM funcionarios f
JOIN retiradas r ON r.funcionario_id=f.id
GROUP BY f.id,f.nome
ORDER BY quantidade_total DESC
LIMIT 10;

-- 5. Movimentação mensal (entradas e retiradas).
SELECT DATE_FORMAT(momento,'%Y-%m') AS mes,'ENTRADA' AS tipo,SUM(quantidade) AS quantidade
FROM entradas GROUP BY DATE_FORMAT(momento,'%Y-%m')
UNION ALL
SELECT DATE_FORMAT(momento,'%Y-%m'),'RETIRADA',SUM(quantidade)
FROM retiradas GROUP BY DATE_FORMAT(momento,'%Y-%m')
ORDER BY mes,tipo;

-- 6. Saldo por categoria.
SELECT categoria,COUNT(*) AS quantidade_materiais,SUM(quantidade) AS saldo_total
FROM materiais
GROUP BY categoria
ORDER BY saldo_total DESC;

-- 7. Histórico detalhado de movimentações (entradas + retiradas).
SELECT 'ENTRADA' AS tipo,e.id,e.momento,f.nome AS funcionario,m.nome AS material,e.quantidade,e.observacao
FROM entradas e
JOIN funcionarios f ON f.id=e.funcionario_id
JOIN materiais m ON m.codigo=e.material_codigo
UNION ALL
SELECT 'RETIRADA',r.id,r.momento,f.nome,m.nome,r.quantidade,r.observacao
FROM retiradas r
JOIN funcionarios f ON f.id=r.funcionario_id
JOIN materiais m ON m.codigo=r.material_codigo
ORDER BY momento DESC;
