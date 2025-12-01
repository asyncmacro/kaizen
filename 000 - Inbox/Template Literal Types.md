
# Template Literal Types

**What are they?**

A template literal type (TLT) is the type system's equivalent of string interpolation.
but instead of a single string, it results in union of possible values, for example

```typescript
type A = "a" | "A"
type B = "1" | "2"
type C = `${A}${B}` // "a1" | "a2" | "A1" | "A2"
```

TLTs only work on string literal, unions of them or the generic type `string`, for the latter it results in `string`

**Destructuring and extration using infer and extends**
to extract or match strings using template literals, we use extends and infer:

```typescript
type ExtractToken<T extends string> T extends `Bearer ${infer Tk}` 
  ? Tk 
  : never
  
type A = ExtractToken<"Bearer mytoken"> // A: "mytoken"
type B = ExtractToken<"Basic 123"> // B: never
```

**Recursive calling and TLTs**
we can also use TLTs and recursive calling for extracting and manipulation strings by using recursion, for that there need to be two conditions:
1. Recursive step: here, the type calls itself with updated or same types
2. Base step, this is the Escape step where the type returns result

