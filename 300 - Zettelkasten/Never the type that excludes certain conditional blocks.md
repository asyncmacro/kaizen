---
aliases: []
tags:
  - topic/typescript
  - concept/conditional-types
UID: 202512011047
date-created: 2025-12-01
---

#  Never, the type that excludes certain conditional blocks

## 1. How can never exclude certain blocks in conditional

Type conditionals have true and false blocks each emit value based on the condition, but sometimes we may want to not include a value at one of the blocks, here comes the job of the type `never`

Let's say we want to to return `"P"` if given a primitive type, if not then we include nothing. normally we do the following:

```tsx
type Primitive = string | number | boolean
type PForPrimitive<T> = T extends Primitive ? "P" : "N"

type A = PForPrimitive<string | null> // A: "P" | "N"
```

but what if we just want `"P"`, we don't want to have a value returned in the false branch, essentially we want to *skip* the branch. That's where the `never` comes handy by replacing `"N"` with never it will result in `A`'s type becoming `"P" | never` which the compiler skips and make it `"P"` only

```tsx
type Primitive = string | number | boolean
type PForPrimitive<T> = T extends Primitive ? "P" : "N"

type A = PForPrimitive<string | null> // A: "P" | never
```

## 2. Connections & Synthesis

* [[Typescript conditionals distributes on unions by default]] (explains how the typescript conditional type works with union)
* [[Conditional types in typescript are a building blocks for a lot of complex type-level functionalities]] (explains the type conditional)

## 3. Source & Reference
* **Original Source:** [[10_Sources/Source Title Here]]
* **Relevant Page/Section:** Page 42, Chapter 3.