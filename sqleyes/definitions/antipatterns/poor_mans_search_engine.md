### Poor Man's Search Engine

Suppose we want to search for words or sentences in our database. The first thing that comes to mind is using a SQL pattern-matching predicate, such as the `LIKE` keyword, to which we can specify a pattern or using `REGEXP`. Both methods seem like a very good option for full searches.

However, the main problem of pattern-matching predicates is their poor performance. Because they cannot use a traditional index, they must scan every row of the specified tables. The overall cost of a table scan for this search is very high, since matching a pattern against a column of strings is a costly operation when we compare it to other comparison methods like integer equality.

Another problem with simple pattern-matching using the keyword `LIKE` or regular expressions is that they can find unintended matches, making the search result not accurate or erroneous.

#### Example code

```SQL
SELECT *
FROM products
WHERE pName LIKE "%cat%"
```

The code above shows an example of how to search products that have the word "cat" in their product name. This should be avoided if the products table is large.

#### Fix

Use a specialized search engine method to do pattern matching. They sometimes come as standard with certain databases or DBMS's.
