---
tags:
  - type/zettel
  - concept/hono
  - concept/backend
  - concept/server
aliases: 
created: 2025-04-17 19:13:25
---
# How to Handle Thrown Exception from Handler in Hono Framework

Sometimes a handler can throw and even though Hono can handle it in middlewares (see: [[Hono runs middlewares in the order they're registered on]]) we can define `app.onError(handler)` that will take care of it.

`onError` provides two parameters, the error thrown and context:

```ts
import { HTTPException } from 'hono/http-exception'

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return err.getResponse()
  }
})
```

## References

- [[Hono provides custom Error type for throwing errors inside handlers with custom body and headers]]

## Questions/Thoughts