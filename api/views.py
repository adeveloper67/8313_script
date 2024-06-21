from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from api.forms import UploadForm
from ai_asistent.services import read_file
from ai_asistent.gpt4_service import OpenAIClient
from api.models import Prompts


class ApiView(TemplateView):
    def get(self, request, *args, **kwargs):
        prompts = Prompts.objects.all().order_by('-created_at')
        context = {
            'prompts': prompts,
        }

        return render(request, 'api/index.html', context)

    def post(self, request, *args, **kwargs):
        prompts = Prompts.objects.all().order_by('-created_at')
        form = UploadForm(request.POST, request.FILES)
        result = None

        if form.is_valid():
            prompt = prompts.get(id=request.POST.get('prompt')).prompt
            files = request.FILES.getlist('files')
            client = OpenAIClient()
            # files_ids = [file_id.get('id') for file_id in client.get_files()]

            files_ids = []
            for file in files:
                files_ids += [client.upload_file(file)]
            res = client.generate_video_script(
                prompt,
                files_ids,
            )

            result = res.choices[0].message.content
        return render(
            request,
            'api/index.html',
            {'form': form, 'text': result, 'prompts': prompts},
        )


# class UploadSessionViewSet(viewsets.ModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]
#
#     def get(self, request, *args, **kwargs):
#         upload_sessions = UploadSession.objects.all()
#         serializer = UploadSessionSerializer(upload_sessions, many=True)
#         return Response(serializer.data)
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'prompt',
#                 openapi.IN_FORM,
#                 description="Prompt for the upload session",
#                 type=openapi.TYPE_STRING,
#                 required=True,
#             ),
#             openapi.Parameter(
#                 'files',
#                 openapi.IN_FORM,
#                 description="List of files to upload",
#                 type=openapi.TYPE_FILE,
#                 required=True,
#                 multiple=True,
#             ),
#         ],
#         responses={
#             status.HTTP_201_CREATED: UploadSessionSerializer,
#             status.HTTP_400_BAD_REQUEST: 'Bad Request',
#         },
#     )
#     def post(self, request, *args, **kwargs):
#         serializer = UploadSessionSerializer(data=request.data)
#
#         if serializer.is_valid():
#             prompt = serializer.validated_data.get('prompt')
#             files = serializer.validated_data.get('files')
#
#             upload_session = UploadSession.objects.create(prompt=prompt)
#             documents = []
#
#             for file in files:
#                 document_serializer = DocumentSerializer(data={'file': file})
#                 if document_serializer.is_valid():
#                     document = document_serializer.save()
#                     upload_session.files.add(document)
#                     documents.append(document_serializer.instance)
#                 else:
#                     upload_session.delete()
#                     return Response(
#                         document_serializer.errors, status=status.HTTP_400_BAD_REQUEST
#                     )
#             upload_session_serializer = UploadSessionSerializer(upload_session)
#             return Response(
#                 upload_session_serializer.data, status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
