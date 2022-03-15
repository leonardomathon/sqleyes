### Ambiguous Groups

This anti-pattern occurs when developers misuse the aggregation command `GROUP BY`.

Every column in a query's `SELECT` statement must have a single value row per row group, which is also known as the **Single-Value Rule**. Now, for columns in the `GROUP BY` aggregation this is guaranteed, because it returns exactly one value per group, regardless of how many rows the group matches. For other SQL commands such as `MAX(), MIN(), AVG()`, it will also result in a single value for each group, so this is also guaranteed.
The database server, on the other hand, cannot be so certain about any other field listed in the `SELECT` statement. It cannot always ensure that the identical value for the other columns appears on every row in a group. This may cause erroneous results.

#### Example code

```SQL
SELECT CID, PID, MIN(date)
FROM customers JOIN shoppinglists USING (CID)
GROUP BY CID;
```

The code above shows a basic example of this anti-pattern. In this example, because the `shoppinglists` table identifies numerous products to a specific customer, there are several distinct values for product ID for a given customer ID. There is no way to express all product ID values in a grouping query that reduces to a single row per customer.

#### Fix

Always make sure that the columns in the `SELECT` clause have single values. This can be achieved by grouping over multiple columns.
