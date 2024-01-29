from rest_framework.serializers import Serializer


class SwaggerResponseSerializerBase(Serializer):
    """
    only used for Swagger Response
    """

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
