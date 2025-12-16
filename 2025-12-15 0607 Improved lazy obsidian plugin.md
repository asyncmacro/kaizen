---
created: 2025-12-15
tags:
  - note
  - journal
  - ideas
  - plugins
  - developments
day: "[[2025-12-15]]"
---

There is already an obsidian plugin that makes obsidian plugins lazily loaded by deferring the plugins load. Four types of plugins:
1. Instantly loaded plugins: which are plugins that will be loaded on obsidian startup like the default behavior of obsidian
2. Short delayed plugins: a custom value that plugins will be loaded in, it's how many seconds after obsidian startup
3. Long delayed plugins: similar to *short delayed plugins* but it usually longer wait
4. Disabled plugins: plugins that will not be loaded

The flow of the plugin is good but it could be improved.

## Redundancy of Long and Short delays

The term Long and Short can be abused by the user *if the user gives short delay greater number than long delay*

Some plugins could be wanted the same time but one more important than other, in this case I think having custom periods for each plugin is better. By giving plugins the same loading seconds by default we let the user decides which plugin loads when.

The only types will be: **Instant, Delayed, Disabled, and Deferred**

## Starting plugins custom commands 

With the current flow, if a user wants to load a disabled plugin he has to enable it (set whether instant, short, or long delay) then restart obsidian.

A better solution to this issue is introducing a new category that could possibly replace *disabled* which is: *deferred*

What deferred does is that during startup, it will assign custom commands for each deferred plugin, when the custom command is executed it will start the plugin. This is better than having to change the type then restart.

## Customization of plugin load space time
 
The time between each plugin being loaded, for example if it is 10ms then the type between plugin A and plugin B being loaded is 10ms

By allowing customization of this, give user more power into customizing 

## Resetting settings to default

In case the user want to get the default settings, he can restore it with a single click

## Can be good ideas but not important 

### Categorizing plugins

This can be a good feature to add, it essentially allows user to create custom categories which allows plugins to be loaded in batch on-demand

**Scenario:**
The user is an author and a doctor, he has a lot of plugins that he uses throughout his day.

But there's a plugins pollution which essentially means that plugins needed for his doctor woerk are interfering when he's writing for his books and vice versa.

With categorization, he essentially defer all plugins only when `Enable Category` command is called. Now, his obsidian acts as the following:

1. Instant plugins are loaded
2. Delayed plugins are loaded based on time 
3. When he gets into writing, he enable his author category 
4. When needs his doctor category, he can disable his author category and enable his doctor category 

**Extra featute:** adding the property or feature `disabled when` allows for toggle like behavior. Eg: author category will be disabled when the doctor feature is enabled.

