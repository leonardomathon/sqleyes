### Fear of the Unknown

In SQL, values in columns can be left empty. This results in an attribute of a certain row having a `NULL` value. SQL considers `NULL` to be a special value, distinct from zero, false, true, or an empty string. Therefore, it is not possible to test for `NULL` values with standard comparison operators such as `=, >=, <>, etc`. Instead use `IS NULL` and `IS NOT NULL`.

#### Example code

```SQL
SELECT pName, suffix
FROM products
WHERE suffix <> NULL;
```

The code shown above is querying the product name and suffix columns from the products table where the suffix is not equal to `NULL`. One might think that this will result in all rows that have a suffix, however this is not the case. Any comparison to `NULL` returns _unknown_, not true or false. Therefore, this query does not return any data.

#### Fix

Use `IS NULL` and `IS NOT NULL` when comparing against `NULL` values.
