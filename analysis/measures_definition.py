from ehrql import INTERVAL, create_measures, years
from ehrql.tables.tpp import (
    practice_registrations,
    clinical_events,
)

from codelists import adhd_codelist

measures = create_measures()
measures.configure_dummy_data(population_size=10000)

# Population variables
has_registration = practice_registrations.spanning(
    INTERVAL.start_date, INTERVAL.end_date
).exists_for_patient()

has_adhd_cod = (clinical_events
                .where(clinical_events.date.is_on_or_before(INTERVAL.end_date))
                .where(clinical_events.snomedct_code.is_in(adhd_codelist))
                .exists_for_patient()
)

measures.define_measure(
    name=f"FAKE_DATA_adhd_prevalence",
    numerator= has_adhd_cod,
    denominator= has_registration,
    intervals=years(3).starting_on("2021-04-01"),
)
