# OSHit -- Get your hit of the Orange Site in the terminal

*Screenshot goes here*

## Introduction

OSHit is a read-only terminal-based client for HackerNews. It provides the
ability to view all the top/recent items in the major categories, as well as
allowing viewing comments and user details. Where relevant, bindings are
always available to open the relevant view on HackerNews itself in your web
browser.

## Installing

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install oshit
```

Once installed run the `oshit` command.

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/oshit/issues) or [start a
discussion](https://github.com/davep/oshit/discussions).

## TODO

Things I'm considering adding or addressing:

- [ ] Some degree of caching of items to reduce API hits.
- [ ] Improve the navigation of comments.
- [ ] Expand the text-cleaning code to handle links, etc.
- [ ] Add searching
  - [ ] Amongst the current view
  - [ ] Amongst loaded comments within comment view
  - [ ] All of history ([`hn.algolia.com`](https://hn.algolia.com/api))

[//]: # (README.md ends here)
