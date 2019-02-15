import aiohttp.web
import urllib.parse
from . import app, CONFIG
from .database import DATABASE

host = CONFIG['ap']['host']
note = CONFIG['note']

inboxes = DATABASE.get('relay-list', [])

async def default(request):
    targets = '<br>'.join([urllib.parse.urlsplit(target).hostname for target in inboxes])
    return aiohttp.web.Response(
        status=200,
        content_type="text/html",
        charset="utf-8",
        text="""
<!DOCTYPE html>
<html lang='en'><head>
 <meta charset='utf-8'>
 <link href='https://kazvam.com/kaz-favicon.png' rel='icon' type='image/x-icon'>
 <link href='https://relay.kazvam.com/' rel='canonical'>
 <title>ActivityPub Relay at {host}</title>
 <meta name='author' content='Roumen Damianoff (damianoff.com)'>
 <meta name='publisher' content='Kazvam.com (kazvam.com)'>
 <meta name='generator' content='Kazvam.com (kazvam.com)'>
 <meta name='description' content='ActivityPub (Mastodon/Pleroma) relay server hosted by Kazvam.com'>
 <meta name='keywords' content='ActivityPub relay, kazvam, mastodon, pleroma'>
 <meta name='robots' content='index, follow, noodp, noydir'>
<style>
  h1,h2,p {{ color: #FFFFFF; font-family: monospace, arial; font-size: 100%; }}
  body {{ background-color: #000000; }}
  </style>
</head>
<body>
<section>
<h1>{note}</h1>
<h2>This is an Activity Relay for fediverse instances.</h2>
<p>For Mastodon instances, you may subscribe to this relay with the address: <a href="https://{host}/inbox">https://{host}/inbox</a></p>
<p>For Pleroma and other instances, you may subscribe to this relay with the address: <a href="https://{host}/actor">https://{host}/actor</a></p>
<p>To host your own relay, you may download the code at this address: <a href="https://gitlab.com/Kazvam/relay">https://gitlab.com/Kazvam/relay</a></p>
<br><p>List of {count} registered instances:<br><br><b>{targets}</b></p>
<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="kazvam logo" style="display:none;">
</section>
</body></html>

""".format(host=host, note=note,targets=targets,count=len(inboxes)))

app.router.add_get('/', default)
