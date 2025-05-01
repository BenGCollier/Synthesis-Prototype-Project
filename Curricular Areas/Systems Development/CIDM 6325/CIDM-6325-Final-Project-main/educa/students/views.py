from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from courses.models import Course
from .models import PortfolioEntry
from .forms import PortfolioEntryForm
from django.shortcuts import get_object_or_404


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )
        login(self.request, user)
        return result
    
    
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )
    

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context
    

class PortfolioEntryCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioEntry
    form_class = PortfolioEntryForm
    template_name = 'students/portfolio/portfolio_form.html'

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_portfolio_list', args=[self.kwargs['course_id']])


class PortfolioEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = PortfolioEntry
    form_class = PortfolioEntryForm
    template_name = 'students/portfolio/portfolio_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)

    def get_success_url(self):
        return reverse_lazy('student_portfolio_list', args=[self.object.course.id])


class PortfolioEntryDetailView(LoginRequiredMixin, DetailView):
    model = PortfolioEntry
    template_name = 'students/portfolio/portfolio_detail.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='Instructor').exists():
            return super().get_queryset()
        return super().get_queryset().filter(student=user)



class PortfolioEntryListView(LoginRequiredMixin, ListView):
    model = PortfolioEntry
    template_name = 'students/portfolio/portfolio_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name='Instructor').exists():
            return super().get_queryset().filter(course_id=self.kwargs['course_id'])
        return super().get_queryset().filter(
            student=user,
            course_id=self.kwargs['course_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context
