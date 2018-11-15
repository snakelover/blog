from flask import Blueprint, render_template, request
from helpers import object_list
from models import Entry, Tag

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    entries = Entry.query.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return entry_list('entries/tag_index.html', tags)


@entries.route('/tags/<slugs>/')
def tag_detail(slugs):
    tags_list = []
    entries = set()
    slugs = slugs.split('+')
    for slug in slugs:
        tags_list.append(Tag.query.filter(Tag.slug == slug).first_or_404())
        print(tags_list)
    tags_names = [tag.name for tag in tags_list]
    entries = Entry.query.filter(set(tags_names) == set(tags_list))
    print("")
    print(entries)
    return object_list('entries/tag_detail.html', entries, tag=tags_list)


@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter((Entry.slug == slug) 
                             & (Entry.status == Entry.STATUS_PUBLIC)).first_or_404()
    return render_template('entries/detail.html', entry=entry)


def entry_list(template, query, **context):
    search = request.args.get('q')
    if search:
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search)))
    return object_list(template, query, **context)
