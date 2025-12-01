
## Conditional type in TS

conditional type in typescript is made by using the following syntax `A extends B ? C : D`
in this example if type A is assignable to type B then the condition will return C otherwise it will return D

**With unions**: if A were to be union, the compiler will generate a list of if statements and run it at compile-time, for example: 

```typescript
type Primitive<T> = T extends string | number ? T : never
type A = Primitive<string | undefined> // Result: string
```

in this example, the type A is made into two conditional syntax:
* string extends string | number ? T : never
* undefined extends string | number ? T : never

which would result in A being `string` type

---------

to escape the union distribution, use tuple wrapping

```typescript
type P<T> = [T] extends [string] ? T : never
type A = P<string> // A: string
type B = P<string | number> // B: never
```

### Recurse in conditional types

Conditional types can also be recursive allowing complex type changes like the following example:

```typescript
type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T;

type Result = Flatten<number[][][]>; // Result: number
```

Flatten will keep calling itself if T is an array, unwrapping its inside type and calling itself, until it gets to the original non array type

### Type Relations: narrowing and widening

**Narrowing:**

When conditions are met that lead to specific types, typescript narrows down to the most specific type:

```typescript
type Check<T> = T extends number ? "Number type" : "Other type";

type A = Check<5> // A: "Number type"
```

Instead of returning a string, it returns "Number type" which is how narrowing work.
It also happens in type guards (instanceof, typeof) and also if conditions

**Widening**

In the past example, if a union were to be provided the compiler returns the most inclusive type but instead of string it would return `"Number type" | "Other type"`

this happens in assignment:

```typescript
let num: 5 = 5
num = 10 // Error

let n: number = 5
n = 10 // Works
```


### Infer Keyword

Infer is used to extract subtypes and for doing complex type manipulation. For example, we can extract the type being held inside an array, or the arguments types or return type of a function.
We can also extract multiple values at once (return and arguments types, first and last array types)
it can happen only inside extends clauses
inferred names are local to the true branch

If infer fails (incorrect type) it will go to the false branch, if the false branch yields never, the branch is filtered out

if infer is given a union it will distribute the union types over the condition
which can produce unexpected types, wrapping it in a tuple can help prevent distribution

for debugging, replace the true branch with literal marker with inferred name `{inferred: X}` to inspect what's being inferred

## Relationships of never, unknown and any
### Never: the empty type

Never is an empty type, it means not at all (unlike null or undefined which represent a value of nothing), never is used in conditional which means to skip the condition type.
In unions and after the compiler distribute union items to the, every item that results in never will be filtered out

`A | never = A`

never is also behaving differently in conditionals, so if we have conditional

```typescript
type A = T extends B ? X : Y
```

if `T` is never, it would result in `A = never` not `X` or `Y` but `never`.
since the type `never` is always filtered out of conditionals

but if `T` is a union of `never | B` then the resulting type will be `X`

`never` is used to remove properties from mapped types by returning `never` as the key,
since also `never` propagates the `T[never]` type results in a `never`

### Unknown: the safe type

unknown is a safe type that usually used in place of any, it accepts any type but requires to do checking before performing any action like:

* arithmetic operations
* function calling
* property access

all of these cannot be performed by an `unknown` type unless explicitly check and narrow the type further more (inside if statements or type guards)

in conditionals `T extends unknown ? X : Y` it will result always in the true branch

The only type that does not extend `unknown` is never, only when passed as a generic parameter

```typescript
type Test<T> = T extends unknown ? true : false

type L1 = Test<never> // L1: never
type L2 = never extends unknown ? true : false // L2: true
```

The reason behind this is:

* in generic parameter, the type `never` is filtered out which why it yields `never`
* in concrete type checking, it yields true because every type extends `unknown`

### any: the unsafe type

the type `any` behavior is exclusive and what it means is it disables all type checking which makes it not safe

Inside conditional type, `any` will result in in a union of both branches

```typescript
type A = any extends string ? "S" : "N" // A: "S" | "N"
```

any must always be avoided unless prototyping where you consciously want to opt out of type checking

## Non-distributive behavior

Since in conditionals all union members will be distributed, sometimes we would want to opt-out of distributive behavior, to do so we must wrap it in tuple `[T] extends [U]` which will not use distribution

`[T] extends [U] ? A : B`

If `T` were to be `A | B` it will test `A|B` as a whole and not distribute and check each member alone

one of the uses can be: 

1. **checking all members to be certain type**

```typescript
type IsAllString<U> = [U] extends [string] ? true : false

type A = IsAllString<string | number> // A: false
type B = IsAllString<string | string> // B: true
```

In this case if union type are string then it would result in true otherwise it results in false

So you may ask, why not normal conditional? in normal conditional `A` will be of type `boolean` because typescript will do the following

    1. `(string | number) extends string ? true : false` -> `string extends string ? true : false` and `number extends string ? true : false`
    2. Since the first condition will yield `true` and the second yields `false` the type will result in boolean (since boolean is just `true | false`

2. **Extracting uniform type**

Let's say you want to extract the type of a promise union, only when all promises are of a certain type, in normal conditional it will result in a union but with non-distributive conditional, it will only resolve when all types are same.

```typescript
type ExtractUniformPromise<T> = [T] extends [Promise<infer R>] ? R : never;
type A = ExtractUniformPromise<Promise<string> | Promise<string>>; // string
type B = ExtractUniformPromise<Promise<string> | Promise<number>>; // never
```

3. **Use with mapped keys**

With mapped types, the behavior can be unexpected to distribution, lets take the following example:

```typescript
type MapValuesIfAllMatch<T, V, R> = [T] extends [Record<string, V>] ? { [K in keyof T]: R } : never;

type DistributedMapValuesIfAllMatch<T, V, R> = { [K in keyof T as T[K] extends V ? K : never]: R }

type M = {
  a: string;
  b: string | number;
}

type O1 = MapValuesIfAllMatch<M, string, number> // O1: never
type O2 = DistributedMapValuesIfAllMatch<M, string, number> // O2: { a: number }
```

1. Non-distributive behavior: in this one, it will first check value `T` is a map of `Record<string, V>` meaning all types of the map are of types `V`. if they're it will create new map with `R` as the value type otherwise return `never`
2. Distributive behavior: the unexpected behavior occurs at property `b`: 
    - `T[K] extends V ? K : never` distributes: string -> K, number -> never, giving `K | never` which simplifies to `K`. But when used in `as` remapping, a branch that produces `never` for some union member means that member contributes no mapped entry; since at least one union branch fails, the whole property ends up omitted. So b is omitted and only a remains.