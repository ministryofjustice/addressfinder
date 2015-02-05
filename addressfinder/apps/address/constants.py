from extended_choices import Choices


# Definition - describes the physical nature of the property or land object.
# These are used to represent the physical state or the feature
# for example, the BLPU or the LPI.
BLPU_STATE_CODE = Choices(
    # constant, db_id, friendly string
    ('UNDER_CONSTRUCTION', 1, 'Under construction'),
    ('IN_USE', 2, 'In use'),
    ('UNOCCUPIED', 3, 'Unoccupied'),
    ('NO_LONGER_EXISTING', 4, 'No longer existing'),
    ('PLANNING_PERMISSION_GRANTED', 6, 'Planning permission granted'),
)


# Definition - the language is used to identify the
# primary language of the address displayed.
LANGUAGE_CODE = Choices(
    # constant, db_id, friendly string
    ('ENG', 'ENG', 'English'),
    ('CYM', 'CYM', 'Welsh'),
    ('GAE', 'GAE', 'Gaelic (Scottish)'),
    ('BIL', 'BIL', 'Bilingual (metadata record identifier only)'),
)


# Definition - the Logical Status reflects where the BLPU/LPI has reached
# in its life cycle. Logical status is important in identification of the
# addresses' requirements, for example, whether it is an alternative
# address or an historic address.
LOGICAL_STATUS_CODE = Choices(
    # constant, db_id, friendly string
    ('APPROVED', 1, 'Approved'),
    ('ALTERNATIVE', 3, 'Alternative'),
    ('PROVISIONAL', 6, 'Provisional'),
    ('HISTORICAL', 8, 'Historical'),
)


# Definition - indicator as whether the address recorded in the LPI
# corresponds to an entry in the official street naming and numbering register.
OFFICIAL_FLAG_CODE = Choices(
    # constant, db_id, friendly string
    ('YES', 'Y', 'Yes'),  # This means that this address has passed through the Statutory Street Naming and Numbering process and is the official address.
    ('NO', 'N', 'No'),  # Unofficial address
)


# Definition - the POSTAL_ADDRESS_CODE describes the type of postal
# delivery that the object is subject to.
POSTAL_ADDRESS_CODE = Choices(
    # constant, db_id, friendly string
    ('SINGLE', 'S', 'Single address'),  # A single address, for example, 56 High Street.
    ('NON_POSTAL', 'N', 'Non postal address'),  # Not a postal address, for example, Car Park.
    ('CHILD_ADDRESS', 'C', 'Child address'),  # This is a multiple-occupancy or 'child' address, for example, a flat behind a parent address.
    ('PARENT_ADDRESS', 'M', 'Parent address'),  # This is a 'parent' address with at least one child or associated address that may receive post, for example, 56 the High Street with flat 56a and 56b behind it.
)


# Definition - the RECORD_TYPE describes the type of street the record is
# identifying - whether it is a named street, numbered street or an
# unofficial name.
STREET_RECORD_TYPE_CODE = Choices(
    # constant, db_id, friendly string
    ('OFFICIAL_DESIGNATED_STREET_NAME', 1, 'Official designated street name'),
    ('STREET_DESCRIPTION', 2, 'Street description'),
    ('NUMBERED_STREET', 3, 'Numbered street'),
    ('UNOFFICIAL_STREET_DESCRIPTION', 4, 'Unofficial street description'),
    ('DESCRIPTION_USED_FOR_LLPG_ACCESS', 9, 'Description used for LLPG access'),
)


# Definition - the Representative Point Code is used to describe the
# nature of the coordinates allocated to the BLPU.
RPC_CODE = Choices(
    # constant, db_id, friendly string
    ('VISUAL_CENTRE', 1, 'Visual centre'),
    ('GENERAL_INTERNAL_POINT', 2, 'General internal point'),
    ('SW_CORNER_OF_REFERENCED_100_M_GRID', 3, 'SW corner of referenced 100 m grid'),
    ('START_OF_REFERENCED_STREET', 4, 'Start of referenced street'),
    ('GENERAL_POINT_BASED_ON_POSTCODE_UNIT', 5, 'General point based on postcode unit'),
    ('CENTRE_OF_A_CONTRIBUTING_AUTHORITY_AREA', 9, 'Centre of a contributing authority area'),
)


# Definition - this is an indication of how the object was matched to the USRN.
# A value of 1 indicates a manual match, usually defining the nearest access road.
# A value of 2 is matched spatially to the nearest USRN.
USRN_MATCH_INDICATOR_CODE = Choices(
    # constant, db_id, friendly string
    ('MATCHED_MANUALLY', '1', 'Matched manually'),  # Matched manually to the nearest accessible street.
    ('MATCHED_SPATIALLY', '2', 'Matched spatially'),  # Matched spatially to the nearest USRN (not necessarily the street that provides access).
)


# Definition - street state is used to describe the state in which the road is in
STREET_STATE_CODE = Choices(
    # constant, db_id, friendly string
    ('UNDER_CONSTRUCTION', 1, 'Under construction'),
    ('OPEN', 2, 'Open'),
    ('PERMANENTLY_CLOSED', 4, 'Permanently closed'),
)


# Definition - street classification is used to describe the type of street.
STREET_CLASSIFICATION_CODE = Choices(
    # constant, db_id, friendly string
    ('PEDESTRIAN_WAY', 4, 'Pedestrian way or footpath'),
    ('CYCLE_TRACK', 6, 'Cycle track or cycleway'),
    ('ALL_VEHICLES', 8, 'All vehicles'),
    ('RESTRICTED_BYWAY', 9, 'Restricted byway'),
    ('BRIDLEWAY', 10, 'Bridleway'),
)


# Definition - surface is used to describe the type of surface the majority
# of the road is covering.
STREET_SURFACE_CODE = Choices(
    # constant, db_id, friendly string
    ('METALLED', 1, 'Metalled'),
    ('UNMETALLED', 2, 'UnMetalled'),
    ('MIXED', 3, 'Mixed'),
)


# Definition - code used by Royal Mail to describe the user as a small or large
# user as defined for postal services based upon the number of letters
# delivered to that user.
POSTCODE_TYPE_CODE = Choices(
    # constant, db_id, friendly string
    ('SMALL_USER', 'S', 'Small user'),  # Indicates a small user, for example, a residential property.
    ('LARGE_USER', 'L', 'Large user'),  # Indicates a large user for example - a large commercial property.
)
