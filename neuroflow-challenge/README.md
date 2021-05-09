# Neuroflow Data Team Take-Home Project

### Running the code:
I am an avid user of conda environments, so I have used one here in creating the environment for this task. Included in this repository is a file called **neuroflow_challenge.yaml**. Running **conda env create --file neuroflow_challenge.yaml** in your terminal should download all dependencies and packages used in this solution. I also wrote this solution on Pop! OS, my Linux distro of choice. If there are any issues with running the code, please let me know and I can think of another solution. I greatly appreciate this opportunity.

Running **main.py** will prompt you to enter a **user_id**, which is given by the dataset. An example of one for testing is 3788.

### Documentation: 
Each function has specific workings in DocString format. Do **help()** to get more information.

## Part 1:
My solution is essentially a csv parser that upon putting in the patient's id, which I am assuming the provider would have acess to, provides a line graph to show all the scores vs. dates of the tests.
I chose this solution because I find that line graphs are the best way to represent data over time. Given the desired time restriction, I also did not want to make something complicated or convoluted. 
This solution provides a simple and strightforward way to analyze patient progress.

I had to account for a few edge cases that I found while making this. The first is that when reading through the csv file, I saw that some patients had mutilple tests on the same day, and some even one minute apart. 
I assumed this to be a mistake and chose the last one taken on that day while filtering out all others. Running main.py prompts the user with a place to enter a patient id, and upon entering an id that is not within the 
data, the user is told to try again.

In terms of additional information, I think it would be much more helpful to providers if they knew what type(s) of treatment the patient has been undergoing. I would also think it is important to see any notes or comments the provider
has on the patient, as doing analysis of mental health status based purely on quantitative self-assessment does not seem thorough enough. With this, the solution could be changed to demonstrate what type of treatment and life-changes/provider notes are the most useful to the patient. I feel that in dealing with mental health issues, there needs to be as much relevant information as possible. I do think, however, that in this current state, and assuming a relationship between the patient and the provider, a simple graph to show the overall results of the assessment over time would be the most useful.

## Part 2:

1. How many users completed an exercise in their first month per monthly cohort?

**NOTE:** I ended up only doing total users instead of the percent because I was not sure what was meant by cohort, i.e. if someone who enrolled Jan. 28 completed an exercise on Feb. 2, which would be within a month, counted towards the Jan. or Feb. cohort.

~~~~sql
DROP TABLE IF EXISTS temp;
CREATE TEMP TABLE temp(counter int, month int);
INSERT INTO temp(counter,month)
SELECT Count(*), DATE_PART('month', u.created_at::date)
FROM nfc.users u
JOIN nfc.exercises e
ON u.user_id = e.user_id
WHERE ((DATE_PART('day', e.exercise_completion_date::date) - DATE_PART('day', u.created_at::date) <= 30) AND
(DATE_PART('month', e.exercise_completion_date::date) - DATE_PART('month', u.created_at::date) = 0))
OR (((DATE_PART('month', e.exercise_completion_date::date) - DATE_PART('month', u.created_at::date) = 1) OR
	(DATE_PART('month', e.exercise_completion_date::date) - DATE_PART('month', u.created_at::date) = -11)) AND 
	(DATE_PART('day', e.exercise_completion_date::date) - DATE_PART('day', u.created_at::date) <= 0))
GROUP BY u.created_at, u.user_id;
SELECT month, count(*)
FROM temp
GROUP BY month
ORDER BY MONTH asc;
~~~~

2. How many users completed a given amount of exercises?

~~~~sql
SELECT e.exercise_id, Count(e.exercise_id) as freq
FROM nfc.exercises e
GROUP BY e.exercise_id
ORDER BY e.exercise_id asc;
~~~~

3. Which organizations have the most severe patient population?

~~~~sql
SELECT Count(*), p.organization_name, SUM(q.score) / count(*) as avg
FROM nfc.phq9 q
JOIN nfc.providers p
ON q.provider_id = p.provider_id
GROUP BY p.organization_name
ORDER BY count(*) desc
LIMIT 5;
~~~~
