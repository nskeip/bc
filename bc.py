#-*- coding: UTF-8 -*-
import os
from yaml import load
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = './_build'
JINJA2_TEMPLATE_DIR = './_templates'
SITE_URL = 'http://localhost'

# fuckyeahbrainlambda!
ext_cleaner = lambda f: f.replace('.yaml', '.html')

loader = lambda d, f: dict(_directory=d,
                           _filename=f,
                           _output=os.path.join(OUTPUT_DIR, d, ext_cleaner(f)),
                           **load(open(os.path.join(d, f))))

get_yamls = lambda ext='.yaml', func=loader: \
                    sorted([loader('.', f) 
                            for f in os.listdir('.') 
                                if f.endswith(ext)], 
                           reverse=True)

# this is how your posts' urls are built
def post_url(post, external=False):
    post_filename = post['_filename']
    if not external:
        return '/%s' % ext_cleaner(post_filename)
    else:
        return '%s/%s' % SITE_URL, ext_cleaner(post_filename)


class UnknownEndpointException(Exception):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __str__(self):
        return repr('I don\'t know such endpoint: %s' % self.endpoint)


# a simple url_for - no directories support
def url_for(endpoint, external=False, **kwargs):
    if endpoint == 'index':
        pattern = '/'
    elif endpoint == 'static':
        pattern = '/static/%(filename)s'
    elif endpoint == 'post':
        pattern = post_url(kwargs['post'], external)
    else:
        raise UnknownEndpointException(endpoint)

    if not external:
        return pattern % kwargs
    else:
        return SITE_URL + pattern % kwargs

jinja_env = Environment(loader=FileSystemLoader(JINJA2_TEMPLATE_DIR))

jinja_env.globals['url_for'] = url_for


def render_template(template, return_response=True, **context):
    return jinja_env.get_template(template).render(**context)


def write_to_page(output_path, template, **template_kwargs):
    text = render_template(template, **template_kwargs)
    f = open(output_path, mode='w')
    f.write(text)
    f.close()


def main():
    posts = get_yamls()

    #render index.html and all posts' pages
    write_to_page(os.path.join(OUTPUT_DIR, 'index.html'),
                  'index.html',
                  posts=posts)
    for p in posts:
        write_to_page(p['_output'], 'one.html', post=p)

if __name__ == '__main__':
    main()
