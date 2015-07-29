learn_drf_nested_resources
==========================

Introduction
------------

This project was created to provide a complete example that illustrates how to implement nested resources on a `Django REST framework <http://www.django-rest-framework.org/>`_ API using `drf-nested-routers <https://github.com/alanjds/drf-nested-routers>`_. In order to make the project as real as possible, the authentication is handled using `Django OAuth Toolkit <https://github.com/evonove/django-oauth-toolkit>`_.

The application
---------------

The application exposes an API to manage blogposts and comments. No provision has been made to display either blogposts nor comments. The model is quite simple as well

::

    class UUIDIdMixin(models.Model):
        class Meta:
            abstract = True

        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    class AuthorMixin(models.Model):
        class Meta:
            abstract = True

        author = models.ForeignKey(
            settings.AUTH_USER_MODEL, editable=False, verbose_name=_('author'),
            related_name='%(app_label)s_%(class)s_author'
        )


    class Blogpost(UUIDIdMixin, TimeStampedModel, TitleSlugDescriptionModel, AuthorMixin):
        content = models.TextField(_('content'), blank=True, null=True)
        allow_comments = models.BooleanField(_('allow comments'), default=True)

        def __str__(self):
            return self.title

    class Comment(UUIDIdMixin, TimeStampedModel, AuthorMixin):
        blogpost = models.ForeignKey(
            Blogpost, editable=False, verbose_name=_('blogpost'), related_name='comments'
        )
        content = models.TextField(_('content'), max_length=255, blank=False, null=False)

I made use of `django-extension <https://github.com/django-extensions/django-extensions>`_'s TimeStampedModel and TitleSlugDescriptionModel to provide the basic features of the model and only added a few things here and there to make it interesting.

The API
-------

The API is where things get interesting. The access to the blogposts is exposed through a DRF ``ModelViewSet``, which provides the usual actions:

    * **list:** ``GET /api/blogposts/`` List all blogposts.
    * **create:** ``POST /api/blogposts/`` Create a new blogpost.
    * **retrieve:** ``GET /api/blogposts/(?P<pk>[^/.]+)/`` Show the details of a specific blogpost.
    * **update:** ``PUT /api/blogposts/(?P<pk>[^/.]+)/`` Update all fields of a specific blogpost.
    * **partial** update: ``PATCH /api/blogposts/(?P<pk>[^/.]+)/`` Update a field of a specific blogpost.
    * **destroy:** ``DELETE /api/blogposts/(?P<pk>[^/.]+)/`` Delete a specific blogpost.

The whole point of the project is to show you how to implement nested resources, so comments are exposed under blogposts:

    * **list:** ``GET /api/blogposts/(?P<blogpost_pk>[^/.]+)/comments`` List all the comments on a specific blogpost.
    * **create:** ``POST /api/blogposts/(?P<blogpost_pk>[^/.]+)/comments`` Create a new comment on a specific blogpost.

The rest of the comment actions are exposed through a top-level ``/comments`` endpoint. The reason for this is that I (and others believe) that resources should be accessible through a single URI.

    * **list:** ``GET /api/comments/`` List all blogposts.
    * **retrieve:** ``GET /api/comments/(?P<pk>[^/.]+)/`` Show the details of a specific comment.
    * **update:** ``PUT /api/comments/(?P<pk>[^/.]+)/`` Update all fields of a specific comment.
    * **partial** update: ``PATCH /api/comments/(?P<pk>[^/.]+)/`` Update a field of a specific comment.
    * **destroy:** ``DELETE /api/comments/(?P<pk>[^/.]+)/`` Delete a specific comment.

This also has the advantage of being quite easy to implement, as it leverages DRF's auto-magic functionality. Everything is handled by three simple viewsets:

::

    class BlogpostViewSet(ModelViewSet):
        serializer_class = BlogpostSerializer
        queryset = Blogpost.objects.all()
        permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

        def perform_create(self, serializer):
            serializer.save(author=self.request.user)


    class CommentViewSet(
        RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
    ):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        permission_classes = (IsAuthenticatedOrReadOnly, CommentDeleteOrUpdatePermission)


    class NestedCommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        permission_classes = (IsAuthenticatedOrReadOnly, CommentsAllowed)

        def get_blogpost(self, request, blogpost_pk=None):
            """
            Look for the referenced blogpost
            """
            # Check if the referenced blogpost exists
            blogpost = get_object_or_404(Blogpost.objects.all(), pk=blogpost_pk)

            # Check permissions
            self.check_object_permissions(self.request, blogpost)

            return blogpost

        def create(self, request, *args, **kwargs):
            self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

            return super().create(request, *args, **kwargs)

        def perform_create(self, serializer):
            serializer.save(
                author=self.request.user,
                blogpost_id=self.kwargs['blogpost_pk']
            )

        def get_queryset(self):
            return Comment.objects.filter(blogpost=self.kwargs['blogpost_pk'])

        def list(self, request, *args, **kwargs):
            self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

            return super().list(request, *args, **kwargs)


The URLs are then wired using a couple of routers:

::

    router = DefaultRouter()
    router.register(r'users', UserViewSet)
    router.register(r'blogposts', BlogpostViewSet)
    router.register(r'comments', CommentViewSet)

    blogposts_router = NestedSimpleRouter(router, r'blogposts', lookup='blogpost')
    blogposts_router.register(r'comments', NestedCommentViewSet)

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^api/', include(router.urls)),
        url(r'^api/', include(blogposts_router.urls)),
        url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]

Usage
--------------

I used OAuth2 for authentication and authorization, and created an application to allow access to the API. The application was defined as "Public" with grant type "Resource owner password-base", so all we need to do to access the API is request an access token: ::

    $ curl --silent --header "Content-Type: application/x-www-form-urlencoded" --data "username=admin&password=admin&grant_type=password&client_id=7ytbv0sG9FusDdDYRcZPUIGoNrx9TBZJnye5CVvj" --request POST http://localhost:8000/o/token/|python -mjson.tool; echo
    {
        "access_token": "Q8Wbo12h5jwgwR208WDNrhNpK20Ta0",
        "expires_in": 36000,
        "refresh_token": "inEHtHuerVRXSH5QjbvokgrqJYxngL",
        "scope": "read write",
        "token_type": "Bearer"
    }

You can request a list of blogposts: ::

    $ curl --header "Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0" --header "Accept: application/json; indent=4"  --request GET http://localhost:8000/api/blogposts/; echo
    [
        {
            "url": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/",
            "title": "A longer blogpost",
            "slug": "a-longer-blogpost",
            "description": "Lorem ipsum dolor sit amet...",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus maximus, lorem eget accumsan maximus, ante mauris lacinia massa, sit amet pellentesque nisl leo eu libero. Fusce hendrerit risus eu vehicula cursus. Duis tincidunt enim eget felis tempus, ut consequat purus elementum.",
            "allow_comments": true,
            "author": "http://127.0.0.1:8000/api/users/2/",
            "created": "2015-07-10T00:15:38.135000Z",
            "modified": "2015-07-10T00:16:34.192000Z"
        },
        {
            "url": "http://127.0.0.1:8000/api/blogposts/b44d4918-219e-4496-9318-b68ab13e2b25/",
            "title": "A short blogpost",
            "slug": "a-short-blogpost",
            "description": "The description of the blogpost is short",
            "content": "This is just a short blogpost.",
            "allow_comments": true,
            "author": "http://127.0.0.1:8000/api/users/2/",
            "created": "2015-07-10T00:14:06.500000Z",
            "modified": "2015-07-10T00:14:06.501000Z"
        }
    ]

You can request a list of comments for a specific blogpost: ::

    $ curl --header "Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0" --header "Accept: application/json; indent=4"  --request GET http://localhost:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/comments/; echo
    [
        {
            "url": "http://127.0.0.1:8000/api/comments/17288f69-bbd7-4758-adfd-a96d0fa5ca01/",
            "content": "I hate the Internet",
            "author": "http://127.0.0.1:8000/api/users/2/",
            "created": "2015-07-10T00:24:47.766000Z",
            "modified": "2015-07-10T00:24:47.766000Z",
            "blogpost": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/"
        }
    ]

You can create create a new comment POSTing to the nested URL for a specific blogpost: ::

    $ curl --verbose --header "Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0" --header "Accept: application/json; indent=4" --header "Content-Type: application/json" --request POST --data '{"content": "No RESTful for the wicked"}' http://localhost:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/comments/; echo
    *   Trying 127.0.0.1...
    * Connected to localhost (127.0.0.1) port 8000 (#0)
    > POST /api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/comments/ HTTP/1.1
    > User-Agent: curl/7.40.0
    > Host: localhost:8000
    > Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0
    > Accept: application/json; indent=4
    > Content-Type: application/json
    > Content-Length: 40
    >
    * upload completely sent off: 40 out of 40 bytes
    < HTTP/1.1 201 CREATED
    < Server: nginx/1.4.6 (Ubuntu)
    < Date: Wed, 29 Jul 2015 18:15:30 GMT
    < Content-Type: application/json; indent=4
    < Transfer-Encoding: chunked
    < Connection: keep-alive
    < Vary: Accept
    < Allow: GET, POST, HEAD, OPTIONS
    < Location: http://127.0.0.1:8000/api/comments/81e5afc6-56fc-47d4-9665-db56229d0fba/
    < X-Frame-Options: SAMEORIGIN
    <
    {
        "url": "http://127.0.0.1:8000/api/comments/81e5afc6-56fc-47d4-9665-db56229d0fba/",
        "content": "No RESTful for the wicked",
        "author": "http://127.0.0.1:8000/api/users/1/",
        "created": "2015-07-29T18:15:30.294242Z",
        "modified": "2015-07-29T18:15:30.294635Z",
        "blogpost": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/"
    * Connection #0 to host localhost left intact
    }

You can verify that the comment was actually created by requesting the list of comments again: ::

    $ curl --header "Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0" --header "Accept: application/json; indent=4"  --request GET http://localhost:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/comments/; echo
    [
        {
            "url": "http://127.0.0.1:8000/api/comments/17288f69-bbd7-4758-adfd-a96d0fa5ca01/",
            "content": "I hate the Internet",
            "author": "http://127.0.0.1:8000/api/users/2/",
            "created": "2015-07-10T00:24:47.766000Z",
            "modified": "2015-07-10T00:24:47.766000Z",
            "blogpost": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/"
        },
        {
            "url": "http://127.0.0.1:8000/api/comments/81e5afc6-56fc-47d4-9665-db56229d0fba/",
            "content": "No RESTful for the wicked",
            "author": "http://127.0.0.1:8000/api/users/1/",
            "created": "2015-07-29T18:15:30.294242Z",
            "modified": "2015-07-29T18:15:30.294635Z",
            "blogpost": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/"
        }
    ]

You can also hit the ``/comments`` endpoint directly to list, update or delete a comment: ::

    $ curl --header "Authorization: Bearer Q8Wbo12h5jwgwR208WDNrhNpK20Ta0" --header "Accept: application/json; indent=4"  --request GET http://localhost:8000/api/comments/81e5afc6-56fc-47d4-9665-db56229d0fba/; echo
    {
        "url": "http://127.0.0.1:8000/api/comments/81e5afc6-56fc-47d4-9665-db56229d0fba/",
        "content": "No RESTful for the wicked",
        "author": "http://127.0.0.1:8000/api/users/1/",
        "created": "2015-07-29T18:15:30.294242Z",
        "modified": "2015-07-29T18:15:30.294635Z",
        "blogpost": "http://127.0.0.1:8000/api/blogposts/588660f1-4848-4a32-8eb5-9688fd4409dd/"
    }

A `Vagrant <https://www.vagrantup.com/>`_ configuration file is included if you want to test the service yourself.

Feedback
--------

As usual, I welcome comments, suggestions and pull requests.
