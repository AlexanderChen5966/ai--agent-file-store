#!/usr/bin/env node
/**
 * Browser Relay CLI — start a relay server for a headless Chrome tab
 * Usage: node browser-relay-cli.js [--port 8787] [--cdp-port 18800] [--target-id <id>]
 */
const { createBrowserRelay } = require('./lib/browser-relay');
const { getTailscaleIp } = require('./lib/tunnel');

const args = process.argv.slice(2);
function getArg(name, def) {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] ? args[i + 1] : def;
}

function parsePort(val) {
  const n = parseInt(val, 10);
  if (isNaN(n) || n < 1 || n > 65535) throw new Error(`Invalid port: ${val}`);
  return n;
}

function parseTimeout(val) {
  const n = parseInt(val, 10);
  if (isNaN(n) || n < 1) throw new Error(`Invalid timeout: ${val}`);
  return n;
}

(async () => {
  try {
    const relay = await createBrowserRelay({
      cdpPort: parsePort(getArg('--cdp-port', '18800')),
      targetId: getArg('--target-id', undefined),
      port: parsePort(getArg('--port', '8787')),
      timeout: parseTimeout(getArg('--timeout', '300')) * 1000,
    });
    console.log(`\n Browser Relay running!`);
    console.log(`   Local:     http://localhost:${relay.port}`);
    const tsIp = getTailscaleIp();
    if (tsIp) {
      console.log(`   Tailscale: http://${tsIp}:${relay.port}`);
    }
    console.log();
  } catch (e) {
    console.error('Failed to start:', e.message);
    process.exit(1);
  }
})();
