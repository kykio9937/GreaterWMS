#!/bin/bash
cd /GreaterWMS/templates
quasar build
exec node /GreaterWMS/templates/serve-spa.js
