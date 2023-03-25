from django import forms
from .models import Alumno, Docente, Aspirante
from django.contrib.auth import password_validation


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente

        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'matricula'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
        }

    def save(self, commit=True):
        user = super(DocenteForm, self).save(commit=False)
        # Encripta la contraseña
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
            password_validation.MinimumLengthValidator(8)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        return password

    def clean(self):
        super(DocenteForm, self).clean()
        if any(self.errors):
            return self.errors
        matricula_docente = self.cleaned_data['matricula']
        for matricula in Alumno.objects.all().values('matricula'):
            if matricula_docente == matricula['matricula']:
                self.add_error('matricula', forms.ValidationError(
                    'La matrícula ya está en uso por un alumno'))

class DocenteEditForm(forms.ModelForm):
    class Meta:
        model = Docente

        fields = 'username', 'first_name', 'last_name', 'email', 'matricula'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
        }

    def clean(self):
        super(DocenteForm, self).clean()
        if any(self.errors):
            return self.errors
        matricula_docente = self.cleaned_data['matricula']
        for matricula in Alumno.objects.all().values('matricula'):
            if matricula_docente == matricula['matricula']:
                self.add_error('matricula', forms.ValidationError(
                    'La matrícula ya está en uso por un alumno'))

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'matricula'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'password': 'Contraseña',
            'matricula': 'Matrícula',
        }

        # help_texts = {
        #     'username': '',
        # }

    def save(self, commit=True):
        user = super(AlumnoForm, self).save(commit=False)
        # Encripta la contraseña
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
            password_validation.MinimumLengthValidator(8)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        return password

    def clean(self):
        super(AlumnoForm, self).clean()

        if any(self.errors):
            return self.errors
        matricula_alumno = self.cleaned_data['matricula']
        for matricula in Docente.objects.all().values('matricula'):
            if matricula_alumno == matricula['matricula']:
                self.add_error('matricula', forms.ValidationError(
                    'La matrícula ya está en uso por un docente'))
                    
class AlumnoEditForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = 'username', 'first_name', 'last_name', 'email', 'matricula'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'matricula': 'Matrícula',
        }

        # help_texts = {
        #     'username': '',
        # }

    def clean(self):
        super(AlumnoEditForm, self).clean()

        if any(self.errors):
            return self.errors
        matricula_alumno = self.cleaned_data['matricula']
        for matricula in Docente.objects.all().values('matricula'):
            if matricula_alumno == matricula['matricula']:
                self.add_error('matricula', forms.ValidationError(
                    'La matrícula ya está en uso por un docente'))


class AspiranteForm(forms.ModelForm):

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Aspirante
        fields = 'username', 'first_name', 'last_name', 'email', 'password', 'num_aspirante', 'comprobante_pago'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'num_aspirante': forms.NumberInput(attrs={'class': 'form-control'}),
            'comprobante_pago':forms.FileInput(attrs={'class':'form-control'}),
        }

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'password': 'Contraseña',
            'num_aspirante': 'Numero de aspirante',
            'comprobante_pago': 'Comprobante de pago',
        }

    def save(self, commit=True):
        user = super(AspiranteForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password']) #Encripta la contraseña
        if commit:
            user.save()
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
            password_validation.MinimumLengthValidator(8)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        return password

    # Validaciones
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error(
                'password', 'Las contraseñas no coinciden')
        if any(self.errors):
            return self.errors


class AspiranteCorregirForm(forms.ModelForm):
    class Meta:
        model = Aspirante
        fields = ('comprobante_pago',)

        widgets={
            'comprobante_pago':forms.FileInput(attrs={'class':'form-control', "accept":"application/pdf,image/png,image/jpeg"})
        }

        labels={
            'comprobante_pago': 'Comprobante de pago'
        }