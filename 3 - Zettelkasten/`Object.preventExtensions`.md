---
tags:
  - type/zettel
aliases:
created: 2025-09-03 16:21:46
---
# The `Object.preventExtensions`

This function takes an object as an argument, it works similar to `Object.freeze` but it does allow the object currently set fields to be modified, it just doesn't allow you to add new fields hence the name `preventExtensions` which prevent *Extending* the object.

If you attempt to add new field it will throw an Error

## Examples

```javascript
let obj = {}
obj["a"] = 1; // {a: 1}
obj["b"] = 0; // {a: 1, b: 0}
Object.preventExtensions(obj)

obj["c"] = 0; // Error
obj["b"] = 2; // {a: 1, b: 2}
```


## References


## Questions/Thoughts