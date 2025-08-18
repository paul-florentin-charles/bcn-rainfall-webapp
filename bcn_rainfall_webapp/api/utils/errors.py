from bcn_rainfall_core.utils import Month, Season, TimeMode
from fastapi import HTTPException


def raise_time_mode_error_or_do_nothing(
    time_mode: TimeMode,
    month: Month | None = None,
    season: Season | None = None,
):
    """
    Manage errors related to time mode issues.

    :param time_mode: A TimeMode Enum ['yearly', 'monthly', 'seasonal']
    :param month: A Month Enum ['January', 'February', ..., 'December'].
    Set if time_mode is 'monthly' (optional).
    :param season: A Season Enum ['winter', 'spring', 'summer', 'fall'].
    Set if time_mode is 'seasonal' (optional).
    :raise HTTPException: if time_mode is 'monthly' and month is None or
    if time_mode is 'seasonal' and season is None.
    :return: None.
    """
    if time_mode == TimeMode.MONTHLY and month is None:
        raise HTTPException(
            status_code=400,
            detail=f"You gave {time_mode=}, month cannot be null and should be one these values: {Month.values()}.",
        )

    if time_mode == TimeMode.SEASONAL and season is None:
        raise HTTPException(
            status_code=400,
            detail=f"You gave {time_mode=}, season cannot be null and should be one these values: {Season.values()}.",
        )


def raise_year_related_error_or_do_nothing(begin_year: int, end_year: int):
    """
    Manage errors related to year related issues.

    :param int begin_year: An integer representing year of start.
    :param int end_year: An integer representing year of end.
    :raise HTTPException: if begin_year > end_year.
    :return: None.
    """
    if begin_year > end_year:
        raise HTTPException(
            status_code=400,
            detail=f"{begin_year=} must be lower or equal than {end_year=}.",
        )
