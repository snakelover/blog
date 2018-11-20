from flask import Blueprint, redirect, render_template, request, url_for
from helpers import object_list
from models import Entry, Tag
from entries.forms import EntryForm
from app import db

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    entries = Entry.query.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return entry_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    tag_list = []
    entries_ids = set()
    tags = set(slug.split('+'))
    tag_entries = []
    for tag in tags:
        tag_obj = Tag.query.filter(Tag.slug == tag).first_or_404()
        tag_list.append(tag_obj)
        tag_entries.append([entry.id for entry in tag_obj.entries])
        entries_ids |= set([entry.id for entry in tag_obj.entries])
    for entries in tag_entries:
        entries_ids &= set(entries)
    entries = Entry.query.filter(Entry.id.in_(entries_ids))
    tag_names = ", ".join(["<{}>".format(tag.name) for tag in tag_list])
    return object_list('entries/tag_detail.html', entries, tag=tag_names)


@entries.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm()

    return render_template('entries/create.html', form=form)


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
