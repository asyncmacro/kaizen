---
tags:
  - journal
  - daily
  - Softwares
aliases:
created: 2025-04-11 22:13:56
---
# Does Tree Shaking Work

## How does it work 

* The bundler (**Webpack, Rollup, Esbuild...etc**) analyzes the code to find unused code
* The bundler then evaluates and removes **ONLY** if the unused code is safe to remove (*Bundlers can't remove function calls that are not pure*) see [[Pure function is a function with no side effects and returns save value given the same input]]
