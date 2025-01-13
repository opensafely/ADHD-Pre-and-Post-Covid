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
    """_summary_

    Args:
        events (clinical_events): _description_
        codelist (codelist): _description_
        where (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
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
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
    when(age.is_null()).then("Missing"),
)

#In terms of dates -  Latest <= RPED
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

has_adhd_cod_date = last_matching_event(selected_events, adhd_codelist).date

has_aadhdrem_cod_date = last_matching_event(selected_events, adhdrem_codelist).date

has_adhd_rule_1 = has_adhd_cod_date.is_not_null()

has_adhd_rule_2 = (has_aadhdrem_cod_date.is_null()) | (has_adhd_cod_date > has_aadhdrem_cod_date)

has_adhd_rule_1_and_2 = has_adhd_rule_1 & has_adhd_rule_2

measures.define_measure(
    name=f"adhd_prevalence",
    numerator=has_adhd_rule_1_and_2,
    denominator=(
        has_registration
        & patients.sex.is_in(["male", "female"])
        & (age >= 18)
        & (age <= 120)
        & patients.is_alive_on(INTERVAL.start_date)
    ),
    group_by={"sex": sex, "age_band": age_band},
    intervals=years(3).starting_on("2016-01-01"),
)
