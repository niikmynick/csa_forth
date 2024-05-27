class Memory:
    def __init__(self):
        self._memory = {}
        self._last_allocated = 0

    def allocate(self, size: int) -> int:
        base_pointer = self.get_last_allocated()
        for i in range(size):
            self._memory[base_pointer + i] = None

        self._last_allocated += size

        return base_pointer

    def get_last_allocated(self):
        return self._last_allocated

    def read(self, key):
        assert key in self._memory, f"Key {key} not found in memory"

        return self._memory.get(key)

    def write(self, key, value):
        assert key in self._memory, f"Key {key} not found in memory"

        self._memory[key] = value

    def __str__(self):
        return str(self._memory)

    def __repr__(self):
        return str(self._memory)
