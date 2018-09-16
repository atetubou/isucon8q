USE profile;
CREATE TABLE IF NOT EXISTS `profile` (
    `id`       int(11) NOT NULL AUTO_INCREMENT,
    `commit_id`   varchar(40) NOT NULL,
    `hostname` varchar(100) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE  IF NOT EXISTS `cpuprofile`(
    `profile_id` int(11) NOT NULL,
    `ratio`      float(7,3) NOT NULL,
    `func_name`  VARCHAR(200) NOT NULL,
    `body`       TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

