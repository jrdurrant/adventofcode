from functools import reduce
from itertools import count, islice
from operator import xor


def reverse(sequence, start, length):
    indices = [i % len(sequence) for i in range(start, start + length)]
    pairs = zip(indices, reversed(indices))

    for i, j in islice(pairs, length // 2):
        sequence[j], sequence[i] = sequence[i], sequence[j]


def twists(circle, lengths, position=0, skip_size=0):
    while True:
        for length in lengths:
            reverse(circle, position, length)
            position += length + skip_size
            skip_size += 1
        yield


def blocks(sequence, length=16):
    for i in range(0, len(sequence), length):
        yield sequence[i:(i + length)]

def knot_hash(string):
    circle = list(range(256))
    lengths = [ord(digit) for digit in string] + [17, 31, 73, 47, 23]

    rounds = twists(circle, lengths)
    for _ in range(64): next(rounds)

    sparse_hash = circle
    dense_hash = [reduce(xor, block) for block in blocks(sparse_hash, 16)]
    return ''.join(hex(number)[2:].zfill(2) for number in dense_hash)
