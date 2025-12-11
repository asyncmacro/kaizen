---
tags: type/zettel, 
aliases: 
created: 2025-04-17 12:15:25
---
# LinearRouter

This router registers router as first-registered-first-matched, which means that routes are checked in the order they're registered in. similar to Express' router but the catch is LinearRouter is optimized for Edge and Serverless environments while Express' router is general purpose router.

This router is still generally faster that Express' own router

## References

- [[Hono has 5 Routers each for different use case and speed]]
- [[RegExpRouter is Hono's router that uses RegEx similar to express.js]]
- [[LinearRouter is Hono's router similar to Express router but optimized for Edge and Serverless]]