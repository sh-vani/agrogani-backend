-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 12, 2025 at 10:10 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `agro`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_otp`
--

CREATE TABLE `accounts_otp` (
  `id` bigint(20) NOT NULL,
  `email_otp` varchar(6) DEFAULT NULL,
  `mobile_otp` varchar(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_otp`
--

INSERT INTO `accounts_otp` (`id`, `email_otp`, `mobile_otp`, `created_at`, `user_id`) VALUES
(4, '727557', '580147', '2025-06-29 11:49:18.515210', 4),
(5, '500954', '629328', '2025-06-29 11:59:55.813023', 5),
(6, '891513', '720940', '2025-07-05 05:16:09.339604', 6),
(7, '828810', '631756', '2025-07-05 05:16:57.494522', 7),
(8, '762794', '315344', '2025-07-05 06:31:41.645586', 8),
(9, '413215', '459989', '2025-07-05 06:56:49.191357', 9),
(10, '774386', '845699', '2025-07-05 06:57:48.078343', 10),
(11, '337241', '192310', '2025-07-05 07:10:56.097482', 11),
(12, '202574', '136405', '2025-07-05 07:19:29.160412', 12);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_plan`
--

CREATE TABLE `accounts_plan` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `duration` varchar(50) NOT NULL,
  `features` longtext NOT NULL,
  `device_limit` int(10) UNSIGNED NOT NULL CHECK (`device_limit` >= 0),
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_plan`
--

INSERT INTO `accounts_plan` (`id`, `name`, `price`, `duration`, `features`, `device_limit`, `is_active`) VALUES
(1, 'Free', 0.00, '1 year', 'Default free plan', 1, 1),
(2, 'Vegetable Plan', 699.00, '1 year', '1 vegetable field, Expense & task tracking, Image upload', 1, 1),
(3, 'Multi-Field Plan', 1199.00, '1 year', 'Multiple fields, Multi-device login, Full crop/expense tracking', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

CREATE TABLE `accounts_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `full_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `plan_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_user`
--

INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `email`, `mobile`, `full_name`, `is_active`, `date_joined`, `plan_id`) VALUES
(4, '', NULL, 't@gmail.com', '143456789', 't', 1, '2025-06-29 11:49:18.490829', 1),
(5, 'pbkdf2_sha256$600000$k9tXY3rWt2OVxzBOJJwXGI$e+BKV0RoXK98fgJvKdS25hHOGrJxBlYidgAoE1h20V8=', NULL, 'rahul@gmail.com', '145456789', 'rahul', 1, '2025-06-29 11:59:55.801270', 1),
(6, 'pbkdf2_sha256$600000$k9tXY3rWt2OVxzBOJJwXGI$e+BKV0RoXK98fgJvKdS25hHOGrJxBlYidgAoE1h20V8=', NULL, 'gopal@gmail.com', '123536789', 'gopal', 1, '2025-07-05 05:16:09.302137', 1),
(7, '', NULL, 'gopalbgurjar435@gmail.com', '9926202390', 'gopal', 1, '2025-07-05 05:16:57.474454', 1),
(8, '', NULL, 'gopal1@gmail.com', '123536788', 'gopal', 1, '2025-07-05 06:31:41.605383', 1),
(9, '', NULL, 'gopal123@gmail.com', '6666666666', 'Gopal Bankey', 1, '2025-07-05 06:56:49.163221', 1),
(10, '', NULL, 'gopal12345@gmail.com', '6666666667', 'Gopal Bankey', 1, '2025-07-05 06:57:48.069373', 1),
(11, '', NULL, 'gopal1235@gmail.com', '6666666668', 'Gopal Bankey', 1, '2025-07-05 07:10:56.081055', 1),
(12, '', NULL, 'gopal111@gmail.com', '3356443466', 'kkkk', 1, '2025-07-05 07:19:29.135533', 1);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_userplan`
--

CREATE TABLE `accounts_userplan` (
  `id` bigint(20) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `plan_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_userplan`
--

INSERT INTO `accounts_userplan` (`id`, `start_date`, `end_date`, `plan_id`, `user_id`) VALUES
(1, '2025-07-02 05:50:27.000000', '2025-07-31 05:50:27.000000', 2, 5);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add plan', 7, 'add_plan'),
(26, 'Can change plan', 7, 'change_plan'),
(27, 'Can delete plan', 7, 'delete_plan'),
(28, 'Can view plan', 7, 'view_plan'),
(29, 'Can add user plan', 8, 'add_userplan'),
(30, 'Can change user plan', 8, 'change_userplan'),
(31, 'Can delete user plan', 8, 'delete_userplan'),
(32, 'Can view user plan', 8, 'view_userplan'),
(33, 'Can add otp', 9, 'add_otp'),
(34, 'Can change otp', 9, 'change_otp'),
(35, 'Can delete otp', 9, 'delete_otp'),
(36, 'Can view otp', 9, 'view_otp'),
(37, 'Can add user profile', 10, 'add_userprofile'),
(38, 'Can change user profile', 10, 'change_userprofile'),
(39, 'Can delete user profile', 10, 'delete_userprofile'),
(40, 'Can view user profile', 10, 'view_userprofile'),
(41, 'Can add device', 11, 'add_device'),
(42, 'Can change device', 11, 'change_device'),
(43, 'Can delete device', 11, 'delete_device'),
(44, 'Can view device', 11, 'view_device'),
(45, 'Can add plan', 12, 'add_plan'),
(46, 'Can change plan', 12, 'change_plan'),
(47, 'Can delete plan', 12, 'delete_plan'),
(48, 'Can view plan', 12, 'view_plan'),
(49, 'Can add crop', 13, 'add_crop'),
(50, 'Can change crop', 13, 'change_crop'),
(51, 'Can delete crop', 13, 'delete_crop'),
(52, 'Can view crop', 13, 'view_crop'),
(53, 'Can add labour', 14, 'add_labour'),
(54, 'Can change labour', 14, 'change_labour'),
(55, 'Can delete labour', 14, 'delete_labour'),
(56, 'Can view labour', 14, 'view_labour'),
(57, 'Can add attendance', 15, 'add_attendance'),
(58, 'Can change attendance', 15, 'change_attendance'),
(59, 'Can delete attendance', 15, 'delete_attendance'),
(60, 'Can view attendance', 15, 'view_attendance'),
(61, 'Can add expense', 16, 'add_expense'),
(62, 'Can change expense', 16, 'change_expense'),
(63, 'Can delete expense', 16, 'delete_expense'),
(64, 'Can view expense', 16, 'view_expense'),
(65, 'Can add quick sale', 17, 'add_quicksale'),
(66, 'Can change quick sale', 17, 'change_quicksale'),
(67, 'Can delete quick sale', 17, 'delete_quicksale'),
(68, 'Can view quick sale', 17, 'view_quicksale'),
(69, 'Can add detailed sale', 18, 'add_detailedsale'),
(70, 'Can change detailed sale', 18, 'change_detailedsale'),
(71, 'Can delete detailed sale', 18, 'delete_detailedsale'),
(72, 'Can view detailed sale', 18, 'view_detailedsale'),
(73, 'Can add task', 19, 'add_task'),
(74, 'Can change task', 19, 'change_task'),
(75, 'Can delete task', 19, 'delete_task'),
(76, 'Can view task', 19, 'view_task'),
(77, 'Can add shop', 20, 'add_shop'),
(78, 'Can change shop', 20, 'change_shop'),
(79, 'Can delete shop', 20, 'delete_shop'),
(80, 'Can view shop', 20, 'view_shop');

-- --------------------------------------------------------

--
-- Table structure for table `crop_crop`
--

CREATE TABLE `crop_crop` (
  `id` bigint(20) NOT NULL,
  `field_name` varchar(100) NOT NULL,
  `crop_name` varchar(100) NOT NULL,
  `field_size` decimal(10,2) NOT NULL,
  `field_unit` varchar(20) NOT NULL,
  `crop_type` varchar(10) NOT NULL,
  `sowing_date` date NOT NULL,
  `irrigation_source` varchar(10) NOT NULL,
  `additional_notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crop_crop`
--

INSERT INTO `crop_crop` (`id`, `field_name`, `crop_name`, `field_size`, `field_unit`, `crop_type`, `sowing_date`, `irrigation_source`, `additional_notes`, `created_at`, `user_id`) VALUES
(1, 'My Field', 'Wheat', 5.50, 'Acres', 'type1', '2025-06-22', 'Canal', 'First sowing of the season.', '2025-07-05 09:48:34.635397', 5),
(2, 'Field 1', 'Wheat', 5.00, 'Acres', 'type1', '2025-06-25', 'Canal', 'Good soil quality', '2025-07-05 09:53:55.002450', 5),
(3, 'Field 101', 'Wheat', 5.50, 'Acres', 'type1', '2025-06-22', 'Canal', 'First crop of the season', '2025-07-05 09:57:06.392156', 5),
(4, 'Field 101', 'Wheat', 5.50, 'Acres', 'type1', '2025-06-22', 'Canal', 'First crop of the season', '2025-07-05 10:02:58.483663', 5),
(5, 'Field 101', 'Wheat', 5.50, 'Acres', 'type1', '2025-06-22', 'Canal', 'First crop of the season', '2025-07-05 10:12:13.703150', 5),
(6, 'South', 'wheat', 2.50, 'Acres', 'type1', '2025-07-06', 'Canal', NULL, '2025-07-05 10:28:33.035986', 5),
(7, 'bsbsv', 'dhdhh', 2.50, 'Acres', 'type1', '2025-07-05', 'Canal', NULL, '2025-07-05 10:35:30.647299', 5),
(8, 'Field 1', 'Wheat', 5.00, 'Acres', 'type1', '2025-06-25', 'Canal', 'Good soil quality', '2025-07-06 05:58:40.192665', 5);

-- --------------------------------------------------------

--
-- Table structure for table `crop_plan`
--

CREATE TABLE `crop_plan` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `device_limit` int(10) UNSIGNED NOT NULL CHECK (`device_limit` >= 0),
  `allowed_crop_types` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`allowed_crop_types`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `device_device`
--

CREATE TABLE `device_device` (
  `id` bigint(20) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `device_name` varchar(255) DEFAULT NULL,
  `last_login` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(9, 'accounts', 'otp'),
(7, 'accounts', 'plan'),
(6, 'accounts', 'user'),
(8, 'accounts', 'userplan'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(13, 'crop', 'crop'),
(12, 'crop', 'plan'),
(11, 'device', 'device'),
(16, 'expenses', 'expense'),
(15, 'labour', 'attendance'),
(14, 'labour', 'labour'),
(18, 'sale', 'detailedsale'),
(17, 'sale', 'quicksale'),
(5, 'sessions', 'session'),
(20, 'shop', 'shop'),
(19, 'Task', 'task'),
(10, 'userprofile', 'userprofile');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'accounts', '0001_initial', '2025-06-29 08:54:01.169039'),
(2, 'Task', '0001_initial', '2025-06-29 08:54:01.279744'),
(3, 'contenttypes', '0001_initial', '2025-06-29 08:54:01.347563'),
(4, 'admin', '0001_initial', '2025-06-29 08:54:01.528314'),
(5, 'admin', '0002_logentry_remove_auto_add', '2025-06-29 08:54:01.540282'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-29 08:54:01.550257'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-06-29 08:54:01.682047'),
(8, 'auth', '0001_initial', '2025-06-29 08:54:02.139215'),
(9, 'auth', '0002_alter_permission_name_max_length', '2025-06-29 08:54:02.227570'),
(10, 'auth', '0003_alter_user_email_max_length', '2025-06-29 08:54:02.241048'),
(11, 'auth', '0004_alter_user_username_opts', '2025-06-29 08:54:02.251631'),
(12, 'auth', '0005_alter_user_last_login_null', '2025-06-29 08:54:02.261902'),
(13, 'auth', '0006_require_contenttypes_0002', '2025-06-29 08:54:02.268472'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2025-06-29 08:54:02.282434'),
(15, 'auth', '0008_alter_user_username_max_length', '2025-06-29 08:54:02.295405'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2025-06-29 08:54:02.305374'),
(17, 'auth', '0010_alter_group_name_max_length', '2025-06-29 08:54:02.324330'),
(18, 'auth', '0011_update_proxy_permissions', '2025-06-29 08:54:02.340280'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2025-06-29 08:54:02.351250'),
(20, 'device', '0001_initial', '2025-06-29 08:54:02.458962'),
(21, 'shop', '0001_initial', '2025-06-29 08:54:02.563838'),
(22, 'expenses', '0001_initial', '2025-06-29 08:54:02.769419'),
(23, 'labour', '0001_initial', '2025-06-29 08:54:03.071950'),
(24, 'sale', '0001_initial', '2025-06-29 08:54:03.278813'),
(25, 'sessions', '0001_initial', '2025-06-29 08:54:03.328073'),
(26, 'userprofile', '0001_initial', '2025-06-29 08:54:03.453262'),
(27, 'crop', '0001_initial', '2025-07-05 09:48:10.469090');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `expenses_expense`
--

CREATE TABLE `expenses_expense` (
  `id` bigint(20) NOT NULL,
  `crop` varchar(100) NOT NULL,
  `expense_type` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `paying_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(10) NOT NULL,
  `payment_type` varchar(10) NOT NULL,
  `note` longtext DEFAULT NULL,
  `bill_photo` varchar(100) DEFAULT NULL,
  `bill_no` varchar(20) NOT NULL,
  `labour_name` varchar(100) DEFAULT NULL,
  `work_description` longtext DEFAULT NULL,
  `daily_wage` decimal(7,2) DEFAULT NULL,
  `seed_name` varchar(100) DEFAULT NULL,
  `equipment_name` varchar(100) DEFAULT NULL,
  `equipment_type` varchar(20) DEFAULT NULL,
  `vendor_name` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `shop_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses_expense`
--

INSERT INTO `expenses_expense` (`id`, `crop`, `expense_type`, `date`, `paying_amount`, `payment_method`, `payment_type`, `note`, `bill_photo`, `bill_no`, `labour_name`, `work_description`, `daily_wage`, `seed_name`, `equipment_name`, `equipment_type`, `vendor_name`, `created_at`, `shop_id`, `user_id`) VALUES
(1, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'credit', 'Advanced fertilizer purchase', '', '20250705001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-05 10:08:28.335299', 1, 5),
(2, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'credit', 'Advanced fertilizer purchase', '', '20250705002', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-05 11:47:58.563217', NULL, 5),
(3, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'credit', 'Advanced fertilizer purchase', '', '20250706001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-06 06:37:24.178876', NULL, 5),
(4, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'credit', 'Advanced fertilizer purchase', '', '20250706002', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-06 06:38:17.937579', NULL, 5),
(5, 'गेहूं', 'labour', '2025-07-06', 200.00, 'upi', 'credit', 'work this complete', 'bills/1000157981.jpg', '20250706003', 'kallu', 'irrigation', 200.00, NULL, NULL, NULL, NULL, '2025-07-06 06:46:10.993053', NULL, 5),
(6, 'सोयाबीन', 'equipment', '2025-07-07', 90000.00, 'cash', 'credit', 'bbbb', 'bills/1000157981_PgnsLfM.jpg', '20250706004', NULL, NULL, NULL, NULL, 'tfyfyf', 'tffyfy', 'ycyfyf', '2025-07-06 06:49:12.815986', NULL, 5),
(7, 'चना', 'seed', '2025-07-06', 499.00, 'cash', 'credit', 'bsbsb', 'bills/1000164004.jpg', '20250706005', NULL, NULL, NULL, 'bsbsv', NULL, NULL, NULL, '2025-07-06 06:50:18.325595', NULL, 5),
(8, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'advance', 'Advanced fertilizer purchase', '', '20250706006', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-06 06:53:48.265187', NULL, 5),
(9, '3', 'fertilizer', '2025-06-04', 17500.00, 'cash', 'regular', 'Advanced fertilizer purchase', '', '20250706007', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-06 06:54:17.253438', NULL, 5),
(10, 'गेहूं', 'fertilizer', '2025-07-06', 25.00, 'cash', 'credit', 'tvvv', 'bills/1000157981_lZ7jNac.jpg', '20250706008', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-06 06:55:43.852908', 1, 5),
(11, 'चना', 'labour', '2025-07-06', 200.00, 'cash', 'regular', 'hdhdhdbbd', 'bills/1000157981_sFkzJ93.jpg', '20250706009', 'bhh', 'bbn', 200.00, NULL, NULL, NULL, NULL, '2025-07-06 06:57:13.741432', NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `labour_attendance`
--

CREATE TABLE `labour_attendance` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `labour_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `labour_attendance`
--

INSERT INTO `labour_attendance` (`id`, `date`, `status`, `labour_id`) VALUES
(2, '2025-06-27', 'absent', 1),
(3, '2025-07-02', 'absent', 1);

-- --------------------------------------------------------

--
-- Table structure for table `labour_labour`
--

CREATE TABLE `labour_labour` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `daily_wage` decimal(10,2) NOT NULL,
  `gender` varchar(6) NOT NULL,
  `address` longtext DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `labour_labour`
--

INSERT INTO `labour_labour` (`id`, `name`, `mobile`, `daily_wage`, `gender`, `address`, `user_id`) VALUES
(1, 'Ram Lal', '9876543210', 500.00, 'male', 'Village ABC', 5),
(6, 'Ram Lal', '9876543210', 500.00, 'male', 'Village ABC', 5),
(7, 'kkk', '9999999', 200.00, 'male', '', 5),
(8, 'gsgsg', '8855888588', 300.00, 'male', '', 5),
(9, 'gdgsg', '2665565665', 200.00, 'male', '', 5),
(10, 'sbsh', '5656888888', 8989.00, 'male', 'zvvz', 5);

-- --------------------------------------------------------

--
-- Table structure for table `sale_detailedsale`
--

CREATE TABLE `sale_detailedsale` (
  `id` bigint(20) NOT NULL,
  `sale_date` date NOT NULL,
  `crops` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`crops`)),
  `transport_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`transport_details`)),
  `buyer_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`buyer_details`)),
  `payment_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`payment_details`)),
  `total_sale_amount` decimal(12,2) NOT NULL,
  `total_expenses` decimal(12,2) NOT NULL,
  `net_income` decimal(12,2) NOT NULL,
  `note` longtext DEFAULT NULL,
  `receipt` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale_detailedsale`
--

INSERT INTO `sale_detailedsale` (`id`, `sale_date`, `crops`, `transport_details`, `buyer_details`, `payment_details`, `total_sale_amount`, `total_expenses`, `net_income`, `note`, `receipt`, `created_at`, `user_id`) VALUES
(1, '2025-06-23', '[{\"crop_name\": \"Wheat\", \"bags\": 10, \"weight_per_bag\": 50, \"total_weight\": 500, \"rate_per_kg\": 20, \"total_amount\": 10000}]', '{\"vehicle_type\": \"Truck\", \"vehicle_number\": \"HR26AB1234\", \"driver_name\": \"Ramesh\", \"driver_mobile\": \"9999999999\", \"transport_cost\": 1000, \"loading_unloading_cost\": 500}', '{\"buyer_name\": \"Mohan\", \"buyer_mobile\": \"8888888888\", \"market_location\": \"Agra\"}', '{\"payment_method\": \"UPI\", \"payment_note\": \"Paid full\"}', 10000.00, 1500.00, 8500.00, 'Detailed sale test', '', '2025-07-05 10:43:23.911299', 5);

-- --------------------------------------------------------

--
-- Table structure for table `sale_quicksale`
--

CREATE TABLE `sale_quicksale` (
  `id` bigint(20) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `note` longtext DEFAULT NULL,
  `receipt` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sale_quicksale`
--

INSERT INTO `sale_quicksale` (`id`, `amount`, `note`, `receipt`, `created_at`, `user_id`) VALUES
(1, 10000.00, 'Quick sale test', '', '2025-07-05 10:29:58.364246', 5);

-- --------------------------------------------------------

--
-- Table structure for table `shop_shop`
--

CREATE TABLE `shop_shop` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `shop_type` varchar(100) NOT NULL,
  `mobile_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shop_shop`
--

INSERT INTO `shop_shop` (`id`, `name`, `shop_type`, `mobile_number`, `address`, `notes`, `created_at`, `user_id`) VALUES
(1, 'Krishi Kendra', 'Fertilizer', '9876543210', 'Main Market', 'Trusted vendor', '2025-07-05 10:13:59.971351', 5);

-- --------------------------------------------------------

--
-- Table structure for table `task_task`
--

CREATE TABLE `task_task` (
  `id` bigint(20) NOT NULL,
  `task_name` varchar(200) NOT NULL,
  `category` varchar(50) NOT NULL,
  `crop` varchar(100) NOT NULL,
  `field` varchar(100) NOT NULL,
  `start_datetime` datetime(6) NOT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `reminder` varchar(50) NOT NULL,
  `assigned_to` varchar(100) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `weather_sensitive` tinyint(1) NOT NULL,
  `details` longtext NOT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `task_task`
--

INSERT INTO `task_task` (`id`, `task_name`, `category`, `crop`, `field`, `start_datetime`, `end_datetime`, `reminder`, `assigned_to`, `priority`, `weather_sensitive`, `details`, `is_completed`, `created_at`, `user_id`) VALUES
(1, 'Task2', 'Irrigation', 'Wheat', 'Field V', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-1', 'Low', 0, '', 1, '2025-06-29 14:36:28.313668', 5),
(2, 'Task2', 'Irrigation', 'Wheat', 'Field V', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-1', 'Low', 0, '', 0, '2025-06-29 14:43:19.142422', 5),
(3, 'Tasks', 'Irrigation', 'crop', 'Field', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-4', 'Low', 0, '', 0, '2025-06-29 15:58:40.067371', 5),
(4, 'Task6', 'Other', 'Wheat', 'Field V', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-1', 'High', 0, '', 0, '2025-06-29 16:16:17.395162', 5),
(5, 'Task2', 'Irrigation', 'Wheat', 'Field V', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-1', 'Low', 0, '', 0, '2025-07-05 08:32:11.214636', 5),
(6, 'Gopal Task', 'Irrigation', 'Wheat', 'Field V', '2025-06-23 00:00:00.000000', NULL, '15 minutes before', 'Labour-1', 'Low', 0, '', 0, '2025-07-05 09:28:11.493465', 5),
(7, 'Gopal create task', 'Irrigation', 'Wheat', 'East Field', '2025-07-06 04:59:00.000000', '2025-07-06 04:59:00.000000', '15 minutes before', 'John Smith', 'Low', 1, 'water irrigation', 0, '2025-07-06 05:00:10.639301', 5);

-- --------------------------------------------------------

--
-- Table structure for table `userprofile_userprofile`
--

CREATE TABLE `userprofile_userprofile` (
  `id` bigint(20) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `language` varchar(50) NOT NULL,
  `timezone` varchar(50) NOT NULL,
  `push_notification` tinyint(1) NOT NULL,
  `advisory_alert` tinyint(1) NOT NULL,
  `auto_backup` tinyint(1) NOT NULL,
  `share_on_whatsapp` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userprofile_userprofile`
--

INSERT INTO `userprofile_userprofile` (`id`, `location`, `language`, `timezone`, `push_notification`, `advisory_alert`, `auto_backup`, `share_on_whatsapp`, `user_id`) VALUES
(5, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 5),
(6, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 6),
(7, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 7),
(8, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 8),
(9, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 9),
(10, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 10),
(11, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 11),
(12, NULL, 'English', 'Asia/Kolkata', 1, 0, 1, 0, 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_otp`
--
ALTER TABLE `accounts_otp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_otp_user_id_7275536e_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `accounts_plan`
--
ALTER TABLE `accounts_plan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `accounts_user`
--
ALTER TABLE `accounts_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `mobile` (`mobile`),
  ADD KEY `accounts_user_plan_id_954973d5_fk_accounts_plan_id` (`plan_id`);

--
-- Indexes for table `accounts_userplan`
--
ALTER TABLE `accounts_userplan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `accounts_userplan_plan_id_09e522df_fk_accounts_plan_id` (`plan_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `crop_crop`
--
ALTER TABLE `crop_crop`
  ADD PRIMARY KEY (`id`),
  ADD KEY `crop_crop_user_id_5fcd7f54_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `crop_plan`
--
ALTER TABLE `crop_plan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `device_device`
--
ALTER TABLE `device_device`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_device_user_id_f5cc8c87_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `expenses_expense`
--
ALTER TABLE `expenses_expense`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bill_no` (`bill_no`),
  ADD KEY `expenses_expense_shop_id_4ed22fa3_fk_shop_shop_id` (`shop_id`),
  ADD KEY `expenses_expense_user_id_ab1aae2b_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `labour_attendance`
--
ALTER TABLE `labour_attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `labour_attendance_labour_id_c46997f4_fk_labour_labour_id` (`labour_id`);

--
-- Indexes for table `labour_labour`
--
ALTER TABLE `labour_labour`
  ADD PRIMARY KEY (`id`),
  ADD KEY `labour_labour_user_id_bda9972d_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `sale_detailedsale`
--
ALTER TABLE `sale_detailedsale`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sale_detailedsale_user_id_2481e1fd_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `sale_quicksale`
--
ALTER TABLE `sale_quicksale`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sale_quicksale_user_id_3ce1a1d4_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `shop_shop`
--
ALTER TABLE `shop_shop`
  ADD PRIMARY KEY (`id`),
  ADD KEY `shop_shop_user_id_2ca99439_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `task_task`
--
ALTER TABLE `task_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Task_task_user_id_284e1ae7_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `userprofile_userprofile`
--
ALTER TABLE `userprofile_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_otp`
--
ALTER TABLE `accounts_otp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `accounts_plan`
--
ALTER TABLE `accounts_plan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `accounts_user`
--
ALTER TABLE `accounts_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `accounts_userplan`
--
ALTER TABLE `accounts_userplan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `crop_crop`
--
ALTER TABLE `crop_crop`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `crop_plan`
--
ALTER TABLE `crop_plan`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `device_device`
--
ALTER TABLE `device_device`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `expenses_expense`
--
ALTER TABLE `expenses_expense`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `labour_attendance`
--
ALTER TABLE `labour_attendance`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `labour_labour`
--
ALTER TABLE `labour_labour`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `sale_detailedsale`
--
ALTER TABLE `sale_detailedsale`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sale_quicksale`
--
ALTER TABLE `sale_quicksale`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `shop_shop`
--
ALTER TABLE `shop_shop`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `task_task`
--
ALTER TABLE `task_task`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `userprofile_userprofile`
--
ALTER TABLE `userprofile_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_otp`
--
ALTER TABLE `accounts_otp`
  ADD CONSTRAINT `accounts_otp_user_id_7275536e_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user`
--
ALTER TABLE `accounts_user`
  ADD CONSTRAINT `accounts_user_plan_id_954973d5_fk_accounts_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `accounts_plan` (`id`);

--
-- Constraints for table `accounts_userplan`
--
ALTER TABLE `accounts_userplan`
  ADD CONSTRAINT `accounts_userplan_plan_id_09e522df_fk_accounts_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `accounts_plan` (`id`),
  ADD CONSTRAINT `accounts_userplan_user_id_0bbb76de_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `crop_crop`
--
ALTER TABLE `crop_crop`
  ADD CONSTRAINT `crop_crop_user_id_5fcd7f54_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `device_device`
--
ALTER TABLE `device_device`
  ADD CONSTRAINT `device_device_user_id_f5cc8c87_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `expenses_expense`
--
ALTER TABLE `expenses_expense`
  ADD CONSTRAINT `expenses_expense_shop_id_4ed22fa3_fk_shop_shop_id` FOREIGN KEY (`shop_id`) REFERENCES `shop_shop` (`id`),
  ADD CONSTRAINT `expenses_expense_user_id_ab1aae2b_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `labour_attendance`
--
ALTER TABLE `labour_attendance`
  ADD CONSTRAINT `labour_attendance_labour_id_c46997f4_fk_labour_labour_id` FOREIGN KEY (`labour_id`) REFERENCES `labour_labour` (`id`);

--
-- Constraints for table `labour_labour`
--
ALTER TABLE `labour_labour`
  ADD CONSTRAINT `labour_labour_user_id_bda9972d_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `sale_detailedsale`
--
ALTER TABLE `sale_detailedsale`
  ADD CONSTRAINT `sale_detailedsale_user_id_2481e1fd_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `sale_quicksale`
--
ALTER TABLE `sale_quicksale`
  ADD CONSTRAINT `sale_quicksale_user_id_3ce1a1d4_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `shop_shop`
--
ALTER TABLE `shop_shop`
  ADD CONSTRAINT `shop_shop_user_id_2ca99439_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `task_task`
--
ALTER TABLE `task_task`
  ADD CONSTRAINT `Task_task_user_id_284e1ae7_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `userprofile_userprofile`
--
ALTER TABLE `userprofile_userprofile`
  ADD CONSTRAINT `userprofile_userprofile_user_id_59dda034_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
