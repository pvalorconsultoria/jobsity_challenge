SELECT 
    region, 
    COUNT(*) occurrences
FROM trips
WHERE datasource = 'cheap_mobile'
GROUP BY region
ORDER BY occurrences DESC;