# coding=utf-8
from skybluetech_scripts.tooldelta.utils.nbt import GetValueWithDefault as GetValue

_K_FLUID_ID = "fluid_id"
_K_FLUID_VOLUME = "fluid_vol"


class FluidSlotServer(object):
    def __init__(
        self,
        block_entity_data,
        index,  # type: int
        max_volume,  # type: float
    ):
        self.bdata = block_entity_data
        self.index = index
        self.max_volume = max_volume
        self.k_id = _K_FLUID_ID + str(index)
        self.k_vol = _K_FLUID_VOLUME + str(index)
        self._cached_fluid_id = block_entity_data[self.k_id]
        self._cached_volume = block_entity_data[self.k_vol] or 0.0
        if self._cached_fluid_id is None or self._cached_volume <= 0:
            self._cached_fluid_id = self.bdata[self.k_id] = None
            self._cached_volume = self.bdata[self.k_vol] = 0.0

    @property
    def fluid_id(self):
        # type: () -> str | None
        return self._cached_fluid_id

    @fluid_id.setter
    def fluid_id(self, value):
        # type: (str | None) -> None
        self._cached_fluid_id = self.bdata[self.k_id] = value
        if value is None:
            self._cached_volume = self.bdata[self.k_vol] = 0.0

    @property
    def volume(self):
        # type: () -> float
        return self._cached_volume

    @volume.setter
    def volume(self, value):
        # type: (float) -> None
        if value is None or value <= 0:
            value = 0.0
            if self._cached_fluid_id is not None:
                self.fluid_id = None
        self._cached_volume = self.bdata[self.k_vol] = value

    def isFull(self):
        return self.volume >= self.max_volume

    def canMerge(self, fluid_id):
        # type： (str | None) -> bool
        if fluid_id is None:
            return False
        if self.isFull():
            return False
        fid = self.fluid_id
        if fid is None or self.volume == 0 or fluid_id == fid:
            return True
        else:
            return False


class FluidSlotClient(object):
    def __init__(self, block_entity_data_ex, index=0):
        self.data = block_entity_data_ex
        self.k_id = _K_FLUID_ID + str(index)
        self.k_vol = _K_FLUID_VOLUME + str(index)

    @property
    def fluid_id(self):
        # type: () -> str | None
        return GetValue(self.data, self.k_id, None)

    @property
    def volume(self):
        # type: () -> float
        return GetValue(self.data, self.k_vol, 0.0)
