-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 17 Şub 2020, 16:03:13
-- Sunucu sürümü: 10.4.11-MariaDB
-- PHP Sürümü: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `personal`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ability`
--

CREATE TABLE `ability` (
  `abiltyId` int(8) NOT NULL,
  `abiltyName` text NOT NULL,
  `abiltyLevel` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `ability`
--

INSERT INTO `ability` (`abiltyId`, `abiltyName`, `abiltyLevel`) VALUES
(1, ' Software Development', 'professional'),
(3, 'Cooking', ' professional'),
(4, 'Analytical thinking', ' professional'),
(5, 'Planning', ' professional'),
(6, 'search solving to problems', ' professional');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `about`
--

CREATE TABLE `about` (
  `aboutInformation` text NOT NULL,
  `aboutId` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `about`
--

INSERT INTO `about` (`aboutInformation`, `aboutId`) VALUES
('Having an idea that aims to follow and examine the developing technology closely is the most important thing for a software developer.', 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `certificate`
--

CREATE TABLE `certificate` (
  `certificateId` int(8) NOT NULL,
  `certificateName` text NOT NULL,
  `certificateTime` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `certificate`
--

INSERT INTO `certificate` (`certificateId`, `certificateName`, `certificateTime`) VALUES
(1, '(42 Saat) Python : Sıfırdan İleri Seviye Programlama (2019)', '01-07-2019'),
(2, 'Her Seviyeye Uygun Uçtan Uca Veri Bilimi, Knime ile ', '01-08-2019'),
(5, 'İşaret Dili Eğitimi ', '01-05-2019'),
(6, 'Sosyal Medya Uzmanlığı Eğitimi ', '01-09-2018'),
(7, 'İngilizce(B1-B2) Eğitimi ', '01-09-2018'),
(8, 'Digital Atölye', '01-06-2017'),
(9, ' Etik Hacker Olma Kursu', '');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contact`
--

CREATE TABLE `contact` (
  `contactId` int(8) NOT NULL,
  `contactHeader` text NOT NULL,
  `contactName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `contact`
--

INSERT INTO `contact` (`contactId`, `contactHeader`, `contactName`) VALUES
(1, 'Mobile Phone ', '05469301472'),
(3, 'Mail', 'kuffar35@gmail.com'),
(4, 'Githup', 'https://github.com/kuffar35'),
(5, 'Instagram', 'https://www.instagram.com/kuffar35'),
(6, 'Twitter', 'https://twitter.com/kuffar35'),
(7, 'Linked', 'https://www.linkedin.com/in/kuffar35');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `education`
--

CREATE TABLE `education` (
  `educationId` int(8) NOT NULL,
  `firstEducation` text NOT NULL,
  `secondEducation` text NOT NULL,
  `universityEducation` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `education`
--

INSERT INTO `education` (`educationId`, `firstEducation`, `secondEducation`, `universityEducation`) VALUES
(1, '80.yıl metaş İ.Ö.O', 'mithatpaşa A.T.L', 'Dokuz Eylül Universty');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `hobby`
--

CREATE TABLE `hobby` (
  `hobbyId` int(8) NOT NULL,
  `hobbyName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `hobby`
--

INSERT INTO `hobby` (`hobbyId`, `hobbyName`) VALUES
(1, 'Drawing');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `language`
--

CREATE TABLE `language` (
  `languageId` int(8) NOT NULL,
  `languageName` text NOT NULL,
  `languageLevel` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `language`
--

INSERT INTO `language` (`languageId`, `languageName`, `languageLevel`) VALUES
(1, 'English', 'professional'),
(3, 'Chinnes', 'beginner'),
(4, 'Japanese', 'beginner');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `login`
--

CREATE TABLE `login` (
  `login_id` int(8) NOT NULL,
  `login_name` text NOT NULL,
  `login_pass` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `login`
--

INSERT INTO `login` (`login_id`, `login_name`, `login_pass`) VALUES
(1, 'kuffar', '181172561121');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `personal_information`
--

CREATE TABLE `personal_information` (
  `name` text NOT NULL,
  `lastname` text NOT NULL,
  `adress` text NOT NULL,
  `phone` text NOT NULL,
  `mail` text NOT NULL,
  `drivinglicence` text NOT NULL,
  `InformationId` int(8) NOT NULL,
  `bloodgroup` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `personal_information`
--

INSERT INTO `personal_information` (`name`, `lastname`, `adress`, `phone`, `mail`, `drivinglicence`, `InformationId`, `bloodgroup`) VALUES
('ömer faruk', 'nar', 'Izmir / Turkey', '+09 546 930 14 72', 'kuffar35@gmail.com', 'Yes', 1, 'A (+)');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `project`
--

CREATE TABLE `project` (
  `projectId` int(8) NOT NULL,
  `projectName` text NOT NULL,
  `projectUrl` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `project`
--

INSERT INTO `project` (`projectId`, `projectName`, `projectUrl`) VALUES
(3, 'mail send', 'https://github.com/kuffar35/mail-send'),
(4, 'blog web page', 'https://github.com/kuffar35/blog-web-page'),
(5, 'footballgame', 'https://github.com/kuffar35/footballgame'),
(6, 'personalwebpagewithPHP', 'https://github.com/kuffar35/personalwebpagewithPHP'),
(7, 'automatich_instagram', 'https://github.com/kuffar35/automatich_instagram'),
(8, 'burgerCapture', 'https://github.com/kuffar35/burgerCapture');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `ability`
--
ALTER TABLE `ability`
  ADD PRIMARY KEY (`abiltyId`);

--
-- Tablo için indeksler `about`
--
ALTER TABLE `about`
  ADD PRIMARY KEY (`aboutId`);

--
-- Tablo için indeksler `certificate`
--
ALTER TABLE `certificate`
  ADD PRIMARY KEY (`certificateId`);

--
-- Tablo için indeksler `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`contactId`);

--
-- Tablo için indeksler `education`
--
ALTER TABLE `education`
  ADD PRIMARY KEY (`educationId`);

--
-- Tablo için indeksler `hobby`
--
ALTER TABLE `hobby`
  ADD PRIMARY KEY (`hobbyId`);

--
-- Tablo için indeksler `language`
--
ALTER TABLE `language`
  ADD PRIMARY KEY (`languageId`);

--
-- Tablo için indeksler `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`login_id`);

--
-- Tablo için indeksler `personal_information`
--
ALTER TABLE `personal_information`
  ADD PRIMARY KEY (`InformationId`);

--
-- Tablo için indeksler `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`projectId`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `ability`
--
ALTER TABLE `ability`
  MODIFY `abiltyId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Tablo için AUTO_INCREMENT değeri `about`
--
ALTER TABLE `about`
  MODIFY `aboutId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `certificate`
--
ALTER TABLE `certificate`
  MODIFY `certificateId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Tablo için AUTO_INCREMENT değeri `contact`
--
ALTER TABLE `contact`
  MODIFY `contactId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Tablo için AUTO_INCREMENT değeri `education`
--
ALTER TABLE `education`
  MODIFY `educationId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `hobby`
--
ALTER TABLE `hobby`
  MODIFY `hobbyId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `language`
--
ALTER TABLE `language`
  MODIFY `languageId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `login`
--
ALTER TABLE `login`
  MODIFY `login_id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `personal_information`
--
ALTER TABLE `personal_information`
  MODIFY `InformationId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `project`
--
ALTER TABLE `project`
  MODIFY `projectId` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
