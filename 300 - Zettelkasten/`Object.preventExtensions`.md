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
let obj = { name: "Jake", age: 18 }
Object.preventExtensions(obj)

obj.occupation = "N/A" // Error
```


## References


## Questions/Thoughts