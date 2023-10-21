from rest_framework.filters import BaseFilterBackend
import coreapi


class ChatMessagesFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [coreapi.Field(
                name='name',
                location='query',
                required=True,
                type='int'
                ),
            coreapi.Field(
                name='user_2',
                location='query',
                required=True,
                type='int'
                # description='Filter user by last_name or first_name',
                ),
            ]
        return fields

    def filter_queryset(self, request, queryset, view):
        return queryset