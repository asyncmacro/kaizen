---
aliases: []
tags:
  - daily
  - journal
  - programmings
  - languages
  - recursions
UID: 202512071226
date-created: 2025-12-07
---

# Recursive types in TypeScript breaks problems into sub-problems

## 1. What is recursion

*Recursion* is when a function (or *type*) calls itself, directly or indirectly, to break complex problems into manageable sub-problems. enabling solutions without overly complex behavior.

Recursion consists of two cases:

* Recursive case: this is where we recursively call the type again usually with different arguments (to avoid infinite looping)
* Base case: here where we return value which breaks recursion

## 2. How to use Recursion in types

Recursion can be used in types for doing complex behavior, an example for that would be:

```typescript
// This type takes a a number, and build a tuple with N length
// containing unknown type
type BuildTuple<N extends number, T extends unknown = unknown, Tup extends T[] = []> = Tup['length'] extends N // check if Tup has the same length as N
  ? Tup // Return the tuple
  : BuildTuple<N, T, [...Tup, T]> // Recursive call with updated arguments
  
type A = BuildTuple<2, string> // A: [string, string]
```

As explained in `BuildTuple` type, it will builds a tuple given a number and an optional type.

## 2. Connections & Synthesis

* [[Conditional types in typescript are a building blocks for a lot of complex type-level functionalities]] (explains conditional types which usually used with recursive types)
* [[The infer keyword is helpful extracting sub-types out of other types]] (the `infer` keyword which can be coupled with recursive types)

## 3. Source & Reference
* **Original Source:** 
* **Relevant Page/Section:** 