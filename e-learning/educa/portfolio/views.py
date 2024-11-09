from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PortfolioForm
from .models import Portfolio
from .models import Course

def portfolio_upload(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.student = request.user
            portfolio.course = course
            portfolio.save()
            return redirect('portfolio_detail', pk=portfolio.pk)
    else:
        form = PortfolioForm()
    
    return render(request, 'portfolio/upload.html', {'form': form, 'course': course})

def portfolio_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.is_staff:  # Instructor or admin
        portfolios = Portfolio.objects.filter(course=course)
    else:  # Logged-in student
        portfolios = Portfolio.objects.filter(course=course, student=request.user)
    
    return render(request, 'portfolio/list.html', {'portfolios': portfolios, 'course': course})

def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    return render(request, 'portfolio/detail.html', {'portfolio': portfolio})
