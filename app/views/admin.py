from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.utils import admin_required

from flask_mongoengine.wtf import model_form

from flask_login import login_required
from app.models import Post, BlogPost, Image, Video
from slugify import slugify

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [login_required, admin_required]
    cls = Post

    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)


class Detail(MethodView):
    decorators = [login_required, admin_required]

    class_map = {
        'post': BlogPost,
        'video': Video,
        'image': Image,
    }

    def get_context(self, slug=None):

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            cls = post.__class__
            form_cls = model_form(cls, exclude=('created_at', 'comments', 'slug'))
            if request.method == 'POST':
                form = form_cls(request.form, initial=post._data)
            else:
                form = form_cls(obj=post)
        else:
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(cls, exclude=('created_at', 'comments', 'slug'))
            form = form_cls(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.tags = request.form['postTags'].split(',')
            post.slug = slugify(post.title)
            post.save()

            return redirect(url_for('admin.index'))

        return render_template('admin/detail.html', **context)

admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))