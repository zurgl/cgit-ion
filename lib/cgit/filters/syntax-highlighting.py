#!/usr/bin/env python3

# This script uses Pygments and Python3. You must have both installed
# for this to work.
#
# http://pygments.org/
# http://python.org/
#
# It may be used with the source-filter or repo.source-filter settings
# in cgitrc.
#
# The following environment variables can be used to retrieve the
# configuration of the repository for which this script is called:
# CGIT_REPO_URL        ( = repo.url       setting )
# CGIT_REPO_NAME       ( = repo.name      setting )
# CGIT_REPO_PATH       ( = repo.path      setting )
# CGIT_REPO_OWNER      ( = repo.owner     setting )
# CGIT_REPO_DEFBRANCH  ( = repo.defbranch setting )
# CGIT_REPO_SECTION    ( = section        setting )
# CGIT_REPO_CLONE_URL  ( = repo.clone-url setting )


import sys
import io
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import TextLexer
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter


sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
data = sys.stdin.read()
filename = sys.argv[1]
#formatter = HtmlFormatter(style='pastie', nobackground=True)
formatter = HtmlFormatter(nobackground=True)

try:
	lexer = guess_lexer_for_filename(filename, data)
except ClassNotFound:
	# check if there is any shebang
	if data[0:2] == '#!':
		lexer = guess_lexer(data)
	else:
		lexer = TextLexer()
except TypeError:
	lexer = TextLexer()

# highlight! :-)
# printout pygments' css definitions as well
sys.stdout.write('<style>')


sys.stdout.write('''
@media only all and (prefers-color-scheme: dark) {
.markdown-body a.absent { color: #f33; }
.markdown-body h1 .mini-icon-link, .markdown-body h2 .mini-icon-link, .markdown-body h3 .mini-icon-link, .markdown-body h4 .mini-icon-link, .markdown-body h5 .mini-icon-link, .markdown-body h6 .mini-icon-link { color: #eee; }
div#cgit .markdown-body h1 a.toclink, div#cgit .markdown-body h2 a.toclink, div#cgit .markdown-body h3 a.toclink, div#cgit .markdown-body h4 a.toclink, div#cgit .markdown-body h5 a.toclink, div#cgit .markdown-body h6 a.toclink { color: #eee; }
.markdown-body h1 { color: #eee; }
.markdown-body h2 { border-bottom-color: #333; color: #eee; }
.markdown-body h6 { color: #888; }
.markdown-body hr { border-color: #333; }
.markdown-body blockquote { border-left-color: #222; color: #888; }
.markdown-body table th, .markdown-body table td { border-color: #333; }
.markdown-body table tr { border-top-color: #333; background-color: #111; }
.markdown-body table tr:nth-child(2n) { background-color: #070707; }
.markdown-body span.frame span span { color: #ccc; }
.markdown-body code, .markdown-body tt { border-color: #151515; background-color: #070707; }
.markdown-body .highlight pre, .markdown-body pre { background-color: #070707; border-color: #333; }
''')
sys.stdout.write(HtmlFormatter(style='github-dark').get_style_defs('.highlight'))
sys.stdout.write('''
}   
''')

sys.stdout.write('''
@media (prefers-color-scheme: light) {
''')
sys.stdout.write(HtmlFormatter(style='pastie').get_style_defs('.highlight'))
sys.stdout.write('''
}   
''')




sys.stdout.write('</style>')
sys.stdout.write(highlight(data, lexer, formatter, outfile=None))
