---
tags:
  - type/zettel
  - concept/hono
  - concept/server
  - concept/backend
aliases: 
created: 2025-04-17 19:45:04
---
# How to Set a Header in Hono Framework Handler

Headers are essential part of REST APIs and Hono allows us to set custom headers using the `c.header(name, value)`

```ts
c.header('X-Header-Name', 'Header-Value')
```

## References

- [[Hono provides path parameters by calling ctx.req.params function]]
- [[Hono allows to access query parameters by calling c.req.query]]
- [[Example of Route handler in Hono]]
## Questions/Thoughts