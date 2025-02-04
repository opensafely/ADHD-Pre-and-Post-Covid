from ehrql import create_dataset
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from variables_library import last_matching_event

from codelists import (
    adhd_codelist,
    adhdrem_codelist,
    methylphenidate_codelist,
)

dataset = create_dataset()
dataset.configure_dummy_data(population_size=5)

# Date range
start_date = "2016-04-01"
end_date = "2017-03-31"

# Population variables
has_registration = practice_registrations.spanning(
    start_date, end_date
).exists_for_patient()
dataset.sex = patients.sex
dataset.age = patients.age_on(end_date)

# Setting up the dates
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(start_date, end_date)
)

selected_medications = medications.where(medications.date.is_on_or_after(start_date))

# Filtering with the codelists
has_adhd_event = selected_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).exists_for_patient()

# Picking the last date for dia and first date for med
dataset.latests_adhd_diagnosis_date = last_matching_event(
    selected_events, adhd_codelist
).date

dataset.latest_adhdrem_cod_date = last_matching_event(
    selected_events, adhdrem_codelist
).date

# Number of counts for ADHD diagonsis and readmission
dataset.count_adhd_diagnoses = selected_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).count_for_patient()

dataset.count_adhd_resolved = selected_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).count_for_patient()

dataset.first_mph_med_date = (
    selected_medications.where(True)
    .where(selected_medications.dmd_code.is_in(methylphenidate_codelist))
    .sort_by(selected_medications.date)
    .first_for_patient()
    .date
)

# Compute the date gap
dataset.times_between_dia_med_weeks = (
    dataset.first_mph_med_date - dataset.latests_adhd_diagnosis_date
).weeks

# Computing the population records
dataset.define_population(
    has_registration
    & dataset.sex.is_in(["male", "female"])
    & (dataset.age <= 120)
    & patients.is_alive_on(start_date)
    & dataset.latests_adhd_diagnosis_date.is_not_null()
    & dataset.first_mph_med_date.is_not_null()
    & (dataset.latest_adhdrem_cod_date <= dataset.latests_adhd_diagnosis_date)
    & (dataset.latests_adhd_diagnosis_date <= dataset.first_mph_med_date)
)
