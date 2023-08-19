from django.contrib import messages
from django.shortcuts import render, redirect
from .mqtt_client import MQTTClient


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MQTTStatusSerializer

mqtt_client = None 

def broker_connection(request):
    global mqtt_client
    BROKER = "broker.emqx.io"
    PORT = 1883
    TOPIC = "DAR/SETUP/ICAD/"
    USERNAME = ""
    PASSWORD = ""
    CONTEXT_TOPIC= [
        "CESS/ICAD/STP/PARAM",
        "CESS/ICAD/STP/FUNC",
        "CESS/ICAD/STP/PIDSET",
        "CESS/ICAD/STP/PIDVAR",
        "CESS/ICAD/STT"
        ]

    mqtt_client = MQTTClient(BROKER, PORT, TOPIC, USERNAME, PASSWORD, CONTEXT_TOPIC)
    
    try:
        mqtt_client.connect() 
    except Exception as e:
        messages.error(request, f"Erro ao conectar ao broker: {str(e)}")
       
    return redirect("MQTT:index_mqtt")

def broker_disconnection(request):
    global mqtt_client

    if mqtt_client is not None:
        mqtt_client.disconnect()
        mqtt_client = None

    return redirect("MQTT:index_mqtt")

def index_mqtt(request):
    global mqtt_client

    if request.method == "POST":
        if "connect_btn" in request.POST:
            return redirect("MQTT:broker_connection")
        if "disconnect_btn" in request.POST and mqtt_client is not None:
            return redirect("MQTT:broker_disconnection")
        if mqtt_client is not None and mqtt_client.is_connected():
            if "subscribe_btn" in request.POST:
                topic = request.POST.get("topic")
                mqtt_client.subscribe(topic)
            elif "publish_btn" in request.POST:
                topic = request.POST.get("topic")
                payload = request.POST.get("payload")
                mqtt_client.publish(topic, payload)

    is_connected = mqtt_client is not None and mqtt_client.is_connected()

    if mqtt_client is not None:
        received_messages = mqtt_client.get_received_messages()
        subscribed_topics = mqtt_client.get_subscribed_topics()
    else:
        received_messages = []
        subscribed_topics = []

    context = {
        "mqtt_client": mqtt_client,
        "is_connected": is_connected,
        "received_messages": received_messages,
        "subscribed_topics": subscribed_topics,
    }

    return render(request, "index_mqtt.html", context)

@api_view(['GET'])
def mqtt_status(request):
    global mqtt_client

    if mqtt_client is None:
        data = {"status_broker": "Not connected", "subscribed_topics": [], "received_messages": [], "status_icad": None, "param_icad": None, "func_icad": None, "pid_set_icad": None, "pid_var_icad": None}
    else:
        is_connected = mqtt_client.is_connected()
        status_broker = "Connected" if is_connected else "Not connected"
        subscribed_topics, received_messages, status_icad, param_icad, func_icad, pid_set_icad, pid_var_icad = process_received_messages(mqtt_client)
        
        if status_icad is not None:
            status_icad = status_icad
        if param_icad is not None:
            param_icad = param_icad
        if func_icad is not None:
            func_icad = func_icad
        if pid_set_icad is not None:
            pid_set_icad = pid_set_icad
        if pid_var_icad is not None:
            pid_var_icad = pid_var_icad
        
        data = {"status_broker": status_broker, "subscribed_topics": subscribed_topics, "received_messages": received_messages, "status_icad": status_icad, "param_icad": param_icad, "func_icad": func_icad, "pid_set_icad": pid_set_icad, "pid_var_icad": pid_var_icad}

    serializer = MQTTStatusSerializer(data)
    return Response(serializer.data)

def process_received_messages(mqtt_client):
    if mqtt_client is not None:
        subscribed_topics = mqtt_client.get_subscribed_topics()
        received_messages = mqtt_client.get_received_messages()
        
        topic_functions = {
            "CESS/ICAD/STP/PARAM": process_param_topic,
            "CESS/ICAD/STP/FUNC": process_func_topic,
            "CESS/ICAD/STP/PIDSET": process_pid_set_topic,
            "CESS/ICAD/STP/PIDVAR": process_pid_var_topic,
            "CESS/ICAD/STT": process_stt_topic, 
        }
        
        status_icad, param_icad, func_icad, pid_set_icad, pid_var_icad = None, None, None, None, None

        for message in received_messages:
            topic = message['topic']
            payload = message['payload']
            
            if topic in topic_functions:
                if topic == "CESS/ICAD/STT":
                    status_icad = process_stt_topic(payload)
                if topic == "CESS/ICAD/STP/PARAM":
                    param_icad = process_param_topic(payload)
                if topic == "CESS/ICAD/STP/FUNC":
                    func_icad = process_func_topic(payload)
                if topic == "CESS/ICAD/STP/PIDSET":
                    pid_set_icad = process_pid_set_topic(payload)
                if topic == "CESS/ICAD/STP/PIDVAR":
                    pid_var_icad = process_pid_var_topic(payload)
                else:
                    topic_functions[topic](payload)
            
    else:
        subscribed_topics = []
        received_messages = []

    return subscribed_topics, received_messages, status_icad, param_icad, func_icad, pid_set_icad, pid_var_icad

def process_stt_topic(payload=None):
    if payload is None:
        return None
    
    payload_parts = payload.split(":")
    if len(payload_parts) != 8:
        print("Invalid payload format:", payload)
        return None

    p_reg01, p_reg02, com_ab_icad, ab_icad, acc_icad, uflow, oflow, pid_erro = payload_parts

    status_icad = {
        'p_reg01': p_reg01,
        'p_reg02': p_reg02,
        'com_ab_icad': com_ab_icad,
        'ab_icad': ab_icad,
        'acc_icad': acc_icad,
        'uflow': uflow,
        'oflow': oflow,
        'pid_erro': pid_erro,
    }

    return status_icad

def process_param_topic(payload=None):
    if payload is None:
        return None

    payload_parts = payload.split(":")
    if len(payload_parts) != 7:
        print ("Invalid payload format:", payload)
        return None

    Func, TP1min, TP1max, TP2min, TP2max, OffsetP01, OffsetP02 = payload_parts

    param_icad = {
        'Func': Func,
        'TP1min': TP1min,
        'TP1max': TP1max,
        'TP2min': TP2min,
        'TP2max': TP2max,
        'OffsetP01': OffsetP01,
        'OffsetP02': OffsetP02,
    }

    return param_icad

    
def process_func_topic(payload=None):
    if payload is None:
       return None
   
    payload_parts = payload.split(":")
    if len(payload_parts) != 7:
        print ("Invalid payload format:", payload)
        return None
    
    P_Reg01_ini, P_Reg02_ini, setPoint, P_Reg01_stop, P_Reg02_stop, Delay_ini, Delay_stop = payload_parts

    func_icad = {
        'P_Reg01_ini': P_Reg01_ini,
        'P_Reg02_ini': P_Reg02_ini,
        'setPoint': setPoint,
        'P_Reg01_stop': P_Reg01_stop,
        'P_Reg02_stop': P_Reg02_stop,
        'Delay_ini': Delay_ini,
        'Delay_stop': Delay_stop,
    }

    return func_icad
    
def process_pid_set_topic(payload=None):
    if payload is None:
       return None
   
    payload_parts = payload.split(":")
    if len(payload_parts) != 8:
        print ("Invalid payload format:", payload)
        return None
    
    Prop , Integ ,Deriv, P_hab,  I_hab,  D_hab, sTIME_hab, S_time = payload_parts

    pid_set_icad = {
        'Prop': Prop,
        'Integ': Integ,
        'Deriv': Deriv,
        'P_hab': P_hab,
        'I_hab': I_hab,
        'D_hab': D_hab,
        'sTIME_hab': sTIME_hab,
        'S_time': S_time,
    }

    return pid_set_icad
    
def process_pid_var_topic(payload=None):
    if payload is None:
       return None
   
    payload_parts = payload.split(":")
    if len(payload_parts) != 5:
        print ("Invalid payload format:", payload)
        return None
    
    PVmin, PVmax, MVmin, Vmax, ABman = payload_parts

    pid_var_icad = {
        'PVmin': PVmin,
        'PVmax': PVmax,
        'MVmin': MVmin,
        'Vmax': Vmax,
        'ABman': ABman,
    }

    return pid_var_icad