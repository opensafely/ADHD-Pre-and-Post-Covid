from ehrql import INTERVAL, case, create_measures, when, years
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from codelists import adhd_codelist, adhdrem_codelist, methylphenidate_codelist

# Helper function for finding the last matching event
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

measures = create_measures()
measures.configure_dummy_data(population_size=10000)

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

#In terms of dates -  Latest <= RPED
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

has_adhd_cod_date = last_matching_event(selected_events, adhd_codelist).date

has_adhdrem_cod_date = last_matching_event(selected_events, adhdrem_codelist).date

has_adhd_rule_1 = has_adhd_cod_date.is_not_null()

has_adhd_rule_2 = (has_aadhdrem_cod_date.is_null()) | (has_adhd_cod_date > has_aadhdrem_cod_date)

has_adhd_rule_1_and_2 = has_adhd_rule_1 & has_adhd_rule_2

measures.define_measure(
    name=f"adhd_prevalence",
    numerator=has_adhd_rule_1_and_2,
    denominator=(
        has_registration
        & patients.sex.is_in(["male", "female"])
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.start_date)
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(3).starting_on("2021-04-01"),
)
