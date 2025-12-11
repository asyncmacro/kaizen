---
tags:
  - note
  - journal
  - Backends
  - Frameworks
aliases:
created: 2025-12-11
---
# How to Modify a Middleware After Response

Sometimes, you'd want to do something with the response before it is fully sent to the user. you can still be able to modify a response by changing the value of the `c.res` like the following:

```ts
const stripRes = createMiddleware(async (c, next) => {
  const res = await next();
  c.res = undefined;
})
```

The `stripRes` middleware will now remove any response that was sent from handler


## References

- [[Middlewares in Hono are functions that runs on all incoming requests]]
