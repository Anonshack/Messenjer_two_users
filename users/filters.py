from rest_framework.filters import BaseFilterBackend
import coreapi


class UsersFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [coreapi.Field(
                name='name',
                location='query',
                required=False,
                type='string'
                # description='Filter user by last_name or first_name',
                ),
            ]
        return fields

    def filter_queryset(self, request, queryset, view):
        try:
            if 'name' in request.query_params:
                name = request.query_params['name']
                queryset = queryset.filter(last_name__icontains=name)|queryset.filter(first_name__icontains=name)|queryset.filter(username__icontains=name)
        except KeyError:
            pass
        return queryset