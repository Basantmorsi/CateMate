from CateMate.utils.distance import distance_km

MUNICH = (48.137, 11.575)
BERLIN = (52.520, 13.405)


def test_same_point_is_zero():
    assert distance_km(*MUNICH, *MUNICH) == 0


def test_munich_to_berlin_is_about_504_km():
    assert distance_km(*MUNICH, *BERLIN) == 504


def test_distance_is_symmetric():
    assert distance_km(*MUNICH, *BERLIN) == distance_km(*BERLIN, *MUNICH)
