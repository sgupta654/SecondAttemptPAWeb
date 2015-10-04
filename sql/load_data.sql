use group36;
INSERT INTO User (username, firstname, lastname, password, email)
  VALUES ('sportslover', 'Paul', 'Walker', '2fast2furious', 'sportslover@hotmail.com');

INSERT INTO User (username, firstname, lastname, password, email)
  VALUES ('traveler', 'Rebecca', 'Travolta', 'doesHeLookLikeaBitch', 'rebt@explorer.org');

INSERT INTO User (username, firstname, lastname, password, email)
  VALUES ('spacejunkie', 'Bob', 'Spacey', 'xX420blaze_itXx', 'bspace@spacejunkies.net');

INSERT INTO Album (title, created, lastupdated, username, access)
  VALUES ('I love sports', '2014-09-15', '2015-09-15', 'sportslover', 'public'),
  ('I love football', '2001-10-25', '2012-04-20', 'sportslover', 'private'),
  ('Around The World', '2004-03-13', '2007-07-30', 'traveler', 'private'),
  ('Cool Space Shots', '2003-08-02', '2010-11-14', 'spacejunkie', 'private');

INSERT INTO Photo (picid, url, format, date)
VALUES ('football_s1', 'football_s1.jpg', 'jpg', '2015-09-18'),
('football_s2', 'football_s2.jpg', 'jpg', '2015-09-18'),
('football_s3', 'football_s3.jpg', 'jpg', '2015-09-18'),
('football_s4', 'football_s4.jpg', 'jpg', '2015-09-18'),
('space_EagleNebula', 'space_EagleNebula.jpg', 'jpg', '2015-09-18'),
('space_GalaxyCollision', 'space_GalaxyCollision.jpg', 'jpg', '2015-09-18'),
('space_HelixNebula', 'space_HelixNebula.jpg', 'jpg', '2015-09-18'),
('space_MilkyWay', 'space_MilkyWay.jpg', 'jpg', '2015-09-18'),
('space_OrionNebula', 'space_OrionNebula.jpg', 'jpg', '2015-09-18'),
('sports_s1', 'sports_s1.jpg', 'jpg', '2015-09-18'),
('sports_s2', 'sports_s2.jpg', 'jpg', '2015-09-18'),
('sports_s3', 'sports_s3.jpg', 'jpg', '2015-09-18'),
('sports_s4', 'sports_s4.jpg', 'jpg', '2015-09-18'),
('sports_s5', 'sports_s5.jpg', 'jpg', '2015-09-18'),
('sports_s6', 'sports_s6.jpg', 'jpg', '2015-09-18'),
('sports_s7', 'sports_s7.jpg', 'jpg', '2015-09-18'),
('sports_s8', 'sports_s8.jpg', 'jpg', '2015-09-18'),
('world_EiffelTower', 'world_EiffelTower.jpg', 'jpg', '2015-09-18'),
('world_firenze', 'world_firenze.jpg', 'jpg', '2015-09-18'),
('world_GreatWall', 'world_GreatWall.jpg', 'jpg', '2015-09-18'),
('world_Isfahan', 'world_Isfahan.jpg', 'jpg', '2015-09-18'),
('world_Istanbul', 'world_Istanbul.jpg', 'jpg', '2015-09-18'),
('world_Persepolis', 'world_Persepolis.jpg', 'jpg', '2015-09-18'),
('world_Reykjavik', 'world_Reykjavik.jpg', 'jpg', '2015-09-18'),
('world_Seoul', 'world_Seoul.jpg', 'jpg', '2015-09-18'),
('world_Stonehenge', 'world_Stonehenge.jpg', 'jpg', '2015-09-18'),
('world_TajMahal', 'world_TajMahal.jpg', 'jpg', '2015-09-18'),
('world_TelAviv', 'world_TelAviv.jpg', 'jpg', '2015-09-18'),
('world_tokyo', 'world_tokyo.jpg', 'jpg', '2015-09-18'),
('world_WashingtonDC', 'world_WashingtonDC.jpg', 'jpg', '2015-09-18');

INSERT INTO Contain (albumid, picid, caption, sequencenum)
VALUES (1, 'sports_s1', 'sports', 0),
(1, 'sports_s2', 'sports', 1),
(1, 'sports_s3', 'sports', 2),
(1, 'sports_s4', 'sports', 3),
(1, 'sports_s5', 'sports', 4),
(1, 'sports_s6', 'sports', 5),
(1, 'sports_s7', 'sports', 6),
(1, 'sports_s8', 'sports', 7),
(2, 'football_s1', 'football', 0),
(2, 'football_s2', 'football', 1),
(2, 'football_s3', 'football', 2),
(2, 'football_s4', 'football', 3),
(3, 'world_EiffelTower', 'Traveling', 0),
(3, 'world_firenze', 'Traveling', 1),
(3, 'world_GreatWall', 'Traveling', 2),
(3, 'world_Isfahan', 'Traveling', 3),
(3, 'world_Istanbul', 'Traveling', 4),
(3, 'world_Persepolis', 'Traveling', 5),
(3, 'world_Reykjavik', 'Traveling', 6),
(3, 'world_Seoul', 'Traveling', 7),
(3, 'world_Stonehenge', 'Traveling', 8),
(3, 'world_TajMahal', 'Traveling', 9),
(3, 'world_TelAviv', 'Traveling', 10),
(3, 'world_tokyo', 'Traveling', 11),
(3, 'world_WashingtonDC', 'Traveling', 12),
(4, 'space_EagleNebula', 'Space', 0),
(4, 'space_GalaxyCollision', 'Space', 1),
(4, 'space_HelixNebula', 'Space', 2),
(4, 'space_MilkyWay', 'Space', 3),
(4, 'space_OrionNebula', 'Space', 4);

INSERT INTO AlbumAccess (albumid, username)
VALUES (1, 'traveler'),
(1, 'spacejunkie'),
(2, 'traveler'),
(3, 'sportslover'),
(3, 'spacejunkie'),
(4, 'sportslover');
