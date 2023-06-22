git switch -m auto-commit
git add -a
git commit -aqm "AUTO COMMIT SERVICE - DEVELOPMENT ONLY"
git switch -m main
git pull
git push
python there_goes_mangoes/util_proxi_ir.py
