from django.contrib import admin
from bdpindex.searchengine import models


class ParameterNameInline(admin.TabularInline):
    model = models.ParameterName
    extra = 0


class SchemaAdmin(admin.ModelAdmin):
    search_fields = ['name', 'namespace']
    inlines = [ParameterNameInline]


class ExperimentParameterInline(admin.TabularInline):
    model = models.ExperimentParameter
    extra = 0
    # formfield_overrides = {
    #   django.db.models.TextField: {'widget': TextInput},
    # }


class ExperimentParameterSetAdmin(admin.ModelAdmin):
    inlines = [ExperimentParameterInline]



admin.site.register(models.Schema, SchemaAdmin)
admin.site.register(models.ParameterName)
admin.site.register(models.ExperimentProfile)
admin.site.register(models.ExperimentProfileParameterSet, ExperimentParameterSetAdmin)


