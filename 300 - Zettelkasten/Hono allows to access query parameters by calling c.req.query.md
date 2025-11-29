---
tags:
  - type/zettel
  - concept/hono
  - concept/server
  - concept/backend
aliases: 
created: 2025-04-17 19:41:15
---
# Hono allows to access query parameters by calling c.req.query

Query parameters are accessible inside of handlers using `c.req.query(key)`. A query does not need to be provided in path.

```ts
app.get('/somepath', (c) => {
  const name = c.req.query('name')
})
```

Now if we request `/somepath?name=admin` the variable `name` will contain `admin`

## References


## Questions/Thoughts