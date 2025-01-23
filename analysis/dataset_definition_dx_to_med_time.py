from ehrql import create_dataset
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from codelists import adhd_codelist, methylphenidate_codelist

def last_matching_event(events, codelist, where=True):
    """Select the last matching SNOMED CT event from specified codelist

    Args:
        events (e.g., clinical_events or ): Many rows per patient event frame to select last matching event from codelist from
        codelist (codelist): Clinical codelist, must be using snomedct codes
        where (bool, optional): _description_. Defaults to True.

    Returns:
        patient frame: One row per patient frame, with the last matching event from codelist
    """
    return (
        events.where(where)
        .where(events.snomedct_code.is_in(codelist))
        .sort_by(events.date)
        .last_for_patient()
    )

dataset = create_dataset()
dataset.configure_dummy_data(population_size=10)

# Date range
start_date = "2016-04-01"
end_date = "2017-03-31"

# Population variables
has_registration = practice_registrations.spanning(
    start_date, end_date
).exists_for_patient()
dataset.sex = patients.sex
dataset.age = patients.age_on(start_date)

selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(start_date, end_date)
)

selected_medications = medications.where(
    medications.date.is_on_or_after(start_date)
)

has_adhd_event = selected_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).exists_for_patient()

dataset.adhd_cod_date = last_matching_event(selected_events, adhd_codelist).date

dataset.mph_med_date = selected_medications.where(True)\
    .where(selected_medications.dmd_code.is_in(methylphenidate_codelist))\
    .sort_by(selected_medications.date)\
    .first_for_patient().date

dataset.times_between_dia_med_weeks = (dataset.mph_med_date - dataset.adhd_cod_date).weeks

dataset.define_population(
    has_registration
    & dataset.sex.is_in(["male", "female"])
    & (dataset.age <= 120)
    & patients.is_alive_on(start_date)
    & dataset.adhd_cod_date.is_not_null()
    & dataset.mph_med_date.is_not_null()
    & (dataset.adhd_cod_date <= dataset.mph_med_date)
)