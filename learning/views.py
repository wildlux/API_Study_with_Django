from django.shortcuts import render
import requests
import json
from django.shortcuts import redirect
from .models import Question

def home(request):
    """Homepage che reindirizza alla teoria."""
    return render(request, 'learning/home.html')

def theory(request):
    """Pagina della teoria."""
    return render(request, 'learning/theory.html')

def practice(request):
    """Pagina della pratica."""
    return render(request, 'learning/practice.html')

def exercises(request):
    """Pagina degli esercizi."""
    return render(request, 'learning/exercises.html')

def methods(request):
    """Pagina dei metodi HTTP."""
    return render(request, 'learning/methods.html')

def test_get_request(request):
    """Esegue una richiesta GET reale e restituisce il risultato."""
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users?_limit=3')
        data = response.json()
        result = {
            'success': True,
            'users': data,
            'message': f'Ho ricevuto {len(data)} utenti'
        }
    except Exception as e:
        result = {
            'success': False,
            'message': f'Errore: {str(e)}'
        }
    return render(request, 'learning/result.html', {'result': result})

def test_post_request(request):
    """Esegue una richiesta POST reale e restituisce il risultato."""
    if request.method == 'POST':
        nome = request.POST.get('userName', '')
        if not nome:
            result = {
                'success': False,
                'message': 'Inserisci un nome!'
            }
        else:
            try:
                response = requests.post(
                    'https://jsonplaceholder.typicode.com/users',
                    json={
                        'name': nome,
                        'email': f'{nome.lower()}@test.com'
                    }
                )
                data = response.json()
                result = {
                    'success': True,
                    'user': data,
                    'message': 'Utente creato con successo!'
                }
            except Exception as e:
                result = {
                    'success': False,
                    'message': f'Errore: {str(e)}'
                }
        return render(request, 'learning/result.html', {'result': result})
    return render(request, 'learning/post_form.html')

def quiz_home(request):
    """Pagina principale del quiz."""
    questions = Question.objects.filter(active=True).order_by('order')
    score = request.session.get('quiz_score', 0)
    width = score * 10
    return render(request, 'learning/quiz_home.html', {
        'questions': questions,
        'score': score,
        'width': width
    })

def check_all_answers(request):
    """Verifica tutte le risposte del quiz e reindirizza ai risultati."""
    if request.method == 'POST':
        questions = Question.objects.filter(active=True).order_by('order')
        score = 0
        results = []

        for question in questions:
            user_answer = request.POST.get(f'q{question.id}', '').strip()
            is_correct = False
            if question.question_type == 'closed':
                is_correct = user_answer.lower() == question.correct_answer.lower()
            else:  # open
                is_correct = user_answer.lower() == question.correct_answer.lower()
            if is_correct:
                score += 1
            results.append({
                'question_text': question.text,
                'question_type': question.question_type,
                'correct_answer': question.correct_answer,
                'user_answer': user_answer,
                'is_correct': is_correct
            })

        total = questions.count()
        percentage = (score / total * 100) if total > 0 else 0

        # Salva i risultati nella sessione
        request.session['quiz_score'] = score
        request.session['quiz_total'] = total
        request.session['quiz_percentage'] = int(percentage)
        request.session['quiz_results'] = results

        # Reindirizza alla pagina dei risultati
        return redirect('quiz_results')

    return render(request, 'learning/quiz_home.html')

def quiz_results(request):
    """Mostra i risultati finali del quiz."""
    score = request.session.get('quiz_score', 0)
    total = request.session.get('quiz_total', 0)
    percentage = request.session.get('quiz_percentage', 0)
    results = request.session.get('quiz_results', [])

    # Se non ci sono risultati, reindirizza al quiz
    if not results:
        return redirect('quiz_home')

    return render(request, 'learning/quiz_final_result.html', {
        'score': score,
        'total': total,
        'percentage': percentage,
        'results': results
    })

def check_answer(request):
    """Verifica la risposta del quiz."""
    if request.method == 'POST':
        question = request.POST.get('question')
        user_answer = request.POST.get('answer', '').strip()
        correct_answer = request.POST.get('correct_answer')

        explanations = {
            '1': "GET è usato per leggere dati, POST per creare nuovi dati",
            '2': "Le API REST possono restituire dati in vari formati, tra cui JSON, XML e HTML. JSON è il formato più comune.",
            '3': "Lo status code 404 indica che la risorsa richiesta non è stata trovata sul server.",
            '4': "Il metodo PUT è usato per aggiornare una risorsa esistente sul server.",
            '5': "Il metodo DELETE è usato per eliminare una risorsa dal server.",
            '6': "Lo status code 200 indica che la richiesta è stata elaborata con successo.",
            '7': "I dati inviati in una richiesta POST possono essere in vari formati, tra cui JSON, XML e form-data.",
            '8': "Il metodo GET è usato per leggere dati dal server.",
            '9': "Lo status code 500 indica un errore del server.",
            '10': "Il metodo POST è usato per creare una nuova risorsa sul server."
        }

        explanation = explanations.get(question, '')

        if user_answer.lower() == correct_answer.lower():
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
            result = {
                'correct': True,
                'message': '✅ Risposta corretta!',
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': explanation
            }
        else:
            result = {
                'correct': False,
                'message': f'❌ Risposta sbagliata. La risposta corretta è: {correct_answer}',
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': explanation
            }
        return render(request, 'learning/quiz_result.html', {'result': result})
    return render(request, 'learning/quiz_home.html')