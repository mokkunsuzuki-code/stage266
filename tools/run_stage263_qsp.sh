#!/usr/bin/env bash
set -e

echo "[INFO] Running Stage263 QSP..."

python3 tools/run_stage263_qsp.py

echo "[INFO] Generating verification page..."

mkdir -p _site

cat > _site/index.html <<'HTML'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Stage263 Verification URL</title>
</head>
<body>
  <h1>Stage263 Verification URL</h1>
  <p>QSP execution completed successfully.</p>
</body>
</html>
HTML

echo "[OK] Stage263 complete"
