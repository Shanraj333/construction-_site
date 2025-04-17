from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import ProfileForm, EngineerRegistrationForm,ContractorRegistrationForm,workerRegistrationForm
from .models import Profile
from allauth.account.forms import SignupForm

from django.shortcuts import render, redirect
from .models import Profile, Feedback
from .forms import FeedbackForm

def home(request):
    # Search query and section
    q = request.GET.get('q', '')
    section = request.GET.get('section', 'default')

    # Filter profiles by category and search
    engineers = Profile.objects.filter(category='engineer', is_approved=True, name__icontains=q)
    contractors = Profile.objects.filter(category='contractor', is_approved=True, name__icontains=q)
    workers = Profile.objects.filter(category='worker', is_approved=True, name__icontains=q)

    # Handle feedback form submission
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/#feedback')  # Redirect to feedback section after submission
    else:
        form = FeedbackForm()

    # Get all feedbacks
    feedbacks = Feedback.objects.all().order_by('-id')

    # Calculate empty card placeholders (to always show 3 cards)
    empty_engineer_cards = max(0, 3 - engineers.count())
    empty_contractor_cards = max(0, 3 - contractors.count())
    empty_worker_cards = max(0, 3 - workers.count())

    context = {
        'engineers': engineers,
        'contractors': contractors,
        'workers': workers,
        'empty_engineer_cards': range(empty_engineer_cards),
        'empty_contractor_cards': range(empty_contractor_cards),
        'empty_worker_cards': range(empty_worker_cards),
        'q': q,
        'section': section,
        'form': form,
        'feedbacks': feedbacks,
    }

    return render(request, 'home.html', context)
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')

@login_required
def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "✅ Your profile has been submitted!")
            return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'add_profile.html', {'form': form})


# ENGINEER REGISTRATION

def register_engineer(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_no = request.POST.get('license_no')
        image = request.FILES.get('image')
        license_file = request.FILES.get('license_file')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        bio = request.POST.get('bio')

        Profile.objects.create(
            name=full_name,
            email=email,
            phone=phone,
            license_no=license_no,
            image=image,
            license_file=license_file,
            specialization=specialization,
            experience=experience,
            description=bio,
            category='engineer',
            is_approved=False
        )
        messages.success(request, '✅ Your engineer profile has been submitted for approval!')
        return redirect('home')  # redirect to home after submission

    return render(request, 'register_engineer_form.html')


def register_contractor(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_no = request.POST.get('license_no')
        license_file = request.FILES.get('license_file')
        image = request.FILES.get('image')  # ✅ get the uploaded profile image
        services_offered = request.POST.get('services_offered')
        years_active = request.POST.get('years_active')
        bio = request.POST.get('bio')

        Profile.objects.create(
            name=company_name,
            email=email,
            phone=phone,
            license_no=license_no,
            license_file=license_file,
            image=image,  # ✅ save the image
            specialization=services_offered,
            experience=years_active,
            description=bio,
            category='contractor',
            is_approved=False
        )
        messages.success(request, '✅ Your contractor profile has been submitted for approval!')
        return redirect('home')

    return render(request, 'register_contractor_form.html')


# worker REGISTRATION
def register_worker(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_no = request.POST.get('license_no')
        license_file = request.FILES.get('license_file')
        specialty = request.POST.get('specialization')
        years_experience = request.POST.get('experience')
        bio = request.POST.get('bio')
        image = request.FILES.get('image') 

        Profile.objects.create(
            name=name,
            email=email,
            phone=phone,
            image=image, 
            license_no=license_no,
            license_file=license_file,
            specialization=specialty,
            experience=years_experience,
            description=bio,
            category='worker',
            is_approved=False
        )
        messages.success(request, '✅ Your worker profile has been submitted for approval!')
        return redirect('home')

    return render(request, 'register_worker_form.html')

def engineers_list(request):
    engineers = Profile.objects.filter(category='engineer', is_approved=True)
    return render(request, 'includes/engineer_list.html', {'profiles': engineers})


def contractors_list(request):
    contractors = Profile.objects.filter(category='contractor', is_approved=True)
    return render(request, 'includes/contractor_list.html', {'profiles': contractors})


def workers_list(request):
    workers = Profile.objects.filter(category='worker', is_approved=True)
    return render(request, 'includes/worker_list.html', {'profiles': workers})


def signup_view(request):
    form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


@staff_member_required
def admin_dashboard(request):
    # List of categories for display
    categories = ['engineer', 'contractor', 'worker']

    # Get selected category from query params, default to 'engineer'
    category = request.GET.get('category', 'engineer')
    feedbacks = Feedback.objects.all().order_by('-id')

    # Get pending and approved profiles for that category
    pending_profiles = Profile.objects.filter(category=category, is_approved=False)
    approved_profiles = Profile.objects.filter(category=category, is_approved=True)

    return render(request, 'admin_dashboard.html', {
        'categories': categories,
        'category': category,
        'profiles': pending_profiles,
        'approved_profiles': approved_profiles,
        'feedbacks': feedbacks,
    })
@staff_member_required
def approve_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.is_approved = True
    profile.save()
    messages.success(request, f"{profile.name} has been approved!")
    return redirect('admin_dashboard')
def reject_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.delete()
    return redirect('admin_dashboard')



def delete_profile(request, profile_id):
    if request.method == "POST":
        profile = get_object_or_404(Profile, id=profile_id)
        profile.delete()
        messages.success(request, "Profile deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', '/admin_dashboard'))

def delete_all_profiles(request, category):
    if request.method == "POST":
        Profile.objects.filter(category=category, is_approved=True).delete()
        messages.success(request, f"All approved {category}s deleted.")
    return redirect('admin_dashboard')

def feedback_view(request):
    feedbacks = Feedback.objects.order_by('-created_at')
    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Or wherever your home view is

    return render(request, 'home.html', {
        'form': form,
        'feedbacks': feedbacks
    })

def delete_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
    return redirect('admin_dashboard')  