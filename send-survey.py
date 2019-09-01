#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Send out survey invites as email (if possible) or talk page message.

Syntax: python pwb.py send-survey <userlist> <email-template> <wiki-template>
<userlist> is the name of a file with one username per line.
<email-template> is the name of a file with the email title as the first line,
  then an empty line, then the email body (plain text).
<wiki-template> is the name of a file with the talk page section header as the
  first line, then an empty line, then the talk page message.
Both templates can contain the variables $username_plain and $username_encoded
  which will be replaced with the target username (plain or URL-encoded).
"""

import re
import urllib
import pywikibot

from pywikibot import i18n
from pywikibot import pagegenerators

ignoreCategories = {
    'hu': ['Kategória:Tömeges üzenetküldésből kijelentkezettek'],
}

def getIgnoreCategories():
    if not hasattr(getIgnoreCategories, 'cache'):
        setattr(getIgnoreCategories, 'cache', [])
        for cat in (i18n.translate(pywikibot.Site(), ignoreCategories) or []):
            getIgnoreCategories.cache.append(pywikibot.Category(pywikibot.Site(), cat))
    return getIgnoreCategories.cache

def renderTemplate(template_file, username):
    with open(template_file) as f:
        template = f.readlines()
    if template[1].strip() != '':
        raise Exception('invalid template %s: second line must be empty' % template_file)
    head, body = template[0], template[2:]
    body = re.sub(r'\$username_plain\b', username, ''.join(template[2:]))
    body = re.sub(r'\$username_encoded\b', urllib.parse.quote(username), body)
    return (template[0].strip(), body)

def addSection(page, title, body):
    page.text += '\n== %s ==\n\n%s' % (title, body)
    try:
        page.save(summary='/* %s */' % title, watch=True, minor=False,
            force=True, quiet=True, botflag=True)
        return True
    except PageNotSaved:
        return False

def process_user(username, email_template_file, wiki_template_file):
    user = pywikibot.User(pywikibot.Site(), 'User:%s' % username)
    
    for page in [user.getUserPage(), user.getUserTalkPage()]:
        for cat in getIgnoreCategories():
            if cat in page.categories():
                pywikibot.stdout('%s: ignored due to category' % username)
                return
    
    if user.isEmailable():
        title, body = renderTemplate(email_template_file, username)
        if user.send_email(title, body, ccme=True):
            pywikibot.stdout('%s: sent email' % username)
            return
    else:
        title, body = renderTemplate(wiki_template_file, username)
        talkpage = user.getUserTalkPage()
        if addSection(talkpage, title, body):
            pywikibot.stdout('%s: sent talk page message' % username)
            return
    
    pywikibot.output('%s: message sending failed' % username)

def main(*args):
    local_args = pywikibot.handle_args(args)
    with open(local_args[0]) as users:
        for user in [line.rstrip('\n') for line in users]:
            process_user(user, local_args[1], local_args[2])

if __name__ == '__main__':
    main()
