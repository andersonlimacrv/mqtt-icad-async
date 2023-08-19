function applyButtonClickBehavior(button) {
    let buttonText = button.querySelector('.tick');

    const tickMark = "<svg width=\"28\" height=\"25\" viewBox=\"0 0 58 45\" xmlns=\"http://www.w3.org/2000/svg\"><path fill=\"#fff\" fill-rule=\"nonzero\" d=\"M19.11 44.64L.27 25.81l5.66-5.66 13.18 13.18L52.07.38l5.65 5.65\"/></svg>";

    buttonText.innerHTML = "SET";

    button.addEventListener('click', function () {
        if (buttonText.innerHTML !== "SET") {
            buttonText.innerHTML = "SET";
        } else if (buttonText.innerHTML === "SET") {
            buttonText.innerHTML = tickMark;
        }
        this.classList.toggle('button__circle');
    });
}

// Selecionar e aplicar o comportamento em cada botão
let buttons = document.querySelectorAll('.button');
buttons.forEach(function (button) {
    applyButtonClickBehavior(button);
});

//Publish
document.getElementById('pub_transdutor_0_min').value = 'OK';
document.getElementById('pub_transdutor_0_max').value = 'OK';
document.getElementById('pub_offset_0').value = 'OK';
document.getElementById('pub_transdutor_10_min').value = 'OK';
document.getElementById('pub_transdutor_10_max').value = 'OK';
document.getElementById('pub_offset_10').value = 'OK';
document.getElementById('pub_pressao_0_maior').value = 'OK';
document.getElementById('pub_pressao_10_menor').value = 'OK';
document.getElementById('pub_pressao_0_menor').value = 'OK';
document.getElementById('pub_pressao_10_maior').value = 'OK';
document.getElementById('pub_setpoint_pid').value = 'OK';
document.getElementById('pub_inicio').value = 'OK';
document.getElementById('pub_parada').value = 'OK';
document.getElementById('pub_proporcional').value = 'OK';
document.getElementById('pub_integral').value = 'OK';
document.getElementById('pub_derivativa').value = 'OK';
document.getElementById('pub_tempo_valor').value = 'OK';
document.getElementById('pub_pv_minimo').value = 'OK';
document.getElementById('pub_pv_maximo').value = 'OK';
document.getElementById('pub_mv_minimo').value = 'OK';
document.getElementById('pub_mv_maximo').value = 'OK';
document.getElementById('pub_funcionamento').value = 'OK';
document.getElementById('pub_abertura_manual').value = 'OK';


const API_URL = '/mqtt_status/';
const INTERVAL = 3000;

async function fetchMQTTStatus() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao obter o status do MQTT:', error);
        return { status: 'Erro', subscribed_topics: [], received_messages: [] };
    }
}

function getElementById(id) {
    return document.getElementById(id);
}

function updateMQTTStatus() {
    const elements = {
        statusBroker: getElementById('mqtt_status'),
        topics: getElementById('subscribed_topics'),
        messages: getElementById('received_messages'),
        statusPressaoRegimeZero: getElementById('status_pressao_0'),
        statusPressaoRegimeNDez: getElementById('status_pressao_10'),
        statusComando: getElementById('status_comando'),
        statusRetorno: getElementById('status_retorno'),
        statusStatusPidErro: getElementById('status_erro'),
        statusErroMessage: getElementById('status_erro_message'),
        statusPidAcionada: getElementById('status_pid_acionada'),
        statusUnderflow: getElementById('status_underflow'),
        statusOverflow: getElementById('status_overflow'),
        paramTransdutorZeroMin: getElementById('sub_transdutor_0_min'),
        paramTransdutorZeroMax: getElementById('sub_transdutor_0_max'),
        paramOffsetZero: getElementById('sub_offset_0'),
        paramTransdutorNDezMin: getElementById('sub_transdutor_10_min'),
        paramTransdutorNDezMax: getElementById('sub_transdutor_10_max'),
        paramOffsetNDez: getElementById('sub_offset_10'),
        funcPressaoRegZeroMaior: getElementById('sub_pressao_0_maior'),
        funcPressaoRegNDezMenor: getElementById('sub_pressao_10_menor'),
        funcPressaoRegZeroMenor: getElementById('sub_pressao_0_menor'),
        funcPressaoRegNDezMaior: getElementById('sub_pressao_10_maior'),
        funcSetpointPid: getElementById('sub_setpoint_pid'),
        funcInicio: getElementById('sub_inicio'),
        funcParada: getElementById('sub_parada'),
        pidsetProporcional: getElementById('sub_proporcional'),
        pidsetIntegral: getElementById('sub_integral'),
        pidsetDerivativa: getElementById('sub_derivativa'),
        pidsetStateProporcional: getElementById('sub_onoff_proporcional'),
        pidsetStateIntegral: getElementById('sub_onoff_integral'),
        pidsetStateDerivativa: getElementById('sub_onoff_derivativa'),
        pidsetStateTime: getElementById('sub_onoff_tempo_automatico'),
        pidsetTempoValor: getElementById('sub_tempo_valor'),
        pidvarPvMin: getElementById('sub_pv_minimo'),
        pidvarPvMax: getElementById('sub_pv_maximo'),
        pidvarMvMin: getElementById('sub_mv_minimo'),
        pidvarMvMax: getElementById('sub_mv_maximo'),
        //pidvarABman: >>> data.pid_var_icad.ABman'); APLICAR A LÓGICA DA REGRA DE NEGOCIO

    };



    fetchMQTTStatus()
        .then(data => {
            elements.statusBroker.innerText = data.status_broker;
            elements.topics.innerText = data.subscribed_topics.join(', ');
            const erroMessages = {
                "1": "MaxMV < MinMV",
                "2": "MaxPV < MinPV",
                "3": "PV > MaxPV",
                "4": "PV < MinPV",
                "5": "Ti < 0,001",
                "6": "Td < 0",
                "7": "Gp ≤ 0",
                "8": "MaxVarMV < 0",
                "9": "DeadBand < 0",
                "10": "SampleTime < 0,001 OU > 1000 seg",
                "11": "SP > MaxPV",
                "12": "SP < MinPV",
            };

            if (data.status_icad !== null) {
                elements.statusUnderflow.checked = data.status_icad.uflow === "1";
                elements.statusOverflow.checked = data.status_icad.oflow === "1";
                elements.statusPressaoRegimeZero.value = data.status_icad.p_reg01;
                elements.statusPressaoRegimeNDez.value = data.status_icad.p_reg02;
                elements.statusComando.value = data.status_icad.com_ab_icad;
                elements.statusRetorno.value = data.status_icad.ab_icad;
                elements.statusStatusPidErro.innerHTML = "( " + data.status_icad.pid_erro + " )";
                if (data.status_icad.pid_erro === "0") {
                    elements.statusPidAcionada.checked = true;
                    elements.statusErroMessage.innerHTML = "Nenhum Erro";
                } else {
                    elements.statusPidAcionada.checked = false;
                    elements.statusErroMessage.innerHTML = erroMessages[data.status_icad.pid_erro] || "Erro desconhecido";
                }
            }
            if (data.pid_set_icad !== null) {
                elements.pidsetStateProporcional.checked = data.pid_set_icad.P_hab === "1";
                elements.pidsetStateIntegral.checked = data.pid_set_icad.I_hab === "1";
                elements.pidsetStateDerivativa.checked = data.pid_set_icad.D_hab === "1";
                elements.pidsetStateTime.checked = data.pid_set_icad.sTIME_hab === "1";
                elements.pidsetProporcional.value = data.pid_set_icad.Prop;
                elements.pidsetIntegral.value = data.pid_set_icad.Integ;
                elements.pidsetDerivativa.value = data.pid_set_icad.Deriv;
                elements.pidsetTempoValor.value = data.pid_set_icad.S_time;

            }
            if (data.param_icad !== null) {
                elements.paramTransdutorZeroMin.value = data.param_icad.TP1min;
                elements.paramTransdutorZeroMax.value = data.param_icad.TP1max;
                elements.paramOffsetZero.value = data.param_icad.OffsetP01;
                elements.paramTransdutorNDezMin.value = data.param_icad.TP2min;
                elements.paramTransdutorNDezMax.value = data.param_icad.TP2max;
                elements.paramOffsetNDez.value = data.param_icad.OffsetP02;

            }
            if (data.func_icad !== null) {
                elements.funcPressaoRegZeroMaior.value = data.func_icad.P_Reg01_ini;
                elements.funcPressaoRegNDezMenor.value = data.func_icad.P_Reg02_ini;
                elements.funcPressaoRegZeroMenor.value = data.func_icad.P_Reg01_stop;
                elements.funcPressaoRegNDezMaior.value = data.func_icad.P_Reg02_stop;
                elements.funcSetpointPid.value = data.func_icad.setPoint;
                elements.funcInicio.value = data.func_icad.Delay_ini;
                elements.funcParada.value = data.func_icad.Delay_stop;
            }
            if (data.pid_var_icad !== null) {
                elements.pidvarPvMin.value = data.pid_var_icad.PVmin;
                elements.pidvarPvMax.value = data.pid_var_icad.PVmax;
                elements.pidvarMvMin.value = data.pid_var_icad.MVmin;
                elements.pidvarMvMax.value = data.pid_var_icad.Vmax;
            }

            elements.messages.innerHTML = '';

            data.received_messages.forEach(message => {
                const match = message.match(/'topic': '([^']+)'/);
                const topic = match ? match[1] : '';

                const matchPayload = message.match(/'payload': '([^']+)'/);
                const payload = matchPayload ? matchPayload[1] : '';

                const listItem = document.createElement('li');
                listItem.classList.add('single_message');

                const topicElement = document.createElement('span');
                topicElement.classList.add('topic');
                topicElement.innerText = topic;

                const separatorElement = document.createElement('span');
                separatorElement.classList.add('separator');
                separatorElement.innerText = ' > ';

                const payloadElement = document.createElement('span');
                payloadElement.classList.add('payload');
                payloadElement.innerText = payload;

                listItem.appendChild(topicElement);
                listItem.appendChild(separatorElement);
                listItem.appendChild(payloadElement);

                elements.messages.appendChild(listItem);
            });


        })
        .catch(error => {
            console.error('Erro ao atualizar o status do MQTT:', error);
        });
}

setInterval(updateMQTTStatus, INTERVAL);

/* DAQUI PRA BAIXO É APENAS ESTILIZAÇÃO DE COMPORTAMENTOS */


// Obtém os elementos do botão, do conteúdo do dropdown e do ícone
var dropbtn = document.getElementById("dropbtn");
var dropdownContent = document.getElementById("dropdown-content");
var icon = document.getElementById("icon");
var spaceDropDown = document.getElementById("parametro_config");
var height = dropdownContent.offsetHeight;


// Adiciona um ouvinte de eventos ao botão para abrir/fechar o dropdown
dropbtn.addEventListener("click", function () {

    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
        dropbtn.style.borderBottomLeftRadius = "10px";
        dropbtn.style.borderBottomRightRadius = "10px";
        spaceDropDown.style.margin = "0";

    } else {
        dropdownContent.style.display = "block";
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
        dropbtn.style.borderBottomLeftRadius = "0";
        dropbtn.style.borderBottomRightRadius = "0";
        spaceDropDown.style.margin = "300px 0 0 0";

    }
});