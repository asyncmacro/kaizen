---
aliases: []
tags:
  - status/seedling
  - topic/typescript
  - concept/infer-keyword
UID: 202512071207
date-created: 2025-12-07
---

#  The infer keyword is helpful extracting sub-types out of other types

## 1. What is `infer`

`infer` is a TypeScript keyword for extracting sub-types out of other types. The types that `infer` can work on are usually types with generics or function definitions

## 2. How to use `infer`

While `infer` is a very powerful keyword it cannot be used anywhere, it can only be used in the constraint (or *conditional type branch*) in type conditionals like the following:

```typescript
// Given type T which is a kind of Array<unknown>
// it will provide the type within Array
type ExtractFromArray<T> = T extends Array<infer U> ? U : never

type A = ExtractFromArray<Array<string>> // A: string
type B = ExtractFromArray<string> // B: never
```

Notice how we used `infer` at the right side of `extends` and not the left side. That is because TypeScript will error if used on the left side.

Because `infer` defines a new type name (*in the previous case `U`*) the defined type can only be used on the true branch only, the false branch will have no access to the defined branch

```typescript
type ExtractFromArray<T> = T extends Array<infer U> ? never : U // Error: undefined U
```

## 2. Connections & Synthesis

* [[Conditional types in typescript are a building blocks for a lot of complex type-level functionalities]] (explains how to use conditional types)
* [[Typescript conditionals distributes on unions by default]] (explains how conditional types behaves with unions)

## 3. Source & Reference
* **Original Source:** 
* **Relevant Page/Section:** 