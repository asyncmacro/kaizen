---
created: 2025-12-11
tags:
  - note
  - journal
  - Frontends
  - UIs
  - Performance
  - React
---
Let's say you have a component that has an interval run and stop buttons, by using `useState` each time we change the `intervalId` value the component will have to re-render.

```tsx
function handleStartInterval() {
  const intervalId = setInterval(() => {
    // ...
  })
  
  setIntervalId(intervalId) // Calling set hook will cause re-render
}

function handleStopInterval() {
  if (intervalId !== null) {
    clearInterval(intervalId)
    setIntervalId(null) // Calling set hook will also cause re-render
  }
}
```

in normal component that uses `setState` hook, assuming we run and stop the interval it will cause the component to re-render twice, once on start and once on stop.

Due to the nature of this component the `intervalId` value is not used in UI and user does not see it therefore we can use [`useRef`]([[2025-12-11 1051 useRef the value reference without rerender]]) which can hold value and allow us to manipulate it without cause component re-render. By replacing the `useState` with `useRef` the component will not re-render but also still work correctly.

```tsx
function handleStartInterval() {
  // no re-render
  intervalIdRef.current = setInterval(() => {
    // ...
  })
}

function handleStopInterval() {
  if (intervalIdRef.current !== null) {
    clearInterval(intervalIdRef.current)
    intervalIdRef.current = null
  }
}
```