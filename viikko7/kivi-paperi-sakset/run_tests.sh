#!/bin/bash
# Skripti testien ajamiseen

echo "======================================"
echo "   Kivi-Paperi-Sakset - Testit"
echo "======================================"
echo ""

# Siirry oikeaan hakemistoon
cd "$(dirname "$0")/.."

echo "📋 Ajetaan testit..."
python -m pytest

echo ""
echo "======================================"
echo "✅ Testit suoritettu!"
echo "======================================"
echo ""
echo "Lisäkomennot:"
echo "  Verbose-tila:     pytest -v"
echo "  Coverage-raportti: pytest --cov=. --cov-report=html"
echo "  Vain yksikkötestit: pytest src/tests/test_tuomari.py src/tests/test_tekoaly.py"
echo "  Vain web-testit:   pytest src/tests/test_web_app.py"
echo ""
