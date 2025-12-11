---
tags:
  - type/zettel
  - concept/server
  - concept/backend
  - concept/framework
aliases: 
created: 2025-04-17 10:05:05
---
# Hono has 5 Routers each for different use case and speed

Unlike Express which employs path-matching algorithm (see: [[What is path-matching algorithm]]), Hono comes with 5 routers and each one of them has its pros and cons and use case. This gives the developer the power to choose between each router and each use case.

## 1. RegExpRouter

This is the fastest Hono route and is more faster than Express' own router. (see: [[RegExpRouter is Hono's router that uses RegEx similar to express.js]]) and its limitations [[Hono's RegExpRouter Limitations]]

## 2. TrieRouter

Although it is not as fast as RegExpRouter, it still faster than Express' router. (see: [[Hono's TrieRouter builds a tree for the router with each node as a segment for fast lookups]]) The only know cons of this router is that it is not as fast as RegExpRouter

## 3. SmartRouter

Since RegExpRouter does have some drawbacks, what this router does is it acts like a Frontend (or a router of routers). it defaults to RegExpRouter but if a route is not supported or limited (see: [[Hono's RegExpRouter Limitations]]) then it would route it to TrieRouter.

## 4. LinearRouter

This is a router for a special use case, it is made for environments where routes are registered frequently. (see: [[LinearRouter is Hono's router similar to Express router but optimized for Edge and Serverless]])

### 5. PatternRouter

The smallest router out of the five, It is made for environments where resources are limited. such as serverless and edge environments. (see: [[PatternRouter is Hono's router that uses list to register routes]])

## References

- [[Hono is a Simple and fast framework built on web APIs]]
- [[Hono Provides a Lightweight Web Standard API]]