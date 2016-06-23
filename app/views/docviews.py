from flask import Blueprint, request, redirect, render_template, url_for, g, jsonify
from flask.views import MethodView, View
from app.models import Post, Comment, User, Replay
from flask_mongoengine.wtf import model_form
from pymongo.errors import OperationFailure


posts = Blueprint('posts', __name__, template_folder='templates')


class Search(View):
    def dispatch_request(self):
        posts = Post.objects()
        if 'tag' in request.args:
            tag = request.args.get('tag')
            posts = posts.filter(tags=tag)
        if 'search' in request.args:
            query = request.args.get('search')
            try:
                posts = posts.search_text(query).order_by('$text_score')
            except OperationFailure:
                return redirect(url_for('index'))
        try:
            return render_template('posts/list.html', posts=posts)
        except OperationFailure:
            return redirect(url_for('index'))


class Taglist(View):
    def dispatch_request(self):
        return jsonify(sorted(list(Post.get_all_tags())))


class ListView(MethodView):

    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at', 'author', 'replays'])
    replay_form = model_form(Replay, exclude=['created_at', 'author'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form if not g.user.is_anonymous else None,

            "author": User.objects(email=g.user.email)[0] if not g.user.is_anonymous else None
        }

        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)
            comment.author = context.get('author')
            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)


posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/taglist', view_func=Taglist.as_view('taglist'))
posts.add_url_rule('/search', view_func=Search.as_view('search'))