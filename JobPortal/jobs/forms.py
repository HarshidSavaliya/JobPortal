from django import forms

JOB_TYPES = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('internship', 'Internship'),
    ('contract', 'Contract'),
]

JOB_CATEGORIES = [
    ('it', 'IT / Software'),
    ('marketing', 'Marketing'),
    ('finance', 'Finance'),
    ('hr', 'Human Resources'),
    ('other', 'Other'),
]

class JobForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    job_type = forms.ChoiceField(
        choices=JOB_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    job_category = forms.ChoiceField(
        choices=JOB_CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    job_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    company = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    education_requirements = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    experience_requirements = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    skills_required = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    languages_required = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    def clean_salary(self):
        salary = self.cleaned_data['salary']

        if salary <= 0:
            raise forms.ValidationError("Salary must be greater than zero.")

        if salary < 1000:
            raise forms.ValidationError("Salary looks too low.")

        return salary