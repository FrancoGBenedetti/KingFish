-- Usuarios
DROP DATABASE IF EXISTS login;
CREATE DATABASE login;
CREATE TABLE login.users (
  userId int(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  userEmail TEXT NOT NULL,
  userName TEXT NOT NULL,
  userPwd LONGTEXT NOT NULL,
  lastLogin DATETIME,
  profile INT,
  onlineStatus INT,
  token TEXT
);

CREATE TABLE login.loginLimit (
 ID INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
 ipAddress VARCHAR(39) NOT NULL,
 timeDiff VARCHAR(100)
);

CREATE TABLE login.pwdReset (
 pwdResetId int(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
 pwdResetEmail TEXT NOT NULL,
 pwdResetSelector TEXT NOT NULL,
 pwdResetToken LONGTEXT NOT NULL,
 pwdResetExpires TEXT NOT NULL
);
-- Fuentes de datos
DROP DATABASE IF EXISTS fuenteDatos;
CREATE DATABASE fuenteDatos;
CREATE TABLE fuenteDatos.rentaClientes (
  FECHA DATETIME NOT NULL,
  RUT varchar(20),
  APORTES DOUBLE,
  RETIROS DOUBLE,
  PATRIMONIO DOUBLE,
  rent_diaria DOUBLE,
  rent_acum DOUBLE
);
CREATE TABLE fuenteDatos.rentaClientes2 (
  FECHA DATETIME NOT NULL,
  RUT varchar(20),
  APORTES DOUBLE,
  RETIROS DOUBLE,
  PATRIMONIO DOUBLE,
  rent_diaria DOUBLE,
  rent_acum DOUBLE
);
-- Cálculos (Validaciones, reconciliación y anomalías)
DROP DATABASE IF EXISTS calculos;
CREATE DATABASE calculos;
CREATE TABLE calculos.validaciones (
  columna varchar(20),
  mensaje TEXT,
  fila INT,
  valor TEXT
);

CREATE TABLE calculos.reconciliacion (
  fila INT,
  columna varchar(20),
  fuente_1 TEXT,
  fuente_2 TEXT
);

CREATE TABLE calculos.anomalias_renta_diaria (
  APORTES DOUBLE,
  PATRIMONIO DOUBLE,
  RETIROS DOUBLE,
  RUT varchar(20),
  ANOMALIA INT,
  DESCRIPCION TEXT,
  FECHA DATETIME,
  IMPORTANCIA DOUBLE,
  rent_diaria DOUBLE,
  VALOR_ESPERADO DOUBLE,
  lower DOUBLE,
  upper DOUBLE
);

CREATE TABLE calculos.anomalias_renta_acumulada (
  APORTES DOUBLE,
  PATRIMONIO DOUBLE,
  RETIROS DOUBLE,
  RUT varchar(20),
  ANOMALIA INT,
  DESCRIPCION TEXT,
  FECHA DATETIME,
  IMPORTANCIA DOUBLE,
  rent_acum DOUBLE,
  VALOR_ESPERADO DOUBLE,
  lower DOUBLE,
  upper DOUBLE
);
-- Cantidad de anomalías en el tiempo
CREATE TABLE calculos.cantidad_anom_renta_diaria (
  FECHA DATETIME,
  cont INT
);

CREATE TABLE calculos.cantidad_anom_renta_acum (
  FECHA DATETIME,
  cont INT
);
-- Fuente de datos con lower y yhat_upper
CREATE TABLE calculos.new_rnt_diaria (
  APORTES DOUBLE,
  PATRIMONIO DOUBLE,
  RETIROS DOUBLE,
  RUT varchar(20),
  anomaly INT,
  DESCRIPCION TEXT,
  ds DATETIME,
  FECHA DATETIME,
  importance DOUBLE,
  rent_diaria DOUBLE,
  trend DOUBLE,
  yhat_lower DOUBLE,
  yhat_upper DOUBLE,
  yhat DOUBLE,
  fact DOUBLE
);
CREATE TABLE calculos.new_rnt_acum (
  APORTES DOUBLE,
  PATRIMONIO DOUBLE,
  RETIROS DOUBLE,
  RUT varchar(20),
  anomaly INT,
  DESCRIPCION TEXT,
  ds DATETIME,
  FECHA DATETIME,
  importance DOUBLE,
  rent_acum DOUBLE,
  trend DOUBLE,
  yhat_lower DOUBLE,
  yhat_upper DOUBLE,
  yhat DOUBLE,
  fact DOUBLE
);
