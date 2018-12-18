-- remove unneeded tables
DROP TABLE Scrambles;
DROP TABLE championships;
DROP TABLE eligible_country_iso2s_for_championship;
DROP TABLE Rounds;

-- rename tables
ALTER TABLE Competitions RENAME TO temp_competition;
ALTER TABLE Results RENAME TO temp_result;
ALTER TABLE RanksAverage RENAME TO temp_rank_average;
ALTER TABLE RanksSingle RENAME TO temp_rank_single;
ALTER TABLE Persons RENAME TO temp_person;
ALTER TABLE Countries RENAME TO temp_country;
ALTER TABLE Continents RENAME TO temp_continent;
ALTER TABLE Events RENAME TO temp_event;
ALTER TABLE Formats RENAME TO temp_event_format;
ALTER TABLE RoundTypes RENAME TO temp_round_type;

-- create tables with relationships
CREATE TABLE continent (
  continent_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  continent_identifier varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  continent_name varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  record_name char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  latitude int(11) NOT NULL DEFAULT '0',
  longitude int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (continent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE event (
  event_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  event_identifier varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  event_name varchar(54) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `rank` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE event_format (
  event_format_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  event_format_identifier char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  event_format_name varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  sort_by varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  sort_by_second varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  expected_solve_count int(11) NOT NULL,
  trim_fastest_n int(11) NOT NULL,
  trim_slowest_n int(11) NOT NULL,
  PRIMARY KEY (event_format_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE round_type (
  round_type_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  round_type_identifier char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `rank` int(11) NOT NULL DEFAULT '0',
  round_type_name varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  final tinyint(1) NOT NULL,
  PRIMARY KEY (round_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT IGNORE INTO continent (continent_identifier, continent_name, record_name, latitude, longitude)
SELECT c.continent_identifier,
c.continent_name,
c.record_name,
c.latitude,
c.longitude
  FROM temp_continent c;

INSERT IGNORE INTO event (event_identifier, event_name, `rank`)
SELECT e.event_identifier, e.event_name, e.rank
  FROM temp_event e
  ORDER BY e.event_identifier;

INSERT IGNORE INTO event_format (event_format_identifier, event_format_name, sort_by, sort_by_second, expected_solve_count, trim_fastest_n, trim_slowest_n )
SELECT ef.event_format_identifier,
ef.event_format_name,
ef.sort_by,
ef.sort_by_second,
ef.expected_solve_count,
ef.trim_fastest_n,
ef.trim_slowest_n
  FROM temp_event_format ef;

INSERT IGNORE INTO round_type (round_type_identifier, `rank`, round_type_name, final)
SELECT rt.round_type_identifier,
rt.rank,
rt.round_type_name,
rt.final
  FROM temp_round_type rt;

-- clean up columns
ALTER TABLE continent RENAME COLUMN id TO continent_identifier;
ALTER TABLE continent RENAME COLUMN name TO continent_name;
ALTER TABLE continent RENAME COLUMN recordName TO record_name;
ALTER TABLE continent DROP COLUMN zoom;

ALTER TABLE event RENAME COLUMN id TO event_identifier;
ALTER TABLE event RENAME COLUMN name TO event_name;
ALTER TABLE event DROP COLUMN cellName;
ALTER TABLE event DROP COLUMN format;

ALTER TABLE event_format RENAME COLUMN id TO event_format_identifier;
ALTER TABLE event_format RENAME COLUMN name TO event_format_name;

ALTER TABLE round_type RENAME COLUMN id TO round_type_identifier;
ALTER TABLE round_type RENAME COLUMN name TO round_type_name;
ALTER TABLE round_type DROP COLUMN cellName;

ALTER TABLE temp_country RENAME COLUMN id TO country_identifier;
ALTER TABLE temp_country RENAME COLUMN name TO country_name;
ALTER TABLE temp_country RENAME COLUMN continentId TO continent_id;
ALTER TABLE temp_country DROP COLUMN iso2;


ALTER TABLE temp_person RENAME COLUMN id TO person_identifier;
ALTER TABLE temp_person RENAME COLUMN name TO person_name;
ALTER TABLE temp_person RENAME COLUMN countryId TO country_id;
-- create person table with unique WCA ID (sub id contains the most updated information)
CREATE TABLE person AS (
    SELECT * FROM temp_person WHERE subid = 1
);
-- delete subid
ALTER TABLE temp_person DROP COLUMN subid;

ALTER TABLE temp_result RENAME COLUMN competitionId TO competition_id;
ALTER TABLE temp_result RENAME COLUMN eventId TO event_id;
ALTER TABLE temp_result RENAME COLUMN roundTypeId TO round_type_id;
ALTER TABLE temp_result RENAME COLUMN personName TO person_name;
ALTER TABLE temp_result RENAME COLUMN personId TO person_id;
ALTER TABLE temp_result RENAME COLUMN formatId TO event_format_id;

ALTER TABLE temp_rank_average RENAME COLUMN personId TO person_id;
ALTER TABLE temp_rank_average RENAME COLUMN eventId TO event_id;
ALTER TABLE temp_rank_average RENAME COLUMN worldRank TO world_rank;
ALTER TABLE temp_rank_average RENAME COLUMN continentRank TO continent_rank;
ALTER TABLE temp_rank_average RENAME COLUMN countryRank TO country_rank;

ALTER TABLE temp_rank_single RENAME COLUMN personId TO person_id;
ALTER TABLE temp_rank_single RENAME COLUMN eventId TO event_id;
ALTER TABLE temp_rank_single RENAME COLUMN worldRank TO world_rank;
ALTER TABLE temp_rank_single RENAME COLUMN continentRank TO continent_rank;
ALTER TABLE temp_rank_single RENAME COLUMN countryRank TO country_rank;



-- create relationships
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE country (
  country_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  country_identifier VARCHAR(50) NOT NULL,
  country_name VARCHAR(50) NOT NULL,
  continent_id INTEGER NOT NULL,
  PRIMARY KEY (country_id),
  FOREIGN KEY (continent_id) REFERENCES continent(continent_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO country (country_identifier, country_name, continent_id)
SELECT IF(TRIM(tcou.country_identifier) = '', NULL, TRIM(tcou.country_identifier)),
       IF(TRIM(tcou.country_name) = '', NULL, TRIM(tcou.country_name)),
       con.continent_id
  FROM temp_country tcou
       LEFT JOIN continent con
              ON TRIM(tcou.continent_identifier) = TRIM(con.continent_identifier)
ORDER BY tcou.country_id;

-- competition
CREATE TABLE competition (
  competition_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  competition_identifier varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  competition_name varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  city_name varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  country_id INTEGER NOT NULL,
  information mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  year smallint(5) unsigned NOT NULL DEFAULT '0',
  month smallint(5) unsigned NOT NULL DEFAULT '0',
  day smallint(5) unsigned NOT NULL DEFAULT '0',
  end_month smallint(5) unsigned NOT NULL DEFAULT '0',
  end_day smallint(5) unsigned NOT NULL DEFAULT '0',
  event_specs varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  wca_delegate text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  organiser text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  venue varchar(240) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  venue_address varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  venue_details varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  external_website varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  latitude int(11) DEFAULT NULL,
  longitude int(11) DEFAULT NULL,
  PRIMARY KEY (competition_id),
  FOREIGN KEY (country_id) REFERENCES country(country_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT IGNORE INTO competition (competition_id, competition_identifier, competition_name, city_name, country_id, information, year, month, day, end_month, end_day, event_specs, wca_delegate, organiser, venue, venue_address, external_website, latitude, longitude)
SELECT IF(TRIM(tcomp.competition_id) = '', NULL, TRIM(tcomp.competition_id)),
IF(TRIM(tcomp.competition_identifier) = '', NULL, TRIM(tcomp.competition_identifier)), 
IF(TRIM(tcomp.competition_name) = '', NULL, TRIM(tcomp.competition_name)), 
IF(TRIM(tcomp.city_name) = '', NULL, TRIM(tcomp.city_name)), 
con.country_id,
IF(TRIM(tcomp.information) = '', NULL, TRIM(tcomp.information)), 
IF(TRIM(tcomp.year) = '', NULL, TRIM(tcomp.year)), 
IF(TRIM(tcomp.month) = '', NULL, TRIM(tcomp.month)), 
IF(TRIM(tcomp.day) = '', NULL, TRIM(tcomp.day)), 
IF(TRIM(tcomp.end_month) = '', NULL, TRIM(tcomp.end_month)), 
IF(TRIM(tcomp.end_day) = '', NULL, TRIM(tcomp.end_day)), 
IF(TRIM(tcomp.event_specs) = '', NULL, TRIM(tcomp.event_specs)), 
IF(TRIM(tcomp.wca_delegate) = '', NULL, TRIM(tcomp.wca_delegate)), 
IF(TRIM(tcomp.organiser) = '', NULL, TRIM(tcomp.organiser)), 
IF(TRIM(tcomp.venue) = '', NULL, TRIM(tcomp.venue)), 
IF(TRIM(tcomp.venue_address) = '', NULL, TRIM(tcomp.venue_address)), 
IF(TRIM(tcomp.external_website) = '', NULL, TRIM(tcomp.external_website)), 
IF(TRIM(tcomp.latitude) = '', NULL, TRIM(tcomp.latitude)), 
IF(TRIM(tcomp.longitude) = '', NULL, TRIM(tcomp.longitude))
  FROM temp_competition tcomp
       LEFT JOIN country con
              ON tcomp.country_identifier = con.country_identifier
ORDER BY tcomp.competition_id;

-- person
CREATE TABLE person (
  person_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  person_identifier varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  person_name varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  country_id INTEGER NOT NULL,
  gender char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (person_id),
  FOREIGN KEY (country_id) REFERENCES country(country_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO person (person_id, person_identifier, person_name, country_id, gender)
SELECT p.person_id,
p.person_identifier,
p.person_name,
con.country_id,
p.gender
  FROM temp_person p
       LEFT JOIN country con
              ON TRIM(p.country_identifier) = TRIM(con.country_identifier)
ORDER BY p.person_id;

-- rank_average
CREATE TABLE rank_average (
  rank_average_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  person_id INTEGER NOT NULL,
  event_id INTEGER NOT NULL,
  best int(11) NOT NULL DEFAULT '0',
  world_rank int(11) NOT NULL DEFAULT '0',
  continent_rank int(11) NOT NULL DEFAULT '0',
  country_rank int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (rank_average_id),
  FOREIGN KEY (person_id) REFERENCES person(person_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT IGNORE INTO rank_average (rank_average_id, person_id, event_id, best, world_rank, continent_rank, country_rank)
SELECT ra.rank_average_id,
p.person_id,
e.event_id,
ra.best,
ra.world_rank,
ra.continent_rank,
ra.country_rank
  FROM temp_rank_average ra
        LEFT JOIN person p
              ON TRIM(ra.person_identifier) = TRIM(p.person_identifier)
        LEFT JOIN event e
              ON TRIM(ra.event_identifier) = TRIM(e.event_identifier)
ORDER BY ra.rank_average_id;

-- rank_single
CREATE TABLE rank_single (
  rank_single_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  person_id INTEGER NOT NULL,
  event_id INTEGER NOT NULL,
  best int(11) NOT NULL DEFAULT '0',
  world_rank int(11) NOT NULL DEFAULT '0',
  continent_rank int(11) NOT NULL DEFAULT '0',
  country_rank int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (rank_single_id),
  FOREIGN KEY (person_id) REFERENCES person(person_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT IGNORE INTO rank_single (rank_single_id, person_id, event_id, best, world_rank, continent_rank, country_rank)
SELECT ra.rank_single_id,
p.person_id,
e.event_id,
ra.best,
ra.world_rank,
ra.continent_rank,
ra.country_rank
  FROM temp_rank_single ra
        LEFT JOIN person p
              ON TRIM(ra.person_identifier) = TRIM(p.person_identifier)
        LEFT JOIN event e
              ON TRIM(ra.event_identifier) = TRIM(e.event_identifier)
ORDER BY ra.rank_single_id;

-- result
CREATE TABLE result (
  result_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  competition_id INTEGER NOT NULL,
  event_id INTEGER NOT NULL,
  round_type_id INTEGER NOT NULL,
  pos smallint(6) NOT NULL DEFAULT '0',
  best int(11) NOT NULL DEFAULT '0',
  average int(11) NOT NULL DEFAULT '0',
  person_name varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  person_id INTEGER NOT NULL,
  event_format_id INTEGER NOT NULL,
  value1 int(11) NOT NULL DEFAULT '0',
  value2 int(11) NOT NULL DEFAULT '0',
  value3 int(11) NOT NULL DEFAULT '0',
  value4 int(11) NOT NULL DEFAULT '0',
  value5 int(11) NOT NULL DEFAULT '0',
  regional_single_record char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  regional_average_record char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (result_id),
  FOREIGN KEY (competition_id) REFERENCES competition(competition_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (event_id) REFERENCES event(event_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (round_type_id) REFERENCES round_type(round_type_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (person_id) REFERENCES person(person_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (event_format_id) REFERENCES event_format(event_format_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO result (result_id, competition_id, event_id, round_type_id, pos, best, average, person_name, person_id, event_format_id, value1, value2, value3, value4, value5, regional_single_record, regional_average_record)
SELECT res.result_id,
comp.competition_id,
e.event_id,
rt.round_type_id,
res.pos,
res.best,
res.average,
res.person_name,
p.person_id,
ef.event_format_id,
res.value1,
res.value2,
res.value3,
res.value4,
res.value5,
res.regional_single_record,
res.regional_average_record
  FROM temp_result res
        LEFT JOIN person p
              ON TRIM(res.person_identifier) = TRIM(p.person_identifier)
        LEFT JOIN event e
              ON TRIM(res.event_identifier) = TRIM(e.event_identifier)
        LEFT JOIN competition comp
              ON TRIM(res.competition_identifier) = TRIM(comp.competition_identifier)
        LEFT JOIN round_type rt
              ON TRIM(res.round_type_identifier) = TRIM(rt.round_type_identifier)
        LEFT JOIN event_format ef
              ON TRIM(res.event_format_identifier) = TRIM(ef.event_format_identifier)
ORDER BY res.result_id;


-- remove temp tables
DROP TABLE temp_competition;
DROP TABLE temp_country;
DROP TABLE temp_person;
DROP TABLE temp_rank_average;
DROP TABLE temp_rank_single;
DROP TABLE temp_result;
DROP TABLE temp_continent;
DROP TABLE temp_event;
DROP TABLE temp_event_format;
DROP TABLE temp_round_type;

