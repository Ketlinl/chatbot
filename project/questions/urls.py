from django.urls import path
from project.questions import views

app_name = 'questions'

urlpatterns = [
    path("", views.QuestionsView.as_view(), name="list")
    # path("pergunta/<int:id>/", views.question)
    # path("<int:user_id>/criar-pergunta/", views.create_question)
    # path("salvar-criacao/", views.save_creation)
    # path("editar-pergunta/<int:id>/", views.update_question)
    # path("salvar-edicao/", views.save_updation)
    # path("deletar-pergunta/<int:id>/", views.delete_question)
    # path("salvar-delecao/", views.save_deletion)
    # path("<int:user_id>/chatbot/", views.chatbot)
    # path("<int:user_id>/answer/<int:question_relation_id>/<str:question>/", views.answer)
    # path("<int:user_id>/api/", views.api)
]
