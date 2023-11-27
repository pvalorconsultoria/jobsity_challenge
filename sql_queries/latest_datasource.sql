WITH top_regions AS (
    SELECT 
        region, 
        COUNT(*) as occurrences 
    FROM trips 
    GROUP BY region 
    ORDER BY occurrences DESC 
    LIMIT 2 
)
SELECT 
    t.region, 
    t.datasource, 
    top_regions.occurrences 
FROM trips t 
INNER JOIN top_regions ON t.region = top_regions.region 
WHERE t.datetime = ( SELECT MAX(datetime) FROM trips WHERE region = t.region );