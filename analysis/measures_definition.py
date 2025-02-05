from ehrql import INTERVAL, case, create_measures, when, years
from ehrql.tables.tpp import (
    patients,
    practice_registrations,
    clinical_events,
    medications,
)

from codelists import adhd_codelist

measures = create_measures()
measures.configure_dummy_data(population_size=10000)

# Population variables
has_registration = practice_registrations.spanning(
    INTERVAL.start_date, INTERVAL.end_date
).exists_for_patient()

#In terms of dates -  Latest <= RPED
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

has_adhd_cod = (selected_events
        .where(selected_events.snomedct_code.is_in(adhd_codelist))
        .exists_for_patient()
)

measures.define_measure(
    name=f"FAKE_DATA_adhd_prevalence",
    numerator=has_adhd_cod,
    denominator=(
        has_registration
    ),
    intervals=years(3).starting_on("2021-04-01"),
)
