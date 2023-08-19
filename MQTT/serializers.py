from rest_framework import serializers

class MQTTStatusSerializer(serializers.Serializer):
    status_broker = serializers.CharField()
    subscribed_topics = serializers.ListField(child=serializers.CharField(max_length=100))
    received_messages = serializers.ListField(child=serializers.CharField(max_length=100))
    status_icad = serializers.DictField()
    param_icad = serializers.DictField()
    func_icad = serializers.DictField()
    pid_set_icad = serializers.DictField()
    pid_var_icad = serializers.DictField()



