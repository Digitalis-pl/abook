from django.shortcuts import render,  redirect

from big_library.forms import DocumentForm
from big_library.models import Document

from django.db.models import Q
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import math
# Create your views here.

"TODO: Переписать все в ооп"
"TODO: Переделать таблицы будем хранить словари с важными словами и ссылки, а не кучу файлов и текста"
"TODO: Нормально прописать пути"
"TODO: Если останется время добавить ассинхронку, пока читаем документ он обрабатывается"
"TODO: Уточнить тот ли поисковик я делаю"
"TODO: Поиграться с шаблонами"
"TODO: Прописать функционал странички для записей пользователя"
"TODO: Тесты"


def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')  # После успешной загрузки
    else:
        form = DocumentForm()
    return render(request, 'big_library/upload.html', {'form': form})


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'big_library/document_list.html', {'documents': documents})


# Предобработка текста
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens


# Расчет TF-IDF
def compute_tf_idf(documents, query):
    # Получаем все документы
    tokenized_documents = [preprocess(doc.content) for doc in documents]

    # Расчет TF для каждого документа
    tf_docs = [Counter(doc) for doc in tokenized_documents]

    # Считаем IDF
    num_docs = len(documents)
    idf_values = {}
    all_tokens = set([word for doc in tokenized_documents for word in doc])

    for term in all_tokens:
        containing_docs = sum(1 for doc in tokenized_documents if term in doc)
        idf_values[term] = math.log(num_docs / (1 + containing_docs))

    # TF-IDF для запроса
    query_tokens = preprocess(query)
    query_tf = Counter(query_tokens)
    query_tf_idf = {term: query_tf[term] * idf_values.get(term, 0) for term in query_tf}

    # Сравниваем запрос с документами
    doc_scores = []
    for idx, tf_doc in enumerate(tf_docs):
        score = sum(query_tf_idf.get(term, 0) * (tf_doc.get(term, 0) / len(tf_doc)) * idf_values.get(term, 0) for term in query_tf_idf)
        doc_scores.append((documents[idx], score))

    return sorted(doc_scores, key=lambda x: x[1], reverse=True)


# Представление для поиска
def search_documents(request):
    query = request.GET.get('q', '')
    documents = Document.objects.all()

    if query:
        ranked_documents = compute_tf_idf(documents, query)
        documents = [doc for doc, score in ranked_documents if score > 0]

    return render(request, 'big_library/search.html', {'documents': documents, 'query': query})
