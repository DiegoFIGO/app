from datetime import datetime
from django import forms
from django.forms import *

from core.erp.models import Acquisitionservices, Budget, Category, Certification, Construcction, Informsuni, Perfil, Product, Client, Project, Publics, Represent, Sale, Position, Employer,  Servicesp, Acquisitionbs, Treasury, Productive, Perfilprod
from django.forms import ModelForm


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        #forma de validar texto nº1
        # self.fields['names'].widget.attrs['onkeypress'] = "return sololetras(event)"
        # self.fields['surnames'].widget.attrs['onkeypress'] = "return sololetras(event)"

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    #forma de validar texto nº2
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    #forma de validar texto nº2
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su número de cédula',
                    'maxlength': "10", # limitar numeros con CHARFIELD EN LA BASE, CON NUMBERINPUT (integerfield en BD) NO FUNCIONA no sale el cero 0
                    'onkeypress': "return solonumeros(event)"

                }
            ),
            'email': EmailInput(
                attrs = {
                    'class': 'form-control form-control-user',
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'phone1': NumberInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'Ingrese su número de Teléfono',
                    # 'required': 'required'
                }
            ),
            'phone2': NumberInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'Ingrese su número de Teléfono',
                    # 'required': 'required'
                }
            ),
           'date_birthday': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_birthday',
                                        'data-target': '#date_birthday',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # form.save()
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class RepresentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['namesr'].widget.attrs['autofocus'] = True

    class Meta:
        model = Represent
        fields = '__all__'
        widgets = {
            'namesr': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su número de cédula',
                    'onkeypress': "return solonumeros(event)",
                    'maxlength': "10", # limitar numeros con CHARFIELD EN LA BASE, CON NUMBERINPUT (integerfield en BD) NO FUNCIONA
                    

                    # 'required': 'required'
                }
            ),
               'hour': TimeInput(format='%H:%M:%S %p',attrs={
                'class': 'form-control',
            }),
            'email': EmailInput(
                attrs = {
                    'class': 'form-control form-control-user',
                    'placeholder': 'Ingrese Correo Electrónico',
                }
            ),
            'profession': TextInput(
                attrs={
                    'placeholder': 'Solamente siglas ejemplo: Ing, Doc, Lic, ',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'organization': TextInput(
                attrs={
                    'placeholder': 'Institución de Trabajo ',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'job': TextInput(
                attrs={
                    'placeholder': 'Ejem: DIRECTOR, JEFE, GERENTE',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'phone1': NumberInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'Ingrese número de Teléfono',
                    # 'required': 'required'
                }
            ),
            'phone2': NumberInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'Ingrese número de Teléfono',
                    # 'required': 'required'
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                        'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_birthday',
                                        'data-target': '#date_birthday',
                                        'data-toggle': 'datetimepicker',                                        
                                    }
                                    ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # form.save()
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    

class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'proposal': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de Propuesta por favor: 020-2020',
                }
            ),
            'date_emission': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                        'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_emission',
                                        'data-target': '#date_emission',
                                        'data-toggle': 'datetimepicker',
                                    }
                                    ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proyecto',
                }
            ),
            'representative': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            # 'profession': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: Ing, Doc, Lic, Solamente siglas',
            #     }
            # ),
            #  'job': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: DIRECTOR, JEFE, GERENTE',
            #     }
            # ),
            # 'managed': TextInput(
            #     attrs={
            #         'placeholder': 'Antecedentes:... ',
            #     }
            # ),
            # 'ogeneral': TextInput(
            #     attrs={
            #         'placeholder': 'Detalle... ',
            #     }
            # ),
        
            'organization': TextInput(
                attrs={
                    'placeholder': 'Ejem: Empresa Pública UPEC-CREATIVA EP',
                }
            ),
            'type_project': TextInput(
                attrs={
                    'placeholder': 'Propuesta de capacitación, formación,...',
                }
            ),
            'desing': Textarea(
                attrs={
                    'placeholder': 'Esta propuesta se ha diseñado de acuerdo a la normativa, necesidades, metodología ',
                }
            ),
            'quantity_mount': Textarea(
                attrs={
                    'placeholder': 'Detalle del monto del proyecto',
                }
            ),
            'reshumans': Textarea(
                attrs={
                    'placeholder': 'Recursos humanos dentro del proyecto',
            
                }
            ),
            # 'offer': Select(
            #     attrs={
            #         'placeholder': 'Ingrese archivo de propuesta',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_personal': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de personal',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_material': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de material',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    
                }
            ),
            # 'dni': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese su número de cédula',
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            #     }
            # ),
            'new': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'finished': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'process': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'results': Textarea(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
          
            'cli': Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
             'hour': TimeInput(format='%H:%M:%S %p',attrs={
                'class': 'form-control',
            }),
      
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
                })              
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ConstrucctionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Construcction
        fields = '__all__'
        # ['name', 'organization', 'reshumans','resmaterials','results']
        widgets ={'proposal': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de Propuesta por favor: 020-2020',
                    'onkeypress': "return solonumeros(event)"
                    
                }
            ),
            'date_emission': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                        'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_emission',
                                        'data-target': '#date_emission',
                                        'data-toggle': 'datetimepicker',
                                    }
                                    ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proyecto',
                    }
            ),
            'representative': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            'organization': TextInput(
                attrs={
                    'placeholder': 'Ejem: Empresa Pública UPEC-CREATIVA EP',
                }
            ),
            'type_project': TextInput(
                attrs={
                    'placeholder': 'Propuesta de capacitación, formación,...',
                }
            ),
            'desing': Textarea(
                attrs={
                    'placeholder': 'Esta propuesta se ha diseñado de acuerdo a la normativa, necesidades, metodología ',
                }
            ),
            'benefits': Textarea(
                attrs={
                    'placeholder': 'Beneficiarios de Proyecto',
                }
                ),
            'quantity_mount': Textarea(
                attrs={
                    'placeholder': 'Detalle del monto del proyecto',
                    
                }
            ),
            'reshumans': Textarea(
                attrs={
                    'placeholder': 'Ingrese los recursos humanos del proyecto',
                    
                }
            ),
            'resmaterials': Textarea(
                attrs={
                    'placeholder': 'Ingrese los materiales usados',
                    
                }
            ),
            # 'managed': Textarea(
            #     attrs={
            #         'placeholder': 'Antecedentes:... ',
            #     }
            # ),
            # 'ogeneral': Textarea(
            #     attrs={
            #         'placeholder': 'Detalle... ',
            #     }
            # ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    
                }
            ),
            # 'dni': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese su número de cédula',
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'new': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'finished': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'process': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'results': Textarea(
                attrs={
                    'placeholder': 'Describa los Resultados del Proyectos',
                                        
                }
            ),                
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
 
    
class PositionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name_position'].widget.attrs['autofocus'] = True

    class Meta:
        model = Position
        fields = '__all__'
        widgets = {
            'name_position': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'area': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción del área estratégica a la que pertenece este cargo',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class EmployerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Employer
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombres del nuevo empleado',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese apellidos del nuevo empleado',
                    'onkeypress': "return sololetras(event)"
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su número de cédula',
                    'maxlength': "10", # limitar numeros con CHARFIELD EN LA BASE, CON NUMBERINPUT (integerfield en BD) NO FUNCIONA no sale el cero 0
                    'onkeypress': "return solonumeros(event)"

                }
            ),
            'position': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            'City': TextInput(
                attrs={
                    'placeholder': 'Ejem: Tulcán, Quito, Cuenca',
                    'onkeypress': "return sololetras(event)"
                    
                }
            ),
            'Country': TextInput(
                attrs={
                    'placeholder': 'Ejem: Ecuador, Colombia, Perú',
                    'onkeypress': "return sololetras(event)"
                    
                }
            ),
            'nationality': TextInput(
                attrs={
                    'placeholder': 'ecuatoriana, colombiana, egipcia',
                    'onkeypress': "return sololetras(event)"
                    
                }
            ),
             'date_birthday': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                        'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_birthday',
                                        'data-target': '#date_birthday',
                                        'data-toggle': 'datetimepicker',                                        
                                    }
                                    ),
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            #     }
            # ),
            'new': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'finished': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class ServicespForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['personal'].widget.attrs['autofocus'] = True

    class Meta:
        model = Servicesp
        fields = '__all__'
        widgets = {
            'personal': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            'personals': Textarea(
                attrs={
                    'placeholder': 'Observaciones del Proyecto',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Observaciones del Proyecto',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class AcquisitionbForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Acquisitionbs
        # fields = '__all__'
        fields = ['personal','price','observations','application',
                'study','proforms',
                'autorization','budget_request',
                'budget_certification','certification_pac',
                'certification_not_exist','comparative_chart',
                'purchase_order','delivery_certificate',
                'enabling_documents','entry_egress','payment_memorandum','pay_order','invoice']
        widgets = {
            'personal': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Observaciones del Proyecto',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class AcquisitionServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Acquisitionservices
        fields = '__all__'
        # fields = ['personal','price','observations','application',
        #         'study','proforms',
        #         'autorization','budget_request',
        #         'budget_certification','certification_pac',
        #         'certification_not_exist','comparative_chart','report_satisfaction',
        #         'enabling_documents','payment_memorandum','pay_order','invoice']
    
        widgets = {
            'personal': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Observaciones del Proyecto',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class InformsuniForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Informsuni
        fields = '__all__'
          
        widgets = {
            'personal': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            'observations_one': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº1',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_two': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº2',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_three': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº3',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_four': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº4',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_five': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº5',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_six': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº6',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
            'observations_seven': Textarea(
                attrs={
                    'placeholder': 'Observaciones del proyecto - informe nº7',
                    # 'onkeypress': "return sololetras(event)"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class CertificationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Certification
        fields = '__all__'
        # ['name', 'organization', 'reshumans','resmaterials','results']
        widgets ={
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proyecto',
                    }
            ),
            # 'representative': Select(
            #     attrs={
            #         # 'class': 'form-control',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #         }
            # ),
            'certificate': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de certificación',
                }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Observaciones acerca del proyecto',
                }
                ),
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
        
        
class BudgetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Budget
        fields = '__all__'
        # ['name', 'organization', 'reshumans','resmaterials','results']
        widgets ={
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del documento',
                    }
            ),
            # 'representative': Select(
            #     attrs={
            #         # 'class': 'form-control',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #         }
            # ),
            'state': TextInput(
                attrs={
                    'placeholder': 'Ingrese año',
                }
            ),
            'reforms': TextInput(
                attrs={
                    'placeholder': 'Observaciones acerca del proyecto',
                }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Estado de puesto',
                }
                ),
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class TreasuryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Treasury
        fields = '__all__'
        # ['name', 'organization', 'reshumans','resmaterials','results']
        widgets ={
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proyecto',
                    }
            ),
            # 'representative': Select(
            #     attrs={
            #         # 'class': 'form-control',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #         }
            # ),
            'state': TextInput(
                attrs={
                    'placeholder': 'Inscripciones - matrículas - mensualidades',
                }
            ),
            'observations': Textarea(
                attrs={
                    'placeholder': 'Observaciones acerca del proyecto',
                }
                ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# 789 10 13 16 17 18
class PerfilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['type_perfil'].widget.attrs['autofocus'] = True

    class Meta:
        model = Perfil
        fields = '__all__'
        widgets = {
            
            'type_perfil': TextInput(
                attrs={
                    'placeholder': 'Proyecto de educación continua / inversión / alianzas estratégicas...',
                }
            ),
            'agreement': Textarea(
                attrs={
                    'placeholder': '"CONVENIO ESPECÍFICO DE COOPERACIÓN INTERINSTITUCIONAL ENTRE ..."',
                }
            ),
            'representative': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            # 'month': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese un mes por favor: Enero, Agosto, Noviembre, Diciembre',
            #     }
            # ),
            'month': Select(),
            
            'year': NumberInput(
                attrs={
                    'placeholder': 'Ingrese un año por favor: 2021',
                }
            ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del proyecto por favor: COMERCIALIZACIÓN DE LOS SERVICIOS ...',
                }
            ),
            'location': Textarea(
                attrs={
                    'placeholder': 'Ingrese la ubicacion del proyecto por favor',
                }
            ),
            'analysis': Textarea(
                attrs={
                    'placeholder': 'Describa la situación actual del proyecto por favor',
                }
            ),
            'record': Textarea(
                attrs={
                    'placeholder': 'Ingrese los antecedentes del proyecto por favor',
                }
            ),
            'justification': Textarea(
                attrs={
                    'placeholder': 'Ingrese la justificación del proyecto por favor',
                }
            ),
            'relation': Textarea(
                attrs={
                    'placeholder': 'Describa proyectos relacionados por favor',
                }
            ),
            'duration': Textarea(
                attrs={
                    'placeholder': 'Duración del proyecto',
                }
            ),
            'beneficiaries': Textarea(
                attrs={
                    'placeholder': 'Ingrese a los proyectos del proyecto por favor',
                }
            ),
            'impact': Textarea(
                attrs={
                    'placeholder': 'Impacto ambiental del proyecto',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'impact': Textarea(
                attrs={
                    'placeholder': 'Impacto ambiental del proyecto',
                }
            ),
            'management': Textarea(
                attrs={
                    'placeholder': 'Autogestión y sustentabilidad del proyecto',
                }
            ),
            'description': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción del documento',
                    
                }
            ),
             'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
        
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
        
class ProductiveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Productive
        fields = '__all__'
        widgets = {
            'proposal': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de Propuesta por favor: 020-2020',
                }
            ),
            'date_emission': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                        'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_emission',
                                        'data-target': '#date_emission',
                                        'data-toggle': 'datetimepicker',
                                    }
                                    ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proyecto',
                }
            ),
            'representative': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
            # 'profession': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: Ing, Doc, Lic, Solamente siglas',
            #     }
            # ),
            #  'job': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: DIRECTOR, JEFE, GERENTE',
            #     }
            # ),
            # 'managed': TextInput(
            #     attrs={
            #         'placeholder': 'Antecedentes:... ',
            #     }
            # ),
            # 'ogeneral': TextInput(
            #     attrs={
            #         'placeholder': 'Detalle... ',
            #     }
            # ),
        
            'organization': TextInput(
                attrs={
                    'placeholder': 'Ejem: Empresa Pública UPEC-CREATIVA EP',
                }
            ),
            'type_project': TextInput(
                attrs={
                    'placeholder': 'Propuesta de capacitación, formación,...',
                }
            ),
            'desing': Textarea(
                attrs={
                    'placeholder': 'Esta propuesta se ha diseñado de acuerdo a la normativa, necesidades, metodología ',
                }
            ),
            'quantity_mount': Textarea(
                attrs={
                    'placeholder': 'Detalle del monto del proyecto',
                }
            ),
            'reshumans': Textarea(
                attrs={
                    'placeholder': 'Recursos humanos dentro del proyecto',
            
                }
            ),
            # 'offer': Select(
            #     attrs={
            #         'placeholder': 'Ingrese archivo de propuesta',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_personal': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de personal',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_material': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de material',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    
                }
            ),
            # 'dni': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese su número de cédula',
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            #     }
            # ),
            'new': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'finished': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'process': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'results': Textarea(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
        
    # 789 10 13 16 17 18
class PerfilprodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['type_perfil'].widget.attrs['autofocus'] = True

    class Meta:
        model = Perfilprod
        fields = '__all__'
        widgets = {
            
            'type_perfil': TextInput(
                attrs={
                    'placeholder': 'Proyecto de educación continua / inversión / alianzas estratégicas...',
                }
            ),
            'agreement': Textarea(
                attrs={
                    'placeholder': '"CONVENIO ESPECÍFICO DE COOPERACIÓN INTERINSTITUCIONAL ENTRE ..."',
                }
            ),
            'representative': Select(
                attrs={
                    # 'class': 'form-control',
                    'class': 'select2',
                    'style': 'width: 100%'
                    }
            ),
            # 'month': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese un mes por favor: Enero, Agosto, Noviembre, Diciembre',
            #     }
            # ),
            'month': Select(),
            
            'year': NumberInput(
                attrs={
                    'placeholder': 'Ingrese un año por favor: 2021',
                }
            ),
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del proyecto por favor: COMERCIALIZACIÓN DE LOS SERVICIOS ...',
                }
            ),
            'location': Textarea(
                attrs={
                    'placeholder': 'Ingrese la ubicacion del proyecto por favor',
                }
            ),
            'analysis': Textarea(
                attrs={
                    'placeholder': 'Describa la situación actual del proyecto por favor',
                }
            ),
            'record': Textarea(
                attrs={
                    'placeholder': 'Ingrese los antecedentes del proyecto por favor',
                }
            ),
            'justification': Textarea(
                attrs={
                    'placeholder': 'Ingrese la justificación del proyecto por favor',
                }
            ),
            'relation': Textarea(
                attrs={
                    'placeholder': 'Describa proyectos relacionados por favor',
                }
            ),
            'duration': Textarea(
                attrs={
                    'placeholder': 'Duración del proyecto',
                }
            ),
            'beneficiaries': Textarea(
                attrs={
                    'placeholder': 'Ingrese a los proyectos del proyecto por favor',
                }
            ),
            'impact': Textarea(
                attrs={
                    'placeholder': 'Impacto ambiental del proyecto',
                    'rows': 3,
                    'cols': 3
                }
            ),
            'impact': Textarea(
                attrs={
                    'placeholder': 'Impacto ambiental del proyecto',
                }
            ),
            'management': Textarea(
                attrs={
                    'placeholder': 'Autogestión y sustentabilidad del proyecto',
                }
            ),
            'description': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción del documento',
                    
                }
            ),
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
        
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class PublicsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Publics
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proceso efectuado',
                }
            ),
            # 'representative': Select(
            #     attrs={
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'profession': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: Ing, Doc, Lic, Solamente siglas',
            #     }
            # ),
            #  'job': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: DIRECTOR, JEFE, GERENTE',
            #     }
            # ),
            # 'managed': TextInput(
            #     attrs={
            #         'placeholder': 'Antecedentes:... ',
            #     }
            # ),
            # 'ogeneral': TextInput(
            #     attrs={
            #         'placeholder': 'Detalle... ',
            #     }
            # ),
        
            # 'organization': TextInput(
            #     attrs={
            #         'placeholder': 'Ejem: Empresa Pública UPEC-CREATIVA EP',
            #     }
            # ),
            # 'type_project': TextInput(
            #     attrs={
            #         'placeholder': 'Propuesta de capacitación, formación,...',
            #     }
            # ),
            # 'desing': Textarea(
            #     attrs={
            #         'placeholder': 'Esta propuesta se ha diseñado de acuerdo a la normativa, necesidades, metodología ',
            #     }
            # ),
            # 'quantity_mount': Textarea(
            #     attrs={
            #         'placeholder': 'Detalle del monto del proyecto',
            #     }
            # ),
            # 'reshumans': Textarea(
            #     attrs={
            #         'placeholder': 'Recursos humanos dentro del proyecto',
            
            #     }
            # ),
            # 'offer': Select(
            #     attrs={
            #         'placeholder': 'Ingrese archivo de propuesta',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_personal': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de personal',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            # 'request_material': Select(
            #     attrs={
            #         'placeholder': 'Ingrese solicitud de material',
            #         'class': 'select2',
            #         'style': 'width: 100%'
            #     }
            # ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    
                }
            ),
            # 'dni': TextInput(
            #     attrs={
            #         'placeholder': 'Ingrese su número de cédula',
            'date_registration': DateInput(format='%Y-%m-%d',
                                attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_registration',
                                        'data-target': '#date_registration',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_start': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_start',
                                        'data-target': '#date_start',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            'date_finish': DateInput(format='%Y-%m-%d',
                                    attrs={
                                        'value': datetime.now().strftime('%Y-%m-%d'),
                                    'autocomplete': 'off',
                                        'class': 'form-control datetimepicker-input',
                                        'id': 'date_finish',
                                        'data-target': '#date_finish',
                                        'data-toggle': 'datetimepicker', 
                                    }
                                    ),
            #     }
            # ),
            'new': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'finished': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            'process': CheckboxInput(
                # attrs={
                #     'placeholder': 'Ingrese su dirección',
                # }
            ),
            # 'results': Textarea(
            #     # attrs={
            #     #     'placeholder': 'Ingrese su dirección',
            #     # }
            # ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
# class ProductiveReportForm(Form):
 
#     date_range = CharField(widget=TextInput(attrs={
#         'class': 'form-control',
#         'autocomplete': 'off'
#     }))
