# svbtle-jekyll

Convert svbtle posts to Jekyll.

Svbtle does not offer an export feature. This python script scrapes the Svbtle Dashboard for a list of posts, Gets the metadata and content for each post, then renders markdown files with YAML front matter for Jekyll.

svbtle-jekyll does the bare minimum to generate basic jekyll compatibility. The resulting markdown and front matter will need almost certainly need editing. But this will hopefully save some time.

## Usage

First clone the repo and do the normal python dance:

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Now you need to get a cookie from Svbtle. I didn't build functionality to log in to svbtle and retrieve a cookie, so you need to log in using your browser and find the value for the `remember_user_token` cookie. This is pretty simple. Just use your favorite cookie viewer browser extensions. I use [EditThisCookie for Chrome](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en).

Now you can run the tool like this:

    $ python svbtle-jekyll.py -c <cookie> -t <target directory for generated markdown files>

This should grab each post and create an appropriate named Jekyll markdown file at the target specified in `-t`.
