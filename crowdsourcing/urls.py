from django.conf import settings
from django.conf.urls import handler404, handler500, handler403
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from account import views as user_views
from projects.views import (
    SearchView,
    SearchProjectProfileView,
    SearchProjectContributionView,
    SearchCategorieView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    RequirementDetailView,
    RequirementDeleteView,
    get_pdf,
    like_project,
    dislike_project,
    like_project_list
)
from projects import views

urlpatterns = [
    
    path('pdf/<pk>/<slug:slug>/', views.get_pdf, name="get-pdf"),
    path('like-project/<id>/', views.like_project, name="like-project"),
    path('dislike-project/<id>/', views.dislike_project, name="dislike-project"),
    path('like-project-list/', views.like_project_list, name="like-project-list"),

    path('admin/', admin.site.urls),
    path('', ProjectListView.as_view(), name='project-list'),
    path('search/', SearchView.as_view(), name='search'),
    path('search-profile-project/', SearchProjectProfileView.as_view(), name='search-profile-project'),
    path('search-contribution-project/', SearchProjectContributionView.as_view(), name='search-contribution-project'),
    path('search-categorie/', SearchCategorieView.as_view(), name='search-categorie'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('requirement/<pk>/', RequirementDetailView.as_view(), name='requirement-detail'),
    path('requirement/<pk>/like-req',views.like_req, name='like-req'),
    path('requirement/<pk>/dislike-req', views.dislike_req, name='dislike-req'),
    path('project/<pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('requirement/<pk>/delete/', RequirementDeleteView.as_view(), name='requirement-delete'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('tinymce/', include('tinymce.urls')),
]

admin.site.site_header = ("CROWDSOURCING Administration")
admin.site.site_title = ("CROWDSOURCING PSI 2020")

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = user_views.error_404
handler500 = user_views.error_500
handler403 = user_views.error_403
