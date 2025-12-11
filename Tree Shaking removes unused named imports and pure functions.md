---
tags:
  - note
  - journal
  - Softwares
aliases: []
created: 2025-12-11
---
# Tree Shaking removes unused named imports and pure functions

There are several things that get removed from the final JavaScript  bundle, which are:

## Named Exports

Functions that are exported but not used gets removed from the final bundle. In the following code `unused` will not be on the bundled javascript file.

```javascript
// utils.js
export used = () => {
  return 44;
}
export unused = () => {
  return 77;
}

// main.js
import { used } from './utils.js'
console.log(used())
```

## Unused Pure function calls:

pure functions are functions with no side effects (fetching, logging...etc). In the previous code `used` and `unused` are both pure functions. An unsed function call is calling a function without assigning the returned value into a variable.

```javascript
used() // This line won't get into the final bundle
```


## Connections

* [[Tree Shaking reduces JavaScript bundle size by removing unused function, variables and modules]]
* [[Tree Shaking Works by analyzing and removing safe to remove code]]
* [[The Benefits of Tree Shaking]]