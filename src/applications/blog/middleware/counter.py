from django.http import HttpRequest


class CounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path.startswith("/b"):
            from applications.blog.models import Post

            posts = Post.objects.all()

            path_parts = request.path.split("/")
            pk = path_parts[-2]
            if pk.isdigit():
                posts = posts.filter(pk=pk)

            for post in posts:
                post.nr_views = (post.nr_views or 0) + 1
                post.save()

        response = self.get_response(request)

        return response
