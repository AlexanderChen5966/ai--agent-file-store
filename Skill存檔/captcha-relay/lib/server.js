/**
 * Lightweight HTTP relay server for CAPTCHA solving
 */
const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ALLOWED_TYPES = ['recaptcha-v2', 'hcaptcha', 'turnstile'];
const MAX_BODY_SIZE = 10 * 1024; // 10KB
const MAX_TOKEN_SIZE = 8192; // some providers generate long tokens

function escapeHtmlAttr(s) {
  return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, '&#39;');
}

const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Referrer-Policy': 'no-referrer',
};

function createRelayServer({ type, sitekey, pageUrl, timeout = 120000, bindAll = false }) {
  return new Promise((resolve, reject) => {
    // Validate CAPTCHA type against whitelist
    if (!ALLOWED_TYPES.includes(type)) {
      reject(new Error(`Unsupported CAPTCHA type: ${type}`));
      return;
    }

    // Generate one-time nonce for token submission auth
    const nonce = crypto.randomBytes(16).toString('hex');

    let tokenResolve;
    const tokenPromise = new Promise(r => { tokenResolve = r; });
    let server;
    let timer;
    let tokenReceived = false;

    const templateFile = path.join(__dirname, 'templates', `${type}.html`);
    let template;
    try {
      template = fs.readFileSync(templateFile, 'utf-8');
    } catch {
      reject(new Error('Template not found'));
      return;
    }

    const html = template
      .replace(/\{\{SITEKEY\}\}/g, escapeHtmlAttr(sitekey))
      .replace(/\{\{PAGE_URL\}\}/g, escapeHtmlAttr(pageUrl || ''))
      .replace(/\{\{NONCE\}\}/g, nonce); // nonce is hex-only, safe

    const host = bindAll ? '0.0.0.0' : '127.0.0.1';

    server = http.createServer((req, res) => {
      // Apply security headers to all responses
      for (const [k, v] of Object.entries(SECURITY_HEADERS)) {
        res.setHeader(k, v);
      }

      if (req.method === 'GET' && req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(html);
      } else if (req.method === 'POST' && req.url === '/token') {
        let body = '';
        let size = 0;
        let aborted = false;
        req.on('data', (chunk) => {
          size += chunk.length;
          if (size > MAX_BODY_SIZE) {
            aborted = true;
            res.writeHead(413, { 'Content-Type': 'text/plain' });
            res.end('Payload too large');
            req.destroy();
          } else {
            body += chunk;
          }
        });
        req.on('end', () => {
          if (aborted) return;
          try {
            const parsed = JSON.parse(body);
            const { token, nonce: submittedNonce } = parsed;

            // Verify nonce
            if (!submittedNonce || submittedNonce !== nonce) {
              res.writeHead(403, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ ok: false, error: 'Invalid nonce' }));
              return;
            }

            // Only accept one token
            if (tokenReceived) {
              res.writeHead(409, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ ok: false, error: 'Token already received' }));
              return;
            }

            if (!token || typeof token !== 'string' || token.length > MAX_TOKEN_SIZE) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ ok: false, error: 'Invalid token' }));
              return;
            }

            tokenReceived = true;
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ ok: true }));
            tokenResolve(token);
          } catch {
            res.writeHead(400);
            res.end('Bad request');
          }
        });
      } else {
        res.writeHead(404);
        res.end('Not found');
      }
    });

    // Protect against slow-loris attacks
    server.requestTimeout = 30000;
    server.headersTimeout = 10000;

    server.listen(0, host, () => {
      const port = server.address().port;
      timer = setTimeout(() => {
        server.close();
        tokenResolve(null); // timeout
      }, timeout);

      resolve({
        port,
        waitForToken: async () => {
          const token = await tokenPromise;
          clearTimeout(timer);
          server.close();
          return token;
        },
        close: () => {
          clearTimeout(timer);
          server.close();
        },
      });
    });

    server.on('error', reject);
  });
}

module.exports = { createRelayServer };
