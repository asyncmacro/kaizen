---
tags:
  - type/zettel
aliases:
created: 2025-09-03 16:21:46
---
# The `Object.preventExtensions`

This function takes an object as an argument, it works similar to `Object.freeze` but it does allow the object currently set fields to be modified, it just doesn't allow you to add new fields hence the name `preventExtensions` which prevent *Extending* the object.

## Examples

```javascript
let obj = {}
obj["a"] = 1; // {a: 1}
obj["]
Object.preventExtensions(obj)

obj["b"]
```


## References


## Questions/Thoughts