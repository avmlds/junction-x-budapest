import streamlit as st

from scheduling.constants import TWO_YEAR_LEN_DAYS
from scheduling.scheduler import Scheduler
from scheduling.utils import (
    get_patient_generator,
    get_machine_pool,
    get_machine_calendar,
)
import json

st.session_state["st_report_end"] = 5


if not st.session_state.get("machine_pool"):
    st.session_state["machine_pool"] = get_machine_pool()

if not st.session_state.get("patient_generator"):
    st.session_state["patient_generator"] = get_patient_generator()


def set_report_end_to_day():
    st.session_state["st_report_end"] = 1


def set_report_end_to_week():
    st.session_state["st_report_end"] = 7


def set_report_end_to_month():
    st.session_state["st_report_end"] = 30


def get_st_report_end():
    return st.session_state["st_report_end"]


def generate_patient():
    st.session_state["patient"] = next(
        st.session_state["patient_generator"].get_patient()
    )
    st.session_state["scheduled"] = False


def schedule_patient():
    if st.session_state.get("scheduled"):
        st.warning("Already scheduled, fetch new patient!")

    if st.session_state.get("patient") and not st.session_state["scheduled"]:
        machine, shift = st.session_state["scheduler"].process_patient(
            st.session_state["patient"]
        )
        st.session_state["machine"] = machine
        st.session_state["shift"] = shift
        st.session_state["scheduled"] = True
    else:
        st.warning("Create patient first!")


if not st.session_state.get("machine_calendar"):
    st.session_state["machine_calendar"] = get_machine_calendar(
        st.session_state["machine_pool"], TWO_YEAR_LEN_DAYS
    )

if not st.session_state.get("scheduler"):
    st.session_state["scheduler"] = Scheduler(
        period_length_days=TWO_YEAR_LEN_DAYS,
        machine_pool=st.session_state["machine_pool"],
        patient_generator=st.session_state["patient_generator"],
        machine_calendar=st.session_state["machine_calendar"],
    )


with st.sidebar:
    st.title("General features")
    st.button("Get patient", on_click=generate_patient, use_container_width=True)

with st.container():
    if not st.session_state.get("patient"):
        st.info(
            f"Welcome to the patient management system. Open sidebar and click 'Get patient' to start working."
        )


with st.container():
    if st.session_state.get("patient"):
        st.title("Patient managing")
        patient_data = st.session_state["patient"]
        st.info(
            f"Current patient: {patient_data.name}\n\n"
            f"Cancer type: {patient_data.cancer.name()}\n\n"
            f"Prescribed treatment: {patient_data.fraction_time_days or 0} days"
        )
        fraction_time = st.select_slider(
            "Prescribed fraction, days",
            options=patient_data.cancer.fraction_time(),
            value=patient_data.cancer.fraction_time()[0],
        )
        patient_data.fraction_time_days = fraction_time
        st.button(
            "Schedule patient", on_click=schedule_patient, use_container_width=True
        )

    if st.session_state.get("machine"):
        st.info(
            f'Scheduled to machine: {st.session_state["machine"].name()}\n\n'
            f'Treatment will start in {st.session_state["shift"]} days'
        )

with st.container():
    if st.session_state.get("patient"):
        st.title("Utilization reports")
        start_day, end_day = st.select_slider(
            "Select a report range",
            options=list(
                range(0, st.session_state["machine_calendar"].calendar_length_days)
            ),
            value=(0, 2),
        )
        table = st.session_state["machine_calendar"].get_report_data(end_day, start_day)
        st.session_state["utilization_report"] = json.loads(table.get_json_string())[1:]
        if st.session_state.get("utilization_report"):
            st.table(st.session_state["utilization_report"])

with st.container():
    if st.session_state.get("patient"):
        st.title("Utilization charts")
        st.write("Whole period")
        machine_calendar = st.session_state["machine_calendar"]

        machines = sorted(
            [m for m in machine_calendar.calendar.keys()], key=lambda x: x.name()
        )

        data = {
            machine.name(): round((1 - machine_calendar[machine].load_level()) * 100, 3)
            for machine in machines
        }

        st.bar_chart(data, use_container_width=True)
