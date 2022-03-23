### Spaghetti Query

Queries can be of varying degrees of difficulty. Some significantly more sophisticated than others, such as a complex join between two databases or a recursive subqueries. Sometimes, during development of a query for a complex task, the query becomes too complex that the programmer gets stuck. This is most likely because programmers are fixated on solving the task both elegantly and efficiently, thus they try to complete it with a single query. However, the complexity of these single queries can increase exponentially, making both maintainability and correctness more difficult to achieve.

#### Example code

```SQL
SELECT COUNT(p.pID) AS numberOfDistINctProducts,
  SUM(i.quantity) AS numberOfProducts,
  AVG(i.unit_price) AS averagePrice,
  city
FROM products p
  JOIN inventories i ON (p.pID = i.pID)
  JOIN stores s ON (i.sID = s.sID)
GROUP BY s.city
```

The query above can be considered overly complex for what it does, but it demonstrates the type of problem that can occur when a programmer tries to solve a complicated problem in one query. SQL is a sophisticated language that allows you to do a great deal with a single query or statement. However, this does not mean that it is essential to try to solve every problem with a single query or line of code.

#### Fix

Sometimes, it is better to write seperate queries for a certain task, then trying to accomplish it with one query. A simple way to tackle complex queries is to use the **divide and conquer** method, where you divide the problem into multiple parts so you can solve them independently. In other words, if you break up a long complex query into several simpler queries, you can then focus on each part individually and do a better job of each of them, since they are less complex. While it is not always possible to split a query this way, it is a good general strategy, which is often all that is necessary.
