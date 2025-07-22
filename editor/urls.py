from django.urls import path
from .views import dashboard, editor_view,share_document, grammar_suggestions, openai_suggestions, version_history,create_document,upload_document


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload_document, name='upload_document'),
    path('create/', create_document, name='create_document'),
    path('<int:doc_id>/', editor_view, name='editor'),
    path('<int:doc_id>/grammar/', grammar_suggestions, name='grammar'),
    path('<int:doc_id>/openai/', openai_suggestions, name='openai'),
    path('<int:doc_id>/versions/', version_history, name='versions'),
    path('<int:doc_id>/share/', share_document, name='share_document'),

]