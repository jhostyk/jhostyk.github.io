# w4111-proj
## Podcast recommendation website.

**PostgreSQL account**: jh3958  
**URL**: 35.185.16.252:8111

<ins>Myles Ingram (mai2125) and Joseph Hostyk (jh3958)</ins>:  
**PostgreSQL account**: jh3958  


<ins>Part 4 Modifications</ins>:  
1. Each episode has "show notes" associated with it - text about the content of the show, provided by the podcast distributor. We originally had this as a normal text column. Here, we added a ts_vector column to our Episodes table, taking the same content but as a ts_vector. This works pretty well for searching! You might want to do sentiment analysis, finding the most relevant keywords, or any other NLP method on the episode details.


**Query for full text word search**
Searches every show_notes in episode and checks if 'coronavirus' appears in the show_notes. 

```
SELECT Show_notes @@ 'coronavirus'::tsquery
FROM Episode;
```

This returns an array showing that most episodes do not have that keyword; the array has "t" = True for the episode which has that keyword.



2. We added an array attribute for each episode for its daily views. The array is a count with how many listens that particular episode got on each day. Because some episodes were uploaded on different days, some have longer arrays than others. An array is very useful here, because each episode may have a different amount of days, and different view numbers for each day.

**Query for array**:
This query gets the name of the episode with the most views:
```
Select title
FROM episode
Order by (
Select Sum(views) 
From unnest(daily_views) as views) ASC
Limit 1;
```
This query should return 'Round 2...'

3. We added a composite type for Person. We previously had three tables: Person, which kept track of all people, and Host and Guest, which had foreign keys into Person. This allowed us different queries over different groups. However, it felt a bit redundant to define both tables in exactly the same way. Now with a composite type, we were able to define the table just once, and then repeat it for both Host and Guest.

**Query for composite type**:
This query gets all the guests that also host their own podcast on ESPN.
```
SELECT guest.name
From host, guest
WHERE guest.Person_ID = host.Person_ID AND host.person_id IN
(SELECT person_id FROM hosts_show WHERE show_name IN
 (SELECT show_name FROM show WHERE network_name = 'ESPN'));
```
This query should return 'Zach Lowe'.



