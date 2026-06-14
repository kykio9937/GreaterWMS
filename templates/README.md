# GreaterWMS Frontend

This frontend is intentionally kept on the existing Vue 2 / Quasar 1 stack.
For stable local development and reproducible deployment, use `npm` with `Node 16.13.1`.

## Runtime Requirements

```bash
node -v   # must be 16.x
npm -v    # recommended: 8.x
```

If you use `nvm`:

```bash
nvm use
```

## Install Dependencies

```bash
npm ci
```

If `node_modules` does not exist yet and you are doing a first install, `npm install` is also acceptable:

```bash
npm install
```

## Start Development Server

```bash
npm run dev
```

Default URL:

```text
http://127.0.0.1:8080/#/
```

## Build Production Assets

```bash
npm run build
```

## Serve Built SPA

```bash
npm run start
```

## Lint

```bash
npm run lint
```

## Notes

- Use `npm` only for this frontend. Do not mix `npm` and `yarn`.
- The build scripts enforce `Node 16.x` to avoid the OpenSSL / Webpack issues seen on newer Node releases.
- API base URL is read from `public/statics/baseurl.txt`.
