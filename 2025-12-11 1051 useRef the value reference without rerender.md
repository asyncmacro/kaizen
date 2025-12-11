---
created: 2025-12-11
tags:
  - note
  - journal
  - Frontends
  - UIs
  - React
---
`useRef` is a react hook that let's you reference a value that can be used by the component but not used for UI.

let's say we have a value to be used by the component internally, the `useRef` is the best hook for this use case.

```tsx
function Component() {
  const valueRef = useRef(1)
  const increment = () => {
    valueRef.current += 1
  }
  // ...
}
```

notice that we access `valueRef.current` instead of `valueRef` and that's because `useRef` hook returns an object with a single property which is `current`.

another use case for `useRef` hook is by storing DOM elements reference for uses such as accessing class names, focus the element, ...etc. Look at the following example:

```tsx
function Component() {
  const inputElement = useRef<HTMLInputElement | null>(null)
  
  // calling inputElement.current.focus() will cause an error
  useEffect(() => {
    // check if element ref is set
    if (inputElement.current) {
      inputElement.current.focus() // focus the element
    }
  }, [])
  
  return <input ref={inputElement} />
}
```

Notice that we have to provide `ref` to the element we want to control. any attempt to access `inputElement` will result with error because at first render the reference is always of default value.

Even inside `useEffect` it is recommended to check if it is null or not. Since `useRef` does not cause re-render any attempt to use a reference value will result in a frozen value.

```tsx
function Component() {
  const counter = useRef(0)
  const increment = () => {
    counter.current += 1; // will not re-render
    console.log(counter.current)
  }
  
  return <div>
    <p>Counter {counter.current}</p>
    <button onClick={() => increment()}>Increment</button>
  </div>
}
```

Any clicks on button or calls to `increment` function will not updates the counter, though the counter will be logged correctly in the console