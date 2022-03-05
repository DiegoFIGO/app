from datetime import datetime, timezone
from django.utils.html import format_html

from django.db import models
from django.db.models.fields import  DateField
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import *
from core.models import BaseModel

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, integer_validator, validate_email, FileExtensionValidator

# Validations

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("El tamaño máximo de archivo permitido es %sMB" % str(megabyte_limit))
    
def validate_file(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("El tamaño máximo de archivo permitido es %sMB" % str(megabyte_limit))
    
def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value 

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def validate_integer(value):
    return integer_validator(value)

# Category

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre (*) ', unique=True)
    desc = models.CharField(max_length=700, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

# Product

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre (*) ', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría (*) ')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, validators=[validate_image], help_text='El tamaño máximo de archivo permitido es 2Mb', verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock (*)')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

# Client

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres (*) ')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos (*) ')
    dni = models.IntegerField(unique=True, verbose_name='Cédula de Identidad (*) ', help_text='10 characters max.') # max_length=10, lw limito en forms
    email = models.EmailField(max_length=254,unique = True, verbose_name='Correo electrónico (*) ')
    phone1 = models.CharField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 1',)
    phone2 = models.CharField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 2')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo (*) ')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} '.format(self.names, self.surnames)
                # return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def validate_integer(value):
        return integer_validator(value)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item
        

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

# Sale

class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    # date_joined = models.DateField(default=datetime.now)
    date_joined = models.DateTimeField()
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    status = models.CharField(max_length=30, choices=sale_choices, default=sale_choices[0][0])

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    # def delete(self, using=None, keep_parents=False):
    #     for det in self.detsale_set.all():
    #         det.prod.stock += det.cant
    #         det.prod.save()
    #     super(Sale, self).delete()
        
    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.detsale_set.filter():
                i.prod.stock += i.cant
                i.prod.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()
    

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

# Detail Sale

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    
    def validate_integer(value):
        return integer_validator(value)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

# Represent Project

class Represent(models.Model):
    namesr = models.CharField(max_length=150, verbose_name='Nombres completos (*) ')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos completos (*) ')
    dni = models.IntegerField(max_length=10, unique=True, verbose_name='Cédula de Identidad (*) ')
    email = models.EmailField(max_length=254,unique = True, verbose_name='Correo electrónico (*) ')
    organization = models.CharField(max_length=5000, verbose_name='Institución (*) ')
    job = models.CharField(max_length = 150, verbose_name='Cargo dentro de la Institución (*)')
    profession= models.CharField(max_length = 150, verbose_name='Título Académico (*) ')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de Registro (*) ')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    phone1 = models.IntegerField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 1',)
    phone2 = models.IntegerField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 2')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='Masculino', verbose_name='Sexo')

    def validate_integer(value):
            return integer_validator(value) 

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} '.format(self.namesr, self.surnames)
                # return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['hour'] = self.hour.strftime('%H:%M:%S %p')

        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Representante'
        verbose_name_plural = 'Representantes'
        ordering = ['id']

# Project

class Project(models.Model):
    proposal = models.IntegerField(max_length=11, null=True, blank=True, verbose_name='Propuesta No.')
    name = models.CharField(max_length = 5000, verbose_name='Proyecto (*) ')
    representative = models.ForeignKey(Represent, on_delete=models.CASCADE, verbose_name='Administrador de Proyecto (*) ')
    organization = models.CharField(max_length=5000, verbose_name='Entidad Ejecutora (*) ')
    type_project = models.CharField(max_length=5000, verbose_name='Tipo de Proyecto (*) ')
    desing = models.CharField(max_length=5000, verbose_name='Diseño de Proyecto (*) ')
    quantity = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Monto del Proyecto')
    quantity_mount = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='Detalle del Monto')
    reshumans = models.CharField(max_length=5000,null=True, blank=True, verbose_name='Recursos Humanos')
    managed = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Antecedentes del Proyecto')
    ogeneral = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Detalle del Proyecto')
    offer = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo de la Propuesta')
    request_personal = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de Personal')
    request_material = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de Material') 
    description = models.CharField(max_length = 10485760, null=True, blank=True, verbose_name='Descripción de Proyecto')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro de Proyecto (*) ')
    date_start = DateField( default = datetime.now, verbose_name='Fecha de Inicio de Proyecto')
    date_finish = DateField(default = datetime.now, verbose_name='Fecha de Finalización de Proyecto')
    date_emission = DateField( default = datetime.now, verbose_name='Fecha de Emisión de Reporte')
    new = models.BooleanField(verbose_name='Proyecto Nuevo')
    finished = models.BooleanField(verbose_name='Proyecto Cumplido')
    process = models.BooleanField(verbose_name='Proyecto en Proceso')
    results = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='Resultados de Proyecto')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer', 'request_personal','request_material',])
        item['representative'] = self.representative.toJSON()
        item['offer'] = self.get_offer()
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        
        return item

    def get_offer(self):
        if self.offer:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['id']
        
# Perfil

class Perfil(models.Model):
    type_perfil = models.CharField(max_length = 500, verbose_name='Tipo de Proyecto (*) ')    
    agreement = models.CharField(max_length = 7000, null=True, blank=True, verbose_name='Convenio')
    representative = models.ForeignKey(Represent, on_delete=models.CASCADE, verbose_name='Responsable del Proyecto (*) ')
    month = models.CharField(max_length=20, choices=month_choices, null=True, blank=True, default='Enero', verbose_name='Mes')
    year = models.IntegerField(max_length=4, null=True, blank=True, verbose_name='Año')
    name = models.CharField(max_length=7000, verbose_name='1. Nombre del Proyecto (*)  ')
    location = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='2. Localización geográfica')
    analysis = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='3. Análisis de la situación actual (diagnóstico)')
    record = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='4. Antecedentes del Proyecto')
    justification = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='5. Justificación del Proyecto')
    relation = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='6. Proyectos relacionados y / o complementarios')
    objectivs = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='7. Objetivos')
    goals = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='8. Metas')
    activities = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='9. Actividades')
    schedule = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='10. Cronograma de actividades')
    duration = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='11.  Duración del proyecto y vida útil')
    beneficiaries = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='12. Beneficiarios')
    indicators = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='13. Indicadores de resultados alcanzados: cualitativos y cuantitativos')
    impact = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='14. Impacto ambiental')
    management = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='15. Autogestión y sostenibilidad')
    framework = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='16. Marco institucional')
    financing = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='17. Financiamiento y análisis financiero del proyecto')
    annexes = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='18. Anexos')
    documment = models.FileField(upload_to = 'perfilprod/%Y/%m/%d', null=True, blank=True, verbose_name='Documentos') 
    description = models.CharField(max_length = 255000, null=True, blank=True, verbose_name='Descripción del documento')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro (*) ')
    date_start = DateField( default = datetime.now, null=True, blank=True, verbose_name='Fecha de Inicio de Proyecto')
    date_finish = DateField(default = datetime.now, null=True, blank=True, verbose_name='Fecha de Finalización de Proyecto')
    new = models.BooleanField(verbose_name='Proyecto Nuevo')
    finished = models.BooleanField(verbose_name='Proyecto Cumplido')
    process = models.BooleanField(verbose_name='Proyecto en Proceso')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['objectivs','goals','activities','schedule','indicators','framework','financing','annexes','documment'])
        item['representative'] = self.representative.toJSON()
        item['month'] = {'id': self.month, 'name': self.get_month_display()}
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        # item['offer'] = self.get_offer()
        return item

    # def get_offer(self):
    #     if self.offer:
    #         return '{}{}'.format(STATIC_URL, 'perfilpdf/')
    #     return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['id']

# Services Profesionals

class Servicesp(models.Model):
    personal = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Seleccione nombre del proyecto (*)')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto proyecto')
    cant = models.IntegerField(default=0, verbose_name='Personal contratado')
    personals = models.CharField(max_length=10000, null=True, blank=True, verbose_name='Detalles del personal')
    observations = models.CharField(max_length=10000, verbose_name='Observaciones de proyecto (*) ')
    application = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de contratación')
    autorization = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Autorización de contratación')
    budget_request = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de contratación presupuestaria')
    budget_certification = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Certificación presupuestaria')
    contract = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Contrato')
    report_satisfaction = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe satisfacción / Productos generados')
    annexes = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Anexos, fotografías, etc...')
    enabling_documents = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documentos habilitantes: RUC - CERT BANCARIA- COPIA CÉDULA')
    payment_memorandum = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Memorando de pago')
    pay_order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Orden de pago')
    invoice = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Factura electrónica mayor a 1000 USD')
    
    
    def __str__(self):
        return self.personal

    def toJSON(self):
        item = model_to_dict(self, exclude=['application','autorization','budget_request','budget_certification','contract','report_satisfaction','annexes','enabling_documents','payment_memorandum','pay_order','invoice'])
        # item['prod'] = self.prod.toJSON()
        item['personal'] = self.personal.toJSON()
        
        item['price'] = format(self.price, '.2f')
        # item['subtotal'] = format(self.subtotal, '.2f')
        return item
    
    def validate_integer(value):
        return integer_validator(value)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']

# Acquisitions belongings
    
class Acquisitionbs(models.Model):
    personal = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Seleccione nombre del proyecto (*) ')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto proyecto')
    observations = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de proyecto (*) ')
    application = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud requirente - proyecto')
    study = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Estudio de necesidad')
    proforms = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Estudio de mercado / 3 proformas (archivo comprimido)')
    autorization = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Autorización de solicitud de compra')
    budget_request = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de certificación presupuestaria')
    budget_certification = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Certificación presupuestaria')
    certification_pac = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Certificación PAC')
    certification_not_exist = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Certificación NO EXISTE en catálogo electrónico')
    comparative_chart = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Cuadro comparativo - estudio mercado')
    purchase_order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Orden de compra')
    delivery_certificate = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Acta entrega - recepción proveedor')
    report_satisfaction = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de satisfacción / Requirente proyecto')
    enabling_documents = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documentos Habilitantes: RUC - CERT BANCARIA- COPIA CÉDULA')
    
    entry_egress = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Ingreso - Egreso de bodega')
        
    payment_memorandum = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Memorando de Pago')
    pay_order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Orden de Pago')
    invoice = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Factura Electrónica mayor a 1000 USD')
    
    
    def __str__(self):
        return self.personal.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['application','study','proforms','autorization','budget_request','budget_certification','certification_pac','certification_not_exist','comparative_chart','report_satisfaction','purchase_order','delivery_certificate','entry_egress','enabling_documents','payment_memorandum','pay_order','invoice'])
        
        item['personal'] = self.personal.toJSON()
       
        item['price'] = format(self.price, '.2f')
       
        return item
    
    def validate_integer(value):
        return integer_validator(value)
    
    class Meta:
        verbose_name = 'Adquisición'
        verbose_name_plural = 'Adquisiciones'
        ordering = ['id']
        
# Acquisitions services
    
class Acquisitionservices(models.Model):
    personal = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Seleccione nombre del proyecto (*) ')
    # price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto proyecto')
    observations = models.CharField(max_length=10000,  null=True, blank=True, verbose_name='Observaciones de proyecto')
    application = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud requirente - proyecto')
    study = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Estudio de necesidad')
    proforms = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Estudio de mercado / 3 proformas (archivo comprimido)')
    autorization = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Autorización de solicitud de compra')
    budget_request = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de certificación presupuestaria')
    budget_certification = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Certificación presupuestaria')
    certification_pac = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Certificación PAC')
    certification_not_exist = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Certificación NO EXISTE en catálogo electrónico')
    comparative_chart = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name= 'Cuadro comparativo - estudio mercado')
    # purchase_order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Orden de compra')
    # delivery_certificate = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Acta entrega - recepción proveedor')
    report_satisfaction = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de satisfacción / Requirente proyecto')
    enabling_documents = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documentos Habilitantes: RUC - CERT BANCARIA- COPIA CÉDULA')
    
    # entry_egress = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Ingreso - Egreso de bodega')
        
    payment_memorandum = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Memorando de Pago')
    pay_order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Orden de Pago')
    invoice = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Factura Electrónica mayor a 1000 USD')
        
    def __str__(self):
        return self.personal.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['application','study','proforms','autorization','budget_request','budget_certification','certification_pac','certification_not_exist','comparative_chart','report_satisfaction','enabling_documents','payment_memorandum','pay_order','invoice'])
        item['personal'] = self.personal.toJSON()
        return item
    
    def validate_integer(value):
        return integer_validator(value)
    
    class Meta:
        verbose_name = 'Adquisición Servicio'
        verbose_name_plural = 'Adquisición Servicios'
        ordering = ['id']
        
# Informs

class Informsuni(models.Model):
    personal = models.ForeignKey(Project, verbose_name = 'Seleccione nombre del proyecto para Informe de seguimiento (*) ', on_delete=models.CASCADE)
    observations_one = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº1')
    inform_one = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº1')
    observations_two = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº2')
    inform_two = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº2')
    observations_three = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº3')
    inform_three = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº3')
    observations_four = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº4')
    inform_four = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº4')
    observations_five = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº5')
    inform_five = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº5')
    observations_six = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Observaciones de seguimiento nº6')
    inform_six = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº6')
    observations_seven = models.CharField(max_length=1000, null=True, blank=True,verbose_name='Observaciones de seguimiento nº7')
    inform_seven = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Informe de seguimiento nº7')
    
    def __str__(self):
        return self.personal

    def toJSON(self):
        item = model_to_dict(self, exclude=['inform_one','inform_two','inform_three','inform_four','inform_five','inform_six','inform_seven'])
        item['personal'] = self.personal.toJSON()
        item['inform_one'] = self.get_inform_one()
        return item
    
    def get_inform_one(self):
        if self.inform_one:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()
    
    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        ordering = ['id']
    
# Human Talent Position

class Position(models.Model):
    name_position = models.CharField(max_length=150, verbose_name='Nombre del Cargo (*) ', unique=True)
    desc = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Descripción del Cargo')
    area = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Area estretégica del Cargo')

    def __str__(self):
        return self.name_position
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['id']

# Human Talent Employer

class Employer(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres completos (*)  ')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos completos (*) ')
    dni = models.IntegerField(max_length=10, unique=True, verbose_name='Cédula de Identidad (*) ')
    email = models.EmailField(max_length=254,unique = True, verbose_name='Correo electrónico (*) ')
    image = models.ImageField(upload_to='employer/%Y/%m/%d', null=True, blank=True, validators=[validate_image], help_text='El tamaño máximo de archivo permitido es 2Mb', verbose_name='Imagen')
    phone1 = models.IntegerField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 1',)
    phone2 = models.IntegerField(max_length=15, blank = True, null = True, verbose_name='Número telefónico 2')
    phone3 = models.IntegerField(max_length=15, blank = True, null = True, verbose_name='Número alterno emergencia')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    City = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ciudad')
    Country = models.CharField(max_length=150, null=True, blank=True, verbose_name='País')
    nationality = models.CharField(max_length=150, verbose_name='Nacionalidad (*) ')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Cargo a ocupar (*) ')
    curriculum = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Hoja de Vida')
    health_card = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Ficha Médica')
    memorandum_contract = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Memorando de Contratación o Autorización')
    resignation = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documento de renuncia o Solicitud de salida') 
    enabling_document = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documento Habilitante Liquidación') 
    holidays = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Documento de Vacaciones') 
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro')
    date_start = DateField( default = datetime.now, verbose_name='Fecha de inicio')
    date_finish = DateField(default = datetime.now, verbose_name='Fecha de finalización')
    new = models.BooleanField(verbose_name='Activo')
    finished = models.BooleanField(verbose_name='Inactivo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} '.format(self.names, self.surnames)
                # return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def validate_integer(value):
        return integer_validator(value)
    
    def toJSON(self):
        item = model_to_dict(self, exclude = ['resignation', 'curriculum','health_card','memorandum_contract','enabling_document','holidays',])
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = '{} / {}'.format(self.get_full_name, self.position.name_position)
        item['position'] = self.position.toJSON()
        item['full_name'] = self.get_full_name()
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        
        return item
        
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)           
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['id']

# Budget certification

class Certification(models.Model):
    name = models.CharField(max_length = 250, verbose_name='Nombre de Proyecto (*) ')
    certificate = models.CharField(max_length = 150, verbose_name='Número de Certificación (*) ')
    quantity = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Monto del Proyecto')
    observations = models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto (*) ')
    document = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo de Proyecto')


    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['document'])
        item['document'] = self.get_document()
        item['quantity'] = format(self.quantity, '.2f')
        return item

    def get_document(self):
        if self.document:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    class Meta:
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'
        ordering = ['id']

# Budget & PAC

class Budget(models.Model):
    name = models.CharField(max_length = 250, verbose_name='Nombre de Documento (*) ')
    offer = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Presupuesto y PAC')
    state = models.CharField(max_length = 150, verbose_name='Año (*) ')
    refomrs = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Reformas')
    observations = models.CharField(max_length=1000, verbose_name='Presupuesto (*) ')
    
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer','refomrs'])
        item['offer'] = self.get_offer()
        return item

    def get_offer(self):
        if self.offer:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/emptyc.png')
    
    class Meta:
        verbose_name = 'Presupuesto_y_PAC'
        verbose_name_plural = 'Presupuestos_y_PACs'
        ordering = ['id']
        
# Treasury

class Treasury(models.Model):
    name = models.CharField(max_length = 250, verbose_name='Nombre de Proyecto (*) ')
    offer = models.FileField(upload_to = 'treasurypdf/%Y/%m/%d', null=True, blank=True, verbose_name='Archivo de Proyecto')
    state = models.CharField(max_length = 150, verbose_name='Estado (*) ')
    observations = models.CharField(max_length=1000, verbose_name='Observaciones de Proyecto (*) ')
    
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer',])
        item['offer'] = self.get_offer()
        return item

    def get_offer(self):
        if self.offer:
            return '{}{}'.format(MEDIA_URL, self.offer)
        return '{}{}'.format(STATIC_URL, 'img/emptyc.png')
    
    class Meta:
        verbose_name = 'Tesoreria'
        verbose_name_plural = 'Tesorerias'
        ordering = ['id']

# Construcction

class Construcction(models.Model):
    proposal = models.IntegerField(max_length=11, null=True, blank=True, verbose_name='Propuesta No.')
    name = models.CharField(max_length = 1500, verbose_name='Proyecto (*) ')
    representative = models.ForeignKey(Represent, on_delete=models.CASCADE, verbose_name='Administrador de Proyecto (*) ')
    organization = models.CharField(max_length=1500, verbose_name='Entidad Ejecutora (*) ')
    type_project = models.CharField(max_length=5000, verbose_name='Tipo de Proyecto (*) ')
    desing = models.CharField(max_length=5000, verbose_name='Diseño de Proyecto (*) ')
    benefits = models.CharField(max_length = 300000, null=True, blank=True, verbose_name='Cliente Beneficiario')
    quantity = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Monto del Proyecto')
    quantity_mount = models.CharField(max_length=150, null=True, blank=True, verbose_name='Detalle del Monto')
    reshumans = models.CharField(max_length=150000, null=True, blank=True, verbose_name='Recursos Humanos')
    resmaterials = models.CharField(max_length=3000000,null=True, blank=True,  verbose_name='Recursos Materiales')
    managed = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Antecedentes del Proyecto')
    ogeneral = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Detalle del Proyecto')
    offer = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo Propuesta')
    request_personal = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de personal')
    request_material = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de material') 
    description = models.CharField(max_length = 255000, null=True, blank=True, verbose_name='Descripción')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro de Proyecto (*)')
    date_start = DateField( default = datetime.now, verbose_name='Fecha de Inicio de Proyecto')
    date_finish = DateField(default = datetime.now, verbose_name='Fecha de Finalización de Proyecto')
    date_emission = DateField( default = datetime.now, verbose_name='Fecha de Emisión de Reporte')
    new = models.BooleanField(verbose_name='Proyecto Nuevo')
    finished = models.BooleanField(verbose_name='Proyecto Cumplido')
    process = models.BooleanField(verbose_name='Proyecto en Proceso')
    results = models.CharField(max_length=50000, null=True, blank=True, verbose_name='Resultados de Proyecto')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer', 'request_personal','request_material','managed','ogeneral'])
        item['representative'] = self.representative.toJSON()
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        item['offer'] = self.get_offer()
        return item

    def get_offer(self):
        if self.offer:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Construcción'
        verbose_name_plural = 'Construcciones'
        ordering = ['id']
        
# Productive

class Productive(models.Model):
    proposal = models.IntegerField(max_length=11, null=True, blank=True, verbose_name='Propuesta No.')
    name = models.CharField(max_length = 5000, verbose_name='Proyecto (*) ')
    representative = models.ForeignKey(Represent, on_delete=models.CASCADE, verbose_name='Administrador de Proyecto (*) ')
    organization = models.CharField(max_length=5000, verbose_name='Entidad Ejecutora (*) ')
    type_project = models.CharField(max_length=5000, verbose_name='Tipo de Proyecto (*) ')
    desing = models.CharField(max_length=5000, verbose_name='Diseño de Proyecto (*) ')
    quantity = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Monto del Proyecto')
    quantity_mount = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='Detalle del Monto')
    reshumans = models.CharField(max_length=5000,null=True, blank=True, verbose_name='Recursos Humanos')
    managed = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Antecedentes del Proyecto')
    ogeneral = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='Detalle del Proyecto')
    offer = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Archivo Propuesta')
    request_personal = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de personal')
    request_material = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, validators=[FileExtensionValidator(['pdf'])], verbose_name='Solicitud de material') 
    description = models.CharField(max_length = 10485760, null=True, blank=True, verbose_name='Descripción')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro de Proyecto (*)')
    date_start = DateField( default = datetime.now, verbose_name='Fecha de Inicio de Proyecto')
    date_finish = DateField(default = datetime.now, verbose_name='Fecha de Finalización de Proyecto')
    date_emission = DateField( default = datetime.now, verbose_name='Fecha de Emisión de Reporte')
    new = models.BooleanField(verbose_name='Proyecto Nuevo')
    finished = models.BooleanField(verbose_name='Proyecto Cumplido')
    process = models.BooleanField(verbose_name='Proyecto en Proceso')
    results = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='Resultados de Proyecto')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer', 'request_personal','request_material',])
        item['representative'] = self.representative.toJSON()
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        item['offer'] = self.get_offer()
        return item

    def get_offer(self):
        if self.offer:
            return '{}{}'.format(STATIC_URL, 'perfilpdf/')
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Productivo'
        verbose_name_plural = 'Productivos'
        ordering = ['id']
        
# Perfilprod

class Perfilprod(models.Model):
    type_perfil = models.CharField(max_length = 500, verbose_name='Tipo de Proyecto (*) ')    
    agreement = models.CharField(max_length = 7000, null=True, blank=True, verbose_name='Convenio')
    representative = models.ForeignKey(Represent, on_delete=models.CASCADE, verbose_name='Responsable del Proyecto (*) ')
    month = models.CharField(max_length=20, choices=month_choices, null=True, blank=True, default='Enero', verbose_name='Mes')
    year = models.IntegerField(max_length=4, null=True, blank=True, verbose_name='Año')
    name = models.CharField(max_length=7000, verbose_name='1. Nombre del Proyecto (*)  ')
    location = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='2. Localización geográfica')
    analysis = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='3. Análisis de la situación actual (diagnóstico)')
    record = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='4. Antecedentes del Proyecto')
    justification = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='5. Justificación del Proyecto')
    relation = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='6. Proyectos relacionados y / o complementarios')
    objectivs = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='7. Objetivos')
    goals = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='8. Metas')
    activities = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='9. Actividades')
    schedule = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='10. Cronograma de actividades')
    duration = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='11.  Duración del proyecto y vida útil')
    beneficiaries = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='12. Beneficiarios')
    indicators = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='13. Indicadores de resultados alcanzados: cualitativos y cuantitativos')
    impact = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='14. Impacto ambiental')
    management = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='15. Autogestión y sostenibilidad')
    framework = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='16. Marco institucional')
    financing = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='17. Financiamiento y análisis financiero del proyecto')
    annexes = RichTextUploadingField(max_length=10485760, null=True, blank=True, verbose_name='18. Anexos')
    documment = models.FileField(upload_to = 'perfilprod/%Y/%m/%d', null=True, blank=True, verbose_name='Documentos') 
    description = models.CharField(max_length = 255000, null=True, blank=True, verbose_name='Descripción de Documento')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro de Proyecto (*) ')
    date_start = DateField( default = datetime.now, null=True, blank=True, verbose_name='Fecha de Inicio de Proyecto')
    date_finish = DateField(default = datetime.now, null=True, blank=True, verbose_name='Fecha de Finalización de Proyecto')
    new = models.BooleanField(verbose_name='Proyecto Nuevo')
    finished = models.BooleanField(verbose_name='Proyecto Cumplido')
    process = models.BooleanField(verbose_name='Proyecto en Proceso')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['objectivs','goals','activities','schedule','indicators','framework','financing','annexes','documment'])
        item['representative'] = self.representative.toJSON()
        item['month'] = {'id': self.month, 'name': self.get_month_display()}
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        # item['offer'] = self.get_offer()
        return item

    # def get_offer(self):
    #     if self.offer:
    #         return '{}{}'.format(STATIC_URL, 'perfilpdf/')
    #     return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Perfilprod'
        verbose_name_plural = 'Perfilesprod'
        ordering = ['id']

# Publics

class Publics(models.Model):
    name = models.CharField(max_length = 5000, verbose_name='Nombre de la Compra Pública (*) ')
    offer = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='PAC Anual')
    study = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Estudio de necesidad')
    certificate = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Certificación PAC')
    comparative = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Cuadro Comparativo') 
    proforms = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Proformas') 
    catalogue = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Catálogo Electrónico') 
    order = models.FileField(upload_to = 'perfilpdf/%Y/%m/%d', null=True, blank=True, verbose_name='Orden de Compra') 
    description = models.CharField(max_length = 10485760, null=True, blank=True, verbose_name='Observación')
    hour = models.TimeField(default=datetime.now, verbose_name='Hora de Registro (*) ')
    date_registration = models.DateField(default = datetime.now, verbose_name = 'Fecha de Registro')
    date_start = DateField( default = datetime.now, verbose_name='Fecha de Compra')
    date_finish = DateField(default = datetime.now, verbose_name='fecha de Cierre')
    new = models.BooleanField(verbose_name='Nuevo')
    finished = models.BooleanField(verbose_name='Cumplido')
    process = models.BooleanField(verbose_name='Proceso')
    # results = models.CharField(max_length=10485760, null=True, blank=True, verbose_name='Resultados')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude = ['offer', 'study','certificate','comparative','proforms','catalogue','order'])
        # item['representative'] = self.representative.toJSON()
        # item['offer'] = self.get_offer()
        item['hour'] = self.hour.strftime('%H:%M:%S %p')
        return item

    # def get_offer(self):
    #     if self.offer:
    #         return '{}{}'.format(STATIC_URL, 'perfilpdf/')
    #     return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def publish(self):
            self.published_date = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Compra Pública'
        verbose_name_plural = 'Compras Públicas'
        ordering = ['id']
        


# class Provincia (models.Model): 

#     id_provincia=models.AutoField(primary_key=True) 

#     nombre_provincia=models.CharField(max_length=11) 


# class Ciudad (models.Model): 

#     id_ciudad=models.AutoField(primary_key=True) 

#     nombre_ciudad=models.CharField(max_length=11) 

#     id_provincia=models.ForeignKey(Provincia,on_delete=models.CASCADE) 



# class Direccion (models.Model): 

#     id_direc=models.AutoField(primary_key=True) 

#     calle1_direc=models.CharField(max_length=50) 

#     calle2_direc=models.CharField(max_length=50) 

#     id_ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE) 

#     def Direccion (self): 

#         txt = '{0}{1}{2}' 

#         return txt.format(self.calle1_direc," y ",self.calle2_direc) 

 

#     def __str__(self) -> str: 

#         txt = '{0}{1}{2}' 

#         return txt.format(self.calle1_direc," y ",self.calle2_direc) 

 

# class Representante (models.Model):

#     cedula_rep=models.CharField(max_length=10, primary_key=True) 

#     nombres_rep=models.CharField(max_length=25) 

#     apellidos_rep=models.CharField(max_length=25) 

#     direccion_rep=models.ForeignKey(Direccion, on_delete=CASCADE) 

#     email_est=models.EmailField() 

#     telefono_est=models.CharField(max_length=10) 

#     parentezco_rep=models.CharField(max_length=10) 

#     def Representante (self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.nombres_rep, self.apellidos_rep) 

#     def __str__(self) -> str: 

#         txt = '{0} {1} ' 

#         return  txt.format(self.nombres_rep,self.apellidos_rep) 
 

# class Ficha_salud (models.Model): 

#     id_fichsal=models.AutoField(primary_key=True) 

#     NomEnfer_fichsa=models.CharField(max_length=11, verbose_name='Nombre') 

#     descripcion_fichsal=models.TextField(verbose_name='Descripción') 

#     accionesTomar_fichsal=models.TextField(verbose_name='Acciones a tomar') 

#     telefonoEmer_fichsal=models.CharField(max_length=10, verbose_name='Telefono de emergencia') 

#     def Salud (self): 

#         txt = '{0}' 

#         return txt.format(self.NomEnfer_fichsa) 

#     def __str__(self) -> str: 

#         txt = '{0}' 

#         return txt.format(self.NomEnfer_fichsa) 

 

# class Horarios (models.Model): 

#     id_horario=models.AutoField(primary_key=True) 

#     inicio_horario=models.TimeField() 

#     final_horario=models.TimeField() 

#     def Horario (self): 

#         txt = '{0}{1}{2}' 

#         return txt.format(self.inicio_horario," a ", self.final_horario ) 

#     def __str__(self) -> str: 

#         txt = '{0}{1}{2}' 

#         return txt.format(self.inicio_horario," a ", self.final_horario ) 

#          

# class Cursos (models.Model): 

#     imagen_curso=models.ImageField(null=True,upload_to='images/curso',verbose_name="Imagen Curso") 

#     id_curso=models.AutoField(primary_key=True) 

#     nombre_curso=models.CharField(max_length=11) 

#     id_horario=models.ForeignKey(Horarios,on_delete=models.CASCADE ,verbose_name="Horario") 

#     def Cursos (self): 

#         txt = '{0}' 

#         return txt.format(self.nombre_curso) 

#     def __str__(self) -> str: 

#         txt = '{0}' 

#         return txt.format(self.nombre_curso ) 

#     def Horario (self): 

#         txt = '{0} {1} {2} ' 

#         return txt.format(self.horarios.inicio_horario," a ", self.horarios.final_horario ) 

 

# class  Estudiante(models.Model): 

#     # id_est=models.AutoField(primary_key=True) 

#     imagen_est=models.ImageField(null=True,upload_to='images/estudiante') 

#     id_est=models.CharField(max_length=10, primary_key=True, verbose_name= 'Cedula') 

#     nombres_est=models.CharField(max_length=25) 

#     apellidos_est=models.CharField(max_length=25) 

#     #edad_est=models.DateField() 

#     fecha_est=models.DateField(verbose_name='Fecha Nacimiento') 

#     email_est=models.EmailField() 

#     telefono_est=models.CharField(max_length=10) 

#     id_rep=models.ForeignKey(Representante, on_delete=models.CASCADE, verbose_name='Nombre del representante') 

#     id_fichsal=models.ForeignKey(Ficha_salud,on_delete=models.CASCADE) 

#     id_curso=models.ForeignKey(Cursos,on_delete=models.CASCADE) 

#     id_direccion=models.ForeignKey(Direccion,on_delete=models.CASCADE) 

#     def Estudiante(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.nombres_est, self.apellidos_est) 

 #     def __str__(self) -> str: 

#         txt = '{0} {1} ' 

#         return  txt.format(self.nombres_est,self.apellidos_est) 

#     def Representante (self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.representante.nombres_rep, self.representante.apellidos_rep) 

#     def Salud (self): 

#         txt = '{0} ' 

#         return txt.format(self.salud.NomEnfer_fichsa) 

#     def Cursos (self): 

#         txt = '{0}' 

#         return txt.format(self.cursos.nombre_curso) 

#     def Direccion (self): 

#         txt = '{0}{1}{2}' 

#         return txt.format(self.direccion.calle1_direc," y ",self.direccion.calle2_direc) 

 
# class Cargo (models.Model): 

#     id_car=models.AutoField(primary_key=True) 

#     nombre_car=models.CharField(max_length=15) 

#     def Cargo (self): 

#         txt = '{0}' 

#         return txt.format(self.nombre_car) 

 
#     def __str__(self) -> str: 

#         txt = '{0}' 

#         return txt.format(self.nombre_car) 

# class Talento_Humano (models.Model): 

#     imagen_th=models.ImageField(null=True,upload_to='images/talento_humano') 

#     cedula_th=models.CharField(max_length=10, primary_key=True,verbose_name='Cedula') 

#     nombres_th=models.CharField(max_length=25, verbose_name='Nombres') 

#     apellidos_th=models.CharField(max_length=25, verbose_name='Apellidos') 

#     cargo_th=models.ForeignKey(Cargo, on_delete=models.CASCADE) 

#     email_est=models.EmailField(verbose_name='E-mail') 

#     telefono_est=models.CharField(max_length=10) 

#     id_curso=models.ForeignKey(Cursos,on_delete=models.CASCADE, verbose_name='Curso') 

#     id_direccion=models.ForeignKey(Direccion, on_delete=models.CASCADE, verbose_name='Dirección') 

#     def Talento_Humano(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.nombres_th, self.apellidos_th) 

#     def __str__(self) -> str: 

#         txt = '{0} {1} ' 

#         return txt.format(self.nombres_th, self.apellidos_th) 

#     def Cargo (self): 

#         txt = '{0}' 

#         return txt.format(self.Cargo.nombre_car) 

 
# class Notas (models.Model): 

#     estudiante = models.ForeignKey(Estudiante, on_delete=CASCADE) 

#     curso_id= models.ForeignKey(Cursos, on_delete=CASCADE, verbose_name='Curso') 

#     parcial = models.CharField(choices=[('1','Uno')], default=1, max_length=1, verbose_name='Parcial') 

#     p_nota1 = models.FloatField(verbose_name='Trabajos',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     p_nota2 = models.FloatField(verbose_name='Tareas', null=1,validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     p_nota3 = models.FloatField(verbose_name='examen',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#      

#     parcial2 = models.CharField(choices=[('1','Dos')], default=1, max_length=1, verbose_name='Parcial') 

#     s_nota1 = models.FloatField(verbose_name='Trabajos',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     s_nota2 = models.FloatField(verbose_name='Tareas', null=1,validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     s_nota3 = models.FloatField(verbose_name='examen',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     parcial3 = models.CharField(choices=[('1','Tres')], default=1, max_length=1, verbose_name='Parcial') 

#     t_nota1 = models.FloatField(verbose_name='Trabajos',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     t_nota2 = models.FloatField(verbose_name='Tareas',null=1, validators=[MaxValueValidator(10),MinValueValidator(0)]) 

#     t_nota3 = models.FloatField(verbose_name='examen', null=1,validators=[MaxValueValidator(10),MinValueValidator(0)]) 


#     def SumaParcialUno(self): 

#         suma = (self.p_nota1 + self.p_nota2 +self.p_nota3) / 3 

#         return round((suma), 2) 

#     def SumaParcialDos(self): 

#         suma = (self.s_nota1 + self.s_nota2 +self.s_nota3) / 3 

#         return round((suma), 2) 

#     def SumaParcialTres(self): 

#         suma = (self.t_nota1 + self.t_nota2 +self.t_nota3) / 3 

#         return round((suma), 2) 

#     def SumaGeneral(self): 

#         uno = Notas.SumaParcialUno(self) 

#         dos = Notas.SumaParcialDos(self) 

#         tres = Notas.SumaParcialTres(self) 

#         suma = uno + dos + tres 

#         return round(suma, 2) 

#     def Promedio(self): 

#         promedio = Notas.SumaGeneral(self) / 3 

#         return round(promedio,2) 

#     def Estado(self): 

#         if Notas.SumaGeneral(self) > 20.5: 

#             return format_html("<spam style='color: green;' > Aprobado </spam>") 

#         else: 

#             return format_html("<spam style='color: red;' > Reprobado </spam>") 

#     def Estudiante(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.estudiante.nombres_est, self.estudiante.apellidos_est) 

#     def Cursos (self): 

#         txt = '{0}' 

#         return txt.format(self.cursos.nombre_curso) 

# class Comprobante (models.Model): 

#     i_comp= models.AutoField(primary_key=True) 

#     id_est=models.ForeignKey(Estudiante, on_delete=CASCADE) 

#     file_comp=models.FileField(null=True,upload_to='files/comprobante') 

#     def Estudiante(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.Estudiante.nombres_est, self.Estudiante.apellidos_est) 

#     def comp (self): 

#         txt='{0}{1}' 

#         return txt.format("comprobante de: ",self.id_est) 

#     def __str__(self) -> str: 

#         txt='{0}{1}' 

#         return txt.format("comprobante de: ",self.id_est) 

#     
# class Matricula(models.Model): 

#     fecha = models.DateField(verbose_name='Fecha de matrícula') 

#     estudiante = models.ForeignKey(Estudiante, on_delete=CASCADE) 

#     id_comp=models.ForeignKey(Comprobante, on_delete=CASCADE) 

#     id_curso= models.ForeignKey(Cursos, on_delete=CASCADE) 

#     matricula=models.BooleanField(default=False) 

#      

#     def Estudiante(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.estudiante.nombres_est, self.estudiante.apellidos_est) 

# class Asistencia (models.Model): 

#     estudiante = models.ForeignKey(Estudiante, on_delete=CASCADE) 

#     id_asis=models.AutoField(primary_key=True) 

#     estado_asis=models.BooleanField() 

#     fecha_asis=models.DateField(verbose_name='Fecha de asistencia') 

#     horario_id= models.ForeignKey(Horarios, on_delete=CASCADE, verbose_name='Hora') 

#     def Estudiante(self): 

#         txt = '{0} {1} ' 

#         return txt.format(self.estudiante.nombres_est, self.estudiante.apellidos_est) 