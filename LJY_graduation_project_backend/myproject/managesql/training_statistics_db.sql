-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2024-04-13 09:56:04
-- 服务器版本： 5.7.43-log
-- PHP 版本： 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `training_statistics_db`
--

-- --------------------------------------------------------

--
-- 表的结构 `training_info`
--

CREATE TABLE `training_info` (
  `id` int(11) NOT NULL,
  `epoch` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `duration` int(11) NOT NULL COMMENT '累计用时，单位秒',
  `user_id` int(11) NOT NULL,
  `model` varchar(255) NOT NULL,
  `top1_accuracy` decimal(5,2) NOT NULL,
  `top2_accuracy` decimal(5,2) DEFAULT NULL,
  `top3_accuracy` decimal(5,2) DEFAULT NULL,
  `top4_accuracy` decimal(5,2) DEFAULT NULL,
  `top5_accuracy` decimal(5,2) DEFAULT NULL,
  `top6_accuracy` decimal(5,2) DEFAULT NULL,
  `top7_accuracy` decimal(5,2) DEFAULT NULL,
  `top8_accuracy` decimal(5,2) DEFAULT NULL,
  `top9_accuracy` decimal(5,2) DEFAULT NULL,
  `top10_accuracy` decimal(5,2) DEFAULT NULL,
  `optional_feature` varchar(255) DEFAULT NULL,
  `learning_rate` decimal(10,8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转储表的索引
--

--
-- 表的索引 `training_info`
--
ALTER TABLE `training_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `training_info`
--
ALTER TABLE `training_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 限制导出的表
--

--
-- 限制表 `training_info`
--
ALTER TABLE `training_info`
  ADD CONSTRAINT `training_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
