from ehrql import INTERVAL, case, create_measures, when, years
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from codelists import (
    adhd_codelist, 
    adhdrem_codelist,
    adhd_medication_codelist,
)

from variables_library import first_matching_event, last_matching_event, event_ADHD

'''
The following scripts looks at the measure of selected medication used
'''

measures = create_measures()
measures.configure_dummy_data(population_size=1000)

# Population variables
has_registration = practice_registrations.spanning(
    INTERVAL.start_date, INTERVAL.end_date
).exists_for_patient()

sex = patients.sex
age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age <= 9)).then("0 to 9"),
    when((age >= 10) & (age <= 17)).then("10 to 17"),
    when((age >= 18) & (age <= 24)).then("18 to 24"),
    when((age >= 25) & (age <= 34)).then("25 to 34"),
    when((age >= 35) & (age <= 44)).then("35 to 44"),
    when((age >= 45) & (age <= 54)).then("45 to 54"),
    when((age >= 55) & (age <= 64)).then("55 to 64"),
    when((age >= 65) & (age <= 74)).then("65 to 74"),
    when(age >= 75).then("75 and over"),
    when(age.is_null()).then("Missing"),
)

# In terms of dates -  Latest <= RPED
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

has_med_date = first_matching_event(selected_events, adhd_medication_codelist).date

has_adhd_cod_date = event_ADHD()

# Select patients with a diagnosis of ADHD
rule_has_adhd = has_adhd_cod_date.is_not_null()

# Select patients with meds
rule_has_meds = has_med_date.is_not_null()

rule_has_med_but_no_adhd =(
    rule_has_meds &
    has_adhd_cod_date.is_null()
    )

rule_has_med_with_adhd = (
    rule_has_meds &
    has_adhd_cod_date.is_not_null()
)

rule_no_med_with_adhd = (
    has_med_date.is_null() &
    has_adhd_cod_date.is_not_null()
)

#This looks at the incidence of ADHD medication in the entire population
measures.define_measure(
    name= f"adhd_medication_general",
    numerator= rule_has_meds,
    denominator=(
        has_registration
        & patients.sex.is_in(["male", "female"])
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.end_date)
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(9).starting_on("2016-04-01"),
)

#This looks at the incidence of medication in the entire population that do not have a ADHD diagonsis
measures.define_measure(
    name= f"no_adhd_medication_general",
    numerator= rule_has_med_but_no_adhd,
    denominator=(
        has_registration
        & patients.sex.is_in(["male", "female"])
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.end_date)
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(9).starting_on("2016-04-01"),
)

#This looks at the incidence of medication in the population for ADHD diagonsis
measures.define_measure(
    name= f"adhd_medication_diagonsis",
    numerator= rule_has_med_with_adhd,
    denominator=(
        has_registration
        & rule_has_adhd
        & patients.sex.is_in(["male", "female"])
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.end_date)
        & has_adhd_cod_date.is_not_null()
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(9).starting_on("2016-04-01"),
)

#This looks at the incidence of population of ADHD diagonsis
measures.define_measure(
    name= f"adhd_no_medication_diagonsis",
    numerator= rule_no_med_with_adhd,
    denominator=(
        has_registration
        & rule_has_adhd
        & patients.sex.is_in(["male", "female"])
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.end_date)
        & has_adhd_cod_date.is_not_null()
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(9).starting_on("2016-04-01"),
)
