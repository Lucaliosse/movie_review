# Movie Review — Frontend

Vue 3 + Vuetify single-page app for browsing and managing movies, consuming the Django REST Framework API.

## Features

- Paginated movie list with average rating and actor count
- Movie detail page: inline-editable title/description, editable actor list (add/edit/delete), submit a review
- Create a new movie
- Delete a movie (with confirmation)
- State management with Pinia, HTTP via axios

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Environment Variables

Copy `.env.example` to `.env` and adjust values for your local setup — `.env` is gitignored, `.env.example` is committed as the reference.

```sh
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Base URL of the backend API the app calls | `http://127.0.0.1:8000/api` |

Note: this value is baked into the built JS bundle at build time (Vite convention), not read at runtime — rebuild after changing it.

### Compile and Hot-Reload for Development

Requires the backend to be running (see `back_movie_review/README.md`) so API calls succeed.

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
