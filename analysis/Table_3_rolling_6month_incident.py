from ehrql import create_dataset, case, create_measures, when, years
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from variables_library import (
    first_matching_event,
    last_matching_event
)

from codelists import (
    adhd_codelist,
    adhdrem_codelist,
    adhd_medication_codelist,
)

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Date range
start_date_point = "2016-04-01"
end_date_point = "2025-03-31"

# Population variables
has_registration = practice_registrations.where(
        practice_registrations.start_date.is_on_or_after(start_date_point)
    ).exists_for_patient()

dataset.sex = patients.sex

dataset.date_of_birth = patients.date_of_birth

# Filtering with the codelists
has_adhd_event = clinical_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).exists_for_patient()

# Picking the first date for dia and first date for med
dataset.first_adhd_diagnosis_date = last_matching_event(
    clinical_events, adhd_codelist
).date

# Number of counts for ADHD diagonsis and readmission
dataset.count_adhd_diagnoses = clinical_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).count_for_patient()

dataset.count_adhd_resolved = clinical_events.where(
    clinical_events.snomedct_code.is_in(adhd_codelist)
).count_for_patient()

dataset.last_mph_med_date = (
    medications.where(True)
    .where(medications.dmd_code.is_in(adhd_medication_codelist))
    .where(medications.date.is_on_or_after(dataset.first_adhd_diagnosis_date))
    .sort_by(medications.date)
    .first_for_patient()
    .date
)

# Compute the date gap
dataset.times_between_dia_med_weeks = (
    dataset.last_mph_med_date - dataset.first_adhd_diagnosis_date
).weeks

dataset.year_of_medication = (dataset.last_mph_med_date).year

#Computing the age at the point of medication
dataset.age = patients.age_on(dataset.last_mph_med_date)

dataset.age_band = case(
    when((dataset.age >= 0) & (dataset.age <= 9)).then("0 to 9"),
    when((dataset.age >= 10) & (dataset.age <= 17)).then("10 to 17"),
    when((dataset.age >= 18) & (dataset.age <= 24)).then("18 to 24"),
    when((dataset.age >= 25) & (dataset.age <= 34)).then("25 to 34"),
    when((dataset.age >= 35) & (dataset.age <= 44)).then("35 to 44"),
    when((dataset.age >= 45) & (dataset.age <= 54)).then("45 to 54"),
    when((dataset.age >= 55) & (dataset.age <= 64)).then("55 to 64"),
    when((dataset.age >= 65) & (dataset.age <= 74)).then("65 to 74"),
    when(dataset.age >= 75).then("75 and over"),
    when(dataset.age.is_null()).then("Missing"),
)

# Computing the population records
dataset.define_population(
    has_registration
    & dataset.sex.is_in(["male", "female"])
    & (dataset.age <= 120)
    & dataset.first_adhd_diagnosis_date.is_not_null()
    & dataset.last_mph_med_date.is_not_null()
    & (dataset.last_mph_med_date > dataset.first_adhd_diagnosis_date)
)
