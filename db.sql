CREATE TABLE `usuarios` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `telegram_id` bigint NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telegram_id` (`telegram_id`)
);

CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `telegram_id` bigint NOT NULL,
  `comando` text COLLATE utf8mb4_general_ci,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_log_telegram_id` (`telegram_id`),
  CONSTRAINT `fk_log_telegram_id` FOREIGN KEY (`telegram_id`) REFERENCES `usuarios` (`telegram_id`)
);
