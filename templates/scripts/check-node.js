'use strict';

const requiredMajor = 16;
const version = process.versions.node;
const major = Number(version.split('.')[0]);

if (major !== requiredMajor) {
  console.error(
    [
      `GreaterWMS frontend requires Node ${requiredMajor}.x for reproducible builds.`,
      `Current Node version: ${version}`,
      'Use `nvm use` in templates/ or switch PATH to a Node 16 installation before running npm scripts.'
    ].join('\n')
  );
  process.exit(1);
}

console.log(`Node version check passed: ${version}`);
