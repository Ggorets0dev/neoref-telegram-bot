'''Modules for data hashing'''

from dataclasses import dataclass
from hashlib import sha3_256
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError


class Hasher:
    '''Hashing data using Argon2id'''

    @dataclass(frozen=True)
    class ArgonHashingPreset:
        '''Settings for Argon2id hashing protocol'''
        memory_cost: int
        time_cost: int
        parallelism: int
        salt_len: int
        hash_len: int

    NORMAL_HASHING_PRESET = ArgonHashingPreset(memory_cost=256*1024,
                                               time_cost=15,
                                               parallelism=8,
                                               salt_len=128,
                                               hash_len=128)

    LIGHT_HASHING_PRESET = ArgonHashingPreset(memory_cost=128*1024,
                                              time_cost=10,
                                              parallelism=4,
                                              salt_len=128,
                                              hash_len=128)
    
    def hash_with_argon2id(self, value: bytes, preset: 'ArgonHashingPreset', salt: bytes = None) -> str:
        '''Create hash with special or random salt with Argon2id protocol'''
        ARGON_HASHER = PasswordHasher(preset.time_cost,
                                      preset.memory_cost,
                                      preset.parallelism,
                                      preset.hash_len,
                                      preset.salt_len)
        
        return ARGON_HASHER.hash(password=value, salt=salt)

    def hash_with_sha3(self, value: bytes) -> bytes:
        '''Convert an arbitrary password into an encryption key using SHA3-256'''
        return sha3_256(value).digest()

    def verify_hash(self, value: bytes, value_hash: bytes) -> bool:
        '''Check if the hash matches the original password'''
        try:
            return PasswordHasher().verify(value_hash, value)
        except (VerifyMismatchError, InvalidHashError):
            return False
