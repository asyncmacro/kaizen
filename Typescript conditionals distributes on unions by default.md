---
aliases: []
tags:
  - daily
  - journal
  - programmings
  - languages
UID: 202512011002
date-created: 2025-12-01
---
#  Typescript conditionals distributes on unions by default

## 1. Conditionals on unions generate conditional statement for each member of the union

If a typescript conditional is given a union, It will distribute and apply the conditional statement for each member of the union. For example:

`{tsx} type A = string | number extends string ? "S" : "N"`

For the previous snippet, the typescript compiler will transform it into:

`{tsx} type A = (string extends string ? "S" : "N") | (number extends string ? "S" : "N")`

the first will result in `"S"` and the second in `"N"`  and then the compiler will result in type `A` being a union `"S" | "N"`

## 2. Connections & Synthesis

* [[Conditional types in typescript are a building blocks for a lot of complex type-level functionalities]] (This explains the basic syntax of conditional.)
* [[Never the type that excludes certain conditional blocks]] (explains how never helps excluding branches in type conditionals)

## 3. Source & Reference
* **Original Source:** 
* **Relevant Page/Section:** 