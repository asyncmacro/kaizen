---
aliases: []
tags:
  - topic/
  - concept/
  - status/seedling
UID: 202512071008
date-created: 2025-12-07
---

#  Narrowing is TypeScript way of selectively choose types instead of wider ones

## 1. What is narrowing?

In TypeScript, when writing a type or a function and in specific conditions TypeScript will attempt on narrowing down the types, an example for such cases would be the following:

```typescript
// This function's return type is "even" | "odd"
function evenOrOdd(n: number) {
  if (n % 2 === 0) {
    return "even"
  }
  
  return "odd"
}
```


## 2. Connections & Synthesis
(Find at least two links to other Zettels. Use this section to explain *why* they are related, making the connection explicit.)

* [[Existing Zettel 1 - The Main Link]] (This idea relates to X by demonstrating the need for isolation.)
* [[Existing Zettel 2 - The Opposite/Analogy Link]] (This parallels the concept of Y in the domain of Z.)
* [[MOC - Relevant Map of Content]] (If this idea fits into a major MOC, link it here.)

## 3. Source & Reference
* **Original Source:** [[10_Sources/Source Title Here]]
* **Relevant Page/Section:** Page 42, Chapter 3.