from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .models import Document, DocumentVersion
from .forms import DocumentForm, FileUploadForm, ShareDocumentForm
from .ai import check_grammar, suggest_edit

import json
import fitz  # PyMuPDF
import docx
from io import BytesIO
from bs4 import BeautifulSoup

# ----------------- DASHBOARD -----------------
@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '-last_updated')
    docs = Document.objects.filter(owner=request.user)
    if query:
        docs = docs.filter(title__icontains=query)
    docs = docs.order_by(sort)
    return render(request, 'editor/dashboard.html', {
        'documents': docs,
        'query': query,
        'sort': sort
    })

# ----------------- EDITOR -----------------
@login_required
def editor_view(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    if request.user != doc.owner and request.user not in doc.collaborators.all():
        return HttpResponseForbidden()
    return render(request, 'editor/editor.html', {'doc': doc})

# ----------------- AI SUGGESTIONS -----------------
@csrf_exempt
@login_required
def grammar_suggestions(request, doc_id):
    print("Grammar API called!")
    doc = get_object_or_404(Document, id=doc_id)

    if request.user != doc.owner and request.user not in doc.collaborators.all():
        return HttpResponseForbidden("You are not authorized.")

    try:
        data = json.loads(request.body)
        html_content = data.get('content', '')
        plain_text = BeautifulSoup(html_content, "html.parser").get_text()

        print("Extracted plain text:", plain_text[:100])
        suggestions = check_grammar(plain_text)
        return JsonResponse(suggestions)
    except Exception as e:
        print("Error in grammar_suggestions:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def openai_suggestions(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    if request.user != doc.owner and request.user not in doc.collaborators.all():
        return HttpResponseForbidden()

    try:
        data = json.loads(request.body)
        html_content = data.get('content', '')
        plain_text = BeautifulSoup(html_content, "html.parser").get_text()

        improved = suggest_edit(plain_text)

        suggested_text = ""
        try:
            suggested_text = improved['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError):
            suggested_text = str(improved)

        return JsonResponse({
            "suggested": suggested_text,
            "tokens_used": improved.get("usage", {}).get("total_tokens", 0)
        })
    except Exception as e:
        print("Error in openai_suggestions:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

# ----------------- VERSION HISTORY -----------------
@login_required
def version_history(request, doc_id):
    versions = DocumentVersion.objects.filter(document_id=doc_id).order_by('-edited_at')
    return render(request, 'editor/versions.html', {'versions': versions})

@login_required
def revert_version(request, doc_id, version_id):
    doc = get_object_or_404(Document, id=doc_id)
    if request.user != doc.owner and request.user not in doc.collaborators.all():
        return HttpResponseForbidden()
    version = get_object_or_404(DocumentVersion, id=version_id, document=doc)
    doc.content = version.content
    doc.save()
    return redirect('editor', doc_id=doc.id)

# ----------------- CREATE DOCUMENT -----------------
@login_required
def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.save()
            return redirect('editor', doc_id=doc.id)
    else:
        form = DocumentForm()
    return render(request, 'editor/create.html', {'form': form})

# ----------------- UPLOAD DOCUMENT -----------------
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            name = file.name
            ext = name.split('.')[-1].lower()

            try:
                if ext == 'pdf':
                    doc_file = fitz.open(stream=file.read(), filetype="pdf")
                    content = "\n".join([page.get_text() for page in doc_file])
                elif ext == 'docx':
                    file_stream = BytesIO(file.read())
                    docx_file = docx.Document(file_stream)
                    content = "\n".join([para.text for para in docx_file.paragraphs])
                else:
                    return JsonResponse({'error': f'Unsupported file type: .{ext}'}, status=400)

                new_doc = Document.objects.create(
                    title=name,
                    content=content,
                    owner=request.user
                )
                return redirect('editor', doc_id=new_doc.id)

            except Exception as e:
                return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)
    else:
        form = FileUploadForm()
    return render(request, 'editor/upload.html', {'form': form})

# ----------------- SHARE DOCUMENT -----------------
@login_required
def share_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id, owner=request.user)
    if request.method == 'POST':
        form = ShareDocumentForm(request.POST)
        if form.is_valid():
            doc.collaborators.set(form.cleaned_data['users'])
            doc.save()
            return redirect('editor', doc_id=doc.id)
    else:
        form = ShareDocumentForm(initial={'users': doc.collaborators.all()})
    return render(request, 'editor/share.html', {'form': form, 'doc': doc})
