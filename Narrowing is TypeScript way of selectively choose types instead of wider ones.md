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