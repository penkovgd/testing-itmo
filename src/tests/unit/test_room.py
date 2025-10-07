import pytest
from reception.domain.entity.room import Room
from reception.domain.exception.room import RoomStatusException
from shared_kernel.domain.value_object import RoomStatus


def test_reserve_available_room():
    # Arrange
    room = Room("R101", RoomStatus.AVAILABLE)
    # Act
    room.reserve()
    # Assert
    assert room.room_status.is_reserved


@pytest.mark.parametrize("room_status", [RoomStatus.OCCUPIED, RoomStatus.RESERVED])
def test_reserve_occupied_or_reserved_room_throws_exception(room_status: RoomStatus):
    # Arrange
    room = Room("R101", room_status)
    # Act and Assert
    with pytest.raises(RoomStatusException):
        room.reserve()
