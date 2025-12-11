---
tags:
  - daily
  - journal
  - buildings
  - programmings
  - Libraries
  - tools
aliases:
created: 2025-04-20 11:13:17
---
# How to configure tsup

Even though tsup can be used with no config (through the `tsup` command) it needs configuration when you want to customize the output (minify, sourcemap...etc).
To configure tsup, all you have to do is create a configuration file (see: [[tsup Compiles TypeScript Projects with Zero Configuration]]) and here's an example of a configuration file:

```ts
import { defineConfig } from 'tsup'

export default defineConfig({
  input: ['src/index.ts'],
  sourcemap: true,
  clean: true,
})
```

`defineConfig` also accepts a function which takes `options` As an argument and returns configuration object.

```ts
import { defineConfig } from 'tsup'

export default defineConfig((options) => ({
  input: ['src/index.ts'],
  sourcemap: true,
  clean: true,
  minify: !options.watch,
}))
```

`options` Is derived from cli flags
## Connections

- [[tsup Compiles TypeScript Projects with Zero Configuration]]
