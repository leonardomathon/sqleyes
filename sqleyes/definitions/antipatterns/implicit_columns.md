### Implicit Columns

When writing a query that needs a lot of columns, developers often opt to use the SQL wildcard selector `*`. This means that every column from the table(s) specified in the `FROM` clause is returned, meaning that the list of columns is implicit instead of explicit. In many ways, this makes the query more concise. However, this can come at a cost as the result set can be quite big for large tables. This will have an impact on the performance of the query.

#### Example code

```SQL
SELECT *
FROM purchases;
```

Suppose we have the task of finding all customer IDs, store IDs, product IDs as well as the quantity and price from the purchases table. This would mean that the only columns from the purchases table that are not present in this query would be the purchase ID and data columns. The query shown in above contains the implicit columns anti-pattern as it uses the wildcard `*`. Instead of selecting only the columns requested by the task, it utilizes a wildcard, returning in a result that includes both the store ID and the date columns.

#### Fix

Always explicitly select the columns you need. Use the wildcard `*` operator with caution.
