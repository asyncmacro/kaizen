---
tags:
  - type/zettel
  - concept/hono
  - concept/backend
  - concept/server
aliases: 
created: 2025-04-17 11:56:58
---
# Hono's TrieRouter builds a tree for the router with each node as a segment for fast lookups

This is another router from Hono, it uses the [[trie-tree algorithm]]. This builds a tree for the router, each node represents one segment. This allows for fast lookups. It also supports all patters unlike [[RegExpRouter is Hono's router that uses RegEx similar to express.js]].


## References

- [[Hono has 5 Routers each for different use case and speed]]