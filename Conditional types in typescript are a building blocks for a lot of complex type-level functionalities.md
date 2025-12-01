---
aliases: []
tags:
  - topic/typescript
  - concept/conditional-types
UID: 202512010850
date-created: 2025-12-01
---

#  Conditional types in typescript are a building blocks for a lot of complex type-level functionalities

## 1. What is conditional type

In Typescript, specifically on type level,  We can define types based on certain conditions with a syntax similar to ternary operators in typescript. 

The following syntax is how conditionals are made in typescript:

`{tsx} type P = A extends B ? X : Y`
* `A extends B` is the condition which essentially means *is A assignable to B?*
* `X` this is called the true block, which would be returned in case the condition is true
* `Y` this is the false block, if condition is false `Y` would be returned


To define `IsString` type that takes a generic type and returns `true` if given type is string and `false` if it is not a string, we use the following syntax:

```typescript
type IsString<T> = T extends string ? true : false

type A = IsString<number> // A: false
type B = IsString<string> // B: true
```


## 2. Connections & Synthesis

* [[Typescript conditionals distributes on unions by default]] (this explains how conditionals behave with unions)
* [[Never the type that excludes certain conditional blocks]] (explains how never helps excluding branches in type conditionals)

## 3. Source & Reference
* **Original Source:** 
* **Relevant Page/Section:** 