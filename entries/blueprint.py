import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app, db
from helpers import object_list, entry_list, get_entry_or_404
from models import Entry, Tag
from entries.forms import EntryForm, ImageForm

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
    tag_entries = []
    raw_tags = set([tag.strip() for tag in slug.split('+') if tag.strip()])
    for tag in raw_tags:
        tag_obj = Tag.query.filter(Tag.slug == tag).first_or_404()
        tag_list.append(tag_obj)
        tag_entries.append([entry.id for entry in tag_obj.entries])
        entries_ids |= set([entry.id for entry in tag_obj.entries])
    for entries in tag_entries:
        entries_ids &= set(entries)
    entries = Entry.query.filter(Entry.id.in_(entries_ids))
    tag_names = " + ".join(["{}".format(tag.name) for tag in tag_list])
    return object_list('entries/tag_detail.html', entries, tag=tag_names)


@entries.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" created successfully.' % entry.title, 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm()

    return render_template('entries/create.html', form=form)


@entries.route('/image-upload/', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        form = ImageForm(request.form)
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'],
                                    secure_filename(image_file.filename))
            image_file.save(filename)
            flash('Saved %s' % os.path.basename(filename), 'success')
            return redirect(url_for('entries.index'))
    else:
        form = ImageForm()

    return render_template('entries/image_upload.html', form=form)


@entries.route('/<slug>/')
def detail(slug):
    entry = get_entry_or_404(slug)
    return render_template('entries/detail.html', entry=entry)


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" has been saved.' % entry.title, 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)

    return render_template('entries/edit.html', entry=entry, form=form)


@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Entry "%s" has been deleted.' % entry.title, 'success')
        return redirect(url_for('entries.index'))

    return render_template('entries/delete.html', entry=entry)
