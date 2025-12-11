---
tags:
  - note
  - journal
  - Frameworks
  - Hono
  - Backends
aliases:
created: 2025-12-11
---
# Middlewares in Hono are functions that runs on all incoming requests

Hono allows to assign middlewares, which are functions that runs on all the incoming requests, you still can restrict which paths they run on though. middleware should return nothing.

```typescript
app.use(async (c, next) => {
  console.log('running middleware 1 start')
  await next()
  console.log('running middleware 2 end')
})
```

The first parameter is the request context and second is the next function which is called to go to the next middleware/handler.


## References


## Questions/Thoughts