#-*- coding: UTF-8 -*-
import os
from yaml import load
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = './_build'
JINJA2_TEMPLATE_DIR = './_templates'
SITE_URL = 'http://localhost'

# fuckyeahbrainlambda!
ext_cleaner = lambda f: f.replace('.yaml', '.html')

# post_url - to use in jinja2
# maybe later it will be used for directories support
# or maybe fuck that - i'm too lazy
post_url = (lambda post: '%s/%s' % SITE_URL, ext_cleaner(post['_filename']))

loader = lambda d, f: dict(_directory=d, 
                           _filename=f,
                           _output=os.path.join(OUTPUT_DIR, d,ext_cleaner(f)),
                           **load(open(os.path.join(d, f))))

def get_yamls(ext='yaml', func=loader):
    for dirname, dirnames, filenames in os.walk('.'):
        return [func(dirname, filename)
                for filename in filenames
                    if filename.endswith(ext)]

jinja_env = Environment(loader=FileSystemLoader(JINJA2_TEMPLATE_DIR))

def render_template(template, return_response=True, **context):
    return jinja_env.get_template(template).render(**context)

def write_to_page(output_path, template, **template_kwargs):
    text = render_template('one.html', **template_kwargs)
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

