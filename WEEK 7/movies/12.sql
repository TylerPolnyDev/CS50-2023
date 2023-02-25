SELECT movies.title
FROM movies
INNER JOIN stars
ON movies.id = stars.movie_id
INNER JOIN people
ON stars.person_id = people.id
WHERE people.name IN ('Johnny Depp', 'Helena Bonham Carter')
GROUP BY movies.id
HAVING COUNT(*) = 2;
