for group in active inactive new; do
    echo "== Sending to $group users"
    python3 /data/project/shared/pywikibot/core/pwb.py /home/tgr/editor-retention-surveys/send-survey.py test.userlist $group-email.tmpl $group-wiki.tmpl -putthrottle:1 |& tee $group-send.log
done
