from django.utils.deprecation import MiddlewareMixin

class GroupContextMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        
        response.context_data['Jornalista'] = request.user.groups.filter(name='Jornalista').exists()
        response.context_data['EDC'] = request.user.groups.filter(name='EDC').exists()
        response.context_data['GuiaDpE'] = request.user.groups.filter(name='GuiaDpE').exists()
        response.context_data['MinistroDpE'] = request.user.groups.filter(name='MinistroDpE').exists()
        response.context_data['LDPE'] = request.user.groups.filter(name='LDPE').exists()
        response.context_data['Analista'] = request.user.groups.filter(name='Analista').exists()
        response.context_data['MINISTRODRH'] = request.user.groups.filter(name='MINISTRODRH').exists()
        response.context_data['LDRH'] = request.user.groups.filter(name='LDRH').exists()
        response.context_data['STAFF'] = request.user.groups.filter(name='STAFF').exists()
        response.context_data['MEMBRODPO'] = request.user.groups.filter(name='MEMBRODPO').exists()
        response.context_data['MINISTRODPO'] = request.user.groups.filter(name='MINISTRODPO').exists()
        response.context_data['LDPO'] = request.user.groups.filter(name='LDPO').exists()
        return response