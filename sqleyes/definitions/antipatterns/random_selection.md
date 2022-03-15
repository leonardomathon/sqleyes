### Random Selection

When writing a query that needs to select a random row from a table, developers might use `ORDER BY RAND() LIMIT 1`, where the `RAND()` function to sort the data randomly. However, this is not the best solution. By using the `RAND()` inside an `ORDER BY` clause, the use of an index is not possible, since there is no index containing the values returned by the random function. This is a big concern for the query's performance because using an index is one of the best ways to increase the computation of sorting. As a result of not employing an index, the query result set must be sorted by the database using a slow table scan, making the performance poor.

#### Example code

```SQL
SELECT CID
FROM customers
ORDER BY RAND() LIMIT 1;
```

A typical use case for this anti-pattern is when we have the task of selecting a random cusomter ID from the customers table. The query above shows a typical (faulty) solution.

#### Fix

Choose a random value using other means. Common ways would be to generate a random value between 1 and the greatest primary key, or counting the total number of rows and generating a random number between 0 and the row count. Then we can use the random number inside a `WHERE` clause.
