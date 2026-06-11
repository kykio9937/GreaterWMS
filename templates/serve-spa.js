const http = require('http')
const fs = require('fs')
const path = require('path')
const url = require('url')

const host = '0.0.0.0'
const port = Number(process.env.PORT || 8080)
const distDir = path.join(__dirname, 'dist', 'spa')
const indexFile = path.join(distDir, 'index.html')

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.map': 'application/json; charset=utf-8'
}

function sendFile (filePath, response, statusCode = 200) {
  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' })
      response.end('Server Error')
      return
    }

    const ext = path.extname(filePath).toLowerCase()
    const noCacheAssets = new Set(['.html', '.js', '.css'])
    const headers = {
      'Content-Type': mimeTypes[ext] || 'application/octet-stream',
      'Cache-Control': noCacheAssets.has(ext) ? 'no-store, no-cache, must-revalidate, proxy-revalidate' : 'public, max-age=3600',
      Pragma: noCacheAssets.has(ext) ? 'no-cache' : 'public'
    }
    if (noCacheAssets.has(ext)) {
      headers.Expires = '0'
    }
    response.writeHead(statusCode, headers)
    response.end(content)
  })
}

function resolvePath (pathname) {
  const safePath = path.normalize(pathname).replace(/^(\.\.[/\\])+/, '')
  return path.join(distDir, safePath)
}

const server = http.createServer((request, response) => {
  const parsedUrl = url.parse(request.url)
  const pathname = parsedUrl.pathname === '/' ? '/index.html' : parsedUrl.pathname
  const filePath = resolvePath(pathname)

  fs.stat(filePath, (error, stats) => {
    if (!error && stats.isFile()) {
      sendFile(filePath, response)
      return
    }

    sendFile(indexFile, response)
  })
})

server.listen(port, host, () => {
  console.log(`GreaterWMS SPA server listening at http://${host}:${port}`)
})

