--Q1 Which party/alliance won the most seats, and how does seat share compare to vote share?

SELECT
    `Party Name`,
    COUNT(*) AS seats_won,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM winners),
        2
    ) AS seat_share_pct,
    ROUND(
        SUM(`Total`) * 100.0 /
        (SELECT SUM(`Total`) FROM winners),
        2
    ) AS vote_share_pct
FROM winners
GROUP BY `Party Name`
ORDER BY seats_won DESC
LIMIT 15;

--Q2 Which states gave one party a near-total sweep (>80% seats), which were most fragmented?

SELECT 
    `State Name` AS state,
    `Party Name` AS party_name,
    COUNT(*) AS seats,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY `State Name`), 2) AS pct_of_state_seats
FROM winners
GROUP BY `State Name`, `Party Name`
ORDER BY `State Name`, seats DESC;

--Q3 Regional seat distribution — did any alliance dominate a region?

ALTER TABLE winners ADD COLUMN region VARCHAR(20);

UPDATE winners SET region = 'North' WHERE `State Name` IN 
('Uttar Pradesh','Delhi','Haryana','Punjab','Uttarakhand','Himachal Pradesh','Rajasthan','Jammu And Kashmir','Chandigarh','Ladakh');

UPDATE winners SET region = 'South' WHERE `State Name` IN 
('Tamil Nadu','Kerala','Karnataka','Andhra Pradesh','Telangana','Puducherry');

UPDATE winners SET region = 'East' WHERE `State Name` IN 
('West Bengal','Odisha','Bihar','Jharkhand');

UPDATE winners SET region = 'West' WHERE `State Name` IN 
('Maharashtra','Gujarat','Goa','Madhya Pradesh','Chhattisgarh','Dadra And Nagar Haveli And Daman And Diu');

UPDATE winners SET region = 'Northeast' WHERE `State Name` IN 
('Assam','Manipur','Meghalaya','Tripura','Nagaland','Mizoram','Arunachal Pradesh','Sikkim');

SELECT 
    region,
    `Party Name` AS party_name,
    COUNT(*) AS seats
FROM winners
GROUP BY region, `Party Name`
ORDER BY region, seats DESC;

--Q4 Top 10 closest contests and top 10 landslide wins?

-- Closest
SELECT m.`PC Name` AS pc_name, w.`State Name` AS state, w.`Party Name` AS party_name, 
       w.`Candidate Name` AS candidate_name, m.margin
FROM margins m
JOIN winners w ON m.`PC Name` = w.`PC Name`
ORDER BY m.margin ASC
LIMIT 10;

-- Landslides
SELECT m.`PC Name` AS pc_name, w.`State Name` AS state, w.`Party Name` AS party_name, 
       w.`Candidate Name` AS candidate_name, m.margin
FROM margins m
JOIN winners w ON m.`PC Name` = w.`PC Name`
ORDER BY m.margin DESC
LIMIT 10;

--Q5 — Distribution of victory margins nationally(Histogram)

SELECT margin FROM margins;

--Q6 — Highest and lowest turnout by state/constituency?

SELECT `PC Name` AS pc_name, `State` AS state, `Turnout_Pct` AS turnout_pct
FROM turnout
ORDER BY turnout_pct DESC
LIMIT 10;

SELECT `PC Name` AS pc_name, `State` AS state, `Turnout_Pct` AS turnout_pct
FROM turnout
ORDER BY turnout_pct ASC
LIMIT 10;

SELECT `State` AS state, ROUND(AVG(`Turnout_Pct`), 2) AS avg_turnout
FROM turnout
GROUP BY `State`
ORDER BY avg_turnout DESC;
--Q7 — Correlation between turnout and margin of victory (Scatter Plot)

SELECT t.Turnout_Pct AS turnout_pct, m.margin
FROM turnout t
JOIN margins m ON t.`PC Name` = m.`PC Name`;
--Q8 — NOTA patterns by constituency and state

SELECT n.`PC Name` AS pc_name, t.`State` AS state, n.`Total` AS nota_votes,
       ROUND(n.`Total` * 100.0 / t.Total_Votes_Polled, 2) AS nota_pct
FROM nota n
JOIN turnout t ON n.`PC Name` = t.`PC Name`
ORDER BY nota_pct DESC
LIMIT 20;
--Q9 — Gender split of winning candidates

-- National
SELECT Gender, COUNT(*) AS count,
ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM winners), 2) AS pct
FROM winners
GROUP BY Gender;

-- State wise
SELECT `State Name` AS state, Gender, COUNT(*) AS count
FROM winners
GROUP BY `State Name`, Gender
ORDER BY `State Name`;

--Q10 — Age distribution of winning candidates

SELECT 
    `Party Name` AS party_name,
    ROUND(AVG(Age), 1) AS avg_age,
    MIN(Age) AS youngest,
    MAX(Age) AS oldest,
    COUNT(*) AS total_winners
FROM winners
GROUP BY `Party Name`
ORDER BY avg_age;