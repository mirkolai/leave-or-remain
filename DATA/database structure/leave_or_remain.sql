SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `leave or remain`
--

-- --------------------------------------------------------

--
-- Table structure for table `resources_parties`
--

CREATE TABLE IF NOT EXISTS `resources_parties` (
  `url` varchar(250) NOT NULL,
  `alias` varchar(250) NOT NULL,
  `stance` varchar(250) NOT NULL,
  PRIMARY KEY (`url`,`alias`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `resources_politics`
--

CREATE TABLE IF NOT EXISTS `resources_politics` (
  `url` varchar(250) NOT NULL,
  `alias` varchar(250) NOT NULL,
  `party` varchar(250) NOT NULL,
  `stance` varchar(250) NOT NULL,
  PRIMARY KEY (`url`,`alias`,`party`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_crowdflower_aggregate`
--

CREATE TABLE IF NOT EXISTS `sample_1_crowdflower_aggregate` (
  `_unit_id` int(10) NOT NULL DEFAULT '0',
  `_golden` varchar(5) DEFAULT NULL,
  `_unit_state` varchar(9) DEFAULT NULL,
  `_trusted_judgments` int(2) DEFAULT NULL,
  `_last_judgment_at` varchar(18) DEFAULT NULL,
  `what_is_the_stance_of_the_user_that_wrote_those_three_messages` varchar(12) DEFAULT NULL,
  `what_is_the_stance_of_the_user:confidence` decimal(5,4) DEFAULT NULL,
  `content` varchar(474) DEFAULT NULL,
  `ids` varchar(56) DEFAULT NULL,
  `what_is_the_stance_of_the_user_gold` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`_unit_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_row`
--

CREATE TABLE IF NOT EXISTS `sample_1_row` (
  `user_id` bigint(20) NOT NULL,
  `phase` int(11) NOT NULL,
  `index` int(11) NOT NULL,
  `tweet_id_1` bigint(20) NOT NULL,
  `tweet_id_2` bigint(20) NOT NULL,
  `tweet_id_3` bigint(20) NOT NULL,
  `text_1` varchar(2500) NOT NULL,
  `text_2` varchar(2500) NOT NULL,
  `text_3` varchar(2500) NOT NULL,
  PRIMARY KEY (`user_id`,`phase`,`index`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_row_stance_confidence`
--

CREATE TABLE IF NOT EXISTS `sample_1_row_stance_confidence` (
  `user_id` bigint(20) NOT NULL,
  `phase` int(11) NOT NULL,
  `index` int(11) NOT NULL,
  `tweet_id_1` bigint(20) NOT NULL,
  `tweet_id_2` bigint(20) NOT NULL,
  `tweet_id_3` bigint(20) NOT NULL,
  `text_1` varchar(2500) NOT NULL,
  `text_2` varchar(2500) NOT NULL,
  `text_3` varchar(2500) NOT NULL,
  `stance` varchar(50) NOT NULL,
  `confidence` float NOT NULL,
  `contributors` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`phase`,`index`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_row_stance_confidence_user`
--

CREATE TABLE IF NOT EXISTS `sample_1_row_stance_confidence_user` (
  `user_id` bigint(20) NOT NULL,
  `stance_1` varchar(45) NOT NULL,
  `stance_2` varchar(45) NOT NULL,
  `stance_3` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_training_corpus`
--

CREATE TABLE IF NOT EXISTS `sample_1_training_corpus` (
  `id` bigint(20) NOT NULL,
  `text` varchar(1500) DEFAULT NULL,
  `phase` int(11) DEFAULT NULL,
  `stance` varchar(7) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_training_corpus_for_user`
--

CREATE TABLE IF NOT EXISTS `sample_1_training_corpus_for_user` (
  `id_1` bigint(20) NOT NULL,
  `text_1` varchar(1500) DEFAULT NULL,
  `id_2` bigint(20) NOT NULL,
  `text_2` varchar(1500) NOT NULL,
  `id_3` bigint(20) NOT NULL,
  `text_3` varchar(1500) NOT NULL,
  `phase` int(11) DEFAULT NULL,
  `stance` varchar(7) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id_1`,`id_2`,`id_3`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sample_1_user_selected`
--

CREATE TABLE IF NOT EXISTS `sample_1_user_selected` (
  `user_id` bigint(20) NOT NULL,
  `screen_name` varchar(250) NOT NULL,
  `phase_1` int(11) NOT NULL,
  `phase_2` int(11) NOT NULL,
  `phase_3` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tweet_phase`
--

CREATE TABLE IF NOT EXISTS `tweet_phase` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `screen_name` varchar(250) NOT NULL,
  `text` varchar(2500) NOT NULL,
  `date` datetime NOT NULL,
  `phase` int(11) NOT NULL,
  `retweet` int(11) NOT NULL,
  `reply` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` bigint(20) NOT NULL,
  `screen_name` varchar(250) NOT NULL,
  `phase_1` int(11) NOT NULL,
  `phase_2` int(11) NOT NULL,
  `phase_3` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_friends_relation`
--

CREATE TABLE IF NOT EXISTS `user_friends_relation` (
  `source` bigint(20) NOT NULL,
  `target` bigint(20) NOT NULL,
  PRIMARY KEY (`source`,`target`),
  KEY `target` (`target`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_friends_relation_communities`
--

CREATE TABLE IF NOT EXISTS `user_friends_relation_communities` (
  `id` bigint(20) NOT NULL,
  `community` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
